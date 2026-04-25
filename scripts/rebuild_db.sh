#!/usr/bin/env bash
# rebuild_db.sh — initialize a fresh btc15m.db and backfill one year of BTC OHLCV.
#
# What this script does:
#   1. Creates an empty btc15m.db with the full 21-table schema.
#   2. Backfills one year of BTC/USD 15-minute OHLCV candles from the Coinbase
#      Advanced Trade REST API (public endpoint, no auth required).
#
# What this script CANNOT do:
#   The joint Kalshi/Polymarket tick history that drives the hedged arb backtest
#   is collected in real time by the two collector agents. It cannot be downloaded
#   from any public source. To rebuild it, run `bash run_all.sh` and let the
#   collectors run for at least 24 hours (longer is better — the backtest results
#   in docs/results.md were produced after 17 days of continuous collection).
#
# Usage:
#   bash scripts/rebuild_db.sh
#   bash run_all.sh              # then leave running for ≥24h

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DB="$ROOT/data/btc15m.db"

echo "[rebuild_db] Working directory: $ROOT"

# 1. Create data directory if missing
mkdir -p "$ROOT/data"

# 2. Initialize schema
echo "[rebuild_db] Initializing schema..."
python3 - <<EOF
import sys
sys.path.insert(0, "$ROOT")
from research_db import init_db
init_db("$DB")
print("[rebuild_db] Schema created: $DB")
EOF

# 3. Backfill 1 year of OHLCV
echo "[rebuild_db] Backfilling BTC OHLCV (1 year via Coinbase REST) ..."
python3 "$ROOT/agents/collectors/historical_btc_ingest.py" \
    --db-path "$DB" \
    --days 365

echo ""
echo "[rebuild_db] Done. Next steps:"
echo "  1. Copy your .env.example to .env and add KALSHI_API_KEY (optional)."
echo "  2. Run:  bash run_all.sh"
echo "  3. Let the collectors run for at least 24 hours to accumulate live ticks."
echo "  4. Then run:  python3 agents/backtesting/hedged_arb_backtest.py --min-edge 0.01 --dollar-size 500 --min-seconds-to-close 90"
