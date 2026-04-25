"""
Hedged cross-exchange arbitrage between Kalshi KXBTC15M and Polymarket
btc-updown-15m contracts. Simultaneously takes opposite sides of the
same underlying event across the two venues when YES_cheap + NO_expensive
+ fees < $1.00, locking in riskless profit.

Math (read carefully):
    YES_payout + NO_payout = $1 at resolution by construction.
    If we pay  p_yes + p_no + fees < 1.00,
    we lock in 1.00 − (p_yes + p_no) − fees per contract pair.
    No direction risk, no vol assumption, no model risk.

Both venues trade BTC up/down for the same 15-minute window, so:
    Kalshi YES = Polymarket UP = BTC closes higher
    Kalshi NO  = Polymarket DOWN = BTC closes flat or lower

Two legal directions:
    A. Buy Kalshi YES + Buy Polymarket DOWN
    B. Buy Polymarket UP + Buy Kalshi NO

Execution is stubbed (paper-trade only) until explicitly flipped live.
"""

from __future__ import annotations

import logging
import math
import os
import re
import sqlite3
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH  = os.path.join(BASE_DIR, "data", "btc15m.db")

# ── Fee model ──────────────────────────────────────────────────────────────────
KALSHI_FEE_RATE    = 0.07        # 0.07 × price × (1 − price) per contract per side
POLYMARKET_FEE     = 0.0         # Polymarket fees are baked into the spread
POLYGON_GAS_USD    = 0.002       # ≈ $0.002 per on-chain tx (approx, treated constant)

# ── Trade sizing and risk ──────────────────────────────────────────────────────
DEFAULT_DOLLAR_SIZE_PER_LEG = 500.0   # target $ per leg
DEFAULT_MIN_EDGE            = 0.01    # trigger when net edge ≥ 1¢
MIN_SECONDS_TO_CLOSE        = 90      # don't open a new arb inside the last 90s


# ══════════════════════════════════════════════════════════════════════════════
# Fee math
# ══════════════════════════════════════════════════════════════════════════════

def _kalshi_fee(price: float, contracts: int) -> float:
    """Kalshi takes 7% of a symmetric per-contract fee, quadratic around 0.5."""
    if price <= 0 or price >= 1:
        return 0.0
    return KALSHI_FEE_RATE * price * (1.0 - price) * contracts


def compute_total_fees(
    kalshi_price: float,
    poly_price: float,
    contracts: int,
) -> dict:
    """
    Return the total fees for a one-pair hedge at the two prices.

    kalshi_price is whichever Kalshi side we bought (YES or NO).
    poly_price   is whichever Polymarket side we bought (UP or DOWN).

    Gas is one tx per Polymarket leg (Kalshi doesn't need gas).
    Kalshi: 7% × p × (1−p) per contract per side.
    Polymarket: zero explicit fee.
    """
    kfee = _kalshi_fee(kalshi_price, contracts)
    pfee = POLYMARKET_FEE * contracts
    gas  = POLYGON_GAS_USD                      # one Polymarket tx per leg-pair
    return {
        "kalshi_fee":     round(kfee, 6),
        "poly_fee":       round(pfee, 6),
        "gas_usd":        round(gas, 6),
        "total":          round(kfee + pfee + gas, 6),
    }


# ══════════════════════════════════════════════════════════════════════════════
# Signal evaluator (stateless; reused by backtest)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ArbSignal:
    direction: str             # "A" or "B"
    kalshi_side: str           # "YES" or "NO"
    kalshi_price: float
    poly_side: str             # "UP" or "DOWN"
    poly_price: float
    contracts: int
    dollar_size_per_leg: float
    gross_edge: float          # 1.00 − (p_a + p_b), before fees
    fees: dict
    net_edge: float            # gross_edge − fees.total / contracts
    locked_pnl: float          # net_edge × contracts (dollars)


def evaluate_arb(
    kalshi_yes_ask: Optional[float],
    kalshi_no_ask:  Optional[float],
    poly_up_ask:    Optional[float],
    poly_down_ask:  Optional[float],
    min_edge:       float = DEFAULT_MIN_EDGE,
    dollar_size_per_leg: float = DEFAULT_DOLLAR_SIZE_PER_LEG,
) -> Optional[ArbSignal]:
    """
    Evaluate both hedge directions at the latest prices and return the larger
    net-edge signal if it clears `min_edge`, else None.
    """
    candidates: list[ArbSignal] = []

    # Direction A: buy Kalshi YES at kalshi_yes_ask, buy Polymarket DOWN at down_ask
    if kalshi_yes_ask is not None and poly_down_ask is not None \
       and 0 < kalshi_yes_ask < 1 and 0 < poly_down_ask < 1:
        gross = 1.0 - kalshi_yes_ask - poly_down_ask
        if gross > 0:
            # Size each leg independently, then take the min so both fill equally
            c_k = int(math.floor(dollar_size_per_leg / kalshi_yes_ask))
            c_p = int(math.floor(dollar_size_per_leg / poly_down_ask))
            contracts = min(c_k, c_p)
            if contracts > 0:
                fees  = compute_total_fees(kalshi_yes_ask, poly_down_ask, contracts)
                net   = gross - (fees["total"] / contracts)
                if net >= min_edge:
                    candidates.append(ArbSignal(
                        direction="A",
                        kalshi_side="YES",    kalshi_price=kalshi_yes_ask,
                        poly_side="DOWN",     poly_price=poly_down_ask,
                        contracts=contracts,  dollar_size_per_leg=dollar_size_per_leg,
                        gross_edge=gross,     fees=fees,
                        net_edge=net,         locked_pnl=net * contracts,
                    ))

    # Direction B: buy Polymarket UP at up_ask, buy Kalshi NO at no_ask
    if poly_up_ask is not None and kalshi_no_ask is not None \
       and 0 < poly_up_ask < 1 and 0 < kalshi_no_ask < 1:
        gross = 1.0 - poly_up_ask - kalshi_no_ask
        if gross > 0:
            c_p = int(math.floor(dollar_size_per_leg / poly_up_ask))
            c_k = int(math.floor(dollar_size_per_leg / kalshi_no_ask))
            contracts = min(c_k, c_p)
            if contracts > 0:
                fees  = compute_total_fees(kalshi_no_ask, poly_up_ask, contracts)
                net   = gross - (fees["total"] / contracts)
                if net >= min_edge:
                    candidates.append(ArbSignal(
                        direction="B",
                        kalshi_side="NO",     kalshi_price=kalshi_no_ask,
                        poly_side="UP",       poly_price=poly_up_ask,
                        contracts=contracts,  dollar_size_per_leg=dollar_size_per_leg,
                        gross_edge=gross,     fees=fees,
                        net_edge=net,         locked_pnl=net * contracts,
                    ))

    if not candidates:
        return None
    return max(candidates, key=lambda s: s.net_edge)


# ══════════════════════════════════════════════════════════════════════════════
# Live execution stubs
# ══════════════════════════════════════════════════════════════════════════════

def execute_kalshi_order(side: str, price: float, contracts: int) -> dict:
    raise NotImplementedError(
        "Live execution requires Kalshi-python auth + signed API requests. "
        "See TODO in hedged_cross_arb.py."
    )


def execute_polymarket_order(side: str, price: float, contracts: int) -> dict:
    raise NotImplementedError(
        "Live execution requires Polymarket CLOB client + wallet signature. "
        "See TODO in hedged_cross_arb.py."
    )


# ══════════════════════════════════════════════════════════════════════════════
# Paper-trade engine (live tick loop + resolution)
# ══════════════════════════════════════════════════════════════════════════════

def _parse_close_time(s: str | None) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


class HedgedArbTrader:
    """
    Paper-trader for the hedged cross-exchange arb. Reads the latest joint
    tick each .tick(), evaluates evaluate_arb(), and opens a paper trade if
    the edge clears min_edge and there's at least MIN_SECONDS_TO_CLOSE left
    in the window. Resolves past trades against btc_labels_15m.direction_up
    at the target close time.
    """

    def __init__(
        self,
        db_path: str = DB_PATH,
        min_edge: float = DEFAULT_MIN_EDGE,
        dollar_size_per_leg: float = DEFAULT_DOLLAR_SIZE_PER_LEG,
    ):
        self.db_path = db_path
        self.min_edge = min_edge
        self.dollar_size_per_leg = dollar_size_per_leg
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    # ── DB schema ─────────────────────────────────────────────────────────────

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        conn = self._connect()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS hedged_arb_trades (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                opened_at           TEXT    NOT NULL,
                closed_at           TEXT,
                direction           TEXT    NOT NULL,   -- 'A' or 'B'
                kalshi_ticker       TEXT,
                poly_ticker         TEXT,
                close_time          TEXT    NOT NULL,   -- UTC ISO, contract resolution
                kalshi_side         TEXT    NOT NULL,   -- 'YES' or 'NO'
                kalshi_entry_price  REAL    NOT NULL,
                kalshi_contracts    INTEGER NOT NULL,
                poly_side           TEXT    NOT NULL,   -- 'UP' or 'DOWN'
                poly_entry_price    REAL    NOT NULL,
                poly_contracts      INTEGER NOT NULL,
                gross_edge          REAL    NOT NULL,
                fees_paid           REAL    NOT NULL,
                net_edge_at_entry   REAL    NOT NULL,
                locked_pnl          REAL    NOT NULL,
                resolution          TEXT,              -- 'kalshi_yes' | 'kalshi_no' | 'unknown'
                realized_pnl        REAL,
                status              TEXT    NOT NULL DEFAULT 'open'  -- 'open' | 'resolved'
            );
            CREATE INDEX IF NOT EXISTS idx_hedged_status   ON hedged_arb_trades(status);
            CREATE INDEX IF NOT EXISTS idx_hedged_close_ts ON hedged_arb_trades(close_time);
            CREATE INDEX IF NOT EXISTS idx_hedged_opened   ON hedged_arb_trades(opened_at);
        """)
        conn.commit()
        conn.close()

    # ── Market data read ──────────────────────────────────────────────────────

    def _latest_joint(self, conn: sqlite3.Connection) -> Optional[dict]:
        """
        Latest joint tick: most recent Kalshi row joined to the most recent
        Polymarket row sharing the same close_time.
        """
        k = conn.execute("""
            SELECT ticker, close_time,
                   yes_bid_dollars, yes_ask_dollars,
                   no_bid_dollars,  no_ask_dollars,
                   collected_at
            FROM markets
            WHERE yes_ask_dollars IS NOT NULL
              AND no_ask_dollars  IS NOT NULL
            ORDER BY collected_at DESC LIMIT 1
        """).fetchone()
        if not k:
            return None

        p = conn.execute("""
            SELECT ticker, close_time,
                   up_bid, up_ask, down_bid, down_ask,
                   collected_at
            FROM polymarket_markets
            WHERE close_time = ?
              AND up_ask   IS NOT NULL
              AND down_ask IS NOT NULL
            ORDER BY collected_at DESC LIMIT 1
        """, (k["close_time"],)).fetchone()
        if not p:
            return None

        return {
            "kalshi_ticker":   k["ticker"],
            "poly_ticker":     p["ticker"],
            "close_time":      k["close_time"],
            "kalshi_yes_ask":  k["yes_ask_dollars"],
            "kalshi_no_ask":   k["no_ask_dollars"],
            "poly_up_ask":     p["up_ask"],
            "poly_down_ask":   p["down_ask"],
            "k_collected_at":  k["collected_at"],
            "p_collected_at":  p["collected_at"],
        }

    # ── Open guards ───────────────────────────────────────────────────────────

    def _seconds_to_close(self, close_time_iso: str) -> float:
        ct = _parse_close_time(close_time_iso)
        if ct is None:
            return -1.0
        now = datetime.now(timezone.utc)
        return (ct - now).total_seconds()

    def _already_have_open_for_window(
        self, conn: sqlite3.Connection, close_time_iso: str,
    ) -> bool:
        row = conn.execute(
            "SELECT 1 FROM hedged_arb_trades "
            "WHERE close_time = ? AND status = 'open' LIMIT 1",
            (close_time_iso,),
        ).fetchone()
        return row is not None

    # ── Tick loop ────────────────────────────────────────────────────────────

    def tick(self) -> dict:
        """One paper-trading cycle. Returns a short summary dict for the caller."""
        with self._lock:
            conn = self._connect()
            summary = {"opened": 0, "resolved": 0, "skipped_reason": None}
            try:
                # 1. Resolve any open trades whose close_time has passed.
                summary["resolved"] = self._resolve_due(conn)

                # 2. Look for a new arb on the current joint tick.
                joint = self._latest_joint(conn)
                if not joint:
                    summary["skipped_reason"] = "no_joint_data"
                    return summary

                ttl = self._seconds_to_close(joint["close_time"])
                if ttl < MIN_SECONDS_TO_CLOSE:
                    summary["skipped_reason"] = f"ttl_{ttl:.0f}s_below_guard"
                    return summary

                if self._already_have_open_for_window(conn, joint["close_time"]):
                    summary["skipped_reason"] = "already_open_for_window"
                    return summary

                sig = evaluate_arb(
                    kalshi_yes_ask=joint["kalshi_yes_ask"],
                    kalshi_no_ask=joint["kalshi_no_ask"],
                    poly_up_ask=joint["poly_up_ask"],
                    poly_down_ask=joint["poly_down_ask"],
                    min_edge=self.min_edge,
                    dollar_size_per_leg=self.dollar_size_per_leg,
                )
                if sig is None:
                    summary["skipped_reason"] = "no_edge"
                    return summary

                self._open_trade(conn, joint, sig)
                summary["opened"] = 1
                return summary
            finally:
                conn.commit()
                conn.close()

    # ── Open a new trade ──────────────────────────────────────────────────────

    def _open_trade(self, conn: sqlite3.Connection, joint: dict, sig: ArbSignal) -> None:
        now_iso = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO hedged_arb_trades
                 (opened_at, direction, kalshi_ticker, poly_ticker, close_time,
                  kalshi_side, kalshi_entry_price, kalshi_contracts,
                  poly_side,   poly_entry_price,   poly_contracts,
                  gross_edge, fees_paid, net_edge_at_entry, locked_pnl, status)
               VALUES (?, ?, ?, ?, ?,
                       ?, ?, ?,
                       ?, ?, ?,
                       ?, ?, ?, ?, 'open')""",
            (
                now_iso, sig.direction,
                joint["kalshi_ticker"], joint["poly_ticker"], joint["close_time"],
                sig.kalshi_side, sig.kalshi_price, sig.contracts,
                sig.poly_side,   sig.poly_price,   sig.contracts,
                sig.gross_edge, sig.fees["total"], sig.net_edge, sig.locked_pnl,
            ),
        )
        log.info(
            "[hedged_arb] OPEN dir=%s  kalshi=%s@%.4f×%d  poly=%s@%.4f×%d  "
            "gross=%.4f  fees=%.4f  net=%.4f  locked=$%.2f",
            sig.direction, sig.kalshi_side, sig.kalshi_price, sig.contracts,
            sig.poly_side,   sig.poly_price,   sig.contracts,
            sig.gross_edge, sig.fees["total"], sig.net_edge, sig.locked_pnl,
        )

    # ── Resolution ────────────────────────────────────────────────────────────

    def _resolve_due(self, conn: sqlite3.Connection) -> int:
        """
        Resolve every open trade whose close_time has passed and for which
        btc_labels_15m has ground-truth direction_up. Returns the number of
        trades resolved.
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        rows = conn.execute(
            "SELECT * FROM hedged_arb_trades "
            "WHERE status = 'open' AND close_time <= ?",
            (now_iso,),
        ).fetchall()

        resolved_count = 0
        for r in rows:
            outcome = self._resolve_one(conn, dict(r))
            if outcome is not None:
                resolved_count += 1
        return resolved_count

    def _resolve_one(self, conn: sqlite3.Connection, trade: dict) -> Optional[str]:
        """
        Look up direction_up from btc_labels_15m at the trade's close_time.
        If found, book realized_pnl = locked_pnl (a true hedge locks in the same
        PnL regardless of direction) and flip status to resolved.
        Returns the resolution string or None if ground truth isn't available yet.
        """
        direction_up = self._lookup_direction_up(conn, trade["close_time"])
        now_iso = datetime.now(timezone.utc).isoformat()

        if direction_up is None:
            return None

        # Gross payout: $1 per winning contract on each leg. Kalshi YES wins if
        # direction_up=1; Kalshi NO wins if direction_up=0. Likewise Poly UP/DOWN.
        kalshi_won = (
            (trade["kalshi_side"] == "YES" and direction_up == 1) or
            (trade["kalshi_side"] == "NO"  and direction_up == 0)
        )
        poly_won = (
            (trade["poly_side"] == "UP"   and direction_up == 1) or
            (trade["poly_side"] == "DOWN" and direction_up == 0)
        )
        # In a correctly-constructed hedge, exactly one leg wins.
        contracts = int(trade["kalshi_contracts"])
        kalshi_payout = contracts if kalshi_won else 0
        poly_payout   = contracts if poly_won   else 0

        kalshi_cost = trade["kalshi_entry_price"] * contracts
        poly_cost   = trade["poly_entry_price"]   * contracts
        gross_pnl   = (kalshi_payout + poly_payout) - (kalshi_cost + poly_cost)
        realized    = gross_pnl - trade["fees_paid"]

        resolution = "kalshi_yes" if direction_up == 1 else "kalshi_no"

        conn.execute(
            """UPDATE hedged_arb_trades
                 SET status = 'resolved', closed_at = ?,
                     resolution = ?,      realized_pnl = ?
               WHERE id = ?""",
            (now_iso, resolution, round(realized, 4), trade["id"]),
        )
        log.info(
            "[hedged_arb] RESOLVE id=%d  close_time=%s  dir_up=%d  "
            "realized=$%.4f  (locked_at_entry=$%.4f)",
            trade["id"], trade["close_time"], direction_up, realized, trade["locked_pnl"],
        )
        return resolution

    @staticmethod
    def _lookup_direction_up(
        conn: sqlite3.Connection, close_time_iso: str,
    ) -> Optional[int]:
        """
        Ground truth from btc_labels_15m. The contract's close_time is when
        the underlying 15m window closes, so we read the label at that
        same timestamp (direction_up = 1 if close[t+1] > close[t]).
        """
        ct = _parse_close_time(close_time_iso)
        if ct is None:
            return None

        # btc_labels_15m.timestamp uses UTC ISO; try direct equality first,
        # then a minute-truncated match for tz-formatting variance.
        row = conn.execute(
            "SELECT direction_up FROM btc_labels_15m WHERE timestamp = ?",
            (close_time_iso,),
        ).fetchone()
        if row and row["direction_up"] is not None:
            return int(row["direction_up"])

        # Fallback: strftime-minute match against labels stored as naive UTC.
        minute_key = ct.strftime("%Y-%m-%dT%H:%M")
        row = conn.execute(
            "SELECT direction_up FROM btc_labels_15m "
            "WHERE strftime('%Y-%m-%dT%H:%M', timestamp) = ? "
            "  AND direction_up IS NOT NULL LIMIT 1",
            (minute_key,),
        ).fetchone()
        if row and row["direction_up"] is not None:
            return int(row["direction_up"])
        return None

    # ── Dashboard-data helpers ────────────────────────────────────────────────

    def get_dashboard_data(self) -> dict:
        conn = self._connect()
        try:
            open_trades = conn.execute(
                """SELECT * FROM hedged_arb_trades
                     WHERE status = 'open'
                     ORDER BY opened_at DESC"""
            ).fetchall()
            closed_trades = conn.execute(
                """SELECT * FROM hedged_arb_trades
                     WHERE status = 'resolved'
                     ORDER BY closed_at DESC LIMIT 20"""
            ).fetchall()

            tot = conn.execute(
                """SELECT COUNT(*)                                     AS total,
                          SUM(CASE WHEN status='open'     THEN 1 ELSE 0 END) AS n_open,
                          SUM(CASE WHEN status='resolved' THEN 1 ELSE 0 END) AS n_resolved,
                          ROUND(SUM(COALESCE(realized_pnl, 0)), 4)     AS total_pnl,
                          ROUND(SUM(COALESCE(locked_pnl,   0)), 4)     AS total_locked
                     FROM hedged_arb_trades"""
            ).fetchone()

            return {
                "open_trades":   [dict(r) for r in open_trades],
                "closed_trades": [dict(r) for r in closed_trades],
                "summary":       dict(tot) if tot else {},
            }
        finally:
            conn.close()


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import time as _time
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s",
    )
    trader = HedgedArbTrader()
    log.info("[hedged_arb] manual tick loop starting")
    while True:
        out = trader.tick()
        log.info("[hedged_arb] tick → %s", out)
        _time.sleep(60)
