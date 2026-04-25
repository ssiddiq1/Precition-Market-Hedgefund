"""
strategy_engine.py — live signal strategies for quant-os

Strategies:
  1. spread_arb()     — cross-exchange mid-price spread arbitrage (DEPRECATED,
                        kept for historical comparison — superseded by
                        hedged_cross_arb.py which captures the full edge
                        with a riskless hedge across both venues).
  2. momentum_fade()  — fade a sharp 4-tick move on Polymarket.

Each strategy returns:
  {
    "strategy":    str,
    "direction":   "YES" | "NO" | "FLAT",
    "confidence":  float 0-1,
    "entry_price": float | None,
    "rationale":   str,
    "timestamp":   ISO UTC str,
  }
"""

import logging
import os
import sqlite3
from datetime import datetime, timezone

log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH  = os.path.join(BASE_DIR, "data", "btc15m.db")


class StrategyEngine:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _now_iso(self) -> str:
        return self._now().isoformat()

    def _current_window(self, conn: sqlite3.Connection) -> str | None:
        """Return the close_time of the most recent window in the markets table."""
        row = conn.execute("""
            SELECT close_time FROM markets
            WHERE close_time IS NOT NULL
            ORDER BY close_time DESC LIMIT 1
        """).fetchone()
        return row["close_time"] if row else None

    def _flat(self, strategy: str, rationale: str) -> dict:
        return {
            "strategy":    strategy,
            "direction":   "FLAT",
            "confidence":  0.0,
            "entry_price": None,
            "rationale":   rationale,
            "timestamp":   self._now_iso(),
        }

    # ── Strategy 1: Spread Arb ─────────────────────────────────────────────────

    def spread_arb(self) -> dict:
        """
        Join both tables on close_time for the current open window.
        Compute mid-prices on each side. If |kalshi_mid - poly_mid| > 0.03,
        signal BUY the cheaper side.
        Confidence = min(|spread| / 0.10, 1.0).
        """
        STRATEGY   = "spread_arb"
        MIN_SPREAD = 0.03

        conn = self._connect()
        try:
            close_time = self._current_window(conn)
            if not close_time:
                return self._flat(STRATEGY, "No active window found in markets table.")

            k = conn.execute("""
                SELECT yes_bid_dollars, yes_ask_dollars, collected_at
                FROM markets
                WHERE close_time = ? AND yes_bid_dollars IS NOT NULL
                ORDER BY collected_at DESC LIMIT 1
            """, (close_time,)).fetchone()

            p = conn.execute("""
                SELECT up_bid, up_ask, collected_at
                FROM polymarket_markets
                WHERE close_time = ? AND up_bid IS NOT NULL
                ORDER BY collected_at DESC LIMIT 1
            """, (close_time,)).fetchone()

            if not k:
                return self._flat(STRATEGY, f"No Kalshi rows for window {close_time}.")
            if not p:
                return self._flat(STRATEGY, f"No Polymarket rows for window {close_time}.")

            kalshi_mid = (k["yes_bid_dollars"] + k["yes_ask_dollars"]) / 2.0
            poly_mid   = (p["up_bid"] + p["up_ask"]) / 2.0
            spread     = kalshi_mid - poly_mid  # positive = Kalshi premium

            if abs(spread) <= MIN_SPREAD:
                return self._flat(
                    STRATEGY,
                    f"Spread {spread:+.4f} ≤ threshold ±{MIN_SPREAD}. "
                    f"kalshi_mid={kalshi_mid:.4f}, poly_mid={poly_mid:.4f}. No edge."
                )

            confidence = round(min(abs(spread) / 0.10, 1.0), 4)

            if spread > 0:
                # Kalshi is expensive → buy the cheaper Polymarket UP side
                direction   = "YES"
                entry_price = round(p["up_ask"], 4)
                rationale   = (
                    f"Kalshi premium: kalshi_mid={kalshi_mid:.4f} vs "
                    f"poly_mid={poly_mid:.4f} (spread={spread:+.4f}). "
                    f"Buy cheaper side: Polymarket UP at {entry_price:.4f}."
                )
            else:
                # Polymarket is expensive → buy the cheaper Kalshi YES side
                direction   = "YES"
                entry_price = round(k["yes_ask_dollars"], 4)
                rationale   = (
                    f"Polymarket premium: poly_mid={poly_mid:.4f} vs "
                    f"kalshi_mid={kalshi_mid:.4f} (spread={spread:+.4f}). "
                    f"Buy cheaper side: Kalshi YES at {entry_price:.4f}."
                )

            return {
                "strategy":    STRATEGY,
                "direction":   direction,
                "confidence":  confidence,
                "entry_price": entry_price,
                "rationale":   rationale,
                "timestamp":   self._now_iso(),
            }

        finally:
            conn.close()

    # ── Strategy 2: Momentum Fade ──────────────────────────────────────────────

    def momentum_fade(self) -> dict:
        """
        Last 4 rows of polymarket_markets for the current window.
        If up_bid moved > 0.08 in one direction across those 4 ticks, fade it.
        Confidence = min(|delta| / 0.15, 1.0).
        """
        STRATEGY  = "momentum_fade"
        MIN_DELTA = 0.08

        conn = self._connect()
        try:
            close_time = self._current_window(conn)
            if not close_time:
                return self._flat(STRATEGY, "No active window found.")

            rows = conn.execute("""
                SELECT up_bid, up_ask, down_bid, down_ask, collected_at
                FROM polymarket_markets
                WHERE close_time = ? AND up_bid IS NOT NULL
                ORDER BY collected_at ASC
            """, (close_time,)).fetchall()

            if len(rows) < 4:
                return self._flat(
                    STRATEGY,
                    f"Only {len(rows)} Polymarket ticks for window {close_time} "
                    f"(need ≥ 4)."
                )

            last4        = rows[-4:]
            first_up_bid = last4[0]["up_bid"]
            last_up_bid  = last4[-1]["up_bid"]
            delta        = last_up_bid - first_up_bid  # positive = price moved UP

            if abs(delta) <= MIN_DELTA:
                return self._flat(
                    STRATEGY,
                    f"Momentum delta {delta:+.4f} ≤ threshold ±{MIN_DELTA}. "
                    f"up_bid: {first_up_bid:.4f} → {last_up_bid:.4f}. No fade signal."
                )

            confidence = round(min(abs(delta) / 0.15, 1.0), 4)

            if delta > 0:
                # Price surged UP over 4 ticks → fade it → signal NO
                direction   = "NO"
                entry_price = round(last4[-1]["down_bid"], 4)
                rationale   = (
                    f"Polymarket UP bid surged {first_up_bid:.4f} → {last_up_bid:.4f} "
                    f"(Δ={delta:+.4f}) over last 4 ticks. "
                    f"Fading momentum — signal NO (DOWN). Entry at down_bid={entry_price:.4f}."
                )
            else:
                # Price fell DOWN over 4 ticks → fade it → signal YES
                direction   = "YES"
                entry_price = round(last4[-1]["up_ask"], 4)
                rationale   = (
                    f"Polymarket UP bid dropped {first_up_bid:.4f} → {last_up_bid:.4f} "
                    f"(Δ={delta:+.4f}) over last 4 ticks. "
                    f"Fading momentum — signal YES (UP). Entry at up_ask={entry_price:.4f}."
                )

            return {
                "strategy":    STRATEGY,
                "direction":   direction,
                "confidence":  confidence,
                "entry_price": entry_price,
                "rationale":   rationale,
                "timestamp":   self._now_iso(),
            }

        finally:
            conn.close()

    # ── Aggregate ──────────────────────────────────────────────────────────────

    def get_signals(self) -> list[dict]:
        """Run all strategies and return their signals. Each failure is caught
        individually so one bad strategy never blocks the others."""
        results = []
        for strategy_fn in (
            self.spread_arb,
            self.momentum_fade,
        ):
            try:
                results.append(strategy_fn())
            except Exception as exc:
                results.append({
                    "strategy":    strategy_fn.__name__,
                    "direction":   "FLAT",
                    "confidence":  0.0,
                    "entry_price": None,
                    "rationale":   f"Unhandled error: {exc}",
                    "timestamp":   self._now_iso(),
                })
        return results


# ── CLI smoke-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine  = StrategyEngine()
    signals = engine.get_signals()

    DIR_COLOR = {"YES": "\033[32m", "NO": "\033[31m", "FLAT": "\033[90m"}
    RESET     = "\033[0m"

    print(f"\n{'─'*60}")
    print(f"  QUANT OS — Strategy Signals  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"{'─'*60}")

    for s in signals:
        col  = DIR_COLOR.get(s["direction"], "")
        bar  = "█" * int(s["confidence"] * 20)
        pad  = "░" * (20 - len(bar))
        conf = f"{s['confidence']:.2f}"

        print(f"\n  [{s['strategy']}]")
        print(f"  direction  : {col}{s['direction']}{RESET}")
        print(f"  confidence : {conf}  {col}{bar}{RESET}{pad}")
        print(f"  entry_price: {s['entry_price']}")
        print(f"  rationale  : {s['rationale']}")

    print(f"\n{'─'*60}\n")
