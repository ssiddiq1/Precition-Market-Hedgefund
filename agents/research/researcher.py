"""
researcher.py — hourly deep analysis agent for quant-os

Analyses:
  1. Spread distribution (mean, std, skew, percentiles)
  2. Cross-correlation (does Kalshi or Polymarket move first?)
  3. Momentum convergence (minute-by-minute probability lock)
  4. Spread persistence (if >0.05 now, still >0.05 in 5 min?)
  5. Spread sign vs BTC direction (does positive spread predict UP outcomes?)
  6. Time-to-lock vs realized volatility (does vol affect convergence speed?)
  7. Spread persistence by time-of-day (UTC 6h buckets)
  8. First-tick spread vs BTC direction (window-open spread as predictor)

Outputs:
  logs/charts/TIMESTAMP_*.png
  logs/reports/report_TIMESTAMP.md
  logs/research_log.md     (appended)
  logs/backlog.md          (appended on "later")
"""

import os
import sys
import sqlite3
import time
import statistics
import textwrap
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats as scipy_stats

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH     = os.path.join(BASE_DIR, "data",   "btc15m.db")
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
CHARTS_DIR  = os.path.join(LOGS_DIR, "charts")
REPORTS_DIR = os.path.join(LOGS_DIR, "reports")
RESEARCH_LOG = os.path.join(LOGS_DIR, "research_log.md")
BACKLOG      = os.path.join(LOGS_DIR, "backlog.md")

INTERVAL = 3600  # 1 hour

# ── Matplotlib dark style ───────────────────────────────────────────────────
DARK = {
    "figure.facecolor":  "#0d0d0d",
    "axes.facecolor":    "#141414",
    "axes.edgecolor":    "#333",
    "axes.labelcolor":   "#888",
    "xtick.color":       "#555",
    "ytick.color":       "#555",
    "grid.color":        "#1e1e1e",
    "text.color":        "#e0e0e0",
    "lines.linewidth":   1.4,
}


def dark_fig(figsize=(10, 4)):
    with plt.rc_context(DARK):
        fig, ax = plt.subplots(figsize=figsize)
        ax.grid(True, linestyle="--", alpha=0.4)
        return fig, ax


def save_chart(fig, ts_tag, name):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, f"{ts_tag}_{name}.png")
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


# ── DB helpers ──────────────────────────────────────────────────────────────
def get_conn():
    return sqlite3.connect(DB_PATH)


def fetch_joined(conn, limit=2000):
    """Return rows joined by minute: (ts, kalshi_mid, poly_mid)."""
    return conn.execute("""
        SELECT k.collected_at,
               (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0,
               (p.up_bid + p.up_ask) / 2.0
        FROM markets k
        JOIN polymarket_markets p
          ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
           = strftime('%Y-%m-%dT%H:%M', p.collected_at)
        WHERE k.yes_bid_dollars IS NOT NULL
          AND k.yes_ask_dollars IS NOT NULL
          AND p.up_bid IS NOT NULL
          AND p.up_ask IS NOT NULL
        ORDER BY k.collected_at ASC
        LIMIT ?
    """, (limit,)).fetchall()


def fetch_kalshi(conn, limit=2000):
    return conn.execute("""
        SELECT collected_at, close_time,
               (yes_bid_dollars + yes_ask_dollars) / 2.0 AS mid,
               yes_ask_dollars - yes_bid_dollars AS spread
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL AND yes_ask_dollars IS NOT NULL
        ORDER BY collected_at ASC
        LIMIT ?
    """, (limit,)).fetchall()


# ── Analysis 1: Spread distribution ────────────────────────────────────────
def analysis_spread_distribution(conn, ts_tag):
    rows = fetch_joined(conn)
    if len(rows) < 10:
        return None, "Spread Distribution: insufficient joined rows (<10)."

    spreads = np.array([r[1] - r[2] for r in rows])
    n = len(spreads)
    mean   = float(np.mean(spreads))
    std    = float(np.std(spreads, ddof=1))
    skew   = float(scipy_stats.skew(spreads))
    kurt   = float(scipy_stats.kurtosis(spreads))
    pcts   = {p: float(np.percentile(spreads, p)) for p in [5, 10, 25, 50, 75, 90, 95]}

    # Normality test
    if n >= 8:
        _, p_norm = scipy_stats.shapiro(spreads[:min(n, 200)])
        normality = f"Shapiro-Wilk p={p_norm:.4f} ({'not normal' if p_norm < 0.05 else 'normal-ish'})"
    else:
        normality = "n too small for normality test"

    # Chart: histogram + KDE
    fig, ax = dark_fig((10, 4))
    with plt.rc_context(DARK):
        ax.hist(spreads, bins=30, color="#00ccff", alpha=0.4, density=True, label="Histogram")
        kde_x = np.linspace(spreads.min(), spreads.max(), 200)
        kde   = scipy_stats.gaussian_kde(spreads)
        ax.plot(kde_x, kde(kde_x), color="#00ff88", lw=2, label="KDE")
        ax.axvline(mean, color="#ff6b6b", lw=1.2, linestyle="--", label=f"mean={mean:.4f}")
        ax.axvline(0, color="#555", lw=0.8, linestyle=":")
        ax.set_xlabel("Spread (Kalshi mid − Polymarket mid)")
        ax.set_ylabel("Density")
        ax.set_title("Spread Distribution", color="#e0e0e0", pad=10)
        ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "spread_distribution")

    plain = (
        f"Spread between Kalshi and Polymarket has mean {mean:+.4f} "
        f"(Kalshi {'premium' if mean > 0 else 'discount'} vs Polymarket). "
        f"Std={std:.4f}, skew={skew:.2f}. "
        f"Median spread is {pcts[50]:+.4f}. "
        f"90% of spreads fall between {pcts[5]:+.4f} and {pcts[95]:+.4f}. "
        f"{normality}."
    )

    md = textwrap.dedent(f"""
        ### Finding 1: Spread Distribution

        | Stat | Value |
        |---|---|
        | n | {n} |
        | Mean | {mean:+.4f} |
        | Std | {std:.4f} |
        | Skew | {skew:.3f} |
        | Kurtosis | {kurt:.3f} |
        | p5 / p95 | {pcts[5]:+.4f} / {pcts[95]:+.4f} |
        | p10 / p90 | {pcts[10]:+.4f} / {pcts[90]:+.4f} |
        | Median | {pcts[50]:+.4f} |

        **Normality:** {normality}

        **Plain English:** {plain}

        **Statistical Significance:** Skew={skew:.3f} suggests {'right-tail outliers (Kalshi occasionally spikes high)' if skew > 0.3 else 'left-tail outliers (Polymarket occasionally spikes high)' if skew < -0.3 else 'roughly symmetric spread'}.

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] If mean spread is consistently non-zero, consider a mean-reversion entry when spread exceeds 1.5× std
        - [RESEARCH] Track whether spread sign (positive vs negative) correlates with BTC price direction
        - [CODE] Add spread z-score alert when |spread| > 2σ in collector
    """).strip()

    return {"plain": plain, "type": "SPREAD", "chart": chart}, md


# ── Analysis 2: Cross-correlation (lead/lag) ────────────────────────────────
def analysis_cross_correlation(conn, ts_tag):
    rows = fetch_joined(conn)
    if len(rows) < 20:
        return None, "Cross-Correlation: insufficient joined rows (<20)."

    k_mid = np.array([r[1] for r in rows])
    p_mid = np.array([r[2] for r in rows])

    # First-difference to get moves
    k_diff = np.diff(k_mid)
    p_diff = np.diff(p_mid)

    max_lag = min(10, len(k_diff) // 4)
    lags    = list(range(-max_lag, max_lag + 1))
    corrs   = []
    for lag in lags:
        if lag == 0:
            corrs.append(float(np.corrcoef(k_diff, p_diff)[0, 1]))
        elif lag > 0:
            # Kalshi leads Polymarket by `lag` steps
            c = np.corrcoef(k_diff[:-lag], p_diff[lag:])[0, 1]
            corrs.append(float(c))
        else:
            # Polymarket leads Kalshi by `|lag|` steps
            c = np.corrcoef(k_diff[-lag:], p_diff[:lag])[0, 1]
            corrs.append(float(c))

    best_lag  = lags[int(np.argmax(np.abs(corrs)))]
    best_corr = corrs[int(np.argmax(np.abs(corrs)))]
    zero_corr = corrs[lags.index(0)]

    if best_lag > 0:
        leader = f"Kalshi leads Polymarket by {best_lag} minute(s)"
    elif best_lag < 0:
        leader = f"Polymarket leads Kalshi by {abs(best_lag)} minute(s)"
    else:
        leader = "No clear lead/lag — markets move simultaneously"

    # Chart
    fig, ax = dark_fig((10, 4))
    with plt.rc_context(DARK):
        colors = ["#00ff88" if c == best_corr else "#00ccff" for c in corrs]
        ax.bar(lags, corrs, color=colors, alpha=0.7)
        ax.axvline(0, color="#555", lw=0.8, linestyle=":")
        ax.axhline(0, color="#333", lw=0.6)
        ax.set_xlabel("Lag (minutes, positive = Kalshi leads)")
        ax.set_ylabel("Cross-correlation")
        ax.set_title("Cross-Correlation: Kalshi vs Polymarket Price Moves", color="#e0e0e0", pad=10)
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    chart = save_chart(fig, ts_tag, "cross_correlation")

    plain = (
        f"{leader}. "
        f"Peak correlation coefficient {best_corr:.3f} at lag={best_lag}. "
        f"Contemporaneous correlation: {zero_corr:.3f}."
    )

    md = textwrap.dedent(f"""
        ### Finding 2: Cross-Correlation (Lead/Lag)

        | Stat | Value |
        |---|---|
        | Best lag | {best_lag} min |
        | Peak correlation | {best_corr:.4f} |
        | Same-time correlation | {zero_corr:.4f} |
        | Max lags tested | ±{max_lag} |

        **Leader:** {leader}

        **Plain English:** {plain}

        **Statistical Significance:** Correlation of {best_corr:.3f} {'is meaningful signal' if abs(best_corr) > 0.3 else 'is weak — markets may be largely independent at this timescale'}.

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] If one exchange reliably leads by 1–2 min, use the lagged signal as an entry trigger on the follower
        - [RESEARCH] Re-run on longer dataset once 500+ matched rows are available
        - [CODE] Add real-time lag indicator to dashboard
    """).strip()

    return {"plain": plain, "type": "LEAD_LAG", "chart": chart}, md


# ── Analysis 3: Momentum convergence ───────────────────────────────────────
def analysis_momentum_convergence(conn, ts_tag):
    rows = fetch_kalshi(conn)
    if not rows:
        return None, "Momentum Convergence: no data."

    windows = defaultdict(list)
    for collected_at, close_time, mid, _ in rows:
        if close_time:
            windows[close_time].append((collected_at, mid))

    conv_data = []  # (close_time, minutes_to_lock, final_prob)
    for close_time, obs in windows.items():
        if len(obs) < 3:
            continue
        obs.sort(key=lambda x: x[0])
        first_ts = datetime.fromisoformat(obs[0][0])
        for i, (ts_str, mid) in enumerate(obs):
            ts = datetime.fromisoformat(ts_str)
            elapsed = (ts - first_ts).total_seconds() / 60
            rest = [o[1] for o in obs[i:]]
            if all(r >= 0.90 or r <= 0.10 for r in rest):
                conv_data.append((close_time, elapsed, rest[-1]))
                break

    if not conv_data:
        plain = (
            f"Analyzed {len(windows)} contract windows. "
            "None reached 90%+ convergence yet — need more ticks per window."
        )
        md = textwrap.dedent(f"""
            ### Finding 3: Momentum Convergence

            **Windows analyzed:** {len(windows)}  |  **Converged:** 0

            **Plain English:** {plain}

            **Proposed Next Steps:**
            - [RESEARCH] Lower threshold to 80% to get initial data points
            - [CODE] Add per-window probability trajectory chart
        """).strip()
        return {"plain": plain, "type": "CONVERGENCE", "chart": None}, md

    minutes  = [d[1] for d in conv_data]
    avg_min  = statistics.mean(minutes)
    med_min  = statistics.median(minutes)
    n_conv   = len(conv_data)

    # Chart: histogram of convergence minutes
    fig, ax = dark_fig((10, 4))
    with plt.rc_context(DARK):
        ax.hist(minutes, bins=max(5, n_conv // 2), color="#00ff88", alpha=0.6)
        ax.axvline(avg_min, color="#ff6b6b", lw=1.2, linestyle="--", label=f"mean={avg_min:.1f}min")
        ax.axvline(med_min, color="#ffcc00", lw=1.2, linestyle=":", label=f"median={med_min:.1f}min")
        ax.set_xlabel("Minutes from window open to 90%+ lock")
        ax.set_ylabel("Count")
        ax.set_title("Momentum Convergence Distribution", color="#e0e0e0", pad=10)
        ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "momentum_convergence")

    plain = (
        f"Across {n_conv} resolved windows, the leading probability locked in at 90%+ "
        f"after an average of {avg_min:.1f} minutes (median {med_min:.1f} min). "
        f"Fastest lock: {min(minutes):.1f} min, slowest: {max(minutes):.1f} min."
    )

    md = textwrap.dedent(f"""
        ### Finding 3: Momentum Convergence

        | Stat | Value |
        |---|---|
        | Windows analyzed | {len(windows)} |
        | Converged (90%+) | {n_conv} |
        | Mean minutes to lock | {avg_min:.1f} |
        | Median minutes to lock | {med_min:.1f} |
        | Min / Max | {min(minutes):.1f} / {max(minutes):.1f} |

        **Plain English:** {plain}

        **Statistical Significance:** {'Good sample size for initial inference.' if n_conv >= 10 else 'Small sample — treat as directional only.'}

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] Enter position at the start of a new 15-min window and exit at avg lock-in time (~{avg_min:.0f} min) if probability has moved
        - [RESEARCH] Check if time-to-lock correlates with BTC volatility (VIX proxy)
        - [CODE] Real-time countdown to expected lock-in on dashboard
    """).strip()

    return {"plain": plain, "type": "CONVERGENCE", "chart": chart}, md


# ── Analysis 4: Spread persistence ─────────────────────────────────────────
def analysis_spread_persistence(conn, ts_tag):
    rows = fetch_joined(conn)
    if len(rows) < 15:
        return None, "Spread Persistence: insufficient rows (<15)."

    spreads = np.array([r[1] - r[2] for r in rows])
    THRESHOLD = 0.05
    HORIZON   = 5  # rows ahead (~5 min given 60s collection interval)

    total, still_above = 0, 0
    for i in range(len(spreads) - HORIZON):
        if abs(spreads[i]) > THRESHOLD:
            total += 1
            if abs(spreads[i + HORIZON]) > THRESHOLD:
                still_above += 1

    if total == 0:
        plain = f"No spreads exceeded |{THRESHOLD}| in this dataset."
        md = textwrap.dedent(f"""
            ### Finding 4: Spread Persistence

            **Plain English:** {plain}

            **Proposed Next Steps:**
            - [RESEARCH] Lower threshold to 0.02 and re-test
        """).strip()
        return {"plain": plain, "type": "PERSISTENCE", "chart": None}, md

    persist_rate = still_above / total

    # Chart: time series with threshold bands
    fig, ax = dark_fig((12, 4))
    with plt.rc_context(DARK):
        xs = range(len(spreads))
        ax.plot(xs, spreads, color="#00ccff", lw=1, alpha=0.8)
        ax.axhline( THRESHOLD, color="#ff6b6b", lw=0.8, linestyle="--", label=f"+{THRESHOLD}")
        ax.axhline(-THRESHOLD, color="#ff6b6b", lw=0.8, linestyle="--", label=f"-{THRESHOLD}")
        ax.axhline(0, color="#333", lw=0.6)
        ax.fill_between(xs, THRESHOLD, spreads,
                        where=(spreads > THRESHOLD), alpha=0.2, color="#ff6b6b")
        ax.fill_between(xs, -THRESHOLD, spreads,
                        where=(spreads < -THRESHOLD), alpha=0.2, color="#ff6b6b")
        ax.set_xlabel("Observation index")
        ax.set_ylabel("Spread")
        ax.set_title(f"Spread Persistence (threshold ±{THRESHOLD})", color="#e0e0e0", pad=10)
        ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "spread_persistence")

    plain = (
        f"When spread exceeded |{THRESHOLD}|, it remained above threshold {persist_rate:.1%} "
        f"of the time {HORIZON} minutes later (out of {total} qualifying observations). "
        f"{'High persistence — spread is mean-reverting slowly.' if persist_rate > 0.6 else 'Low persistence — spread reverts quickly.'}"
    )

    md = textwrap.dedent(f"""
        ### Finding 4: Spread Persistence

        | Stat | Value |
        |---|---|
        | Threshold | ±{THRESHOLD} |
        | Horizon | {HORIZON} min |
        | Qualifying observations | {total} |
        | Still above threshold | {still_above} ({persist_rate:.1%}) |

        **Plain English:** {plain}

        **Statistical Significance:** {'Meaningful sample.' if total >= 20 else 'Small sample — directional only.'}

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] {'Persistent spread → hold position for full window; mean-reversion play.' if persist_rate > 0.6 else 'Fast reversion → tighter stops, smaller hold time.'}
        - [RESEARCH] Segment persistence by time-of-day and BTC volatility
        - [CODE] Add persistence score as a live signal on dashboard
    """).strip()

    return {"plain": plain, "type": "PERSISTENCE", "chart": chart}, md


# ── Analysis 5: Spread sign vs BTC direction ───────────────────────────────
def analysis_spread_vs_direction(conn, ts_tag):
    """
    For each 15-min window: compute avg cross-exchange spread, then check
    whether the final market outcome (YES > 0.5 = BTC UP) correlates with
    the spread sign. Positive spread = Kalshi premium; do traders on Kalshi
    see UP moves coming earlier?
    """
    # Get window-level avg spread + final yes_mid (proxy for resolution)
    rows = conn.execute("""
        SELECT k.close_time,
               AVG((k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
                   - (p.up_bid + p.up_ask) / 2.0)  AS avg_spread,
               AVG((k.yes_bid_dollars + k.yes_ask_dollars) / 2.0) AS avg_kalshi_mid
        FROM markets k
        JOIN polymarket_markets p
          ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
           = strftime('%Y-%m-%dT%H:%M', p.collected_at)
        WHERE k.yes_bid_dollars IS NOT NULL
          AND k.yes_ask_dollars IS NOT NULL
          AND p.up_bid IS NOT NULL
          AND p.up_ask IS NOT NULL
          AND k.close_time IS NOT NULL
        GROUP BY k.close_time
        HAVING COUNT(*) >= 3
        ORDER BY k.close_time ASC
    """).fetchall()

    # Also get final mid per window from Kalshi
    final_mids = {}
    kalshi_rows = conn.execute("""
        SELECT close_time,
               (yes_bid_dollars + yes_ask_dollars) / 2.0 AS mid
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL AND yes_ask_dollars IS NOT NULL
          AND close_time IS NOT NULL
        ORDER BY close_time, collected_at DESC
    """).fetchall()
    seen = set()
    for ct, mid in kalshi_rows:
        if ct not in seen:
            final_mids[ct] = mid
            seen.add(ct)

    # Build paired (spread, direction) dataset
    paired = []
    for close_time, avg_spread, _ in rows:
        if close_time in final_mids:
            direction = 1 if final_mids[close_time] > 0.5 else 0
            paired.append((avg_spread, direction))

    if len(paired) < 4:
        plain = f"Only {len(paired)} matched windows — need more data for spread vs direction."
        return {"plain": plain, "type": "SPREAD_DIR", "chart": None}, textwrap.dedent(f"""
            ### Finding 5: Spread Sign vs BTC Direction
            **Plain English:** {plain}
            **Proposed Next Steps:**
            - [RESEARCH] Re-run once 20+ resolved windows are available
        """).strip()

    spreads   = np.array([p[0] for p in paired])
    outcomes  = np.array([p[1] for p in paired])
    n = len(paired)

    # Point-biserial correlation
    corr, p_val = scipy_stats.pointbiserialr(outcomes, spreads)

    # Split stats
    up_spreads   = spreads[outcomes == 1]
    down_spreads = spreads[outcomes == 0]
    up_mean   = float(np.mean(up_spreads))   if len(up_spreads)   > 0 else float("nan")
    down_mean = float(np.mean(down_spreads)) if len(down_spreads) > 0 else float("nan")

    # Chart: spread by outcome
    fig, ax = dark_fig((9, 4))
    with plt.rc_context(DARK):
        ax.scatter(spreads[outcomes == 1], [1] * int(outcomes.sum()),
                   color="#00ff88", alpha=0.7, s=60, label=f"UP ({int(outcomes.sum())})")
        ax.scatter(spreads[outcomes == 0], [0] * int((1 - outcomes).sum()),
                   color="#ff6b6b", alpha=0.7, s=60, label=f"DOWN ({int((1 - outcomes).sum())})")
        ax.axvline(0, color="#555", lw=0.8, linestyle=":")
        ax.axvline(up_mean,   color="#00ff88", lw=1, linestyle="--", alpha=0.6)
        ax.axvline(down_mean, color="#ff6b6b", lw=1, linestyle="--", alpha=0.6)
        ax.set_xlabel("Avg window spread (Kalshi − Polymarket)")
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["DOWN", "UP"])
        ax.set_title("Spread Sign vs BTC Direction by Window", color="#e0e0e0", pad=10)
        ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "spread_vs_direction")

    sig = "statistically significant" if p_val < 0.05 else "not significant"
    plain = (
        f"Point-biserial correlation between avg window spread and BTC UP outcome: "
        f"r={corr:.3f}, p={p_val:.3f} ({sig}, n={n}). "
        f"Mean spread when BTC goes UP: {up_mean:+.4f}. "
        f"Mean spread when BTC goes DOWN: {down_mean:+.4f}. "
        f"{'Kalshi premium (positive spread) correlates with UP moves.' if corr > 0.2 else 'No clear directional signal in spread sign yet.'}"
    )

    md = textwrap.dedent(f"""
        ### Finding 5: Spread Sign vs BTC Direction

        | Stat | Value |
        |---|---|
        | Windows | {n} |
        | Point-biserial r | {corr:.4f} |
        | p-value | {p_val:.4f} |
        | Significant (p<0.05) | {"Yes" if p_val < 0.05 else "No"} |
        | Mean spread (UP windows) | {up_mean:+.4f} |
        | Mean spread (DOWN windows) | {down_mean:+.4f} |

        **Plain English:** {plain}

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] {'Use positive spread as weak UP signal for entry timing' if corr > 0.2 else 'No actionable signal yet — accumulate more windows'}
        - [RESEARCH] Re-test with 50+ windows and first-tick spread (not avg) as predictor
    """).strip()

    return {"plain": plain, "type": "SPREAD_DIR", "chart": chart}, md


# ── Analysis 6: Time-to-lock vs realized volatility ────────────────────────
def analysis_lock_vs_volatility(conn, ts_tag):
    """
    For each resolved window: compute realized volatility as std of
    first-differences of yes_mid. Correlate with time-to-lock.
    Hypothesis: high volatility windows → slower convergence.
    """
    rows = fetch_kalshi(conn)
    if not rows:
        return None, "Lock vs Volatility: no data."

    windows = defaultdict(list)
    for collected_at, close_time, mid, _ in rows:
        if close_time:
            windows[close_time].append((collected_at, mid))

    vol_lock_pairs = []  # (realized_vol, minutes_to_lock)
    for close_time, obs in windows.items():
        if len(obs) < 5:
            continue
        obs.sort(key=lambda x: x[0])
        mids = np.array([o[1] for o in obs])
        realized_vol = float(np.std(np.diff(mids))) if len(mids) > 1 else 0.0

        first_ts = datetime.fromisoformat(obs[0][0])
        lock_min = None
        for i, (ts_str, mid) in enumerate(obs):
            ts_dt = datetime.fromisoformat(ts_str)
            elapsed = (ts_dt - first_ts).total_seconds() / 60
            rest = [o[1] for o in obs[i:]]
            if all(r >= 0.90 or r <= 0.10 for r in rest):
                lock_min = elapsed
                break

        if lock_min is not None:
            vol_lock_pairs.append((realized_vol, lock_min))

    if len(vol_lock_pairs) < 4:
        plain = f"Only {len(vol_lock_pairs)} converged windows — need more data."
        return {"plain": plain, "type": "VOL_LOCK", "chart": None}, textwrap.dedent(f"""
            ### Finding 6: Time-to-Lock vs Realized Volatility
            **Plain English:** {plain}
            **Proposed Next Steps:**
            - [RESEARCH] Re-run once 15+ resolved windows available
        """).strip()

    vols  = np.array([p[0] for p in vol_lock_pairs])
    locks = np.array([p[1] for p in vol_lock_pairs])
    corr, p_val = scipy_stats.pearsonr(vols, locks)

    # Chart: scatter
    fig, ax = dark_fig((9, 4))
    with plt.rc_context(DARK):
        ax.scatter(vols, locks, color="#00ccff", alpha=0.8, s=70)
        # Fit line
        if len(vols) >= 3:
            m, b = np.polyfit(vols, locks, 1)
            x_line = np.linspace(vols.min(), vols.max(), 50)
            ax.plot(x_line, m * x_line + b, color="#ff6b6b", lw=1.2,
                    linestyle="--", alpha=0.8, label=f"slope={m:.1f}")
        ax.set_xlabel("Realized Volatility (std of mid first-differences)")
        ax.set_ylabel("Minutes to 90%+ lock")
        ax.set_title("Time-to-Lock vs Realized Volatility", color="#e0e0e0", pad=10)
        if len(vols) >= 3:
            ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "lock_vs_volatility")

    sig = "significant" if p_val < 0.05 else "not significant"
    plain = (
        f"Pearson r={corr:.3f} (p={p_val:.3f}, {sig}) between realized volatility "
        f"and minutes to 90%+ lock-in across {len(vol_lock_pairs)} windows. "
        f"{'Higher volatility → slower convergence, as expected.' if corr > 0.2 else 'Higher volatility → faster convergence (surprise — fast movers lock in quickly).' if corr < -0.2 else 'No clear relationship between volatility and convergence speed.'}"
    )

    md = textwrap.dedent(f"""
        ### Finding 6: Time-to-Lock vs Realized Volatility

        | Stat | Value |
        |---|---|
        | Windows | {len(vol_lock_pairs)} |
        | Pearson r | {corr:.4f} |
        | p-value | {p_val:.4f} |
        | Significant | {"Yes" if p_val < 0.05 else "No"} |
        | Avg vol | {float(np.mean(vols)):.4f} |
        | Avg lock min | {float(np.mean(locks)):.1f} |

        **Plain English:** {plain}

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [RESEARCH] Add external BTC realized vol (from Binance/CoinGecko) to see if macro vol predicts lock speed
        - [STRATEGY] In high-vol windows, adjust exit timing relative to avg lock-in
    """).strip()

    return {"plain": plain, "type": "VOL_LOCK", "chart": chart}, md


# ── Analysis 7: Spread persistence by time-of-day ──────────────────────────
def analysis_persistence_by_tod(conn, ts_tag):
    """
    Split observations into 6-hour UTC buckets (0-6, 6-12, 12-18, 18-24)
    and compare spread persistence rates across buckets.
    """
    rows = fetch_joined(conn)
    if len(rows) < 20:
        return None, "Persistence by ToD: insufficient rows (<20)."

    THRESHOLD = 0.05
    HORIZON   = 5

    # Bucket each row
    buckets = {"00-06": [], "06-12": [], "12-18": [], "18-24": []}
    for ts_str, k_mid, p_mid in rows:
        try:
            hour = datetime.fromisoformat(ts_str).hour
        except Exception:
            continue
        spread = k_mid - p_mid
        if   hour <  6: buckets["00-06"].append(spread)
        elif hour < 12: buckets["06-12"].append(spread)
        elif hour < 18: buckets["12-18"].append(spread)
        else:           buckets["18-24"].append(spread)

    # Compute persistence per bucket
    results = {}
    for label, sprs in buckets.items():
        sprs_arr = np.array(sprs)
        total = still_above = 0
        for i in range(len(sprs_arr) - HORIZON):
            if abs(sprs_arr[i]) > THRESHOLD:
                total += 1
                if abs(sprs_arr[i + HORIZON]) > THRESHOLD:
                    still_above += 1
        rate = still_above / total if total > 0 else None
        results[label] = {"n": len(sprs), "qualifying": total, "rate": rate}

    # Chart: bar chart of persistence rates
    labels_with_data = [(lb, r) for lb, r in results.items() if r["rate"] is not None]
    fig, ax = dark_fig((9, 4))
    with plt.rc_context(DARK):
        if labels_with_data:
            bar_labels = [lb for lb, _ in labels_with_data]
            bar_rates  = [r["rate"] for _, r in labels_with_data]
            bar_colors = ["#00ff88" if r > 0.6 else "#ffcc00" if r > 0.4 else "#ff6b6b"
                          for r in bar_rates]
            ax.bar(bar_labels, bar_rates, color=bar_colors, alpha=0.7)
            ax.axhline(0.5, color="#555", lw=0.8, linestyle="--", label="50% baseline")
            ax.set_ylim(0, 1)
            ax.set_xlabel("UTC Hour Bucket")
            ax.set_ylabel(f"Persistence Rate (|spread|>{THRESHOLD} after {HORIZON} min)")
            ax.set_title("Spread Persistence by Time of Day (UTC)", color="#e0e0e0", pad=10)
            ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
        else:
            ax.text(0.5, 0.5, "Insufficient qualifying observations",
                    ha="center", va="center", color="#555", transform=ax.transAxes)
    chart = save_chart(fig, ts_tag, "persistence_by_tod")

    # Build summary
    lines = []
    for lb, r in results.items():
        if r["rate"] is not None:
            lines.append(f"{lb} UTC: {r['rate']:.1%} persistence (n={r['n']}, qualifying={r['qualifying']})")
        else:
            lines.append(f"{lb} UTC: no qualifying observations (n={r['n']})")

    best_bucket = max(
        [(lb, r) for lb, r in results.items() if r["rate"] is not None],
        key=lambda x: x[1]["rate"],
        default=(None, None)
    )
    best_label = best_bucket[0]
    best_rate  = best_bucket[1]["rate"] if best_bucket[1] else None

    plain = (
        f"Spread persistence varies by time of day. "
        + (f"Highest persistence in {best_label} UTC bucket ({best_rate:.1%}). " if best_label else "")
        + " | ".join(lines) + "."
    )

    def fmt_rate(r):
        return f"{r['rate']:.1%}" if r["rate"] is not None else "—"

    table_rows = "\n".join(
        f"| {lb} UTC | {r['n']} | {r['qualifying']} | {fmt_rate(r)} |"
        for lb, r in results.items()
    )

    md = textwrap.dedent(f"""
        ### Finding 7: Spread Persistence by Time of Day

        | UTC Bucket | Observations | Qualifying (>±{THRESHOLD}) | Persistence Rate |
        |---|---|---|---|
        {table_rows}

        **Plain English:** {plain}

        **Statistical Significance:** Small sample per bucket — treat as directional signal only.

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] {'Prefer trading in ' + best_label + ' UTC when spread is large — highest persistence' if best_label else 'Accumulate more data per bucket'}
        - [RESEARCH] Add day-of-week dimension once 7+ days of data are collected
    """).strip()

    return {"plain": plain, "type": "TOD_PERSIST", "chart": chart}, md


# ── Analysis 8: First-tick spread vs BTC direction ────────────────────────
def analysis_first_tick_spread(conn, ts_tag):
    """
    Hypothesis: the cross-exchange spread at window open (first tick) is a
    cleaner signal than the avg-window spread, because later ticks reflect
    price discovery already in progress.

    For each 15-min close_time:
      - first-tick spread = kalshi_mid - poly_mid at the earliest collected_at
      - outcome = final kalshi_mid > 0.5 (proxy for BTC UP resolution)
    Run point-biserial correlation between first-tick spread and direction_up.
    """
    # First tick per window: earliest collected_at for each close_time
    rows = conn.execute("""
        SELECT k.close_time,
               (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0
                   - (p.up_bid + p.up_ask) / 2.0  AS first_spread
        FROM markets k
        JOIN polymarket_markets p
          ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
           = strftime('%Y-%m-%dT%H:%M', p.collected_at)
        WHERE k.yes_bid_dollars IS NOT NULL
          AND k.yes_ask_dollars IS NOT NULL
          AND p.up_bid IS NOT NULL
          AND p.up_ask IS NOT NULL
          AND k.close_time IS NOT NULL
        GROUP BY k.close_time
        HAVING k.collected_at = MIN(k.collected_at)
        ORDER BY k.close_time ASC
    """).fetchall()

    # Final kalshi mid per window (last tick before close_time, same as Finding 5)
    final_mids = {}
    kalshi_rows = conn.execute("""
        SELECT close_time,
               (yes_bid_dollars + yes_ask_dollars) / 2.0 AS mid
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL AND yes_ask_dollars IS NOT NULL
          AND close_time IS NOT NULL
        ORDER BY close_time, collected_at DESC
    """).fetchall()
    seen = set()
    for ct, mid in kalshi_rows:
        if ct not in seen:
            final_mids[ct] = mid
            seen.add(ct)

    paired = []
    for close_time, first_spread in rows:
        if close_time in final_mids:
            direction = 1 if final_mids[close_time] > 0.5 else 0
            paired.append((first_spread, direction))

    if len(paired) < 4:
        plain = f"Only {len(paired)} matched windows — need more data for first-tick spread analysis."
        return {"plain": plain, "type": "FIRST_TICK_SPREAD", "chart": None}, textwrap.dedent(f"""
            ### Finding 8: First-Tick Spread vs BTC Direction
            **Plain English:** {plain}
            **Proposed Next Steps:**
            - [RESEARCH] Re-run once 20+ resolved windows are available
        """).strip()

    spreads  = np.array([p[0] for p in paired])
    outcomes = np.array([p[1] for p in paired])
    n = len(paired)

    corr, p_val = scipy_stats.pointbiserialr(outcomes, spreads)

    up_spreads   = spreads[outcomes == 1]
    down_spreads = spreads[outcomes == 0]
    up_mean   = float(np.mean(up_spreads))   if len(up_spreads)   > 0 else float("nan")
    down_mean = float(np.mean(down_spreads)) if len(down_spreads) > 0 else float("nan")

    # Chart: first-tick spread by outcome (mirrors Finding 5 layout)
    fig, ax = dark_fig((9, 4))
    with plt.rc_context(DARK):
        ax.scatter(spreads[outcomes == 1], [1] * int(outcomes.sum()),
                   color="#00ff88", alpha=0.7, s=60, label=f"UP ({int(outcomes.sum())})")
        ax.scatter(spreads[outcomes == 0], [0] * int((1 - outcomes).sum()),
                   color="#ff6b6b", alpha=0.7, s=60, label=f"DOWN ({int((1 - outcomes).sum())})")
        ax.axvline(0,         color="#555",    lw=0.8, linestyle=":")
        ax.axvline(up_mean,   color="#00ff88", lw=1,   linestyle="--", alpha=0.6)
        ax.axvline(down_mean, color="#ff6b6b", lw=1,   linestyle="--", alpha=0.6)
        ax.set_xlabel("First-tick spread at window open (Kalshi − Polymarket)")
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["DOWN", "UP"])
        ax.set_title("First-Tick Spread vs BTC Direction by Window", color="#e0e0e0", pad=10)
        ax.legend(fontsize=9, facecolor="#1e1e1e", labelcolor="#e0e0e0")
    chart = save_chart(fig, ts_tag, "first_tick_spread_vs_direction")

    sig = "statistically significant" if p_val < 0.05 else "not significant"
    stronger_than_avg = abs(corr) > 0.2

    plain = (
        f"Point-biserial correlation between first-tick spread (window open) and BTC UP outcome: "
        f"r={corr:.3f}, p={p_val:.3f} ({sig}, n={n}). "
        f"Mean first-tick spread when BTC goes UP: {up_mean:+.4f}. "
        f"Mean first-tick spread when BTC goes DOWN: {down_mean:+.4f}. "
        f"{'First-tick (window-open) Kalshi premium correlates with UP outcomes — supports the hypothesis that early spread is a cleaner signal.' if corr > 0.2 else 'No clear directional signal in first-tick spread — hypothesis not supported with current data.'}"
    )

    md = textwrap.dedent(f"""
        ### Finding 8: First-Tick Spread vs BTC Direction

        **Hypothesis:** The cross-exchange spread at window open (first collected tick per
        close_time) is more informative than the average spread, because later ticks are
        contaminated by price discovery already in progress.

        | Stat | Value |
        |---|---|
        | Windows | {n} |
        | Point-biserial r | {corr:.4f} |
        | p-value | {p_val:.4f} |
        | Significant (p<0.05) | {"Yes" if p_val < 0.05 else "No"} |
        | Mean first-tick spread (UP windows) | {up_mean:+.4f} |
        | Mean first-tick spread (DOWN windows) | {down_mean:+.4f} |

        **Plain English:** {plain}

        **Chart:** `{os.path.basename(chart)}`

        **Proposed Next Steps:**
        - [STRATEGY] {'Use first-tick spread as entry signal — positive = weak UP bias at window open' if stronger_than_avg else 'No actionable signal yet — accumulate more windows'}
        - [RESEARCH] Compare r here vs Finding 5 r to quantify whether first-tick is cleaner than avg-window spread
        - [RESEARCH] Test first-tick spread as a feature in the cross-market RF (Strategy Explorer)
    """).strip()

    return {"plain": plain, "type": "FIRST_TICK_SPREAD", "chart": chart}, md


# ── Compose full report ─────────────────────────────────────────────────────
def compose_report(ts, findings, mds):
    sections = "\n\n".join(mds)
    charts   = "\n".join(
        f"- `logs/charts/{os.path.basename(f['chart'])}`"
        for f in findings if f and f.get("chart")
    )
    return textwrap.dedent(f"""
        # Research Report — {ts}

        **Generated by:** researcher.py
        **Data source:** data/btc15m.db
        **Charts:** {len([f for f in findings if f and f.get('chart')])} generated

        ---

        ## Findings

        {sections}

        ---

        ## Charts

        {charts if charts else '_No charts generated._'}

        ---

        ## Risks & Limitations

        - Dataset is small (<500 joined rows); all findings are preliminary.
        - 60-second polling means true sub-minute lead/lag is invisible.
        - Both markets cover the same underlying (BTC 15-min window) but resolve independently; price differences may reflect liquidity, not arbitrage opportunity.
        - Spread calculation assumes contemporaneous quotes (joined by minute), not true simultaneous sampling.
    """).strip()


# ── Append to research_log.md ───────────────────────────────────────────────
def append_research_log(ts, findings):
    with open(RESEARCH_LOG, "a") as f:
        for item in findings:
            if not item:
                continue
            f.write(f"\n### {ts} — [{item['type']}] {item['plain']}\n\n")


# ── Interactive proposal loop ───────────────────────────────────────────────
def propose(ts, report_md):
    """Extract [STRATEGY]/[RESEARCH]/[CODE] lines, prompt y/n/later."""
    action_lines = [
        line.strip()
        for line in report_md.splitlines()
        if line.strip().startswith("- [STRATEGY]")
        or line.strip().startswith("- [RESEARCH]")
        or line.strip().startswith("- [CODE]")
    ]

    if not action_lines:
        print("[researcher] No action items found.")
        return

    print(f"\n[researcher] {len(action_lines)} proposed action(s) — {ts}\n")
    for item in action_lines:
        tag   = item.split("]")[0].lstrip("- [")
        label = {"STRATEGY": "\033[33m", "RESEARCH": "\033[36m", "CODE": "\033[35m"}.get(tag, "")
        reset = "\033[0m"
        print(f"  {label}[{tag}]{reset} {item.split('] ', 1)[-1]}")
        try:
            ans = input("  Implement this? (y/n/later): ").strip().lower()
        except EOFError:
            ans = "n"

        if ans == "y":
            print(f"  → [TODO] Implement now — add to your Claude Code session.")
        elif ans == "later":
            os.makedirs(LOGS_DIR, exist_ok=True)
            with open(BACKLOG, "a") as f:
                f.write(f"\n- [{ts}] [{tag}] {item.split('] ', 1)[-1]}\n")
            print(f"  → Saved to logs/backlog.md")
        else:
            print(f"  → Skipped")
        print()


# ── Main run ────────────────────────────────────────────────────────────────
def run_once():
    os.makedirs(CHARTS_DIR,  exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    ts     = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    ts_iso = datetime.now(timezone.utc).isoformat()
    print(f"[researcher] Starting analysis — {ts_iso}")

    conn = get_conn()
    results = [
        analysis_spread_distribution(conn, ts),
        analysis_cross_correlation(conn, ts),
        analysis_momentum_convergence(conn, ts),
        analysis_spread_persistence(conn, ts),
        analysis_spread_vs_direction(conn, ts),
        analysis_lock_vs_volatility(conn, ts),
        analysis_persistence_by_tod(conn, ts),
        analysis_first_tick_spread(conn, ts),
    ]
    conn.close()

    findings = [r[0] for r in results]
    mds      = [r[1] for r in results]

    report_md = compose_report(ts_iso, findings, mds)

    report_path = os.path.join(REPORTS_DIR, f"report_{ts}.md")
    with open(report_path, "w") as f:
        f.write(report_md)
    print(f"[researcher] Report → {report_path}")

    # Charts
    chart_paths = [f["chart"] for f in findings if f and f.get("chart")]
    for cp in chart_paths:
        print(f"[researcher] Chart  → {cp}")

    append_research_log(ts_iso, findings)
    print(f"[researcher] Log    → {RESEARCH_LOG}")

    propose(ts_iso, report_md)
    return report_md


def main():
    print(f"[researcher] Running every {INTERVAL // 60}min → {REPORTS_DIR}/")
    while True:
        try:
            run_once()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            import traceback
            print(f"[researcher ERROR] {e}")
            traceback.print_exc()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    if "--once" in sys.argv:
        run_once()
    else:
        main()
