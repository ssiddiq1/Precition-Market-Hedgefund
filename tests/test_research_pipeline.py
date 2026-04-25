from datetime import timedelta

import numpy as np
import pandas as pd

from agents.ml.dataset_builder import compute_features, compute_labels
from agents.backtesting.monte_carlo import bootstrap_trade_returns
from agents.backtesting.research_backtester import run_backtest
from agents.strategies.strategy_runner import generate_signals


def sample_ohlcv(n: int = 40) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=n, freq="15min", tz="UTC")
    close = pd.Series(np.linspace(100, 120, n))
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": close - 0.4,
            "high": close + 0.8,
            "low": close - 0.9,
            "close": close,
            "volume": np.linspace(1_000, 2_000, n),
            "source": "test",
        }
    )


def test_label_generation_uses_next_bar():
    df = sample_ohlcv(5)
    labels = compute_labels(df, threshold_bps=5.0)
    assert labels.loc[0, "direction_up"] == 1.0
    assert labels.loc[0, "close_t1"] == df.loc[1, "close"]
    assert np.isnan(labels.loc[len(labels) - 1, "direction_up"])


def test_feature_generation_has_no_forward_dependency_on_next_close():
    df = sample_ohlcv(40)
    base = compute_features(df)
    changed = df.copy()
    changed.loc[39, "close"] = changed.loc[39, "close"] * 1.5
    changed_features = compute_features(changed)
    row_to_check = 30
    assert base.loc[row_to_check, "return_1"] == changed_features.loc[row_to_check, "return_1"]
    assert base.loc[row_to_check, "momentum_8"] == changed_features.loc[row_to_check, "momentum_8"]


def test_backtest_uses_same_row_signal_with_that_row_forward_return():
    pred_df = pd.DataFrame(
        [
            {"timestamp": "2026-01-01T00:00:00+00:00", "y_true": 1, "y_pred": 1, "prob_up": 0.9, "forward_return": 0.01},
            {"timestamp": "2026-01-01T00:15:00+00:00", "y_true": 0, "y_pred": 0, "prob_up": 0.1, "forward_return": -0.02},
        ]
    )
    points, trades, metrics = run_backtest(
        pred_df,
        strategy_name="test",
        strategy_mode="probability_threshold",
        threshold=0.55,
        transaction_cost=0.0,
        slippage=0.0,
    )
    assert round(points.loc[0, "strategy_return"], 4) == 0.01
    assert round(points.loc[1, "strategy_return"], 4) == 0.02
    assert metrics["number_of_trades"] == 2


def test_monte_carlo_is_seed_deterministic():
    returns = np.array([0.01, -0.02, 0.015, 0.005, -0.01])
    first = bootstrap_trade_returns(returns, n_simulations=25, seed=7)
    second = bootstrap_trade_returns(returns, n_simulations=25, seed=7)
    assert first.equals(second)


def test_forward_signal_band_logic():
    pred_df = pd.DataFrame(
        [
            {"timestamp": "2026-01-01T00:00:00+00:00", "y_true": 1, "y_pred": 1, "prob_up": 0.62, "forward_return": 0.01},
            {"timestamp": "2026-01-01T00:15:00+00:00", "y_true": 0, "y_pred": 0, "prob_up": 0.49, "forward_return": -0.01},
        ]
    )
    signals = generate_signals(pred_df, mode="banded", no_trade_band=0.03)
    assert signals.loc[0, "position"] == 1.0
    assert signals.loc[1, "position"] == 0.0
