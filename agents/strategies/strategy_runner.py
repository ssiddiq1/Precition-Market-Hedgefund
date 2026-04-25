import argparse

import pandas as pd

try:
    from research_db import DB_PATH, ensure_research_schema, get_conn
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import DB_PATH, ensure_research_schema, get_conn


def latest_run_id(conn, model_name: str | None = None) -> int:
    if model_name:
        row = conn.execute(
            "SELECT id FROM model_runs WHERE model_name = ? ORDER BY id DESC LIMIT 1",
            (model_name,),
        ).fetchone()
    else:
        row = conn.execute("SELECT id FROM model_runs ORDER BY id DESC LIMIT 1").fetchone()
    if not row:
        raise ValueError("No model runs available.")
    return int(row[0])


def load_prediction_frame(conn, run_id: int, split_name: str = "test") -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT p.timestamp, p.y_true, p.y_pred, p.prob_up, l.forward_return, l.no_trade
        FROM model_predictions p
        JOIN btc_labels_15m l ON l.timestamp = p.timestamp
        WHERE p.run_id = ? AND p.split_name = ?
        ORDER BY p.timestamp ASC
        """,
        conn,
        params=(run_id, split_name),
    )
    if df.empty:
        raise ValueError(f"No predictions found for run_id={run_id} split={split_name}.")
    return df


def generate_signals(
    pred_df: pd.DataFrame,
    mode: str = "probability_threshold",
    threshold: float = 0.55,
    no_trade_band: float = 0.05,
    cooldown_bars: int = 0,
) -> pd.DataFrame:
    rows = []
    cooldown = 0
    prev_position = 0.0
    for row in pred_df.itertuples(index=False):
        prob_up = float(row.prob_up)
        pred = int(row.y_pred)
        action = "hold"
        position = prev_position
        reason = mode

        if cooldown > 0:
            cooldown -= 1
            action = "cooldown"
            position = 0.0
        elif mode == "long_short":
            position = 1.0 if pred == 1 else -1.0
            action = "enter_long" if position > 0 else "enter_short"
        elif mode == "long_flat":
            position = 1.0 if pred == 1 else 0.0
            action = "enter_long" if position > 0 else "flat"
        elif mode == "probability_threshold":
            if prob_up >= threshold:
                position = 1.0
                action = "long"
                reason = f"prob_up>={threshold:.2f}"
            elif prob_up <= 1.0 - threshold:
                position = -1.0
                action = "short"
                reason = f"prob_up<={1.0-threshold:.2f}"
            else:
                position = 0.0
                action = "flat"
                reason = "inside_threshold"
        elif mode == "banded":
            lower = 0.5 - no_trade_band
            upper = 0.5 + no_trade_band
            if prob_up >= upper:
                position = 1.0
                action = "long"
                reason = f"prob_up>={upper:.2f}"
            elif prob_up <= lower:
                position = -1.0
                action = "short"
                reason = f"prob_up<={lower:.2f}"
            else:
                position = 0.0
                action = "flat"
                reason = "no_trade_band"
        else:
            raise ValueError(f"Unsupported strategy mode '{mode}'")

        if cooldown_bars > 0 and position != prev_position and action not in ("flat", "hold", "cooldown"):
            cooldown = cooldown_bars

        rows.append(
            {
                "timestamp": row.timestamp,
                "model_prediction": pred,
                "prob_up": prob_up,
                "action": action,
                "position": position,
                "rule_tag": reason,
                "forward_return": float(row.forward_return),
                "y_true": int(row.y_true),
            }
        )
        prev_position = position
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate strategy signals from model outputs")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--run-id", type=int)
    parser.add_argument("--model-name")
    parser.add_argument("--split", default="test")
    parser.add_argument("--mode", default="probability_threshold", choices=["long_short", "long_flat", "probability_threshold", "banded"])
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--no-trade-band", type=float, default=0.05)
    parser.add_argument("--cooldown", type=int, default=0)
    args = parser.parse_args()
    conn = get_conn(args.db_path)
    try:
        ensure_research_schema(conn)
        run_id = args.run_id or latest_run_id(conn, args.model_name)
        pred_df = load_prediction_frame(conn, run_id, args.split)
    finally:
        conn.close()
    signals = generate_signals(
        pred_df,
        mode=args.mode,
        threshold=args.threshold,
        no_trade_band=args.no_trade_band,
        cooldown_bars=args.cooldown,
    )
    print(signals.tail(10).to_string(index=False))


if __name__ == "__main__":
    main()
