import os
import sqlite3
import time
import statistics
from collections import defaultdict
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH  = os.path.join(BASE_DIR, "data", "btc15m.db")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
INTERVAL = 6 * 3600  # 6 hours


def get_conn():
    return sqlite3.connect(DB_PATH)


def spread_distribution(conn):
    rows = conn.execute("""
        SELECT (k.yes_bid_dollars + k.yes_ask_dollars) / 2.0,
               (p.up_bid + p.up_ask) / 2.0
        FROM markets k
        JOIN polymarket_markets p
          ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
           = strftime('%Y-%m-%dT%H:%M', p.collected_at)
        WHERE k.yes_bid_dollars IS NOT NULL
          AND k.yes_ask_dollars IS NOT NULL
          AND p.up_bid IS NOT NULL
          AND p.up_ask IS NOT NULL
        ORDER BY k.collected_at DESC
        LIMIT 2000
    """).fetchall()

    if not rows:
        return "### Kalshi vs Polymarket Spread Distribution\n_No matched rows (collectors may not be running simultaneously yet)._\n"

    spreads = [r[0] - r[1] for r in rows]
    n = len(spreads)
    s = sorted(spreads)
    mean   = statistics.mean(spreads)
    median = statistics.median(spreads)
    stdev  = statistics.stdev(spreads) if n > 1 else 0.0

    def pct(q): return s[int(n * q)]

    return (
        f"### Kalshi vs Polymarket Spread Distribution\n"
        f"- Sample (n): {n}\n"
        f"- Mean: {mean:+.4f}  |  Median: {median:+.4f}  |  Std: {stdev:.4f}\n"
        f"- Min: {min(spreads):+.4f}  |  Max: {max(spreads):+.4f}\n"
        f"- p10: {pct(0.10):+.4f}  p25: {pct(0.25):+.4f}  p75: {pct(0.75):+.4f}  p90: {pct(0.90):+.4f}\n"
    )


def momentum_convergence(conn):
    rows = conn.execute("""
        SELECT close_time, collected_at,
               (yes_bid_dollars + yes_ask_dollars) / 2.0 AS mid
        FROM markets
        WHERE close_time IS NOT NULL
          AND yes_bid_dollars IS NOT NULL
          AND yes_ask_dollars IS NOT NULL
        ORDER BY close_time, collected_at
    """).fetchall()

    if not rows:
        return "### Momentum Convergence\n_No data._\n"

    windows = defaultdict(list)
    for close_time, collected_at, mid in rows:
        windows[close_time].append((collected_at, mid))

    convergence_minutes = []
    total_windows = len(windows)
    for close_time, obs in windows.items():
        if len(obs) < 3:
            continue
        obs.sort(key=lambda x: x[0])
        first_ts = datetime.fromisoformat(obs[0][0])
        for i, (ts_str, mid) in enumerate(obs):
            ts = datetime.fromisoformat(ts_str)
            elapsed = (ts - first_ts).total_seconds() / 60
            # Converged = stays >=0.9 or <=0.1 from this point onward
            rest = [o[1] for o in obs[i:]]
            if all(r >= 0.90 or r <= 0.10 for r in rest):
                convergence_minutes.append(elapsed)
                break

    if not convergence_minutes:
        return (
            f"### Momentum Convergence\n"
            f"- Windows analyzed: {total_windows}\n"
            f"_No windows converged to 90%+ yet — need more data per window._\n"
        )

    avg = statistics.mean(convergence_minutes)
    med = statistics.median(convergence_minutes)
    mn  = min(convergence_minutes)
    mx  = max(convergence_minutes)

    return (
        f"### Momentum Convergence\n"
        f"- Windows analyzed: {total_windows}  |  Converged: {len(convergence_minutes)}\n"
        f"- Avg minutes to 90%+ lock: {avg:.1f}\n"
        f"- Median: {med:.1f}  |  Min: {mn:.1f}  |  Max: {mx:.1f}\n"
    )


def spread_efficiency(conn):
    rows = conn.execute("""
        SELECT yes_bid_dollars, yes_ask_dollars
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL
          AND yes_ask_dollars IS NOT NULL
        ORDER BY collected_at DESC
        LIMIT 2000
    """).fetchall()

    if not rows:
        return "### Spread Efficiency (Ask−Bid vs Probability)\n_No data._\n"

    buckets = {
        "0–10%":   [],
        "10–30%":  [],
        "30–50%":  [],
        "50–70%":  [],
        "70–90%":  [],
        "90–100%": [],
    }
    for bid, ask in rows:
        mid    = (bid + ask) / 2.0
        spread = ask - bid
        if   mid < 0.10: buckets["0–10%"].append(spread)
        elif mid < 0.30: buckets["10–30%"].append(spread)
        elif mid < 0.50: buckets["30–50%"].append(spread)
        elif mid < 0.70: buckets["50–70%"].append(spread)
        elif mid < 0.90: buckets["70–90%"].append(spread)
        else:            buckets["90–100%"].append(spread)

    lines = ["### Spread Efficiency (Ask−Bid vs Probability)"]
    for label, vals in buckets.items():
        if vals:
            lines.append(f"- {label}: avg {statistics.mean(vals):.4f}  (n={len(vals)})")
        else:
            lines.append(f"- {label}: no data")

    return "\n".join(lines) + "\n"


def run_analysis():
    os.makedirs(LOGS_DIR, exist_ok=True)
    conn = get_conn()
    ts   = datetime.now(timezone.utc).isoformat()

    report = (
        f"## Analysis — {ts}\n\n"
        + spread_distribution(conn) + "\n"
        + momentum_convergence(conn) + "\n"
        + spread_efficiency(conn)
        + "\n---\n"
    )
    conn.close()

    log_path = os.path.join(LOGS_DIR, "analysis.md")
    with open(log_path, "a") as f:
        f.write(report)

    print(f"[analyst] Report written → {log_path}")
    return report


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    print(f"[analyst] Running every {INTERVAL // 3600}h → {LOGS_DIR}/analysis.md")
    while True:
        try:
            run_analysis()
        except Exception as e:
            print(f"[analyst ERROR] {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    # Support --once flag for manual test runs
    import sys
    if "--once" in sys.argv:
        print(run_analysis())
    else:
        main()
