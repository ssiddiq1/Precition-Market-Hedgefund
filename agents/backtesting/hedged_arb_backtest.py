"""
hedged_arb_backtest.py — historical backtest for hedged_cross_arb.

Reads joint Kalshi / Polymarket ticks and simulates the hedged arb signal
with the same fee model used live, then persists the run to the
`strategy_backtests` table (strategy_name='hedged_cross_arb') so the
dashboard Arb tab can surface it alongside the other strategies.

Joins Kalshi and Polymarket ticks on close_time (exactly as the live signal
does).  Resolution ground truth comes from btc_labels_15m.direction_up at
the contract's close_time.

Known limitation (intentional, documented in output header):
  Polymarket DOWN-side data was captured from the very first collector run,
  so both Direction A and Direction B are simulated on the full history.
  (An earlier draft of this doc said DOWN data was missing — that turned
   out to be incorrect once we inspected the live table.)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sqlite3
import statistics
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional

import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _ROOT)
from agents.strategies.hedged_cross_arb import (  # noqa: E402
    DEFAULT_DOLLAR_SIZE_PER_LEG,
    DEFAULT_MIN_EDGE,
    MIN_SECONDS_TO_CLOSE,
    evaluate_arb,
)

BASE_DIR = _ROOT
DB_PATH  = os.path.join(_ROOT, "data", "btc15m.db")


# ── Data loading ───────────────────────────────────────────────────────────────

def _load_joint_ticks(db_path: str) -> list[dict]:
    """
    All joint Kalshi/Polymarket ticks, joined on close_time. One row per
    Kalshi tick whose close_time is also present in polymarket_markets; when
    multiple Polymarket ticks share a close_time we take the one closest in
    collected_at to the Kalshi tick (so the price pair is a realistic snapshot).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT k.collected_at   AS k_ts,
               k.ticker          AS kalshi_ticker,
               k.close_time      AS close_time,
               k.yes_bid_dollars AS yes_bid,
               k.yes_ask_dollars AS yes_ask,
               k.no_bid_dollars  AS no_bid,
               k.no_ask_dollars  AS no_ask,
               p.ticker          AS poly_ticker,
               p.up_bid          AS up_bid,
               p.up_ask          AS up_ask,
               p.down_bid        AS down_bid,
               p.down_ask        AS down_ask,
               p.collected_at    AS p_ts
        FROM markets k
        JOIN polymarket_markets p
          ON p.close_time = k.close_time
        WHERE k.yes_ask_dollars IS NOT NULL
          AND k.no_ask_dollars  IS NOT NULL
          AND p.up_ask          IS NOT NULL
          AND p.down_ask        IS NOT NULL
        ORDER BY k.collected_at ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _load_resolutions(db_path: str) -> dict[str, int]:
    """Map of close_time → direction_up from btc_labels_15m."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT timestamp, direction_up FROM btc_labels_15m "
        "WHERE direction_up IS NOT NULL"
    ).fetchall()
    conn.close()
    out: dict[str, int] = {}
    for ts, dir_up in rows:
        if not ts:
            continue
        out[ts] = int(dir_up)
        # Also index under minute-key for tz-formatting variance
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            out[dt.strftime("%Y-%m-%dT%H:%M")] = int(dir_up)
        except (ValueError, AttributeError):
            pass
    return out


def _resolve(
    close_time: str, resolutions: dict[str, int],
) -> Optional[int]:
    if close_time in resolutions:
        return resolutions[close_time]
    try:
        dt = datetime.fromisoformat(close_time.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return resolutions.get(dt.strftime("%Y-%m-%dT%H:%M"))


def _seconds_to_close(collected_at: str, close_time: str) -> float:
    """TTL used by the live 90s guard."""
    try:
        now = datetime.fromisoformat(collected_at.replace("Z", "+00:00"))
        ct  = datetime.fromisoformat(close_time.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return -1.0
    return (ct - now).total_seconds()


# ── Backtest core ──────────────────────────────────────────────────────────────

def run_backtest(
    db_path: str = DB_PATH,
    min_edge: float = DEFAULT_MIN_EDGE,
    dollar_size_per_leg: float = DEFAULT_DOLLAR_SIZE_PER_LEG,
    persist: bool = True,
) -> dict:
    """
    Walk joint ticks in time order. For each tick, evaluate the signal. If
    it's tradeable (edge ≥ min_edge AND TTL ≥ 90s AND no other open trade
    for this close_time yet), open a paper trade; resolve it when the
    ground-truth direction_up is available.

    Returns a result dict with opportunity/capture/PnL/Sharpe/drawdown.
    """
    ticks = _load_joint_ticks(db_path)
    resolutions = _load_resolutions(db_path)

    # Per-window state: we only open one arb per close_time to match live
    # behavior. Once a trade is opened for a window, further opportunities
    # are counted but not retraded.
    opened_for_window: dict[str, dict] = {}
    opportunities_any: int = 0         # any tick with net_edge ≥ min_edge
    tradeable: int        = 0          # opportunity whose tick passed the TTL guard
    trades: list[dict]    = []         # actually opened
    edge_distribution: list[float] = []
    positive_net_edge_ticks = 0

    for t in ticks:
        sig = evaluate_arb(
            kalshi_yes_ask=t["yes_ask"],
            kalshi_no_ask=t["no_ask"],
            poly_up_ask=t["up_ask"],
            poly_down_ask=t["down_ask"],
            min_edge=0.0,                    # count all positive-edge ticks for the distribution
            dollar_size_per_leg=dollar_size_per_leg,
        )
        if sig is None:
            continue

        edge_distribution.append(sig.net_edge)
        if sig.net_edge > 0:
            positive_net_edge_ticks += 1

        if sig.net_edge < min_edge:
            continue
        opportunities_any += 1

        ttl = _seconds_to_close(t["k_ts"], t["close_time"])
        if ttl < MIN_SECONDS_TO_CLOSE:
            continue
        tradeable += 1

        # One trade per close_time
        if t["close_time"] in opened_for_window:
            continue

        trade = {
            "opened_at":         t["k_ts"],
            "close_time":        t["close_time"],
            "direction":         sig.direction,
            "kalshi_side":       sig.kalshi_side,
            "kalshi_entry":      sig.kalshi_price,
            "kalshi_contracts":  sig.contracts,
            "poly_side":         sig.poly_side,
            "poly_entry":        sig.poly_price,
            "poly_contracts":    sig.contracts,
            "gross_edge":        sig.gross_edge,
            "net_edge":          sig.net_edge,
            "fees":              sig.fees["total"],
            "locked_pnl":        sig.locked_pnl,
            "ttl_at_entry":      ttl,
        }
        opened_for_window[t["close_time"]] = trade
        trades.append(trade)

    # Resolve
    resolved_trades = []
    unresolved = 0
    for tr in trades:
        dir_up = _resolve(tr["close_time"], resolutions)
        if dir_up is None:
            unresolved += 1
            tr["realized_pnl"] = None
            continue

        c = tr["kalshi_contracts"]
        kalshi_payout = c if (
            (tr["kalshi_side"] == "YES" and dir_up == 1) or
            (tr["kalshi_side"] == "NO"  and dir_up == 0)
        ) else 0
        poly_payout = c if (
            (tr["poly_side"] == "UP"   and dir_up == 1) or
            (tr["poly_side"] == "DOWN" and dir_up == 0)
        ) else 0

        cost  = (tr["kalshi_entry"] + tr["poly_entry"]) * c
        gross = (kalshi_payout + poly_payout) - cost
        realized = gross - tr["fees"]
        tr["realized_pnl"] = round(realized, 4)
        tr["direction_up"] = dir_up
        resolved_trades.append(tr)

    # Aggregate metrics
    realised_pnls = [tr["realized_pnl"] for tr in resolved_trades]
    locked_pnls   = [tr["locked_pnl"]   for tr in trades]
    gross_pnl_total = round(sum(locked_pnls), 4)
    net_pnl_total   = round(sum(realised_pnls), 4) if realised_pnls else 0.0

    sharpe = 0.0
    if len(realised_pnls) >= 2:
        mu = statistics.mean(realised_pnls)
        sd = statistics.pstdev(realised_pnls)
        if sd > 0:
            # Per-trade Sharpe × sqrt(trades-per-year) if we treat each 15m
            # window as an observation:  365 × 24 × 4 = 35,040 windows/year.
            sharpe = mu / sd * math.sqrt(35_040)

    # Equity curve + drawdown
    equity = 0.0
    peak   = 0.0
    mdd    = 0.0
    equity_curve: list[float] = []
    for tr in resolved_trades:
        equity += tr["realized_pnl"]
        equity_curve.append(round(equity, 4))
        peak = max(peak, equity)
        if peak > 0:
            mdd = max(mdd, peak - equity)

    # Edge distribution → 0.5¢ buckets over [−5¢, +15¢]
    hist: dict[str, int] = {}
    for e in edge_distribution:
        bucket = round(math.floor(e * 200) / 200.0 + 0.0025, 4)  # 0.005-wide, centered
        key = f"{bucket:+.4f}"
        hist[key] = hist.get(key, 0) + 1

    result = {
        "strategy":          "hedged_cross_arb",
        "config": {
            "min_edge":              min_edge,
            "dollar_size_per_leg":   dollar_size_per_leg,
            "min_seconds_to_close":  MIN_SECONDS_TO_CLOSE,
        },
        "joint_windows_total":   len({t["close_time"] for t in ticks}),
        "joint_ticks_total":     len(ticks),
        "ticks_with_any_positive_net_edge": positive_net_edge_ticks,
        "opportunities_detected":      opportunities_any,
        "tradeable_after_ttl_guard":   tradeable,
        "capture_rate":                (
            round(tradeable / opportunities_any, 4) if opportunities_any else None
        ),
        "trades_opened":             len(trades),
        "trades_resolved":           len(resolved_trades),
        "trades_unresolved":         unresolved,
        "gross_pnl_locked":          gross_pnl_total,
        "net_pnl_realized":          net_pnl_total,
        "sharpe_per_trade_annualised": round(sharpe, 4),
        "max_drawdown_dollars":      round(mdd, 4),
        "equity_curve":              equity_curve,
        "edge_histogram":            hist,
        "trades":                    trades,
        "run_at":                    datetime.now(timezone.utc).isoformat(),
    }

    if persist:
        _persist_to_strategy_backtests(db_path, result)
    return result


def _persist_to_strategy_backtests(db_path: str, result: dict) -> int:
    """
    Write the run to the strategy_backtests table so the dashboard Arb
    tab can pick it up alongside other backtests.
    """
    conn = sqlite3.connect(db_path)
    metrics = {k: v for k, v in result.items() if k not in ("trades", "equity_curve", "edge_histogram", "config")}
    start_ts = result["trades"][0]["opened_at"]     if result["trades"] else None
    end_ts   = result["trades"][-1]["opened_at"]    if result["trades"] else None
    cur = conn.execute(
        """INSERT INTO strategy_backtests
             (run_id, strategy_name, backtest_type, config_json, metrics_json,
              trade_count, start_timestamp, end_timestamp, created_at)
           VALUES (NULL, ?, 'historical_walk', ?, ?, ?, ?, ?, ?)""",
        (
            "hedged_cross_arb",
            json.dumps(result["config"], sort_keys=True),
            json.dumps(metrics,          sort_keys=True),
            result["trades_opened"],
            start_ts,
            end_ts,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    backtest_id = cur.lastrowid
    conn.commit()
    conn.close()
    return backtest_id


# ── CLI ────────────────────────────────────────────────────────────────────────

def _fmt_money(x: float) -> str:
    sign = "-" if x < 0 else "+"
    return f"{sign}${abs(x):,.2f}"


def _print_report(result: dict) -> None:
    cfg = result["config"]
    print("\n" + "─" * 70)
    print("  HEDGED CROSS-EXCHANGE ARB — Historical Backtest")
    print("─" * 70)
    print(f"  Note: Polymarket DOWN-side data was present from collector")
    print(f"        start; both Direction A and Direction B are backtested.")
    print("─" * 70)
    print(f"  min_edge                     {cfg['min_edge']*100:.2f} ¢")
    print(f"  dollar_size_per_leg          ${cfg['dollar_size_per_leg']:,.0f}")
    print(f"  min_seconds_to_close (guard) {cfg['min_seconds_to_close']}s")
    print("─" * 70)
    print(f"  Joint windows                {result['joint_windows_total']:,}")
    print(f"  Joint ticks                  {result['joint_ticks_total']:,}")
    print(f"  Ticks with positive edge     {result['ticks_with_any_positive_net_edge']:,}")
    if result["joint_ticks_total"] > 0:
        pct = result["ticks_with_any_positive_net_edge"] / result["joint_ticks_total"] * 100
        print(f"    pct positive-edge          {pct:.2f}%")
    print(f"  Opportunities (≥ min_edge)   {result['opportunities_detected']:,}")
    print(f"  Tradeable after 90s guard    {result['tradeable_after_ttl_guard']:,}")
    if result["capture_rate"] is not None:
        print(f"    capture rate               {result['capture_rate']*100:.2f}%")
    print(f"  Trades opened                {result['trades_opened']:,}")
    print(f"  Trades resolved              {result['trades_resolved']:,}")
    print(f"  Trades unresolved            {result['trades_unresolved']:,}")
    print("─" * 70)
    print(f"  Gross PnL (locked)           {_fmt_money(result['gross_pnl_locked'])}")
    print(f"  Net PnL  (realised)          {_fmt_money(result['net_pnl_realized'])}")
    print(f"  Max drawdown                 {_fmt_money(-result['max_drawdown_dollars'])}")
    print(f"  Sharpe (annualised per-trade) {result['sharpe_per_trade_annualised']:.3f}")
    print("─" * 70 + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Historical backtest for hedged_cross_arb")
    ap.add_argument("--min-edge",    type=float, default=DEFAULT_MIN_EDGE)
    ap.add_argument("--dollar-size", type=float, default=DEFAULT_DOLLAR_SIZE_PER_LEG)
    ap.add_argument("--db-path",     type=str,   default=DB_PATH)
    ap.add_argument("--no-persist",  action="store_true")
    args = ap.parse_args()

    result = run_backtest(
        db_path=args.db_path,
        min_edge=args.min_edge,
        dollar_size_per_leg=args.dollar_size,
        persist=not args.no_persist,
    )
    _print_report(result)
