import argparse
import logging
import os
import pickle
from datetime import timedelta

import pandas as pd

log = logging.getLogger(__name__)

_EDGE_THRESHOLD = 0.05

try:
    from agents.ml.modeling import FEATURE_COLUMNS
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso
    from agents.strategies.strategy_runner import generate_signals, latest_run_id
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from agents.ml.modeling import FEATURE_COLUMNS
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso
    from agents.strategies.strategy_runner import generate_signals, latest_run_id

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ARTIFACTS_DIR = os.path.join(_BASE_DIR, "artifacts", "models")

# Must match CROSS_MARKET_FEATURE_COLUMNS in dashboard/app.py exactly.
_CROSS_MARKET_FEATURE_COLUMNS = [
    "return_1", "return_2", "return_4", "return_8",
    "rolling_mean_return_4", "rolling_mean_return_8",
    "rolling_vol_4", "rolling_vol_8", "rolling_vol_16",
    "momentum_4", "momentum_8", "momentum_16",
    "rsi_14",
    "sma_4_dist", "sma_8_dist", "sma_16_dist",
    "ema_4_dist", "ema_8_dist",
    "volume_z_16",
    "candle_body", "upper_wick_ratio", "lower_wick_ratio", "hl_range",
    "realized_vol_proxy",
    "streak_up", "streak_down",
    "hour_of_day", "day_of_week",
    "session_asia", "session_europe", "session_us",
    "regime_vol_high", "regime_trend_up",
    "kalshi_mid", "poly_mid", "cross_spread", "kalshi_volume", "poly_volume",
]


def _load_kalshi_snapshot(conn) -> tuple[float | None, float | None]:
    """Return (yes_ask, yes_bid) from the most recent kalshi_market_snapshots row."""
    row = conn.execute(
        """SELECT yes_ask_dollars, yes_bid_dollars
           FROM kalshi_market_snapshots
           WHERE yes_ask_dollars IS NOT NULL AND yes_bid_dollars IS NOT NULL
           ORDER BY snapped_at DESC LIMIT 1"""
    ).fetchone()
    if row is None:
        return None, None
    return float(row[0]), float(row[1])


def _edge_action(prob_up: float, yes_ask: float, yes_bid: float) -> tuple[str, float, float]:
    """Compute edge for each side and return (action, position, edge_value).

    YES edge  = prob_up - yes_ask
    NO  edge  = (1 - prob_up) - (1 - yes_bid)  =  yes_bid - prob_up

    Enters only when the relevant edge exceeds _EDGE_THRESHOLD (0.05).
    Returns ("flat", 0.0, best_edge) and logs at DEBUG when no edge qualifies.
    """
    yes_edge = prob_up - yes_ask
    no_edge  = (1.0 - prob_up) - (1.0 - yes_bid)  # == yes_bid - prob_up

    if yes_edge > _EDGE_THRESHOLD:
        return "long", 1.0, yes_edge
    if no_edge > _EDGE_THRESHOLD:
        return "short", -1.0, no_edge

    best_edge = max(yes_edge, no_edge)
    log.debug("forward_paper: no edge (edge=%.3f)", best_edge)
    return "flat", 0.0, best_edge


def latest_feature_timestamp(conn) -> str | None:
    row = conn.execute("SELECT MAX(timestamp) FROM btc_features_15m").fetchone()
    return row[0] if row and row[0] else None


def load_artifact_and_predict(conn, run_id: int, strategy_name: str, threshold: float = 0.55) -> dict | None:
    run = conn.execute(
        "SELECT artifact_path FROM model_runs WHERE id = ?",
        (run_id,),
    ).fetchone()
    if not run or not run[0]:
        raise ValueError(f"No artifact found for run_id={run_id}")

    import pickle

    with open(run[0], "rb") as f:
        pipeline = pickle.load(f)

    feature_row = pd.read_sql_query(
        """
        SELECT *
        FROM btc_features_15m
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        conn,
    )
    if feature_row.empty:
        return None

    timestamp = feature_row["timestamp"].iloc[0]
    target_timestamp = (pd.Timestamp(timestamp) + timedelta(minutes=15)).isoformat()
    prob_up = float(pipeline.predict_proba(feature_row[FEATURE_COLUMNS])[:, 1][0])
    pred = int(prob_up >= 0.5)

    yes_ask, yes_bid = _load_kalshi_snapshot(conn)
    if yes_ask is None:
        log.warning("forward_paper: no kalshi_market_snapshots row — skipping entry")
        return None

    action, position, edge_val = _edge_action(prob_up, yes_ask, yes_bid)
    return {
        "strategy_name": strategy_name,
        "run_id": run_id,
        "prediction_timestamp": utc_now_iso(),
        "target_timestamp": target_timestamp,
        "predicted_direction": pred,
        "prob_up": prob_up,
        "action": action,
        "position": position,
        "rationale": (
            f"edge_based prob_up={prob_up:.4f} yes_ask={yes_ask:.4f} "
            f"yes_bid={yes_bid:.4f} edge={edge_val:.4f}"
        ),
    }


def persist_prediction(conn, payload: dict) -> int | None:
    if payload is None:
        return None
    created_at = utc_now_iso()
    conn.execute(
        """
        INSERT INTO paper_model_predictions
            (strategy_name, run_id, prediction_timestamp, target_timestamp, predicted_direction, prob_up,
             action, position, rationale, market_context_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(strategy_name, target_timestamp) DO UPDATE SET
            predicted_direction=excluded.predicted_direction,
            prob_up=excluded.prob_up,
            action=excluded.action,
            position=excluded.position,
            rationale=excluded.rationale,
            market_context_json=excluded.market_context_json
        """,
        (
            payload["strategy_name"],
            payload["run_id"],
            payload["prediction_timestamp"],
            payload["target_timestamp"],
            payload["predicted_direction"],
            payload["prob_up"],
            payload["action"],
            payload["position"],
            payload["rationale"],
            json_dumps({"source": "btc_features_15m"}),
            created_at,
        ),
    )
    conn.commit()
    row = conn.execute(
        """
        SELECT id
        FROM paper_model_predictions
        WHERE strategy_name = ? AND target_timestamp = ?
        """,
        (payload["strategy_name"], payload["target_timestamp"]),
    ).fetchone()
    return int(row[0]) if row else None


def resolve_predictions(conn) -> int:
    labels = {
        row["timestamp"]: row
        for row in conn.execute(
            """
            SELECT timestamp, direction_up, forward_return
            FROM btc_labels_15m
            WHERE direction_up IS NOT NULL
            """
        ).fetchall()
    }
    open_rows = conn.execute(
        """
        SELECT id, strategy_name, target_timestamp, predicted_direction, position
        FROM paper_model_predictions
        WHERE status = 'open'
        ORDER BY target_timestamp ASC
        """
    ).fetchall()
    resolved = 0
    cumulative_by_strategy = {}
    for row in conn.execute(
        """
        SELECT strategy_name, COALESCE(MAX(cumulative_pnl), 0.0)
        FROM paper_model_predictions
        WHERE status = 'resolved'
        GROUP BY strategy_name
        """
    ).fetchall():
        cumulative_by_strategy[row[0]] = float(row[1] or 0.0)

    for item in open_rows:
        label = labels.get(item["target_timestamp"])
        if not label:
            continue
        actual_direction = int(label["direction_up"])
        actual_return = float(label["forward_return"])
        correct = int(actual_direction == int(item["predicted_direction"]))
        pnl = float(item["position"]) * actual_return
        cumulative = cumulative_by_strategy.get(item["strategy_name"], 0.0) + pnl
        cumulative_by_strategy[item["strategy_name"]] = cumulative
        conn.execute(
            """
            UPDATE paper_model_predictions
            SET status = 'resolved',
                actual_direction = ?,
                actual_return = ?,
                correct = ?,
                pnl = ?,
                cumulative_pnl = ?,
                resolved_at = ?
            WHERE id = ?
            """,
            (
                actual_direction,
                actual_return,
                correct,
                pnl,
                cumulative,
                utc_now_iso(),
                int(item["id"]),
            ),
        )
        resolved += 1
    conn.commit()
    return resolved


def predict_cross_market_rf(conn, strategy_name: str, threshold: float = 0.55) -> dict | None:
    """
    Load the cross_market_rf artifact trained by /api/strategy-explorer, assemble
    the latest feature row with live Kalshi + Polymarket cross-market features,
    predict direction, and return a payload suitable for persist_prediction().
    """
    artifact_path = os.path.join(_ARTIFACTS_DIR, "cross_market_rf.pkl")
    if not os.path.exists(artifact_path):
        raise FileNotFoundError(
            f"No artifact at {artifact_path}. "
            "Train first via the dashboard Explorer tab or GET /api/strategy-explorer?refresh=1"
        )

    with open(artifact_path, "rb") as fh:
        pipeline = pickle.load(fh)

    # Latest BTC feature row
    feature_row = pd.read_sql_query(
        "SELECT * FROM btc_features_15m ORDER BY timestamp DESC LIMIT 1", conn
    )
    if feature_row.empty:
        return None

    timestamp = feature_row["timestamp"].iloc[0]
    target_timestamp = (pd.Timestamp(timestamp) + timedelta(minutes=15)).isoformat()

    # Latest Kalshi tick
    kalshi = conn.execute(
        """SELECT yes_bid_dollars, yes_ask_dollars, volume_24h_fp
           FROM markets WHERE yes_bid_dollars IS NOT NULL
           ORDER BY collected_at DESC LIMIT 1"""
    ).fetchone()

    # Latest Polymarket tick
    poly = conn.execute(
        """SELECT up_bid, up_ask, volume_24h
           FROM polymarket_markets WHERE up_bid IS NOT NULL
           ORDER BY collected_at DESC LIMIT 1"""
    ).fetchone()

    if kalshi and poly:
        kalshi_mid   = (kalshi["yes_bid_dollars"] + kalshi["yes_ask_dollars"]) / 2.0
        poly_mid     = (poly["up_bid"] + poly["up_ask"]) / 2.0
        cross_spread = kalshi_mid - poly_mid
        kalshi_volume = float(kalshi["volume_24h_fp"]) if kalshi["volume_24h_fp"] is not None else float("nan")
        poly_volume   = float(poly["volume_24h"])      if poly["volume_24h"]      is not None else float("nan")
    else:
        kalshi_mid = poly_mid = cross_spread = kalshi_volume = poly_volume = float("nan")

    # Assemble feature vector in training column order
    X = feature_row[FEATURE_COLUMNS].copy()
    X["kalshi_mid"]   = kalshi_mid
    X["poly_mid"]     = poly_mid
    X["cross_spread"] = cross_spread
    X["kalshi_volume"] = kalshi_volume
    X["poly_volume"]   = poly_volume
    X = X[_CROSS_MARKET_FEATURE_COLUMNS]

    prob_up = float(pipeline.predict_proba(X)[:, 1][0])
    pred    = int(prob_up >= 0.5)

    yes_ask, yes_bid = _load_kalshi_snapshot(conn)
    if yes_ask is None:
        log.warning("forward_paper: no kalshi_market_snapshots row — skipping entry")
        return None

    action, position, edge_val = _edge_action(prob_up, yes_ask, yes_bid)
    return {
        "strategy_name":        strategy_name,
        "run_id":               None,
        "prediction_timestamp": utc_now_iso(),
        "target_timestamp":     target_timestamp,
        "predicted_direction":  pred,
        "prob_up":              prob_up,
        "action":               action,
        "position":             position,
        "rationale":            (
            f"cross_market_rf prob_up={prob_up:.4f} yes_ask={yes_ask:.4f} "
            f"yes_bid={yes_bid:.4f} edge={edge_val:.4f}"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate/resolve forward paper model predictions")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--predict", action="store_true")
    parser.add_argument("--resolve", action="store_true")
    parser.add_argument("--run-id", type=int)
    parser.add_argument("--model-name")
    parser.add_argument("--strategy-name", default="ml_probability_threshold")
    parser.add_argument("--strategy", default="ml_probability_threshold",
                        choices=["ml_probability_threshold", "cross_market_rf"],
                        help="Which strategy to use for prediction")
    parser.add_argument("--threshold", type=float, default=0.55)
    args = parser.parse_args()

    conn = get_conn(args.db_path)
    try:
        ensure_research_schema(conn)
        if args.predict:
            if args.strategy == "cross_market_rf":
                pred = predict_cross_market_rf(conn, args.strategy_name or "cross_market_rf", threshold=args.threshold)
            else:
                run_id = args.run_id or latest_run_id(conn, args.model_name)
                pred = load_artifact_and_predict(conn, run_id, args.strategy_name, threshold=args.threshold)
            pred_id = persist_prediction(conn, pred)
            print(f"Stored forward paper prediction id={pred_id}")
        if args.resolve:
            resolved = resolve_predictions(conn)
            print(f"Resolved predictions: {resolved}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
