"""
backtest_momentum.py — backtest the 8-minute momentum lock-in strategy

Logic:
  For each resolved 15-min window in btc15m.db with >= 5 ticks:
    1. Observe first tick: if yes_mid > 0.5 → bet YES; else bet NO
    2. Entry price = ask at first tick
    3. At the tick closest to 8 minutes elapsed:
         - Exit if condition met (YES bet: mid > 0.70 / NO bet: mid < 0.30)
         - Otherwise hold
    4. Final exit = last observed tick bid price
    5. PnL per contract = exit_price - entry_price  (contracts pay $1 at resolution)

Saves results to: logs/backlog_momentum_backtest.md
"""

import os
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH     = os.path.join(BASE_DIR, "data", "btc15m.db")
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
CHARTS_DIR  = os.path.join(LOGS_DIR, "charts")
OUT_PATH    = os.path.join(LOGS_DIR, "backlog_momentum_backtest.md")

DARK = {
    "figure.facecolor": "#0d0d0d", "axes.facecolor": "#141414",
    "axes.edgecolor": "#333", "axes.labelcolor": "#888",
    "xtick.color": "#555", "ytick.color": "#555",
    "grid.color": "#1e1e1e", "text.color": "#e0e0e0",
}

EXIT_MIN      = 8     # target exit minute
ENTRY_THRESH  = 0.50  # enter if |mid - 0.5| > 0 (any directional signal)
EXIT_THRESH   = 0.70  # early exit if conviction reaches 70% in our direction


def load_windows():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT close_time, collected_at,
               yes_bid_dollars, yes_ask_dollars,
               no_bid_dollars,  no_ask_dollars,
               last_price_dollars
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL
          AND yes_ask_dollars IS NOT NULL
          AND close_time IS NOT NULL
        ORDER BY close_time, collected_at ASC
    """).fetchall()
    conn.close()

    windows = defaultdict(list)
    for ct, ts, y_bid, y_ask, n_bid, n_ask, last in rows:
        windows[ct].append({
            "ts":    ts,
            "y_bid": y_bid, "y_ask": y_ask,
            "n_bid": n_bid, "n_ask": n_ask,
            "mid":   (y_bid + y_ask) / 2.0,
            "last":  last,
        })
    return windows


def simulate_window(close_time, ticks):
    """Simulate one trade on a single window. Returns trade dict or None."""
    if len(ticks) < 5:
        return None

    first = ticks[0]
    t0    = datetime.fromisoformat(first["ts"])

    # Determine direction
    direction = "YES" if first["mid"] >= 0.5 else "NO"
    entry_price = first["y_ask"] if direction == "YES" else first["n_ask"]

    # Find tick at ~EXIT_MIN minutes
    exit_tick  = None
    exit_type  = "hold_to_close"
    for tick in ticks[1:]:
        elapsed = (datetime.fromisoformat(tick["ts"]) - t0).total_seconds() / 60
        if elapsed >= EXIT_MIN and exit_tick is None:
            exit_tick = tick
            # Check exit condition
            if direction == "YES" and tick["mid"] > EXIT_THRESH:
                exit_type = "early_exit"
            elif direction == "NO" and tick["mid"] < (1 - EXIT_THRESH):
                exit_type = "early_exit"
            break

    # If no tick at minute 8, use last tick
    if exit_tick is None:
        exit_tick = ticks[-1]
        elapsed_at_exit = (datetime.fromisoformat(exit_tick["ts"]) - t0).total_seconds() / 60
        exit_type = f"last_tick ({elapsed_at_exit:.1f}min)"

    # Exit price = bid at exit tick
    exit_price = exit_tick["y_bid"] if direction == "YES" else exit_tick["n_bid"]

    # PnL: exit price minus entry price (both normalized 0-1)
    pnl = exit_price - entry_price

    # Estimate resolution: last tick price as proxy
    last_mid = ticks[-1]["mid"]
    resolved_yes = last_mid > 0.5
    won = (direction == "YES" and resolved_yes) or (direction == "NO" and not resolved_yes)

    return {
        "close_time":    close_time,
        "ticks":         len(ticks),
        "direction":     direction,
        "entry_price":   round(entry_price, 4),
        "exit_price":    round(exit_price,  4),
        "exit_type":     exit_type,
        "pnl":           round(pnl, 4),
        "last_mid":      round(last_mid, 4),
        "won":           won,
    }


def run_backtest():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    windows = load_windows()
    ts_run  = datetime.now(timezone.utc).isoformat()

    trades = []
    skipped = 0
    for close_time, ticks in sorted(windows.items()):
        result = simulate_window(close_time, ticks)
        if result:
            trades.append(result)
        else:
            skipped += 1

    if not trades:
        print("[backtest] No trades simulated — need more data.")
        return

    pnls       = [t["pnl"]  for t in trades]
    wins       = [t for t in trades if t["won"]]
    total_pnl  = sum(pnls)
    win_rate   = len(wins) / len(trades)
    avg_pnl    = total_pnl / len(trades)
    best_trade = max(trades, key=lambda t: t["pnl"])
    worst_trade= min(trades, key=lambda t: t["pnl"])

    early_exits = [t for t in trades if t["exit_type"] == "early_exit"]
    hold_trades = [t for t in trades if t["exit_type"] != "early_exit"]

    # ── Chart: cumulative PnL ──
    cum_pnl = list(np.cumsum(pnls))
    colors  = ["#00ff88" if p >= 0 else "#ff6b6b" for p in pnls]

    with plt.rc_context(DARK):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))

        # Cumulative PnL
        ax1.plot(cum_pnl, color="#00ccff", lw=1.5)
        ax1.axhline(0, color="#333", lw=0.8)
        ax1.fill_between(range(len(cum_pnl)), 0, cum_pnl,
                         where=[v >= 0 for v in cum_pnl], alpha=0.15, color="#00ff88")
        ax1.fill_between(range(len(cum_pnl)), 0, cum_pnl,
                         where=[v < 0 for v in cum_pnl], alpha=0.15, color="#ff6b6b")
        ax1.set_title("Cumulative PnL per Contract ($)", color="#e0e0e0", pad=10)
        ax1.set_xlabel("Trade #")
        ax1.set_ylabel("Cumulative PnL ($)")
        ax1.grid(True, linestyle="--", alpha=0.3)

        # Per-trade PnL bar
        ax2.bar(range(len(pnls)), pnls, color=colors, alpha=0.7)
        ax2.axhline(0, color="#333", lw=0.8)
        ax2.set_title("Per-Trade PnL ($)", color="#e0e0e0", pad=10)
        ax2.set_xlabel("Trade #")
        ax2.set_ylabel("PnL ($)")
        ax2.grid(True, linestyle="--", alpha=0.3)

        fig.tight_layout()

    ts_tag   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    chart_path = os.path.join(CHARTS_DIR, f"{ts_tag}_momentum_backtest.png")
    fig.savefig(chart_path, dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)

    # ── Compose report ──
    trade_rows = "\n".join(
        f"| {t['close_time'][:16]} | {t['ticks']} | {t['direction']} "
        f"| {t['entry_price']:.4f} | {t['exit_price']:.4f} | {t['exit_type']} "
        f"| **{t['pnl']:+.4f}** | {'✓' if t['won'] else '✗'} |"
        for t in trades
    )

    report = f"""# Momentum Backtest — 8-Minute Lock-In Strategy

**Run at:** {ts_run}
**Strategy:** Enter at window open if mid ≠ 0.50; exit at minute {EXIT_MIN} if conviction >{EXIT_THRESH:.0%}; else hold to close.
**Data:** {len(windows)} windows loaded, {len(trades)} simulated, {skipped} skipped (<5 ticks).

---

## Summary

| Metric | Value |
|---|---|
| Trades simulated | {len(trades)} |
| Win rate (by market direction) | {win_rate:.1%} |
| Total PnL | ${total_pnl:+.4f} |
| Avg PnL per trade | ${avg_pnl:+.4f} |
| Early exits (conviction >{EXIT_THRESH:.0%}) | {len(early_exits)} |
| Held to close | {len(hold_trades)} |
| Best trade | ${best_trade['pnl']:+.4f} ({best_trade['close_time'][:16]}) |
| Worst trade | ${worst_trade['pnl']:+.4f} ({worst_trade['close_time'][:16]}) |

**Chart:** `{os.path.basename(chart_path)}`

---

## Trade Log

| Window Close | Ticks | Dir | Entry | Exit | Exit Type | PnL | Won |
|---|---|---|---|---|---|---|---|
{trade_rows}

---

## Interpretation

- **Win rate {win_rate:.1%}** reflects how often the market moved in the predicted direction by exit time.
- **Avg PnL {avg_pnl:+.4f}** per contract means {'positive edge — strategy earns on average' if avg_pnl > 0 else 'negative edge at current data size — likely noise with n={}'.format(len(trades))}.
- Early exits fired {len(early_exits)} time(s) — high conviction moves {'exist in data' if early_exits else 'not yet seen'}.
- **Caveat:** {len(trades)} trades is a very small sample. Results are directional only; rerun when 50+ windows are available.

---

## Risks & Limitations

- Entry/exit uses mid-price as proxy; real fills would pay ask on entry and receive bid on exit (spread cost already included in entry_price/exit_price above).
- We cannot confirm true resolution from market data alone — `last_mid` is used as a proxy for outcome.
- No transaction fees, slippage, or position sizing applied.
- Time resolution is 60s — "minute 8" may land on tick 7 or 9 in practice.
"""

    with open(OUT_PATH, "w") as f:
        f.write(report)

    print(f"[backtest] {len(trades)} trades simulated → {OUT_PATH}")
    print(f"[backtest] Chart → {chart_path}")
    print(f"[backtest] Win rate: {win_rate:.1%}  |  Total PnL: ${total_pnl:+.4f}  |  Avg: ${avg_pnl:+.4f}")
    return report


if __name__ == "__main__":
    run_backtest()
