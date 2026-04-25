# data/

`btc15m.db` is gitignored. It is a SQLite database (WAL mode) containing all live-collected tick data, ML features/labels, backtest results, and paper trading records.

## Rebuilding from scratch

```bash
bash scripts/rebuild_db.sh      # creates schema + backfills 1 year of BTC OHLCV
bash run_all.sh                 # run for ≥24h to accumulate Kalshi/Polymarket ticks
bash scripts/rebuild_models.sh  # build ML models once tick data is available
```

## Schema

All 21 tables are defined in `research_db.py` (repo root). The `init_db()` function there creates the full schema idempotently.

Key tables:

| Table | Contents |
|-------|----------|
| `markets` | Kalshi KXBTC15M tick data (bid/ask/mid per 60s) |
| `polymarket_markets` | Polymarket btc-updown-15m tick data |
| `btc_ohlcv_15m` | BTC/USD 15-minute OHLCV from Coinbase |
| `hedged_arb_trades` | Paper hedged arb positions |
| `arb_edge_log` | Every arb signal evaluation (live) |
| `model_runs` | ML training metadata and metrics |
| `strategy_backtests` | Backtest results per strategy run |

## Note on reproducibility

The BTC OHLCV history is fully reproducible from the Coinbase public REST API. The joint Kalshi/Polymarket tick history used in the hedged arb backtest (9,127 Kalshi rows, 5,398 Polymarket rows, Apr 8 – Apr 25 2026) was collected in real time and cannot be regenerated retroactively from public sources. Re-running `run_all.sh` will rebuild an equivalent dataset going forward.
