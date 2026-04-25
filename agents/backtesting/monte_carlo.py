import argparse

import numpy as np
import pandas as pd

try:
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import DB_PATH, ensure_research_schema, get_conn, json_dumps, utc_now_iso


def load_backtest_returns(conn, backtest_id: int) -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT timestamp, pnl
        FROM strategy_backtest_points
        WHERE backtest_id = ?
        ORDER BY timestamp ASC
        """,
        conn,
        params=(backtest_id,),
    )
    if df.empty:
        raise ValueError(f"No backtest points found for backtest_id={backtest_id}")
    return df


def _path_metrics(returns: np.ndarray) -> tuple[float, float, float, float]:
    equity = np.cumprod(1.0 + returns)
    running_max = np.maximum.accumulate(equity)
    drawdown = equity / running_max - 1.0
    total_return = float(equity[-1] - 1.0)
    max_drawdown = float(drawdown.min())
    sharpe = 0.0
    if returns.std(ddof=0) > 0:
        sharpe = float((returns.mean() / returns.std(ddof=0)) * np.sqrt(365 * 24 * 4))
    return total_return, max_drawdown, sharpe, float(equity[-1])


def bootstrap_trade_returns(returns: np.ndarray, n_simulations: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    results = []
    for sim_idx in range(n_simulations):
        sampled = rng.choice(returns, size=len(returns), replace=True)
        total_return, max_drawdown, sharpe, final_equity = _path_metrics(sampled)
        results.append(
            {
                "simulation_index": sim_idx,
                "total_return": total_return,
                "max_drawdown": max_drawdown,
                "sharpe": sharpe,
                "final_equity": final_equity,
            }
        )
    return pd.DataFrame(results)


def persist_monte_carlo(conn, backtest_id: int, method: str, seed: int, config: dict, results: pd.DataFrame) -> int:
    summary = {
        "mean_total_return": float(results["total_return"].mean()),
        "p05_total_return": float(results["total_return"].quantile(0.05)),
        "p50_total_return": float(results["total_return"].quantile(0.50)),
        "p95_total_return": float(results["total_return"].quantile(0.95)),
        "mean_max_drawdown": float(results["max_drawdown"].mean()),
        "p95_max_drawdown": float(results["max_drawdown"].quantile(0.95)),
        "mean_sharpe": float(results["sharpe"].mean()),
    }
    created_at = utc_now_iso()
    conn.execute(
        """
        INSERT INTO monte_carlo_runs
            (backtest_id, method, n_simulations, seed, config_json, summary_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            backtest_id,
            method,
            int(len(results)),
            seed,
            json_dumps(config),
            json_dumps(summary),
            created_at,
        ),
    )
    mc_run_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
    conn.executemany(
        """
        INSERT INTO monte_carlo_results
            (mc_run_id, simulation_index, total_return, max_drawdown, sharpe, final_equity, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                mc_run_id,
                int(row.simulation_index),
                float(row.total_return),
                float(row.max_drawdown),
                float(row.sharpe),
                float(row.final_equity),
                created_at,
            )
            for row in results.itertuples(index=False)
        ],
    )
    conn.commit()
    return mc_run_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Monte Carlo stress tests on a stored backtest")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--backtest-id", type=int, required=True)
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    conn = get_conn(args.db_path)
    try:
        ensure_research_schema(conn)
        df = load_backtest_returns(conn, args.backtest_id)
        results = bootstrap_trade_returns(df["pnl"].to_numpy(dtype=float), n_simulations=args.n, seed=args.seed)
        mc_run_id = persist_monte_carlo(
            conn,
            args.backtest_id,
            method="bootstrap_trade_returns",
            seed=args.seed,
            config={"n": args.n},
            results=results,
        )
    finally:
        conn.close()

    print(f"Monte Carlo stored as id={mc_run_id}")
    print(results.describe().to_string())


if __name__ == "__main__":
    main()
