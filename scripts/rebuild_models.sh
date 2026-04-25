#!/usr/bin/env bash
# rebuild_models.sh — rebuild all ML artifacts from the data in btc15m.db.
#
# Runs the full research pipeline:
#   1. Build feature and label datasets from btc_ohlcv_15m.
#   2. Train logistic regression and random forest models.
#   3. Run walk-forward backtest on the trained models.
#   4. Run Monte Carlo block-bootstrap on backtest returns.
#   5. Generate live forward predictions on the latest features.
#
# Outputs saved to:
#   artifacts/models/  — .pkl model files (gitignored; tracked by model_runs table)
#   data/btc15m.db     — model_runs, model_predictions, strategy_backtests,
#                        monte_carlo_results, paper_model_predictions tables
#
# Requirements:
#   btc15m.db must exist with at least btc_ohlcv_15m populated.
#   Run scripts/rebuild_db.sh first if starting from scratch.
#
# Usage:
#   bash scripts/rebuild_models.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "[rebuild_models] Root: $ROOT"
echo "[rebuild_models] Running end-to-end research workflow..."

python3 "$ROOT/agents/orchestration/research_workflow.py" \
    --db-path "$ROOT/data/btc15m.db"

echo ""
echo "[rebuild_models] Done. Artifacts written to artifacts/models/"
echo "  Run 'python3 agents/ml/calibration.py' to evaluate model calibration."
