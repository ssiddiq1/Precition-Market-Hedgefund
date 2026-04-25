import json
import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "btc15m.db")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_conn(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def json_dumps(value) -> str:
    return json.dumps(value, sort_keys=True)


def json_loads(value: str | None, default=None):
    if not value:
        return default
    return json.loads(value)


def ensure_research_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS btc_ohlcv_15m (
            timestamp TEXT PRIMARY KEY,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS btc_data_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            expected_timestamp TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            details TEXT,
            created_at TEXT NOT NULL,
            UNIQUE(source, expected_timestamp, issue_type)
        );

        CREATE TABLE IF NOT EXISTS btc_labels_15m (
            timestamp TEXT PRIMARY KEY,
            next_timestamp TEXT,
            close_t REAL NOT NULL,
            close_t1 REAL,
            direction_up INTEGER,
            forward_return REAL,
            abs_move REAL,
            significant_up INTEGER,
            significant_down INTEGER,
            no_trade INTEGER,
            threshold_bps REAL NOT NULL,
            label_version TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS btc_features_15m (
            timestamp TEXT PRIMARY KEY,
            close REAL NOT NULL,
            volume REAL,
            return_1 REAL,
            return_2 REAL,
            return_4 REAL,
            return_8 REAL,
            rolling_mean_return_4 REAL,
            rolling_mean_return_8 REAL,
            rolling_vol_4 REAL,
            rolling_vol_8 REAL,
            rolling_vol_16 REAL,
            momentum_4 REAL,
            momentum_8 REAL,
            momentum_16 REAL,
            rsi_14 REAL,
            sma_4_dist REAL,
            sma_8_dist REAL,
            sma_16_dist REAL,
            ema_4_dist REAL,
            ema_8_dist REAL,
            volume_z_16 REAL,
            candle_body REAL,
            upper_wick_ratio REAL,
            lower_wick_ratio REAL,
            hl_range REAL,
            realized_vol_proxy REAL,
            streak_up REAL,
            streak_down REAL,
            hour_of_day INTEGER,
            day_of_week INTEGER,
            session_asia INTEGER,
            session_europe INTEGER,
            session_us INTEGER,
            regime_vol_high INTEGER,
            regime_trend_up INTEGER,
            feature_version TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS model_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            feature_version TEXT NOT NULL,
            label_version TEXT NOT NULL,
            train_start TEXT,
            train_end TEXT,
            valid_start TEXT,
            valid_end TEXT,
            test_start TEXT,
            test_end TEXT,
            target_col TEXT NOT NULL,
            params_json TEXT NOT NULL,
            metrics_json TEXT NOT NULL,
            feature_importance_json TEXT,
            artifact_path TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            split_name TEXT NOT NULL,
            y_true INTEGER,
            y_pred INTEGER NOT NULL,
            prob_down REAL,
            prob_up REAL,
            created_at TEXT NOT NULL,
            UNIQUE(run_id, timestamp, split_name),
            FOREIGN KEY(run_id) REFERENCES model_runs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS strategy_backtests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            strategy_name TEXT NOT NULL,
            backtest_type TEXT NOT NULL,
            config_json TEXT NOT NULL,
            metrics_json TEXT NOT NULL,
            trade_count INTEGER NOT NULL,
            start_timestamp TEXT,
            end_timestamp TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(run_id) REFERENCES model_runs(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS strategy_backtest_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backtest_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            equity REAL NOT NULL,
            drawdown REAL NOT NULL,
            position REAL NOT NULL,
            signal INTEGER NOT NULL,
            realized_return REAL NOT NULL,
            pnl REAL NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(backtest_id, timestamp),
            FOREIGN KEY(backtest_id) REFERENCES strategy_backtests(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS strategy_backtest_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backtest_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            position REAL NOT NULL,
            prob_up REAL,
            pnl REAL NOT NULL,
            reason TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(backtest_id) REFERENCES strategy_backtests(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS monte_carlo_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backtest_id INTEGER NOT NULL,
            method TEXT NOT NULL,
            n_simulations INTEGER NOT NULL,
            seed INTEGER,
            config_json TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(backtest_id) REFERENCES strategy_backtests(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS monte_carlo_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mc_run_id INTEGER NOT NULL,
            simulation_index INTEGER NOT NULL,
            total_return REAL NOT NULL,
            max_drawdown REAL NOT NULL,
            sharpe REAL NOT NULL,
            final_equity REAL NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(mc_run_id, simulation_index),
            FOREIGN KEY(mc_run_id) REFERENCES monte_carlo_runs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS paper_model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_name TEXT NOT NULL,
            run_id INTEGER,
            prediction_timestamp TEXT NOT NULL,
            target_timestamp TEXT NOT NULL,
            predicted_direction INTEGER NOT NULL,
            prob_up REAL,
            action TEXT NOT NULL,
            position REAL NOT NULL,
            rationale TEXT,
            market_context_json TEXT,
            status TEXT NOT NULL DEFAULT 'open',
            actual_direction INTEGER,
            actual_return REAL,
            correct INTEGER,
            pnl REAL,
            cumulative_pnl REAL,
            resolved_at TEXT,
            created_at TEXT NOT NULL,
            UNIQUE(strategy_name, target_timestamp),
            FOREIGN KEY(run_id) REFERENCES model_runs(id) ON DELETE SET NULL
        );

        CREATE INDEX IF NOT EXISTS idx_btc_ohlcv_source_ts
            ON btc_ohlcv_15m(source, timestamp);
        CREATE INDEX IF NOT EXISTS idx_labels_next_ts
            ON btc_labels_15m(next_timestamp);
        CREATE INDEX IF NOT EXISTS idx_predictions_run_split_ts
            ON model_predictions(run_id, split_name, timestamp);
        CREATE INDEX IF NOT EXISTS idx_backtests_strategy_created
            ON strategy_backtests(strategy_name, created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_backtest_points_backtest_ts
            ON strategy_backtest_points(backtest_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_mc_results_run_sim
            ON monte_carlo_results(mc_run_id, simulation_index);
        CREATE INDEX IF NOT EXISTS idx_paper_model_predictions_status
            ON paper_model_predictions(status, target_timestamp);

        CREATE TABLE IF NOT EXISTS arb_edge_log (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            ts                   DATETIME NOT NULL,
            btc_spot             REAL,
            btc_spot_age_seconds REAL,
            kalshi_yes_ask       REAL,
            kalshi_strike        REAL,
            t_remaining_seconds  REAL,
            sigma                REAL,
            fair_value           REAL,
            raw_edge             REAL,
            net_edge             REAL,
            kalshi_fee           REAL,
            tradeable            INTEGER
        );

        CREATE INDEX IF NOT EXISTS idx_arb_edge_log_ts
            ON arb_edge_log(ts DESC);

        CREATE TABLE IF NOT EXISTS kalshi_market_snapshots (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            snapped_at         TEXT NOT NULL,
            ticker             TEXT,
            close_time         TEXT,
            strike             REAL,
            yes_bid_dollars    REAL,
            yes_ask_dollars    REAL,
            no_bid_dollars     REAL,
            no_ask_dollars     REAL,
            last_price_dollars REAL,
            volume_24h_fp      REAL
        );

        CREATE TABLE IF NOT EXISTS latency_arb_paper_trades (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            opened_at           DATETIME,
            closed_at           DATETIME,
            side                TEXT,
            entry_price         REAL,
            close_price         REAL,
            fair_value_at_entry REAL,
            net_edge_at_entry   REAL,
            contracts           REAL,
            dollar_size         REAL,
            pnl                 REAL,
            status              TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_kalshi_snapshots_snapped_at
            ON kalshi_market_snapshots(snapped_at DESC);
        CREATE INDEX IF NOT EXISTS idx_latency_arb_trades_status
            ON latency_arb_paper_trades(status, opened_at DESC);
        """
    )
    conn.commit()


def init_db(db_path: str = DB_PATH) -> None:
    conn = get_conn(db_path)
    try:
        ensure_research_schema(conn)
    finally:
        conn.close()
