import argparse
import sqlite3

import numpy as np
import pandas as pd

try:
    from research_db import DB_PATH, ensure_research_schema, get_conn, utc_now_iso
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import DB_PATH, ensure_research_schema, get_conn, utc_now_iso

FEATURE_VERSION = "v1"
LABEL_VERSION = "v1"


def load_ohlcv_frame(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT timestamp, open, high, low, close, volume, source
        FROM btc_ohlcv_15m
        ORDER BY timestamp ASC
        """,
        conn,
    )
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def compute_labels(df: pd.DataFrame, threshold_bps: float = 5.0) -> pd.DataFrame:
    out = df[["timestamp", "close"]].copy()
    out["next_timestamp"] = df["timestamp"].shift(-1)
    out["close_t"] = df["close"]
    out["close_t1"] = df["close"].shift(-1)
    out["forward_return"] = out["close_t1"] / out["close_t"] - 1.0
    out["abs_move"] = out["forward_return"].abs()
    out["direction_up"] = (out["close_t1"] > out["close_t"]).astype("float")
    thr = threshold_bps / 10000.0
    out["significant_up"] = (out["forward_return"] > thr).astype("float")
    out["significant_down"] = (out["forward_return"] < -thr).astype("float")
    out["no_trade"] = (out["abs_move"] < thr).astype("float")
    out["threshold_bps"] = threshold_bps
    out["label_version"] = LABEL_VERSION
    out["created_at"] = utc_now_iso()
    out.loc[out["close_t1"].isna(), ["direction_up", "significant_up", "significant_down", "no_trade"]] = np.nan
    out["timestamp"] = out["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S%z").str.replace("+0000", "+00:00", regex=False)
    out["next_timestamp"] = out["next_timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S%z").str.replace("+0000", "+00:00", regex=False)
    return out


def _rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0.0)
    down = -delta.clip(upper=0.0)
    avg_gain = up.rolling(window, min_periods=window).mean()
    avg_loss = down.rolling(window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def _streak_flags(returns: pd.Series) -> tuple[pd.Series, pd.Series]:
    up_streak = []
    down_streak = []
    up = 0
    down = 0
    for value in returns.fillna(0.0):
        if value > 0:
            up += 1
            down = 0
        elif value < 0:
            down += 1
            up = 0
        else:
            up = 0
            down = 0
        up_streak.append(up)
        down_streak.append(down)
    return pd.Series(up_streak, index=returns.index), pd.Series(down_streak, index=returns.index)


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df[["timestamp", "close", "volume", "open", "high", "low"]].copy()
    out["return_1"] = df["close"].pct_change(1)
    out["return_2"] = df["close"].pct_change(2)
    out["return_4"] = df["close"].pct_change(4)
    out["return_8"] = df["close"].pct_change(8)
    out["rolling_mean_return_4"] = out["return_1"].rolling(4, min_periods=4).mean()
    out["rolling_mean_return_8"] = out["return_1"].rolling(8, min_periods=8).mean()
    out["rolling_vol_4"] = out["return_1"].rolling(4, min_periods=4).std()
    out["rolling_vol_8"] = out["return_1"].rolling(8, min_periods=8).std()
    out["rolling_vol_16"] = out["return_1"].rolling(16, min_periods=16).std()
    out["momentum_4"] = df["close"] / df["close"].shift(4) - 1.0
    out["momentum_8"] = df["close"] / df["close"].shift(8) - 1.0
    out["momentum_16"] = df["close"] / df["close"].shift(16) - 1.0
    out["rsi_14"] = _rsi(df["close"], 14)
    out["sma_4_dist"] = df["close"] / df["close"].rolling(4, min_periods=4).mean() - 1.0
    out["sma_8_dist"] = df["close"] / df["close"].rolling(8, min_periods=8).mean() - 1.0
    out["sma_16_dist"] = df["close"] / df["close"].rolling(16, min_periods=16).mean() - 1.0
    out["ema_4_dist"] = df["close"] / df["close"].ewm(span=4, adjust=False).mean() - 1.0
    out["ema_8_dist"] = df["close"] / df["close"].ewm(span=8, adjust=False).mean() - 1.0
    vol_mean = df["volume"].rolling(16, min_periods=16).mean()
    vol_std = df["volume"].rolling(16, min_periods=16).std()
    out["volume_z_16"] = (df["volume"] - vol_mean) / vol_std.replace(0.0, np.nan)
    body = df["close"] - df["open"]
    range_ = (df["high"] - df["low"]).replace(0.0, np.nan)
    out["candle_body"] = body / df["open"].replace(0.0, np.nan)
    out["upper_wick_ratio"] = (df["high"] - np.maximum(df["open"], df["close"])) / range_
    out["lower_wick_ratio"] = (np.minimum(df["open"], df["close"]) - df["low"]) / range_
    out["hl_range"] = range_ / df["close"].replace(0.0, np.nan)
    out["realized_vol_proxy"] = np.log(df["high"] / df["low"]).replace([np.inf, -np.inf], np.nan)
    out["streak_up"], out["streak_down"] = _streak_flags(out["return_1"])
    out["hour_of_day"] = df["timestamp"].dt.hour
    out["day_of_week"] = df["timestamp"].dt.dayofweek
    out["session_asia"] = df["timestamp"].dt.hour.isin([0, 1, 2, 3, 4, 5, 6, 7]).astype(int)
    out["session_europe"] = df["timestamp"].dt.hour.isin([8, 9, 10, 11, 12, 13, 14, 15]).astype(int)
    out["session_us"] = df["timestamp"].dt.hour.isin([16, 17, 18, 19, 20, 21, 22, 23]).astype(int)
    out["regime_vol_high"] = (
        out["rolling_vol_16"] > out["rolling_vol_16"].rolling(32, min_periods=16).median()
    ).astype("float")
    out["regime_trend_up"] = (out["momentum_16"] > 0).astype("float")
    out["feature_version"] = FEATURE_VERSION
    out["created_at"] = utc_now_iso()
    out["timestamp"] = out["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S%z").str.replace("+0000", "+00:00", regex=False)
    return out.drop(columns=["open", "high", "low"])


def persist_labels(conn: sqlite3.Connection, labels: pd.DataFrame) -> int:
    ordered = labels[
        [
            "timestamp",
            "next_timestamp",
            "close_t",
            "close_t1",
            "direction_up",
            "forward_return",
            "abs_move",
            "significant_up",
            "significant_down",
            "no_trade",
            "threshold_bps",
            "label_version",
            "created_at",
        ]
    ].copy()
    conn.execute("BEGIN")
    try:
        conn.execute("DELETE FROM btc_labels_15m")
        conn.executemany(
            """
            INSERT INTO btc_labels_15m
                (timestamp, next_timestamp, close_t, close_t1, direction_up, forward_return, abs_move,
                 significant_up, significant_down, no_trade, threshold_bps, label_version, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ordered.where(pd.notnull(ordered), None).values.tolist(),
        )
        conn.commit()
    except:
        conn.execute("ROLLBACK")
        raise
    return len(ordered)


def persist_features(conn: sqlite3.Connection, features: pd.DataFrame) -> int:
    ordered = features[
        [
            "timestamp",
            "close",
            "volume",
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
            "feature_version",
            "created_at",
        ]
    ].copy()
    conn.execute("BEGIN")
    try:
        conn.execute("DELETE FROM btc_features_15m")
        conn.executemany(
            """
            INSERT INTO btc_features_15m
                (timestamp, close, volume, return_1, return_2, return_4, return_8,
                 rolling_mean_return_4, rolling_mean_return_8, rolling_vol_4, rolling_vol_8, rolling_vol_16,
                 momentum_4, momentum_8, momentum_16, rsi_14, sma_4_dist, sma_8_dist, sma_16_dist,
                 ema_4_dist, ema_8_dist, volume_z_16, candle_body, upper_wick_ratio, lower_wick_ratio,
                 hl_range, realized_vol_proxy, streak_up, streak_down, hour_of_day, day_of_week,
                 session_asia, session_europe, session_us, regime_vol_high, regime_trend_up,
                 feature_version, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ordered.where(pd.notnull(ordered), None).values.tolist(),
        )
        conn.commit()
    except:
        conn.execute("ROLLBACK")
        raise
    return len(ordered)


def build_datasets(conn: sqlite3.Connection, threshold_bps: float = 5.0) -> dict:
    ensure_research_schema(conn)
    df = load_ohlcv_frame(conn)
    if df.empty:
        return {"ohlcv_rows": 0, "label_rows": 0, "feature_rows": 0}
    labels = compute_labels(df, threshold_bps=threshold_bps)
    features = compute_features(df)
    return {
        "ohlcv_rows": len(df),
        "label_rows": persist_labels(conn, labels),
        "feature_rows": persist_features(conn, features),
        "feature_version": FEATURE_VERSION,
        "label_version": LABEL_VERSION,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build BTC labels and features")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--threshold-bps", type=float, default=5.0)
    args = parser.parse_args()
    conn = get_conn(args.db_path)
    try:
        summary = build_datasets(conn, threshold_bps=args.threshold_bps)
    finally:
        conn.close()
    print("Dataset build complete")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
