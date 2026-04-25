import argparse
import logging
import os
import pickle
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

log = logging.getLogger(__name__)

try:
    from research_db import (
        DB_PATH,
        ensure_research_schema,
        get_conn,
        json_dumps,
        utc_now_iso,
    )
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import (
        DB_PATH,
        ensure_research_schema,
        get_conn,
        json_dumps,
        utc_now_iso,
    )

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "artifacts", "models")


@dataclass
class SplitSlices:
    train: pd.DataFrame
    valid: pd.DataFrame
    test: pd.DataFrame


FEATURE_COLUMNS = [
    "return_1",
    "return_2",
    "return_4",
    "return_8",
    "rolling_mean_return_4",
    "rolling_mean_return_8",
    "rolling_vol_4",
    "rolling_vol_8",
    "rolling_vol_16",
    "momentum_4",
    "momentum_8",
    "momentum_16",
    "rsi_14",
    "sma_4_dist",
    "sma_8_dist",
    "sma_16_dist",
    "ema_4_dist",
    "ema_8_dist",
    "volume_z_16",
    "candle_body",
    "upper_wick_ratio",
    "lower_wick_ratio",
    "hl_range",
    "realized_vol_proxy",
    "streak_up",
    "streak_down",
    "hour_of_day",
    "day_of_week",
    "session_asia",
    "session_europe",
    "session_us",
    "regime_vol_high",
    "regime_trend_up",
]

CROSS_MARKET_FEATURE_COLUMNS = FEATURE_COLUMNS + [
    "kalshi_mid",
    "poly_mid",
    "cross_spread",
    "kalshi_volume",
    "poly_volume",
]


def _ensure_brier_score_column(conn) -> None:
    """Add brier_score column to model_runs if it doesn't already exist."""
    try:
        conn.execute("ALTER TABLE model_runs ADD COLUMN brier_score REAL")
        conn.commit()
    except Exception:
        pass  # column already exists


def load_model_frame(conn) -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT f.*, l.direction_up, l.forward_return, l.no_trade, l.label_version
        FROM btc_features_15m f
        JOIN btc_labels_15m l USING(timestamp)
        ORDER BY f.timestamp ASC
        """,
        conn,
    )
    if df.empty:
        return df
    df = df.dropna(subset=["direction_up"])
    df["direction_up"] = df["direction_up"].astype(int)
    return df


def split_time_series(df: pd.DataFrame, train_frac: float = 0.6, valid_frac: float = 0.2) -> SplitSlices:
    n = len(df)
    train_end = max(1, int(n * train_frac))
    valid_end = max(train_end + 1, int(n * (train_frac + valid_frac)))
    return SplitSlices(
        train=df.iloc[:train_end].copy(),
        valid=df.iloc[train_end:valid_end].copy(),
        test=df.iloc[valid_end:].copy(),
    )


def build_model(model_name: str):
    if model_name == "logistic_regression":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
            ]
        )
    if model_name == "random_forest":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=8,
                        min_samples_leaf=10,
                        random_state=42,
                        n_jobs=-1,
                        class_weight="balanced_subsample",
                    ),
                ),
            ]
        )
    raise ValueError(f"Unsupported model '{model_name}'")


def build_cross_market_model() -> Pipeline:
    """RandomForest wrapped with isotonic calibration for the 40-feature cross-market model."""
    base_rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    calibrated = CalibratedClassifierCV(base_rf, method="isotonic", cv=3)
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("model", calibrated),
        ]
    )


def load_cross_market_frame(conn) -> pd.DataFrame:
    """Join BTC features + labels + Kalshi + Polymarket snapshots into one frame."""
    df = pd.read_sql_query(
        """
        SELECT
            f.*,
            l.direction_up,
            l.forward_return,
            l.no_trade,
            l.label_version,
            -- Kalshi mid price
            (km.yes_bid_dollars + km.yes_ask_dollars) / 2.0 AS kalshi_mid,
            km.volume_24h_fp                                 AS kalshi_volume,
            (km.yes_ask_dollars - km.yes_bid_dollars)        AS kalshi_spread,
            -- Polymarket mid price (NULL if table absent)
            (pm.best_bid + pm.best_ask) / 2.0               AS poly_mid,
            pm.volume                                        AS poly_volume
        FROM btc_features_15m f
        JOIN btc_labels_15m l USING(timestamp)
        LEFT JOIN kalshi_market_snapshots km
               ON km.snapped_at = (
                   SELECT MAX(snapped_at)
                   FROM kalshi_market_snapshots k2
                   WHERE k2.snapped_at <= f.timestamp
               )
        LEFT JOIN polymarket_markets pm
               ON pm.timestamp = (
                   SELECT MAX(p2.timestamp)
                   FROM polymarket_markets p2
                   WHERE p2.timestamp <= f.timestamp
               )
        ORDER BY f.timestamp ASC
        """,
        conn,
    )
    if df.empty:
        return df
    df = df.dropna(subset=["direction_up"])
    df["direction_up"] = df["direction_up"].astype(int)
    # Derived cross-market spread
    df["cross_spread"] = df["kalshi_mid"].sub(df["poly_mid"])
    return df


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, prob_up: np.ndarray) -> dict:
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "directional_hit_rate": float((y_true == y_pred).mean()),
        "class_balance_up": float(np.mean(y_true)),
        "confusion_matrix": matrix,
    }
    if len(np.unique(y_true)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_true, prob_up))
    else:
        metrics["roc_auc"] = None
    return metrics


def feature_importance_from_pipeline(model_name: str, pipeline: Pipeline, columns: list[str]) -> dict:
    model = pipeline.named_steps["model"]
    # Unwrap CalibratedClassifierCV to get underlying estimator
    if isinstance(model, CalibratedClassifierCV):
        if hasattr(model, "calibrated_classifiers_") and model.calibrated_classifiers_:
            model = model.calibrated_classifiers_[0].estimator
        else:
            return {}
    if model_name in ("random_forest", "cross_market_rf") and hasattr(model, "feature_importances_"):
        values = model.feature_importances_
        return dict(sorted(zip(columns, map(float, values)), key=lambda kv: kv[1], reverse=True)[:15])
    if model_name == "logistic_regression" and hasattr(model, "coef_"):
        coefs = model.coef_[0]
        ranked = sorted(zip(columns, map(float, coefs)), key=lambda kv: abs(kv[1]), reverse=True)
        return dict(ranked[:15])
    return {}


def save_artifact(pipeline: Pipeline, run_name: str) -> str:
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    path = os.path.join(ARTIFACTS_DIR, f"{run_name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(pipeline, f)
    return path


def persist_run(
    conn,
    model_name: str,
    run_name: str,
    frame: pd.DataFrame,
    splits: SplitSlices,
    pipeline: Pipeline,
    feature_cols: list[str] | None = None,
    brier_score: float | None = None,
) -> int:
    if feature_cols is None:
        feature_cols = FEATURE_COLUMNS
    X_train = splits.train[feature_cols]
    y_train = splits.train["direction_up"].to_numpy()
    pipeline.fit(X_train, y_train)

    split_frames = {"train": splits.train, "valid": splits.valid, "test": splits.test}
    split_metrics = {}
    prediction_rows = []

    for split_name, split_df in split_frames.items():
        if split_df.empty:
            continue
        X = split_df[feature_cols]
        y = split_df["direction_up"].to_numpy()
        prob_up = pipeline.predict_proba(X)[:, 1]
        y_pred = (prob_up >= 0.5).astype(int)
        metrics = compute_metrics(y, y_pred, prob_up)
        if split_name == "test" and brier_score is None and len(np.unique(y)) > 1:
            brier_score = float(brier_score_loss(y, prob_up))
        split_metrics[split_name] = metrics
        for ts, true_value, pred_value, prob in zip(split_df["timestamp"], y, y_pred, prob_up):
            prediction_rows.append((ts, split_name, int(true_value), int(pred_value), float(1.0 - prob), float(prob)))

    artifact_path = save_artifact(pipeline, run_name)
    feature_importance = feature_importance_from_pipeline(model_name, pipeline, feature_cols)
    created_at = utc_now_iso()
    params = pipeline.named_steps["model"].get_params()
    _ensure_brier_score_column(conn)
    conn.execute(
        """
        INSERT INTO model_runs
            (run_name, model_name, feature_version, label_version, train_start, train_end, valid_start, valid_end,
             test_start, test_end, target_col, params_json, metrics_json, feature_importance_json, artifact_path,
             brier_score, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_name,
            model_name,
            str(frame["feature_version"].iloc[-1]),
            str(frame["label_version"].iloc[-1]),
            splits.train["timestamp"].iloc[0] if not splits.train.empty else None,
            splits.train["timestamp"].iloc[-1] if not splits.train.empty else None,
            splits.valid["timestamp"].iloc[0] if not splits.valid.empty else None,
            splits.valid["timestamp"].iloc[-1] if not splits.valid.empty else None,
            splits.test["timestamp"].iloc[0] if not splits.test.empty else None,
            splits.test["timestamp"].iloc[-1] if not splits.test.empty else None,
            "direction_up",
            json_dumps(params),
            json_dumps(split_metrics),
            json_dumps(feature_importance),
            artifact_path,
            brier_score,
            created_at,
        ),
    )
    run_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
    conn.executemany(
        """
        INSERT INTO model_predictions
            (run_id, timestamp, split_name, y_true, y_pred, prob_down, prob_up, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(run_id, ts, split_name, y_true, y_pred, prob_down, prob_up, created_at) for ts, split_name, y_true, y_pred, prob_down, prob_up in prediction_rows],
    )
    conn.commit()
    return run_id


def train_cross_market_model(conn) -> dict:
    """Train calibrated RF on 40 cross-market features and persist the run."""
    ensure_research_schema(conn)
    frame = load_cross_market_frame(conn)
    if len(frame) < 50:
        raise ValueError("Need at least 50 labeled rows before training cross-market model.")
    # Fill missing cross-market cols (tables may be empty / not yet joined)
    for col in CROSS_MARKET_FEATURE_COLUMNS:
        if col not in frame.columns:
            frame[col] = np.nan
    splits = split_time_series(frame)
    pipeline = build_cross_market_model()
    run_name = f"cross_market_rf_{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%S')}"
    run_id = persist_run(conn, "cross_market_rf", run_name, frame, splits, pipeline, feature_cols=CROSS_MARKET_FEATURE_COLUMNS)

    # Save dedicated artifact
    calibrated_path = os.path.join(ARTIFACTS_DIR, "cross_market_rf_calibrated.pkl")
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    import pickle as _pkl
    with open(calibrated_path, "wb") as fh:
        _pkl.dump(pipeline, fh)

    row = conn.execute("SELECT metrics_json, brier_score FROM model_runs WHERE id = ?", (run_id,)).fetchone()
    brier = row[1]
    log.info("cross_market_rf run_id=%d brier_score=%.4f saved to %s", run_id, brier or 0.0, calibrated_path)
    return {"run_id": run_id, "run_name": run_name, "model_name": "cross_market_rf", "metrics_json": row[0], "brier_score": brier}


def train_models(conn, model_names: list[str]) -> list[dict]:
    ensure_research_schema(conn)
    frame = load_model_frame(conn)
    if len(frame) < 50:
        raise ValueError("Need at least 50 labeled rows before training models.")
    splits = split_time_series(frame)
    outputs = []
    for model_name in model_names:
        pipeline = build_model(model_name)
        run_name = f"{model_name}_{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%S')}"
        run_id = persist_run(conn, model_name, run_name, frame, splits, pipeline)
        metrics_json = conn.execute("SELECT metrics_json FROM model_runs WHERE id = ?", (run_id,)).fetchone()[0]
        outputs.append({"run_id": run_id, "run_name": run_name, "model_name": model_name, "metrics_json": metrics_json})
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Train BTC 15m direction models")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument(
        "--models",
        nargs="+",
        default=["logistic_regression", "random_forest"],
        choices=["logistic_regression", "random_forest"],
    )
    args = parser.parse_args()
    conn = get_conn(args.db_path)
    try:
        outputs = train_models(conn, args.models)
    finally:
        conn.close()
    for item in outputs:
        print(f"{item['model_name']} -> run_id={item['run_id']} run_name={item['run_name']}")


if __name__ == "__main__":
    main()
