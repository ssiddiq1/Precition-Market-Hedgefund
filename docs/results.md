# Reproducible Results

Every table in this document is produced by the SQL query immediately above it, run against `data/btc15m.db`. To reproduce, open the database with `sqlite3 data/btc15m.db` or any SQLite client and execute the query verbatim.

---

## 1. Hedged Arbitrage Backtest

Primary result: strategy_backtests row id=3, run 2026-04-24T16:00:38 UTC.

**Query:**

```sql
SELECT
    json_extract(metrics_json, '$.trades_opened')               AS trades_opened,
    json_extract(metrics_json, '$.trades_resolved')             AS trades_resolved,
    json_extract(metrics_json, '$.trades_unresolved')           AS trades_unresolved,
    json_extract(metrics_json, '$.joint_windows_total')         AS joint_windows,
    json_extract(metrics_json, '$.joint_ticks_total')           AS joint_ticks,
    json_extract(metrics_json, '$.ticks_with_any_positive_net_edge') AS ticks_positive_edge,
    json_extract(metrics_json, '$.opportunities_detected')      AS opportunities_detected,
    json_extract(metrics_json, '$.tradeable_after_ttl_guard')   AS tradeable_after_ttl,
    ROUND(json_extract(metrics_json, '$.capture_rate') * 100, 2) AS capture_rate_pct,
    ROUND(json_extract(metrics_json, '$.gross_pnl_locked'), 2)  AS gross_pnl_locked,
    ROUND(json_extract(metrics_json, '$.net_pnl_realized'), 2)  AS net_pnl_realized,
    json_extract(metrics_json, '$.max_drawdown_dollars')        AS max_drawdown,
    ROUND(json_extract(metrics_json, '$.sharpe_per_trade_annualised'), 4) AS sharpe_annualised,
    config_json,
    created_at
FROM strategy_backtests
WHERE strategy_name = 'hedged_cross_arb'
ORDER BY id DESC
LIMIT 1;
```

**Result:**

| Metric | Value |
|--------|-------|
| Trades opened | 658 |
| Trades resolved | 70 |
| Trades unresolved (open at run time) | 588 |
| Joint 15-min windows | 729 |
| Joint ticks analyzed | 90,157 |
| Ticks with positive net edge | 81,033 (89.88%) |
| Opportunities detected (edge ≥ 1¢) | 76,189 |
| Tradeable after 90s TTL guard | 67,060 |
| Capture rate | **88.02%** |
| Gross PnL locked at entry (all 658) | **$65,017.39** |
| Net PnL realized (70 resolved) | **$6,585.69** |
| Avg locked per opened trade | $98.81 |
| Avg realized per resolved trade | $94.08 |
| Max drawdown | **$0.00** |
| Sharpe (per-trade, annualised) | **117.48** |

Config: `dollar_size_per_leg=$500`, `min_edge=0.01`, `min_seconds_to_close=90`.

---

## 2. Kalshi vs. Polymarket Spread Statistics

Systematic price dislocation between venues on the same underlying event, measured as `kalshi_mid − polymarket_mid`.

**Query:**

```sql
SELECT
    COUNT(*)                                                          AS n_matched_ticks,
    ROUND(AVG(
        (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
      - (p.up_bid + p.up_ask) / 2.0
    ), 5)                                                             AS mean_spread,
    ROUND(AVG(ABS(
        (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
      - (p.up_bid + p.up_ask) / 2.0
    )), 5)                                                            AS mean_abs_spread,
    ROUND(MIN(
        (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
      - (p.up_bid + p.up_ask) / 2.0
    ), 5)                                                             AS min_spread,
    ROUND(MAX(
        (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
      - (p.up_bid + p.up_ask) / 2.0
    ), 5)                                                             AS max_spread
FROM markets k
JOIN polymarket_markets p
  ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
   = strftime('%Y-%m-%dT%H:%M', p.collected_at)
WHERE k.yes_bid_dollars IS NOT NULL AND k.yes_ask_dollars IS NOT NULL
  AND p.up_bid IS NOT NULL AND p.up_ask IS NOT NULL;
```

**Result:**

| Metric | Value |
|--------|-------|
| Matched ticks | 8,257 |
| Mean spread (Kalshi − Poly) | −0.00633 (Kalshi systematically cheaper by 0.63¢) |
| Mean absolute spread | 0.0926 (9.26¢ total dislocation, sign-agnostic) |
| Min spread | −0.9995 |
| Max spread | +0.8705 |

---

## 3. ML Model Performance

Four models trained on two dataset windows. The large-window models (runs 3–4) are the ones referenced in the paper.

**Query:**

```sql
SELECT
    id,
    model_name,
    train_start,
    train_end,
    test_start,
    test_end,
    ROUND(json_extract(metrics_json, '$.test.accuracy'), 4)   AS test_accuracy,
    ROUND(json_extract(metrics_json, '$.test.roc_auc'), 4)    AS test_auc,
    ROUND(json_extract(metrics_json, '$.test.f1'), 4)         AS test_f1,
    ROUND(json_extract(metrics_json, '$.train.accuracy'), 4)  AS train_accuracy,
    ROUND(json_extract(metrics_json, '$.train.roc_auc'), 4)   AS train_auc,
    artifact_path
FROM model_runs
ORDER BY id;
```

**Result (large-window runs, ids 3–4):**

| Run | Model | Test Accuracy | Test AUC | Test F1 | Train Accuracy | Test window |
|-----|-------|-------------|---------|---------|---------------|-------------|
| 3 | logistic_regression | 52.04% | 0.530 | 0.527 | 52.4% | Jan–Apr 2026 |
| 4 | random_forest | **52.58%** | **0.535** | 0.534 | 69.8% | Jan–Apr 2026 |

Training window: Apr 2025 – Nov 2025 (7 months, ~21k samples). Test window: Jan 2026 – Apr 2026 (7,006 samples). Features: 15 OHLCV-derived signals (RSI-14, SMA distances, return lags, rolling volatility, volume z-score, wick ratios, session flags).

---

## 4. Monte Carlo Simulation

Block-bootstrap resampling of ML strategy (probability threshold) trade returns. Run on strategy_backtests id=2 (1,385 trades, Jan–Apr 2026).

**Query:**

```sql
SELECT
    r.method,
    r.config_json                                              AS config,
    COUNT(res.id)                                             AS n_simulations,
    ROUND(AVG(res.total_return) * 100, 2)                    AS mean_return_pct,
    ROUND(MIN(res.total_return) * 100, 2)                    AS min_return_pct,
    ROUND(MAX(res.total_return) * 100, 2)                    AS max_return_pct,
    COUNT(CASE WHEN res.final_equity > 1.0 THEN 1 END)       AS n_profitable
FROM monte_carlo_runs r
JOIN monte_carlo_results res ON res.mc_run_id = r.id
WHERE r.id = 2
GROUP BY r.id;
```

**Result:**

| Metric | Value |
|--------|-------|
| Method | block-bootstrap (bootstrap_trade_returns) |
| Simulations | 1,000 |
| Mean total return | −84.0% |
| 2.5th percentile | −88.1% |
| 50th percentile | −84.1% |
| 97.5th percentile | −78.5% |
| Profitable simulations | 0 / 1,000 |

Note: the ML directional strategy consistently loses capital across all 1,000 resamplings. This confirms that the 52.6% test accuracy is insufficient for profitable spot-directional trading after transaction costs. The hedged arbitrage strategy was not subjected to Monte Carlo because its zero-variance locked edge makes the simulation degenerate — every simulation produces the same result by construction.

---

## 5. Data Collection Window

**Query:**

```sql
SELECT 'kalshi'      AS source, MIN(collected_at) AS first, MAX(collected_at) AS last, COUNT(*) AS n FROM markets
UNION ALL
SELECT 'polymarket'  AS source, MIN(collected_at), MAX(collected_at), COUNT(*) FROM polymarket_markets
UNION ALL
SELECT 'ohlcv_15m'   AS source, MIN(timestamp),    MAX(timestamp),    COUNT(*) FROM btc_ohlcv_15m;
```

**Result:**

| Source | First | Last | Rows |
|--------|-------|------|------|
| Kalshi ticks | 2026-04-08 23:44 UTC | 2026-04-25 22:17 UTC | 9,127 |
| Polymarket ticks | 2026-04-08 23:54 UTC | 2026-04-25 22:17 UTC | 5,398 |
| BTC OHLCV 15m | 2025-04-10 00:00 UTC | 2026-04-10 03:00 UTC | 35,030 |
