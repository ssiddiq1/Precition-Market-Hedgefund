import argparse
from datetime import datetime, timezone

try:
    from agents.ml.dataset_builder import build_datasets
    from agents.orchestration.forward_paper import load_artifact_and_predict, persist_prediction, resolve_predictions
    from agents.collectors.historical_btc_ingest import infer_default_start, ingest_range, init_tables
    from agents.ml.modeling import train_models
    from agents.backtesting.monte_carlo import bootstrap_trade_returns, load_backtest_returns, persist_monte_carlo
    from agents.backtesting.research_backtester import persist_backtest, run_backtest
    from research_db import DB_PATH, get_conn
    from agents.strategies.strategy_runner import latest_run_id, load_prediction_frame
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from agents.ml.dataset_builder import build_datasets
    from agents.orchestration.forward_paper import load_artifact_and_predict, persist_prediction, resolve_predictions
    from agents.collectors.historical_btc_ingest import infer_default_start, ingest_range, init_tables
    from agents.ml.modeling import train_models
    from agents.backtesting.monte_carlo import bootstrap_trade_returns, load_backtest_returns, persist_monte_carlo
    from agents.backtesting.research_backtester import persist_backtest, run_backtest
    from research_db import DB_PATH, get_conn
    from agents.strategies.strategy_runner import latest_run_id, load_prediction_frame


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the end-to-end BTC 15m research workflow")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--days", type=int, default=60)
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--mc-n", type=int, default=250)
    args = parser.parse_args()

    conn = get_conn(args.db_path)
    try:
        init_tables(conn)
        start = infer_default_start(conn, args.days)
        ingest = ingest_range(conn, start=start, end=datetime.now(timezone.utc))
        dataset = build_datasets(conn)
        train_models(conn, ["logistic_regression", "random_forest"])
        run_id = latest_run_id(conn)
        pred_df = load_prediction_frame(conn, run_id, "test")
        points, trades, metrics = run_backtest(
            pred_df,
            strategy_name="ml_probability_threshold",
            strategy_mode="probability_threshold",
            threshold=args.threshold,
        )
        backtest_id = persist_backtest(
            conn,
            run_id,
            "ml_probability_threshold",
            {"mode": "probability_threshold", "threshold": args.threshold, "split": "test"},
            points,
            trades,
            metrics,
        )
        returns = load_backtest_returns(conn, backtest_id)["pnl"].to_numpy(dtype=float)
        mc_results = bootstrap_trade_returns(returns, n_simulations=args.mc_n)
        persist_monte_carlo(conn, backtest_id, "bootstrap_trade_returns", 42, {"n": args.mc_n}, mc_results)
        pred = load_artifact_and_predict(conn, run_id, "ml_probability_threshold", threshold=args.threshold)
        persist_prediction(conn, pred)
        resolved = resolve_predictions(conn)
    finally:
        conn.close()

    print("Research workflow complete")
    print(f"  ingest_rows: {ingest['inserted_or_updated']}")
    print(f"  label_rows: {dataset['label_rows']}")
    print(f"  feature_rows: {dataset['feature_rows']}")
    print(f"  backtest_id: {backtest_id}")
    print(f"  resolved_paper_predictions: {resolved}")


if __name__ == "__main__":
    main()
