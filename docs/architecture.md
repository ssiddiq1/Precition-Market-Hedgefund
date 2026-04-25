# System Architecture

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  External Sources                                                   │
│                                                                     │
│  Coinbase Advanced Trade WS  ──►  agents/collectors/btc_feed.py    │
│  Kalshi REST  (KXBTC15M)     ──►  agents/collectors/collector.py   │
│  Polymarket REST (CLOB)      ──►  agents/collectors/               │
│                                   polymarket_collector.py          │
│  Coinbase REST  (historical) ──►  agents/collectors/               │
│                                   historical_btc_ingest.py         │
└─────────────────────────────────────────────────────────────────────┘
                       │ write every 60s (REST)
                       │ write on price move (WS)
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  data/btc15m.db  (SQLite, WAL mode)                                 │
│                                                                     │
│  markets               — Kalshi tick data       (9,127 rows)       │
│  polymarket_markets    — Polymarket tick data   (5,398 rows)       │
│  btc_ohlcv_15m         — BTC OHLCV 15m bars    (35,030 rows)      │
│  btc_features_15m      — ML feature store                          │
│  btc_labels_15m        — direction labels                          │
│  model_runs            — training metadata      (4 runs)           │
│  model_predictions     — per-row predictions                       │
│  paper_model_predictions — live forward predictions                │
│  strategy_backtests    — backtest results                          │
│  strategy_backtest_points/trades — equity curves                   │
│  monte_carlo_runs/results — MC simulation output                   │
│  hedged_arb_trades     — paper arb positions    (21 open)         │
│  arb_edge_log          — every edge evaluation  (3,637 rows)      │
│  latency_arb_paper_trades — latency arb paper trades              │
│  paper_accounts/trades — directional paper trading                │
│  kalshi_market_snapshots — raw Kalshi snapshots                   │
└─────────────────────────────────────────────────────────────────────┘
          │                              │
          ▼                              ▼
┌──────────────────┐          ┌──────────────────────────────────────┐
│  Pricing layer   │          │  Signal / strategy layer              │
│                  │          │                                       │
│  fair_value.py   │──────►   │  strategies/hedged_cross_arb.py      │
│  · Black-Scholes │  edge    │  · evaluate_arb() on every tick      │
│    binary approx │  calcs   │  · buy YES (cheap venue) +           │
│  · realized vol  │          │    buy NO (expensive venue)          │
│    from OHLCV    │          │  · fees deducted per Kalshi schedule │
└──────────────────┘          │                                       │
                              │  strategies/latency_arb.py           │
                              │  · every 5s snapshot vs fair value   │
                              │  · enter when net_edge > 0.035       │
                              └──────────────────────────────────────┘
                                            │
                                            ▼
                              ┌──────────────────────────────────────┐
                              │  dashboard/app.py  → :5050           │
                              │  Live tab   — orderbook + open arbs  │
                              │  Arb tab    — edge distribution,     │
                              │               persistence, daily PnL │
                              │  Backtest tab — strategy comparator  │
                              └──────────────────────────────────────┘
```

## Tick-matching join

The hedged arb signal requires simultaneous quotes from both venues for the same contract expiry. Kalshi and Polymarket timestamps are not synchronized — the two collectors poll independently at 60-second intervals with arbitrary phase offsets. The join key is `close_time` (the contract's 15-minute window boundary), matched at minute precision:

```sql
SELECT k.*, p.*
FROM markets k
JOIN polymarket_markets p
  ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
   = strftime('%Y-%m-%dT%H:%M', p.collected_at)
WHERE k.close_time = p.close_time
```

This produces at most one matched row per minute per window, so the maximum quote staleness for either leg is 60 seconds. The backtest applies a 90-second TTL guard (`MIN_SECONDS_TO_CLOSE`) to exclude entries where the contract has less than 90 seconds until resolution — too little time for fills to clear. See paper §2 for the full matching derivation.

## Hedge construction

Both venues write binary contracts on the same underlying event: "BTC closes higher in this 15-minute window." By construction, `YES_payout + NO_payout = $1.00` at resolution on each venue independently.

Two valid hedge directions exist:

| Direction | Leg A | Leg B | Profitable when |
|-----------|-------|-------|-----------------|
| A | Buy Kalshi YES at `p_k` | Buy Polymarket DOWN at `p_d` | `p_k + p_d + fees < 1.00` |
| B | Buy Polymarket UP at `p_u` | Buy Kalshi NO at `p_n` | `p_u + p_n + fees < 1.00` |

In both cases, one leg pays out $1.00 at resolution regardless of BTC's direction; the other pays $0.00. The locked edge is `1.00 − (p_A + p_B) − fees` per contract pair, with zero variance. See paper §2 for the full fee schedule and §3 for the backtest implementation.
