# quant-os

A live quantitative trading research system for cross-exchange arbitrage on Kalshi and Polymarket BTC binary contracts.

---

## Result

658 paper trades opened across 17 days of live data. 88.02% capture rate against detected opportunities. Average locked edge at entry: $98.81 per trade pair. Average realized PnL on 70 resolved trades: $94.08. Zero max drawdown by construction — the hedge eliminates all directional exposure.

Full methodology, fee model, and statistical validation in [docs/paper.pdf](docs/paper.pdf).

---

## What it does

- **Collects** live orderbook quotes from Kalshi (`KXBTC15M`) and Polymarket (`btc-updown-15m`) every 60 seconds via REST, plus real-time BTC/USD spot via Coinbase websocket.
- **Prices** Kalshi binary YES contracts using a closed-form Black-Scholes approximation with realized volatility from 15-minute OHLCV, producing a fair-value estimate and net edge after fees.
- **Executes** a market-neutral hedged arbitrage: buy YES on whichever venue is cheap, buy NO on the other, locking in `1.00 − (p_yes + p_no) − fees` regardless of BTC direction. Execution is paper-only; order stubs are documented in `agents/strategies/hedged_cross_arb.py`.
- **Overlays ML**: a Random Forest trained on one year of BTC OHLCV features (52.6% test accuracy, AUC 0.535) provides a directional probability signal that can filter or size arb entries.
- **Visualizes** everything in a three-tab Flask dashboard (Live / Arb / Backtest) with Plotly charts and a live orderbook view.

---

## Architecture

```
Coinbase WS ──► btc_feed.py ──────────────────────────────────────────────┐
                                                                           ▼
Kalshi REST ──► collectors/collector.py ──► data/btc15m.db ◄── fair_value.py
                                                   │
Polymarket ──► collectors/polymarket_collector.py ─┘
    REST
                                                   │
                        ┌──────────────────────────┘
                        ▼
              strategies/hedged_cross_arb.py
                        │
                        ├──► hedged_arb_trades (paper positions)
                        ├──► arb_edge_log (every signal evaluation)
                        └──► dashboard/app.py → http://localhost:5050
```

See [docs/architecture.md](docs/architecture.md) for the full data-flow diagram and tick-matching logic.

---

## Quickstart

```bash
git clone https://github.com/ssiddiq1/quant-os.git
cd quant-os
pip install -r requirements.txt
cp .env.example .env          # add KALSHI_API_KEY if you have one; system runs unauthenticated without it
bash run_all.sh
```

Open [http://localhost:5050](http://localhost:5050).

To stop all processes:

```bash
kill $(lsof -ti:5050) && pkill -f 'quant-os'
```

---

## Reproducing the paper's numbers

The joint-tick history in `data/btc15m.db` cannot be regenerated from public data — it must be re-collected forward. To start from scratch:

```bash
bash scripts/rebuild_db.sh          # initializes schema + backfills 1 year of BTC OHLCV
bash run_all.sh                     # run for ≥ 24h to accumulate live ticks
```

Once you have joint tick data, reproduce the primary backtest result (strategy_backtests row id=3):

```bash
python3 agents/backtesting/hedged_arb_backtest.py \
    --min-edge 0.01 \
    --dollar-size 500 \
    --min-seconds-to-close 90
```

To rebuild the ML models:

```bash
bash scripts/rebuild_models.sh
```

The exact SQL queries that produced every table in the paper are in [docs/results.md](docs/results.md).

---

## Status

Paper-trading only. The execution layer — Kalshi REST order placement and Polymarket CLOB order submission — is intentionally stubbed. `execute_kalshi_order()` and `execute_polymarket_order()` in `agents/strategies/hedged_cross_arb.py` return simulated fills. See docs/paper.pdf §5 for the reasoning.

---

## Tech stack

Python 3.11 · SQLite (WAL mode) · Flask · scikit-learn · Plotly · websocket-client · NumPy · pandas

---

## License

MIT — see [LICENSE](LICENSE).

**Shayaan Siddique** · [GitHub](https://github.com/ssiddiq1)
