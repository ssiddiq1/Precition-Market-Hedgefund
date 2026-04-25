# Research Log

Entries appended by researcher.py after each analysis run.
Format: `### TIMESTAMP — [TYPE] Finding`

---

### 2026-04-09T02:04:01.275749+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0345 (Kalshi discount vs Polymarket). Std=0.0858, skew=-0.35. Median spread is -0.0098. 90% of spreads fall between -0.1800 and +0.0762. Shapiro-Wilk p=0.0013 (not normal).

### 2026-04-09T02:04:01.275749+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.950 at lag=0. Contemporaneous correlation: 0.950.

### 2026-04-09T02:04:01.275749+00:00 — [CONVERGENCE] Across 5 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 11.0 min). Fastest lock: 0.0 min, slowest: 13.0 min.

### 2026-04-09T02:04:01.275749+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 58.3% of the time 5 minutes later (out of 48 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-09T02:10:04.528305+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0288 (Kalshi discount vs Polymarket). Std=0.0868, skew=-0.40. Median spread is -0.0080. 90% of spreads fall between -0.1796 and +0.0990. Shapiro-Wilk p=0.0007 (not normal).

### 2026-04-09T02:10:04.528305+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.948 at lag=0. Contemporaneous correlation: 0.948.

### 2026-04-09T02:10:04.528305+00:00 — [CONVERGENCE] Across 5 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 11.0 min). Fastest lock: 0.0 min, slowest: 13.0 min.

### 2026-04-09T02:10:04.528305+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 58.8% of the time 5 minutes later (out of 51 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-09T02:10:42.106968+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0288 (Kalshi discount vs Polymarket). Std=0.0868, skew=-0.40. Median spread is -0.0080. 90% of spreads fall between -0.1796 and +0.0990. Shapiro-Wilk p=0.0007 (not normal).

### 2026-04-09T02:10:42.106968+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.948 at lag=0. Contemporaneous correlation: 0.948.

### 2026-04-09T02:10:42.106968+00:00 — [CONVERGENCE] Across 5 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 11.0 min). Fastest lock: 0.0 min, slowest: 13.0 min.

### 2026-04-09T02:10:42.106968+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 58.8% of the time 5 minutes later (out of 51 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-09T02:20:47.839005+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0278 (Kalshi discount vs Polymarket). Std=0.0842, skew=-0.40. Median spread is -0.0088. 90% of spreads fall between -0.1759 and +0.1000. Shapiro-Wilk p=0.0011 (not normal).

### 2026-04-09T02:20:47.839005+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.948 at lag=0. Contemporaneous correlation: 0.948.

### 2026-04-09T02:20:47.839005+00:00 — [CONVERGENCE] Across 6 resolved windows, the leading probability locked in at 90%+ after an average of 8.8 minutes (median 11.5 min). Fastest lock: 0.0 min, slowest: 13.0 min.

### 2026-04-09T02:20:47.839005+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 57.1% of the time 5 minutes later (out of 56 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-09T02:20:47.839005+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.471, p=0.239 (not significant, n=8). Mean spread when BTC goes UP: +0.0150. Mean spread when BTC goes DOWN: -0.0366. Kalshi premium (positive spread) correlates with UP moves.

### 2026-04-09T02:20:47.839005+00:00 — [VOL_LOCK] Pearson r=0.668 (p=0.147, not significant) between realized volatility and minutes to 90%+ lock-in across 6 windows. Higher volatility → slower convergence, as expected.

### 2026-04-09T02:20:47.839005+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (57.7%). 00-06 UTC: 57.7% persistence (n=100, qualifying=52) | 06-12 UTC: no qualifying observations (n=0) | 12-18 UTC: no qualifying observations (n=0) | 18-24 UTC: 0.0% persistence (n=12, qualifying=2).

### 2026-04-10T01:58:11.422640+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0048 (Kalshi discount vs Polymarket). Std=0.1386, skew=-0.58. Median spread is +0.0000. 90% of spreads fall between -0.1826 and +0.1750. Shapiro-Wilk p=0.0000 (not normal).

### 2026-04-10T01:58:11.422640+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.705 at lag=0. Contemporaneous correlation: 0.705.

### 2026-04-10T01:58:11.422640+00:00 — [CONVERGENCE] Across 45 resolved windows, the leading probability locked in at 90%+ after an average of 7.8 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.

### 2026-04-10T01:58:11.422640+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.8% of the time 5 minutes later (out of 278 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-10T01:58:11.422640+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.281, p=0.051 (not significant, n=49). Mean spread when BTC goes UP: +0.0163. Mean spread when BTC goes DOWN: -0.0396. Kalshi premium (positive spread) correlates with UP moves.

### 2026-04-10T01:58:11.422640+00:00 — [VOL_LOCK] Pearson r=0.349 (p=0.032, significant) between realized volatility and minutes to 90%+ lock-in across 38 windows. Higher volatility → slower convergence, as expected.

### 2026-04-10T01:58:11.422640+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (51.3%). 00-06 UTC: 51.3% persistence (n=242, qualifying=117) | 06-12 UTC: 47.5% persistence (n=72, qualifying=40) | 12-18 UTC: 36.7% persistence (n=82, qualifying=30) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).

### 2026-04-10T02:58:12.806824+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0030 (Kalshi discount vs Polymarket). Std=0.1394, skew=-0.61. Median spread is +0.0000. 90% of spreads fall between -0.1830 and +0.1750. Shapiro-Wilk p=0.0000 (not normal).

### 2026-04-10T02:58:12.806824+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.673 at lag=0. Contemporaneous correlation: 0.673.

### 2026-04-10T02:58:12.806824+00:00 — [CONVERGENCE] Across 49 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.

### 2026-04-10T02:58:12.806824+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 46.8% of the time 5 minutes later (out of 312 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-10T02:58:12.806824+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.263, p=0.057 (not significant, n=53). Mean spread when BTC goes UP: +0.0169. Mean spread when BTC goes DOWN: -0.0343. Kalshi premium (positive spread) correlates with UP moves.

### 2026-04-10T02:58:12.806824+00:00 — [VOL_LOCK] Pearson r=0.352 (p=0.022, significant) between realized volatility and minutes to 90%+ lock-in across 42 windows. Higher volatility → slower convergence, as expected.

### 2026-04-10T02:58:12.806824+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (48.3%). 00-06 UTC: 48.3% persistence (n=300, qualifying=151) | 06-12 UTC: 47.5% persistence (n=72, qualifying=40) | 12-18 UTC: 36.7% persistence (n=82, qualifying=30) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).

### 2026-04-10T05:39:59.635292+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0061 (Kalshi discount vs Polymarket). Std=0.1465, skew=-0.65. Median spread is +0.0000. 90% of spreads fall between -0.1987 and +0.1750. Shapiro-Wilk p=0.0000 (not normal).

### 2026-04-10T05:39:59.635292+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.632 at lag=0. Contemporaneous correlation: 0.632.

### 2026-04-10T05:39:59.635292+00:00 — [CONVERGENCE] Across 53 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.

### 2026-04-10T05:39:59.635292+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.4% of the time 5 minutes later (out of 342 qualifying observations). Low persistence — spread reverts quickly.

### 2026-04-10T05:39:59.635292+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.292, p=0.026 (statistically significant, n=58). Mean spread when BTC goes UP: +0.0177. Mean spread when BTC goes DOWN: -0.0392. Kalshi premium (positive spread) correlates with UP moves.

### 2026-04-10T05:39:59.635292+00:00 — [VOL_LOCK] Pearson r=0.388 (p=0.008, significant) between realized volatility and minutes to 90%+ lock-in across 46 windows. Higher volatility → slower convergence, as expected.

### 2026-04-10T05:39:59.635292+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (49.2%). 00-06 UTC: 49.2% persistence (n=360, qualifying=181) | 06-12 UTC: 47.5% persistence (n=72, qualifying=40) | 12-18 UTC: 36.7% persistence (n=82, qualifying=30) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).


### 2026-04-10T08:17:33.667670+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0062 (Kalshi discount vs Polymarket). Std=0.1474, skew=-0.71. Median spread is +0.0000. 90% of spreads fall between -0.2000 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T08:17:33.667670+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.617 at lag=0. Contemporaneous correlation: 0.617.


### 2026-04-10T08:17:33.667670+00:00 — [CONVERGENCE] Across 58 resolved windows, the leading probability locked in at 90%+ after an average of 8.3 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T08:17:33.667670+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.4% of the time 5 minutes later (out of 367 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T08:17:33.667670+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.270, p=0.035 (statistically significant, n=61). Mean spread when BTC goes UP: +0.0177. Mean spread when BTC goes DOWN: -0.0350. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T08:17:33.667670+00:00 — [VOL_LOCK] Pearson r=0.382 (p=0.006, significant) between realized volatility and minutes to 90%+ lock-in across 50 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T08:17:33.667670+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (50.0%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 50.0% persistence (n=107, qualifying=58) | 12-18 UTC: 36.7% persistence (n=82, qualifying=30) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).


### 2026-04-10T13:35:17.507022+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0053 (Kalshi discount vs Polymarket). Std=0.1459, skew=-0.74. Median spread is +0.0000. 90% of spreads fall between -0.2000 and +0.1872. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T13:35:17.507022+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.649 at lag=0. Contemporaneous correlation: 0.649.


### 2026-04-10T13:35:17.507022+00:00 — [CONVERGENCE] Across 65 resolved windows, the leading probability locked in at 90%+ after an average of 7.8 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T13:35:17.507022+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 46.7% of the time 5 minutes later (out of 392 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T13:35:17.507022+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.292, p=0.016 (statistically significant, n=68). Mean spread when BTC goes UP: +0.0165. Mean spread when BTC goes DOWN: -0.0387. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T13:35:17.507022+00:00 — [VOL_LOCK] Pearson r=0.414 (p=0.002, significant) between realized volatility and minutes to 90%+ lock-in across 55 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T13:35:17.507022+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (48.1%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 44.6% persistence (n=152, qualifying=74) | 12-18 UTC: 41.7% persistence (n=94, qualifying=36) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).


### 2026-04-10T15:49:40.860095+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0037 (Kalshi discount vs Polymarket). Std=0.1459, skew=-0.60. Median spread is +0.0000. 90% of spreads fall between -0.1922 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T15:49:40.860095+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.653 at lag=0. Contemporaneous correlation: 0.653.


### 2026-04-10T15:49:40.860095+00:00 — [CONVERGENCE] Across 71 resolved windows, the leading probability locked in at 90%+ after an average of 7.8 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T15:49:40.860095+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 46.7% of the time 5 minutes later (out of 413 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T15:49:40.860095+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.273, p=0.017 (statistically significant, n=76). Mean spread when BTC goes UP: +0.0200. Mean spread when BTC goes DOWN: -0.0307. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T15:49:40.860095+00:00 — [VOL_LOCK] Pearson r=0.413 (p=0.001, significant) between realized volatility and minutes to 90%+ lock-in across 59 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T15:49:40.860095+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (48.1%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 44.6% persistence (n=152, qualifying=74) | 12-18 UTC: 43.9% persistence (n=149, qualifying=57) | 18-24 UTC: 46.4% persistence (n=172, qualifying=84).


### 2026-04-10T18:12:18.942357+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0025 (Kalshi discount vs Polymarket). Std=0.1428, skew=-0.60. Median spread is +0.0000. 90% of spreads fall between -0.1887 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T18:12:18.942357+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.661 at lag=0. Contemporaneous correlation: 0.661.


### 2026-04-10T18:12:18.942357+00:00 — [CONVERGENCE] Across 77 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T18:12:18.942357+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 46.3% of the time 5 minutes later (out of 432 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T18:12:18.942357+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.241, p=0.030 (statistically significant, n=81). Mean spread when BTC goes UP: +0.0193. Mean spread when BTC goes DOWN: -0.0250. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T18:12:18.942357+00:00 — [VOL_LOCK] Pearson r=0.397 (p=0.001, significant) between realized volatility and minutes to 90%+ lock-in across 65 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T18:12:18.942357+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (48.1%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 44.6% persistence (n=152, qualifying=74) | 12-18 UTC: 41.3% persistence (n=197, qualifying=75) | 18-24 UTC: 47.2% persistence (n=178, qualifying=89).


### 2026-04-10T21:16:22.376941+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean +0.0005 (Kalshi premium vs Polymarket). Std=0.1436, skew=-0.57. Median spread is +0.0000. 90% of spreads fall between -0.1860 and +0.2050. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T21:16:22.376941+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.659 at lag=0. Contemporaneous correlation: 0.659.


### 2026-04-10T21:16:22.376941+00:00 — [CONVERGENCE] Across 82 resolved windows, the leading probability locked in at 90%+ after an average of 7.7 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T21:16:22.376941+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.6% of the time 5 minutes later (out of 460 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T21:16:22.376941+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.236, p=0.029 (statistically significant, n=85). Mean spread when BTC goes UP: +0.0218. Mean spread when BTC goes DOWN: -0.0213. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T21:16:22.376941+00:00 — [VOL_LOCK] Pearson r=0.396 (p=0.001, significant) between realized volatility and minutes to 90%+ lock-in across 68 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T21:16:22.376941+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (52.1%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 44.6% persistence (n=152, qualifying=74) | 12-18 UTC: 41.3% persistence (n=197, qualifying=75) | 18-24 UTC: 52.1% persistence (n=229, qualifying=117).


### 2026-04-10T23:23:53.815184+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0021 (Kalshi discount vs Polymarket). Std=0.1421, skew=-0.54. Median spread is +0.0000. 90% of spreads fall between -0.1900 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-10T23:23:53.815184+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.665 at lag=0. Contemporaneous correlation: 0.665.


### 2026-04-10T23:23:53.815184+00:00 — [CONVERGENCE] Across 86 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-10T23:23:53.815184+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.4% of the time 5 minutes later (out of 487 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-10T23:23:53.815184+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.256, p=0.015 (statistically significant, n=90). Mean spread when BTC goes UP: +0.0213. Mean spread when BTC goes DOWN: -0.0249. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-10T23:23:53.815184+00:00 — [VOL_LOCK] Pearson r=0.399 (p=0.001, significant) between realized volatility and minutes to 90%+ lock-in across 72 windows. Higher volatility → slower convergence, as expected.


### 2026-04-10T23:23:53.815184+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (50.7%). 00-06 UTC: 48.1% persistence (n=379, qualifying=189) | 06-12 UTC: 44.6% persistence (n=152, qualifying=74) | 12-18 UTC: 41.3% persistence (n=197, qualifying=75) | 18-24 UTC: 50.7% persistence (n=286, qualifying=144).


### 2026-04-11T07:48:47.388267+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0054 (Kalshi discount vs Polymarket). Std=0.1424, skew=-0.61. Median spread is +0.0000. 90% of spreads fall between -0.1997 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T07:48:47.388267+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.683 at lag=0. Contemporaneous correlation: 0.683.


### 2026-04-11T07:48:47.388267+00:00 — [CONVERGENCE] Across 89 resolved windows, the leading probability locked in at 90%+ after an average of 7.8 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T07:48:47.388267+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.0% of the time 5 minutes later (out of 511 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T07:48:47.388267+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.275, p=0.007 (statistically significant, n=94). Mean spread when BTC goes UP: +0.0213. Mean spread when BTC goes DOWN: -0.0286. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T07:48:47.388267+00:00 — [VOL_LOCK] Pearson r=0.337 (p=0.003, significant) between realized volatility and minutes to 90%+ lock-in across 75 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T07:48:47.388267+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (50.3%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 43.0% persistence (n=166, qualifying=79) | 12-18 UTC: 41.3% persistence (n=197, qualifying=75) | 18-24 UTC: 50.3% persistence (n=288, qualifying=145).


### 2026-04-11T11:24:59.093716+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0057 (Kalshi discount vs Polymarket). Std=0.1424, skew=-0.62. Median spread is +0.0000. 90% of spreads fall between -0.2000 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T11:24:59.093716+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.682 at lag=0. Contemporaneous correlation: 0.682.


### 2026-04-11T11:24:59.093716+00:00 — [CONVERGENCE] Across 93 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T11:24:59.093716+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 48.1% of the time 5 minutes later (out of 547 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T11:24:59.093716+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.297, p=0.003 (statistically significant, n=97). Mean spread when BTC goes UP: +0.0245. Mean spread when BTC goes DOWN: -0.0300. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T11:24:59.093716+00:00 — [VOL_LOCK] Pearson r=0.340 (p=0.002, significant) between realized volatility and minutes to 90%+ lock-in across 79 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T11:24:59.093716+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (50.3%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 49.6% persistence (n=223, qualifying=115) | 12-18 UTC: 41.3% persistence (n=197, qualifying=75) | 18-24 UTC: 50.3% persistence (n=288, qualifying=145).


### 2026-04-11T18:04:22.809606+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0042 (Kalshi discount vs Polymarket). Std=0.1457, skew=-0.41. Median spread is +0.0000. 90% of spreads fall between -0.2034 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T18:04:22.809606+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.657 at lag=0. Contemporaneous correlation: 0.657.


### 2026-04-11T18:04:22.809606+00:00 — [CONVERGENCE] Across 97 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 8.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T18:04:22.809606+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 48.3% of the time 5 minutes later (out of 575 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T18:04:22.809606+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.293, p=0.003 (statistically significant, n=102). Mean spread when BTC goes UP: +0.0259. Mean spread when BTC goes DOWN: -0.0274. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T18:04:22.809606+00:00 — [VOL_LOCK] Pearson r=0.339 (p=0.002, significant) between realized volatility and minutes to 90%+ lock-in across 82 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T18:04:22.809606+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (50.7%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 50.7% persistence (n=292, qualifying=148).


### 2026-04-11T20:09:29.217534+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0019 (Kalshi discount vs Polymarket). Std=0.1447, skew=-0.39. Median spread is +0.0000. 90% of spreads fall between -0.2000 and +0.2027. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T20:09:29.217534+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.663 at lag=0. Contemporaneous correlation: 0.663.


### 2026-04-11T20:09:29.217534+00:00 — [CONVERGENCE] Across 100 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 8.5 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T20:09:29.217534+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 48.6% of the time 5 minutes later (out of 603 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T20:09:29.217534+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.298, p=0.002 (statistically significant, n=106). Mean spread when BTC goes UP: +0.0264. Mean spread when BTC goes DOWN: -0.0271. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T20:09:29.217534+00:00 — [VOL_LOCK] Pearson r=0.365 (p=0.001, significant) between realized volatility and minutes to 90%+ lock-in across 85 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T20:09:29.217534+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (51.1%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 51.1% persistence (n=350, qualifying=176).


### 2026-04-11T22:23:59.416413+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0026 (Kalshi discount vs Polymarket). Std=0.1429, skew=-0.40. Median spread is +0.0000. 90% of spreads fall between -0.1990 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T22:23:59.416413+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.663 at lag=0. Contemporaneous correlation: 0.663.


### 2026-04-11T22:23:59.416413+00:00 — [CONVERGENCE] Across 105 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 8.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T22:23:59.416413+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 48.0% of the time 5 minutes later (out of 619 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T22:23:59.416413+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.296, p=0.002 (statistically significant, n=110). Mean spread when BTC goes UP: +0.0264. Mean spread when BTC goes DOWN: -0.0261. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T22:23:59.416413+00:00 — [VOL_LOCK] Pearson r=0.370 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 89 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T22:23:59.416413+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (50.0%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 49.0% persistence (n=405, qualifying=192).


### 2026-04-11T23:24:44.847431+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0037 (Kalshi discount vs Polymarket). Std=0.1423, skew=-0.34. Median spread is +0.0000. 90% of spreads fall between -0.1950 and +0.1990. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-11T23:24:44.847431+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.658 at lag=0. Contemporaneous correlation: 0.658.


### 2026-04-11T23:24:44.847431+00:00 — [CONVERGENCE] Across 110 resolved windows, the leading probability locked in at 90%+ after an average of 7.9 minutes (median 8.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-11T23:24:44.847431+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.9% of the time 5 minutes later (out of 641 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-11T23:24:44.847431+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.293, p=0.002 (statistically significant, n=114). Mean spread when BTC goes UP: +0.0243. Mean spread when BTC goes DOWN: -0.0267. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-11T23:24:44.847431+00:00 — [VOL_LOCK] Pearson r=0.393 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 94 windows. Higher volatility → slower convergence, as expected.


### 2026-04-11T23:24:44.847431+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (50.0%). 00-06 UTC: 48.1% persistence (n=411, qualifying=206) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 48.6% persistence (n=463, qualifying=214).


### 2026-04-12T01:53:40.227522+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0051 (Kalshi discount vs Polymarket). Std=0.1416, skew=-0.34. Median spread is +0.0000. 90% of spreads fall between -0.2000 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T01:53:40.227522+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.665 at lag=0. Contemporaneous correlation: 0.665.


### 2026-04-12T01:53:40.227522+00:00 — [CONVERGENCE] Across 116 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 8.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-12T01:53:40.227522+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.6% of the time 5 minutes later (out of 666 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T01:53:40.227522+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.307, p=0.001 (statistically significant, n=123). Mean spread when BTC goes UP: +0.0238. Mean spread when BTC goes DOWN: -0.0294. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T01:53:40.227522+00:00 — [VOL_LOCK] Pearson r=0.409 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 97 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T01:53:40.227522+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (50.0%). 00-06 UTC: 47.5% persistence (n=450, qualifying=223) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 48.2% persistence (n=478, qualifying=220).


### 2026-04-12T03:12:51.383662+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0068 (Kalshi discount vs Polymarket). Std=0.1397, skew=-0.32. Median spread is -0.0010. 90% of spreads fall between -0.2000 and +0.1900. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T03:12:51.383662+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.673 at lag=0. Contemporaneous correlation: 0.673.


### 2026-04-12T03:12:51.383662+00:00 — [CONVERGENCE] Across 121 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-12T03:12:51.383662+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 47.3% of the time 5 minutes later (out of 693 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T03:12:51.383662+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.303, p=0.001 (statistically significant, n=127). Mean spread when BTC goes UP: +0.0216. Mean spread when BTC goes DOWN: -0.0302. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T03:12:51.383662+00:00 — [VOL_LOCK] Pearson r=0.402 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 102 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T03:12:51.383662+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (50.0%). 00-06 UTC: 46.8% persistence (n=508, qualifying=250) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 48.2% persistence (n=478, qualifying=220).


### 2026-04-12T04:29:29.485504+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0056 (Kalshi discount vs Polymarket). Std=0.1431, skew=-0.19. Median spread is -0.0010. 90% of spreads fall between -0.2000 and +0.1940. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T04:29:29.485504+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.661 at lag=0. Contemporaneous correlation: 0.661.


### 2026-04-12T04:29:29.485504+00:00 — [CONVERGENCE] Across 123 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-12T04:29:29.485504+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 48.8% of the time 5 minutes later (out of 734 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T04:29:29.485504+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.302, p=0.000 (statistically significant, n=131). Mean spread when BTC goes UP: +0.0239. Mean spread when BTC goes DOWN: -0.0293. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T04:29:29.485504+00:00 — [VOL_LOCK] Pearson r=0.407 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 104 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T04:29:29.485504+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (50.5%). 00-06 UTC: 50.5% persistence (n=566, qualifying=291) | 06-12 UTC: 50.0% persistence (n=226, qualifying=118) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 48.2% persistence (n=478, qualifying=220).


### 2026-04-12T06:50:04.956014+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0074 (Kalshi discount vs Polymarket). Std=0.1467, skew=-0.16. Median spread is -0.0010. 90% of spreads fall between -0.2200 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T06:50:04.956014+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.653 at lag=0. Contemporaneous correlation: 0.653.


### 2026-04-12T06:50:04.956014+00:00 — [CONVERGENCE] Across 130 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-12T06:50:04.956014+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 49.7% of the time 5 minutes later (out of 768 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T06:50:04.956014+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.337, p=0.000 (statistically significant, n=139). Mean spread when BTC goes UP: +0.0256. Mean spread when BTC goes DOWN: -0.0357. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T06:50:04.956014+00:00 — [VOL_LOCK] Pearson r=0.401 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 109 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T06:50:04.956014+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (52.6%). 00-06 UTC: 52.6% persistence (n=609, qualifying=321) | 06-12 UTC: 49.6% persistence (n=237, qualifying=125) | 12-18 UTC: 42.9% persistence (n=243, qualifying=98) | 18-24 UTC: 48.2% persistence (n=478, qualifying=220).


### 2026-04-12T18:47:26.361500+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0066 (Kalshi discount vs Polymarket). Std=0.1503, skew=0.01. Median spread is -0.0005. 90% of spreads fall between -0.2325 and +0.2050. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T18:47:26.361500+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.645 at lag=0. Contemporaneous correlation: 0.645.


### 2026-04-12T18:47:26.361500+00:00 — [CONVERGENCE] Across 135 resolved windows, the leading probability locked in at 90%+ after an average of 8.0 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.0 min.


### 2026-04-12T18:47:26.361500+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 50.3% of the time 5 minutes later (out of 811 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T18:47:26.361500+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.358, p=0.000 (statistically significant, n=147). Mean spread when BTC goes UP: +0.0299. Mean spread when BTC goes DOWN: -0.0368. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T18:47:26.361500+00:00 — [VOL_LOCK] Pearson r=0.446 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 114 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T18:47:26.361500+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 06-12 UTC bucket (53.3%). 00-06 UTC: 52.6% persistence (n=609, qualifying=321) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 49.1% persistence (n=492, qualifying=232).


### 2026-04-12T20:34:12.206917+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0127 (Kalshi discount vs Polymarket). Std=0.1517, skew=-0.03. Median spread is -0.0035. 90% of spreads fall between -0.2698 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-12T20:34:12.206917+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.646 at lag=0. Contemporaneous correlation: 0.646.


### 2026-04-12T20:34:12.206917+00:00 — [CONVERGENCE] Across 140 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-12T20:34:12.206917+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 51.7% of the time 5 minutes later (out of 882 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-12T20:34:12.206917+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.359, p=0.000 (statistically significant, n=153). Mean spread when BTC goes UP: +0.0279. Mean spread when BTC goes DOWN: -0.0395. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-12T20:34:12.206917+00:00 — [VOL_LOCK] Pearson r=0.445 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 119 windows. Higher volatility → slower convergence, as expected.


### 2026-04-12T20:34:12.206917+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 18-24 UTC bucket (53.5%). 00-06 UTC: 52.6% persistence (n=609, qualifying=321) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.5% persistence (n=603, qualifying=303).


### 2026-04-13T01:29:50.392155+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0108 (Kalshi discount vs Polymarket). Std=0.1533, skew=0.04. Median spread is -0.0030. 90% of spreads fall between -0.2695 and +0.2050. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T01:29:50.392155+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.638 at lag=0. Contemporaneous correlation: 0.638.


### 2026-04-13T01:29:50.392155+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T01:29:50.392155+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 52.8% of the time 5 minutes later (out of 947 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T01:29:50.392155+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.343, p=0.000 (statistically significant, n=158). Mean spread when BTC goes UP: +0.0254. Mean spread when BTC goes DOWN: -0.0382. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T01:29:50.392155+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T01:29:50.392155+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (55.1%). 00-06 UTC: 55.1% persistence (n=697, qualifying=376) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T02:31:49.485672+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0151 (Kalshi discount vs Polymarket). Std=0.1567, skew=-0.25. Median spread is -0.0045. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T02:31:49.485672+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.635 at lag=0. Contemporaneous correlation: 0.635.


### 2026-04-13T02:31:49.485672+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T02:31:49.485672+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.5% of the time 5 minutes later (out of 1012 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T02:31:49.485672+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.349, p=0.000 (statistically significant, n=163). Mean spread when BTC goes UP: +0.0254. Mean spread when BTC goes DOWN: -0.0408. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T02:31:49.485672+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T02:31:49.485672+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.2%). 00-06 UTC: 56.2% persistence (n=813, qualifying=441) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T03:32:00.848417+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T03:32:00.848417+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-13T03:32:00.848417+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T03:32:00.848417+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T03:32:00.848417+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.351, p=0.000 (statistically significant, n=167). Mean spread when BTC goes UP: +0.0246. Mean spread when BTC goes DOWN: -0.0426. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T03:32:00.848417+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T03:32:00.848417+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T04:32:12.738215+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T04:32:12.738215+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-13T04:32:12.738215+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T04:32:12.738215+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T04:32:12.738215+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.328, p=0.000 (statistically significant, n=171). Mean spread when BTC goes UP: +0.0191. Mean spread when BTC goes DOWN: -0.0448. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T04:32:12.738215+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T04:32:12.738215+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T05:32:26.310020+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T05:32:26.310020+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-13T05:32:26.310020+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T05:32:26.310020+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T05:32:26.310020+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.355, p=0.000 (statistically significant, n=175). Mean spread when BTC goes UP: +0.0215. Mean spread when BTC goes DOWN: -0.0465. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T05:32:26.310020+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T05:32:26.310020+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T07:55:59.446141+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T07:55:59.446141+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-13T07:55:59.446141+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T07:55:59.446141+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T07:55:59.446141+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.369, p=0.000 (statistically significant, n=180). Mean spread when BTC goes UP: +0.0238. Mean spread when BTC goes DOWN: -0.0469. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T07:55:59.446141+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T07:55:59.446141+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-13T14:35:52.272756+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-13T14:35:52.272756+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-13T14:35:52.272756+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-13T14:35:52.272756+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-13T14:35:52.272756+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.377, p=0.000 (statistically significant, n=200). Mean spread when BTC goes UP: +0.0273. Mean spread when BTC goes DOWN: -0.0467. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-13T14:35:52.272756+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-13T14:35:52.272756+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T02:58:13.952515+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T02:58:13.952515+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T02:58:13.952515+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T02:58:13.952515+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T02:58:13.952515+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.378, p=0.000 (statistically significant, n=205). Mean spread when BTC goes UP: +0.0274. Mean spread when BTC goes DOWN: -0.0461. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T02:58:13.952515+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T02:58:13.952515+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T06:33:38.610094+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T06:33:38.610094+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T06:33:38.610094+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T06:33:38.610094+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T06:33:38.610094+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.386, p=0.000 (statistically significant, n=213). Mean spread when BTC goes UP: +0.0274. Mean spread when BTC goes DOWN: -0.0475. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T06:33:38.610094+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T06:33:38.610094+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T07:33:58.062993+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T07:33:58.062993+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T07:33:58.062993+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T07:33:58.062993+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T07:33:58.062993+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.380, p=0.000 (statistically significant, n=217). Mean spread when BTC goes UP: +0.0267. Mean spread when BTC goes DOWN: -0.0465. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T07:33:58.062993+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T07:33:58.062993+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T08:34:18.045645+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T08:34:18.045645+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T08:34:18.045645+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T08:34:18.045645+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T08:34:18.045645+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.384, p=0.000 (statistically significant, n=221). Mean spread when BTC goes UP: +0.0277. Mean spread when BTC goes DOWN: -0.0466. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T08:34:18.045645+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T08:34:18.045645+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T18:45:21.082185+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T18:45:21.082185+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T18:45:21.082185+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T18:45:21.082185+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T18:45:21.082185+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.380, p=0.000 (statistically significant, n=225). Mean spread when BTC goes UP: +0.0270. Mean spread when BTC goes DOWN: -0.0459. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T18:45:21.082185+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T18:45:21.082185+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-14T20:09:00.466797+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-14T20:09:00.466797+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-14T20:09:00.466797+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-14T20:09:00.466797+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-14T20:09:00.466797+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.376, p=0.000 (statistically significant, n=230). Mean spread when BTC goes UP: +0.0261. Mean spread when BTC goes DOWN: -0.0455. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-14T20:09:00.466797+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-14T20:09:00.466797+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-15T03:40:42.338777+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-15T03:40:42.338777+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-15T03:40:42.338777+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-15T03:40:42.338777+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-15T03:40:42.338777+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.370, p=0.000 (statistically significant, n=233). Mean spread when BTC goes UP: +0.0265. Mean spread when BTC goes DOWN: -0.0436. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-15T03:40:42.338777+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-15T03:40:42.338777+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-15T06:44:50.545758+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-15T06:44:50.545758+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-15T06:44:50.545758+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-15T06:44:50.545758+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-15T06:44:50.545758+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.376, p=0.000 (statistically significant, n=238). Mean spread when BTC goes UP: +0.0259. Mean spread when BTC goes DOWN: -0.0467. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-15T06:44:50.545758+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-15T06:44:50.545758+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-15T14:41:16.627219+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-15T14:41:16.627219+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-15T14:41:16.627219+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-15T14:41:16.627219+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-15T14:41:16.627219+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.375, p=0.000 (statistically significant, n=244). Mean spread when BTC goes UP: +0.0265. Mean spread when BTC goes DOWN: -0.0458. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-15T14:41:16.627219+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-15T14:41:16.627219+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-15T15:56:59.991357+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-15T15:56:59.991357+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-15T15:56:59.991357+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-15T15:56:59.991357+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-15T15:56:59.991357+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.358, p=0.000 (statistically significant, n=249). Mean spread when BTC goes UP: +0.0263. Mean spread when BTC goes DOWN: -0.0433. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-15T15:56:59.991357+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-15T15:56:59.991357+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-15T20:40:45.361393+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-15T20:40:45.361393+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-15T20:40:45.361393+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-15T20:40:45.361393+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-15T20:40:45.361393+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.367, p=0.000 (statistically significant, n=254). Mean spread when BTC goes UP: +0.0273. Mean spread when BTC goes DOWN: -0.0458. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-15T20:40:45.361393+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-15T20:40:45.361393+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T09:25:23.401450+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-16T09:25:23.401450+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-16T09:25:23.401450+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-16T09:25:23.401450+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-16T09:25:23.401450+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.368, p=0.000 (statistically significant, n=257). Mean spread when BTC goes UP: +0.0271. Mean spread when BTC goes DOWN: -0.0457. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-16T09:25:23.401450+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-16T09:25:23.401450+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T10:53:00.062808+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-16T10:53:00.062808+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-16T10:53:00.062808+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-16T10:53:00.062808+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-16T10:53:00.062808+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.370, p=0.000 (statistically significant, n=263). Mean spread when BTC goes UP: +0.0268. Mean spread when BTC goes DOWN: -0.0459. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-16T10:53:00.062808+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-16T10:53:00.062808+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T12:10:25.020386+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-16T12:10:25.020386+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-16T12:10:25.020386+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-16T12:10:25.020386+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-16T12:10:25.020386+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.368, p=0.000 (statistically significant, n=267). Mean spread when BTC goes UP: +0.0257. Mean spread when BTC goes DOWN: -0.0460. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-16T12:10:25.020386+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-16T12:10:25.020386+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T16:03:32.105300+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-16T16:03:32.105300+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-16T16:03:32.105300+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-16T16:03:32.105300+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-16T16:03:32.105300+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.365, p=0.000 (statistically significant, n=277). Mean spread when BTC goes UP: +0.0297. Mean spread when BTC goes DOWN: -0.0441. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-16T16:03:32.105300+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-16T16:03:32.105300+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T21:58:38.728793+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-16T21:58:38.728793+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-16T21:58:38.728793+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-16T21:58:38.728793+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-16T21:58:38.728793+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.367, p=0.000 (statistically significant, n=280). Mean spread when BTC goes UP: +0.0297. Mean spread when BTC goes DOWN: -0.0442. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-16T21:58:38.728793+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-16T21:58:38.728793+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-16T21:58:38.728793+00:00 — [FIRST_TICK_SPREAD] Point-biserial correlation between first-tick spread (window open) and BTC UP outcome: r=0.224, p=0.000 (statistically significant, n=398). Mean first-tick spread when BTC goes UP: +0.0338. Mean first-tick spread when BTC goes DOWN: -0.0326. First-tick (window-open) Kalshi premium correlates with UP outcomes — supports the hypothesis that early spread is a cleaner signal.


### 2026-04-17T00:04:10.497308+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-17T00:04:10.497308+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-17T00:04:10.497308+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-17T00:04:10.497308+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-17T00:04:10.497308+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.374, p=0.000 (statistically significant, n=285). Mean spread when BTC goes UP: +0.0300. Mean spread when BTC goes DOWN: -0.0455. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-17T00:04:10.497308+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-17T00:04:10.497308+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-17T06:33:05.566812+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-17T06:33:05.566812+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-17T06:33:05.566812+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-17T06:33:05.566812+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-17T06:33:05.566812+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.374, p=0.000 (statistically significant, n=293). Mean spread when BTC goes UP: +0.0305. Mean spread when BTC goes DOWN: -0.0441. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-17T06:33:05.566812+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-17T06:33:05.566812+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-17T12:43:43.552443+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-17T12:43:43.552443+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-17T12:43:43.552443+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-17T12:43:43.552443+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-17T12:43:43.552443+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.353, p=0.000 (statistically significant, n=313). Mean spread when BTC goes UP: +0.0292. Mean spread when BTC goes DOWN: -0.0406. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-17T12:43:43.552443+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-17T12:43:43.552443+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-18T16:42:23.856451+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-18T16:42:23.856451+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-18T16:42:23.856451+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-18T16:42:23.856451+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-18T16:42:23.856451+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.356, p=0.000 (statistically significant, n=322). Mean spread when BTC goes UP: +0.0295. Mean spread when BTC goes DOWN: -0.0403. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-18T16:42:23.856451+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-18T16:42:23.856451+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-19T19:25:58.523432+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-19T19:25:58.523432+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-19T19:25:58.523432+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-19T19:25:58.523432+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-19T19:25:58.523432+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.346, p=0.000 (statistically significant, n=330). Mean spread when BTC goes UP: +0.0283. Mean spread when BTC goes DOWN: -0.0388. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-19T19:25:58.523432+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-19T19:25:58.523432+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-19T22:12:22.071622+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-19T22:12:22.071622+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-19T22:12:22.071622+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-19T22:12:22.071622+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-19T22:12:22.071622+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.331, p=0.000 (statistically significant, n=339). Mean spread when BTC goes UP: +0.0257. Mean spread when BTC goes DOWN: -0.0386. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-19T22:12:22.071622+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-19T22:12:22.071622+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-20T03:00:53.237652+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-20T03:00:53.237652+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-20T03:00:53.237652+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-20T03:00:53.237652+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-20T03:00:53.237652+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.313, p=0.000 (statistically significant, n=344). Mean spread when BTC goes UP: +0.0252. Mean spread when BTC goes DOWN: -0.0364. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-20T03:00:53.237652+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-20T03:00:53.237652+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-20T08:40:44.092503+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-20T08:40:44.092503+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-20T08:40:44.092503+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-20T08:40:44.092503+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-20T08:40:44.092503+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.311, p=0.000 (statistically significant, n=354). Mean spread when BTC goes UP: +0.0252. Mean spread when BTC goes DOWN: -0.0355. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-20T08:40:44.092503+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-20T08:40:44.092503+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-20T10:57:13.953289+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-20T10:57:13.953289+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-20T10:57:13.953289+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-20T10:57:13.953289+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-20T10:57:13.953289+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.307, p=0.000 (statistically significant, n=360). Mean spread when BTC goes UP: +0.0251. Mean spread when BTC goes DOWN: -0.0344. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-20T10:57:13.953289+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-20T10:57:13.953289+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-20T16:08:48.472454+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-20T16:08:48.472454+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-20T16:08:48.472454+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-20T16:08:48.472454+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-20T16:08:48.472454+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.311, p=0.000 (statistically significant, n=364). Mean spread when BTC goes UP: +0.0262. Mean spread when BTC goes DOWN: -0.0357. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-20T16:08:48.472454+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-20T16:08:48.472454+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T01:08:45.744547+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T01:08:45.744547+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T01:08:45.744547+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T01:08:45.744547+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T01:08:45.744547+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.311, p=0.000 (statistically significant, n=370). Mean spread when BTC goes UP: +0.0262. Mean spread when BTC goes DOWN: -0.0373. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T01:08:45.744547+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T01:08:45.744547+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T02:20:29.549307+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T02:20:29.549307+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T02:20:29.549307+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T02:20:29.549307+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T02:20:29.549307+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.304, p=0.000 (statistically significant, n=375). Mean spread when BTC goes UP: +0.0264. Mean spread when BTC goes DOWN: -0.0356. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T02:20:29.549307+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T02:20:29.549307+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T07:01:51.591313+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T07:01:51.591313+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T07:01:51.591313+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T07:01:51.591313+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T07:01:51.591313+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.305, p=0.000 (statistically significant, n=380). Mean spread when BTC goes UP: +0.0263. Mean spread when BTC goes DOWN: -0.0358. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T07:01:51.591313+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T07:01:51.591313+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T21:33:39.207463+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T21:33:39.207463+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T21:33:39.207463+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T21:33:39.207463+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T21:33:39.207463+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.304, p=0.000 (statistically significant, n=385). Mean spread when BTC goes UP: +0.0264. Mean spread when BTC goes DOWN: -0.0353. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T21:33:39.207463+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T21:33:39.207463+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T22:39:28.013929+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T22:39:28.013929+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T22:39:28.013929+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T22:39:28.013929+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T22:39:28.013929+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.301, p=0.000 (statistically significant, n=389). Mean spread when BTC goes UP: +0.0260. Mean spread when BTC goes DOWN: -0.0348. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T22:39:28.013929+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T22:39:28.013929+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-21T23:49:09.572276+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-21T23:49:09.572276+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-21T23:49:09.572276+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-21T23:49:09.572276+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-21T23:49:09.572276+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.302, p=0.000 (statistically significant, n=393). Mean spread when BTC goes UP: +0.0260. Mean spread when BTC goes DOWN: -0.0348. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-21T23:49:09.572276+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-21T23:49:09.572276+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-22T04:33:59.949603+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-22T04:33:59.949603+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-22T04:33:59.949603+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-22T04:33:59.949603+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-22T04:33:59.949603+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.305, p=0.000 (statistically significant, n=400). Mean spread when BTC goes UP: +0.0277. Mean spread when BTC goes DOWN: -0.0347. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-22T04:33:59.949603+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-22T04:33:59.949603+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-22T07:02:28.561633+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-22T07:02:28.561633+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-22T07:02:28.561633+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-22T07:02:28.561633+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-22T07:02:28.561633+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.310, p=0.000 (statistically significant, n=405). Mean spread when BTC goes UP: +0.0302. Mean spread when BTC goes DOWN: -0.0342. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-22T07:02:28.561633+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-22T07:02:28.561633+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-22T12:38:01.394509+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-22T12:38:01.394509+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-22T12:38:01.394509+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-22T12:38:01.394509+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-22T12:38:01.394509+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.311, p=0.000 (statistically significant, n=418). Mean spread when BTC goes UP: +0.0307. Mean spread when BTC goes DOWN: -0.0335. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-22T12:38:01.394509+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-22T12:38:01.394509+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-22T15:34:09.851902+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-22T15:34:09.851902+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-22T15:34:09.851902+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-22T15:34:09.851902+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-22T15:34:09.851902+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.316, p=0.000 (statistically significant, n=428). Mean spread when BTC goes UP: +0.0313. Mean spread when BTC goes DOWN: -0.0336. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-22T15:34:09.851902+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-22T15:34:09.851902+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-23T00:01:25.957665+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-23T00:01:25.957665+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-23T00:01:25.957665+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-23T00:01:25.957665+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-23T00:01:25.957665+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.319, p=0.000 (statistically significant, n=435). Mean spread when BTC goes UP: +0.0311. Mean spread when BTC goes DOWN: -0.0341. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-23T00:01:25.957665+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-23T00:01:25.957665+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-23T03:23:44.817385+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-23T03:23:44.817385+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-23T03:23:44.817385+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-23T03:23:44.817385+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-23T03:23:44.817385+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.324, p=0.000 (statistically significant, n=441). Mean spread when BTC goes UP: +0.0315. Mean spread when BTC goes DOWN: -0.0344. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-23T03:23:44.817385+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-23T03:23:44.817385+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-23T14:29:30.462172+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-23T14:29:30.462172+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-23T14:29:30.462172+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-23T14:29:30.462172+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-23T14:29:30.462172+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.322, p=0.000 (statistically significant, n=445). Mean spread when BTC goes UP: +0.0307. Mean spread when BTC goes DOWN: -0.0345. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-23T14:29:30.462172+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-23T14:29:30.462172+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-23T16:40:48.532292+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-23T16:40:48.532292+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-23T16:40:48.532292+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-23T16:40:48.532292+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-23T16:40:48.532292+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.319, p=0.000 (statistically significant, n=450). Mean spread when BTC goes UP: +0.0300. Mean spread when BTC goes DOWN: -0.0345. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-23T16:40:48.532292+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-23T16:40:48.532292+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-23T18:26:44.318551+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-23T18:26:44.318551+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-23T18:26:44.318551+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-23T18:26:44.318551+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-23T18:26:44.318551+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.320, p=0.000 (statistically significant, n=455). Mean spread when BTC goes UP: +0.0298. Mean spread when BTC goes DOWN: -0.0345. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-23T18:26:44.318551+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-23T18:26:44.318551+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T00:48:24.958207+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T00:48:24.958207+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T00:48:24.958207+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T00:48:24.958207+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T00:48:24.958207+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.321, p=0.000 (statistically significant, n=461). Mean spread when BTC goes UP: +0.0303. Mean spread when BTC goes DOWN: -0.0340. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T00:48:24.958207+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T00:48:24.958207+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T04:00:32.006176+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T04:00:32.006176+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T04:00:32.006176+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T04:00:32.006176+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T04:00:32.006176+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.322, p=0.000 (statistically significant, n=465). Mean spread when BTC goes UP: +0.0302. Mean spread when BTC goes DOWN: -0.0343. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T04:00:32.006176+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T04:00:32.006176+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T05:39:07.272315+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T05:39:07.272315+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T05:39:07.272315+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T05:39:07.272315+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T05:39:07.272315+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.323, p=0.000 (statistically significant, n=472). Mean spread when BTC goes UP: +0.0295. Mean spread when BTC goes DOWN: -0.0359. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T05:39:07.272315+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T05:39:07.272315+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T07:15:37.482056+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T07:15:37.482056+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T07:15:37.482056+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T07:15:37.482056+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T07:15:37.482056+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.322, p=0.000 (statistically significant, n=476). Mean spread when BTC goes UP: +0.0296. Mean spread when BTC goes DOWN: -0.0357. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T07:15:37.482056+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T07:15:37.482056+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T08:17:20.545549+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T08:17:20.545549+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T08:17:20.545549+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T08:17:20.545549+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T08:17:20.545549+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.321, p=0.000 (statistically significant, n=481). Mean spread when BTC goes UP: +0.0296. Mean spread when BTC goes DOWN: -0.0352. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T08:17:20.545549+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T08:17:20.545549+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T12:51:22.396756+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T12:51:22.396756+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T12:51:22.396756+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T12:51:22.396756+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T12:51:22.396756+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.305, p=0.000 (statistically significant, n=489). Mean spread when BTC goes UP: +0.0276. Mean spread when BTC goes DOWN: -0.0349. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T12:51:22.396756+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T12:51:22.396756+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T14:16:57.972033+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T14:16:57.972033+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T14:16:57.972033+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T14:16:57.972033+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T14:16:57.972033+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.312, p=0.000 (statistically significant, n=495). Mean spread when BTC goes UP: +0.0283. Mean spread when BTC goes DOWN: -0.0344. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T14:16:57.972033+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T14:16:57.972033+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T16:43:49.366130+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T16:43:49.366130+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T16:43:49.366130+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T16:43:49.366130+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T16:43:49.366130+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.314, p=0.000 (statistically significant, n=502). Mean spread when BTC goes UP: +0.0290. Mean spread when BTC goes DOWN: -0.0343. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T16:43:49.366130+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T16:43:49.366130+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T19:27:55.663697+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T19:27:55.663697+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T19:27:55.663697+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T19:27:55.663697+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T19:27:55.663697+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.307, p=0.000 (statistically significant, n=510). Mean spread when BTC goes UP: +0.0284. Mean spread when BTC goes DOWN: -0.0334. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T19:27:55.663697+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T19:27:55.663697+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-24T21:10:18.372722+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-24T21:10:18.372722+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-24T21:10:18.372722+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-24T21:10:18.372722+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-24T21:10:18.372722+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.310, p=0.000 (statistically significant, n=517). Mean spread when BTC goes UP: +0.0285. Mean spread when BTC goes DOWN: -0.0339. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-24T21:10:18.372722+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-24T21:10:18.372722+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T03:44:37.549244+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-25T03:44:37.549244+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-25T03:44:37.549244+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-25T03:44:37.549244+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-25T03:44:37.549244+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.308, p=0.000 (statistically significant, n=523). Mean spread when BTC goes UP: +0.0286. Mean spread when BTC goes DOWN: -0.0332. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-25T03:44:37.549244+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-25T03:44:37.549244+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T06:19:27.823765+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-25T06:19:27.823765+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-25T06:19:27.823765+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-25T06:19:27.823765+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-25T06:19:27.823765+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.314, p=0.000 (statistically significant, n=529). Mean spread when BTC goes UP: +0.0287. Mean spread when BTC goes DOWN: -0.0345. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-25T06:19:27.823765+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-25T06:19:27.823765+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T21:35:12.585720+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-25T21:35:12.585720+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-25T21:35:12.585720+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-25T21:35:12.585720+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-25T21:35:12.585720+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.311, p=0.000 (statistically significant, n=537). Mean spread when BTC goes UP: +0.0292. Mean spread when BTC goes DOWN: -0.0334. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-25T21:35:12.585720+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-25T21:35:12.585720+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T22:37:12.305265+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-25T22:37:12.305265+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-25T22:37:12.305265+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-25T22:37:12.305265+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-25T22:37:12.305265+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.318, p=0.000 (statistically significant, n=541). Mean spread when BTC goes UP: +0.0304. Mean spread when BTC goes DOWN: -0.0336. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-25T22:37:12.305265+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-25T22:37:12.305265+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T23:21:54.598130+00:00 — [SPREAD] Spread between Kalshi and Polymarket has mean -0.0141 (Kalshi discount vs Polymarket). Std=0.1561, skew=-0.26. Median spread is -0.0028. 90% of spreads fall between -0.2800 and +0.2000. Shapiro-Wilk p=0.0000 (not normal).


### 2026-04-25T23:21:54.598130+00:00 — [LEAD_LAG] No clear lead/lag — markets move simultaneously. Peak correlation coefficient 0.637 at lag=0. Contemporaneous correlation: 0.637.


### 2026-04-25T23:21:54.598130+00:00 — [CONVERGENCE] Across 144 resolved windows, the leading probability locked in at 90%+ after an average of 8.1 minutes (median 9.0 min). Fastest lock: 0.0 min, slowest: 14.4 min.


### 2026-04-25T23:21:54.598130+00:00 — [PERSISTENCE] When spread exceeded |0.05|, it remained above threshold 53.7% of the time 5 minutes later (out of 1028 qualifying observations). Low persistence — spread reverts quickly.


### 2026-04-25T23:21:54.598130+00:00 — [SPREAD_DIR] Point-biserial correlation between avg window spread and BTC UP outcome: r=0.318, p=0.000 (statistically significant, n=544). Mean spread when BTC goes UP: +0.0313. Mean spread when BTC goes DOWN: -0.0329. Kalshi premium (positive spread) correlates with UP moves.


### 2026-04-25T23:21:54.598130+00:00 — [VOL_LOCK] Pearson r=0.454 (p=0.000, significant) between realized volatility and minutes to 90%+ lock-in across 123 windows. Higher volatility → slower convergence, as expected.


### 2026-04-25T23:21:54.598130+00:00 — [TOD_PERSIST] Spread persistence varies by time of day. Highest persistence in 00-06 UTC bucket (56.7%). 00-06 UTC: 56.7% persistence (n=840, qualifying=457) | 06-12 UTC: 53.3% persistence (n=275, qualifying=152) | 12-18 UTC: 41.2% persistence (n=261, qualifying=102) | 18-24 UTC: 53.4% persistence (n=624, qualifying=311).


### 2026-04-25T23:21:54.598130+00:00 — [FIRST_TICK_SPREAD] Point-biserial correlation between first-tick spread (window open) and BTC UP outcome: r=0.162, p=0.000 (statistically significant, n=734). Mean first-tick spread when BTC goes UP: +0.0266. Mean first-tick spread when BTC goes DOWN: -0.0203. No clear directional signal in first-tick spread — hypothesis not supported with current data.

