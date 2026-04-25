import argparse
from math import sqrt

import numpy as np
import pandas as pd

try:
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso
    from agents.strategies.strategy_runner import generate_signals, latest_run_id, load_prediction_frame
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso
    from agents.strategies.strategy_runner import generate_signals, latest_run_id, load_prediction_frame


def compute_drawdown(equity: pd.Series) -> pd.Series:
    running_max = equity.cummax()
    return equity / running_max - 1.0


def summarize_backtest(df: pd.DataFrame) -> dict:
    returns = df["strategy_return"]
    trades = df[df["action"].isin(["long", "short", "enter_long", "enter_short"])]
    downside = returns[returns < 0]
    sharpe = 0.0
    sortino = 0.0
    if returns.std(ddof=0) > 0:
        sharpe = float((returns.mean() / returns.std(ddof=0)) * sqrt(365 * 24 * 4))
    if not downside.empty and downside.std(ddof=0) > 0:
        sortino = float((returns.mean() / downside.std(ddof=0)) * sqrt(365 * 24 * 4))
    gross_profit = trades["pnl"].clip(lower=0).sum()
    gross_loss = -trades["pnl"].clip(upper=0).sum()
    return {
        "total_return": float(df["equity"].iloc[-1] - 1.0),
        "cumulative_pnl": float(df["pnl"].sum()),
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": float(df["drawdown"].min()),
        "win_rate": float((trades["pnl"] > 0).mean()) if not trades.empty else 0.0,
        "average_trade_return": float(trades["strategy_return"].mean()) if not trades.empty else 0.0,
        "number_of_trades": int(len(trades)),
        "exposure": float((df["position"].abs() > 0).mean()),
        "turnover": float(df["position"].diff().abs().fillna(df["position"].abs()).sum()),
        "profit_factor": float(gross_profit / gross_loss) if gross_loss > 0 else None,
    }


def run_backtest(
    pred_df: pd.DataFrame,
    strategy_name: str,
    strategy_mode: str,
    threshold: float = 0.55,
    no_trade_band: float = 0.05,
    transaction_cost: float = 0.0005,
    slippage: float = 0.0005,
    cooldown_bars: int = 0,
    position_size: float = 1.0,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    signals = generate_signals(
        pred_df,
        mode=strategy_mode,
        threshold=threshold,
        no_trade_band=no_trade_band,
        cooldown_bars=cooldown_bars,
    )
    df = signals.copy()
    df["position"] = df["position"] * position_size
    df["turnover"] = df["position"].diff().abs().fillna(df["position"].abs())
    df["execution_cost"] = df["turnover"] * (transaction_cost + slippage)
    df["strategy_return"] = df["position"] * df["forward_return"] - df["execution_cost"]
    df["pnl"] = df["strategy_return"]
    df["equity"] = (1.0 + df["strategy_return"]).cumprod()
    df["drawdown"] = compute_drawdown(df["equity"])
    trades = df[df["turnover"] > 0].copy()
    trades["reason"] = trades["rule_tag"]
    metrics = summarize_backtest(df)
    metrics["backtest_type"] = "spot_directional"
    metrics["strategy_mode"] = strategy_mode
    return df, trades, metrics


def persist_backtest(conn, run_id: int, strategy_name: str, config: dict, points: pd.DataFrame, trades: pd.DataFrame, metrics: dict) -> int:
    created_at = utc_now_iso()
    conn.execute(
        """
        INSERT INTO strategy_backtests
            (run_id, strategy_name, backtest_type, config_json, metrics_json, trade_count, start_timestamp, end_timestamp, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            strategy_name,
            metrics["backtest_type"],
            json_dumps(config),
            json_dumps(metrics),
            int(metrics["number_of_trades"]),
            points["timestamp"].iloc[0] if not points.empty else None,
            points["timestamp"].iloc[-1] if not points.empty else None,
            created_at,
        ),
    )
    backtest_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
    conn.executemany(
        """
        INSERT INTO strategy_backtest_points
            (backtest_id, timestamp, equity, drawdown, position, signal, realized_return, pnl, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                backtest_id,
                row.timestamp,
                float(row.equity),
                float(row.drawdown),
                float(row.position),
                int(np.sign(row.position)),
                float(row.forward_return),
                float(row.pnl),
                created_at,
            )
            for row in points.itertuples(index=False)
        ],
    )
    conn.executemany(
        """
        INSERT INTO strategy_backtest_trades
            (backtest_id, timestamp, action, position, prob_up, pnl, reason, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                backtest_id,
                row.timestamp,
                row.action,
                float(row.position),
                float(row.prob_up),
                float(row.pnl),
                row.reason,
                created_at,
            )
            for row in trades.itertuples(index=False)
        ],
    )
    conn.commit()
    return backtest_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Run research backtest from model predictions")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--run-id", type=int)
    parser.add_argument("--model-name")
    parser.add_argument("--split", default="test")
    parser.add_argument("--strategy-name", default="ml_probability_threshold")
    parser.add_argument("--mode", default="probability_threshold", choices=["long_short", "long_flat", "probability_threshold", "banded"])
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--no-trade-band", type=float, default=0.05)
    parser.add_argument("--transaction-cost", type=float, default=0.0005)
    parser.add_argument("--slippage", type=float, default=0.0005)
    parser.add_argument("--cooldown", type=int, default=0)
    parser.add_argument("--position-size", type=float, default=1.0)
    args = parser.parse_args()

    conn = get_conn(args.db_path)
    try:
        ensure_research_schema(conn)
        run_id = args.run_id or latest_run_id(conn, args.model_name)
        pred_df = load_prediction_frame(conn, run_id, args.split)
        points, trades, metrics = run_backtest(
            pred_df,
            strategy_name=args.strategy_name,
            strategy_mode=args.mode,
            threshold=args.threshold,
            no_trade_band=args.no_trade_band,
            transaction_cost=args.transaction_cost,
            slippage=args.slippage,
            cooldown_bars=args.cooldown,
            position_size=args.position_size,
        )
        config = {
            "mode": args.mode,
            "threshold": args.threshold,
            "no_trade_band": args.no_trade_band,
            "transaction_cost": args.transaction_cost,
            "slippage": args.slippage,
            "cooldown": args.cooldown,
            "position_size": args.position_size,
            "split": args.split,
        }
        backtest_id = persist_backtest(conn, run_id, args.strategy_name, config, points, trades, metrics)
    finally:
        conn.close()

    print(f"Backtest stored as id={backtest_id}")
    for key, value in metrics.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
