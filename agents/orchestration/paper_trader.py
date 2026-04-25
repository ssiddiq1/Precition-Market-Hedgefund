"""
paper_trader.py — live paper trading engine for quant-os

Maintains two active accounts (spread_arb, momentum_fade) at $10,000 each.
Calls StrategyEngine.get_signals() each tick to decide open/hold/close.

Trade mechanics (binary contract model):
  • Open  : size = confidence × $800, entry_adj = entry_price × (1 + 0.15%)
  • Win PnL: size × (1 − entry_adj)
  • Loss  : size × (−entry_adj)
  • Resolution proxy: current last_price_dollars ≥ 0.5 → "resolved YES"

State is persisted in two tables in btc15m.db:
  paper_accounts — one row per tick per strategy (append-only ledger)
  paper_trades   — one row per closed trade
"""

import math
import os
import sys
import sqlite3
import threading
from datetime import datetime, timezone

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(_ROOT, "data", "btc15m.db")

sys.path.insert(0, _ROOT)
from agents.strategies.strategy_engine import StrategyEngine  # noqa: E402

INITIAL_EQUITY    = 10_000.0
ALLOC_SCALE       = 800.0      # position_size = confidence × $800
SLIPPAGE          = 0.0015       # 0.15% entry slippage
OPEN_THRESHOLD    = 0.55       # min confidence to open a position
CLOSE_THRESHOLD   = 0.30       # close if confidence drops below this

ACTIVE_STRATEGIES = frozenset({"spread_arb", "momentum_fade"})
ALL_STRATEGIES    = [
    "spread_arb",
    "momentum_fade",
]


def _json_safe(obj):
    """Recursively convert values so Flask/browser JSON never sees NaN/Inf."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int) and not isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, str):
        return obj
    if hasattr(obj, "item"):
        try:
            return _json_safe(obj.item())
        except Exception:
            pass
    try:
        x = float(obj)
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    except (TypeError, ValueError):
        return str(obj)


class PaperTrader:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._lock   = threading.Lock()
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    # ── DB helpers ────────────────────────────────────────────────────────────

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path, check_same_thread=False, timeout=30.0,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        conn = self._connect()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS paper_accounts (
                id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name         TEXT    NOT NULL,
                timestamp             TEXT    NOT NULL,
                equity                REAL    NOT NULL DEFAULT 10000.0,
                cash                  REAL    NOT NULL DEFAULT 10000.0,
                position_direction    TEXT,
                position_size_dollars REAL    DEFAULT 0.0,
                entry_price           REAL    DEFAULT 0.0,
                unrealized_pnl        REAL    DEFAULT 0.0,
                realized_pnl_total    REAL    DEFAULT 0.0,
                is_active             INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS paper_trades (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name TEXT    NOT NULL,
                timestamp     TEXT    NOT NULL,
                direction     TEXT    NOT NULL,
                size_dollars  REAL    NOT NULL,
                entry_price   REAL    NOT NULL,
                exit_price    REAL,
                pnl           REAL    NOT NULL,
                confidence    REAL    NOT NULL
            );
        """)

        now = datetime.now(timezone.utc).isoformat()
        for strat in ALL_STRATEGIES:
            exists = conn.execute(
                "SELECT 1 FROM paper_accounts WHERE strategy_name = ? LIMIT 1",
                (strat,),
            ).fetchone()
            if not exists:
                active = 1 if strat in ACTIVE_STRATEGIES else 0
                conn.execute(
                    """INSERT INTO paper_accounts
                           (strategy_name, timestamp, equity, cash, is_active)
                       VALUES (?, ?, ?, ?, ?)""",
                    (strat, now, INITIAL_EQUITY, INITIAL_EQUITY, active),
                )

        conn.commit()
        conn.close()

    def _latest_account(self, conn: sqlite3.Connection, strat: str):
        return conn.execute(
            """SELECT * FROM paper_accounts
               WHERE strategy_name = ?
               ORDER BY id DESC LIMIT 1""",
            (strat,),
        ).fetchone()

    def _insert_account(
        self, conn, strat, equity, cash,
        pos_dir, pos_size, entry_price, unrealized_pnl, realized_pnl,
    ) -> None:
        conn.execute(
            """INSERT INTO paper_accounts
                   (strategy_name, timestamp, equity, cash, position_direction,
                    position_size_dollars, entry_price, unrealized_pnl,
                    realized_pnl_total, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                strat,
                datetime.now(timezone.utc).isoformat(),
                equity,
                cash,
                pos_dir,
                pos_size or 0.0,
                entry_price or 0.0,
                unrealized_pnl or 0.0,
                realized_pnl or 0.0,
                1 if strat in ACTIVE_STRATEGIES else 0,
            ),
        )

    def _is_flat(self, pos_dir) -> bool:
        return pos_dir is None or pos_dir == "" or pos_dir == "FLAT"

    def _snapshot_inactive(self, conn) -> None:
        """Append latest state for strategies that never trade (tick always)."""
        for strat in ALL_STRATEGIES:
            if strat in ACTIVE_STRATEGIES:
                continue
            acct = self._latest_account(conn, strat)
            if acct is None:
                continue
            equity = float(acct["equity"] or 0.0)
            cash = float(acct["cash"] or 0.0)
            realized = float(acct["realized_pnl_total"] or 0.0)
            self._insert_account(
                conn, strat,
                equity, cash, None, 0.0, 0.0, 0.0, realized,
            )

    # ── Tick ─────────────────────────────────────────────────────────────────

    def tick(self) -> None:
        """
        Evaluate all signals once and update every strategy account row.
        Active strategies trade; inactive ones only get a timestamp refresh.
        """
        with self._lock:
            try:
                engine = StrategyEngine(self.db_path)
                raw_sigs = engine.get_signals()
                signals = {s["strategy"]: s for s in raw_sigs}
            except Exception as exc:
                print(f"[paper_trader] tick: get_signals() failed: {exc}")
                return

            conn = self._connect()
            try:
                last_row = conn.execute(
                    """SELECT last_price_dollars FROM markets
                       WHERE last_price_dollars IS NOT NULL
                       ORDER BY collected_at DESC LIMIT 1"""
                ).fetchone()
                current_last = (
                    float(last_row["last_price_dollars"]) if last_row else 0.5
                )
                resolved_yes = current_last >= 0.5
                now = datetime.now(timezone.utc).isoformat()

                for strat in ACTIVE_STRATEGIES:
                    sig = signals.get(strat, {})
                    acct = self._latest_account(conn, strat)
                    if acct is None:
                        continue

                    equity = float(acct["equity"] or 0.0)
                    cash = float(acct["cash"] or 0.0)
                    pos_dir = acct["position_direction"]
                    pos_size = float(acct["position_size_dollars"] or 0.0)
                    entry_price = float(acct["entry_price"] or 0.0)
                    realized_total = float(acct["realized_pnl_total"] or 0.0)

                    confidence = float(sig.get("confidence", 0.0))
                    new_dir = sig.get("direction", "FLAT")

                    if self._is_flat(pos_dir):
                        if (
                            confidence > OPEN_THRESHOLD
                            and new_dir in ("YES", "NO")
                        ):
                            raw_entry = float(sig.get("entry_price") or 0.5)
                            entry_adj = raw_entry * (1.0 + SLIPPAGE)
                            size = min(confidence * ALLOC_SCALE, cash)
                            if size > 0 and entry_adj > 0:
                                cash -= size
                                self._insert_account(
                                    conn, strat,
                                    equity, cash,
                                    new_dir, size, entry_adj, 0.0, realized_total,
                                )
                                continue
                        self._insert_account(
                            conn, strat,
                            equity, cash, None, 0.0, 0.0, 0.0, realized_total,
                        )

                    else:
                        won = (
                            (resolved_yes and pos_dir == "YES")
                            or (not resolved_yes and pos_dir == "NO")
                        )
                        unrealized = (
                            pos_size * (1.0 - entry_price)
                            if won
                            else pos_size * (-entry_price)
                        )

                        direction_flip = (
                            new_dir in ("YES", "NO") and new_dir != pos_dir
                        )
                        should_close = (
                            direction_flip or confidence < CLOSE_THRESHOLD
                        )

                        if should_close:
                            pnl = (
                                pos_size * (1.0 - entry_price)
                                if won
                                else pos_size * (-entry_price)
                            )
                            cash += pos_size + pnl
                            equity = cash
                            realized_total += pnl

                            conn.execute(
                                """INSERT INTO paper_trades
                                       (strategy_name, timestamp, direction,
                                        size_dollars, entry_price, exit_price,
                                        pnl, confidence)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (
                                    strat, now, pos_dir, pos_size,
                                    entry_price, current_last, pnl, confidence,
                                ),
                            )

                            self._insert_account(
                                conn, strat,
                                equity, cash, None, 0.0, 0.0, 0.0,
                                realized_total,
                            )

                        else:
                            equity_live = cash + pos_size + unrealized
                            self._insert_account(
                                conn, strat,
                                equity_live, cash,
                                pos_dir, pos_size, entry_price,
                                unrealized, realized_total,
                            )

                self._snapshot_inactive(conn)
                conn.commit()
            finally:
                conn.close()

    # ── Dashboard data ─────────────────────────────────────────────────────

    def get_dashboard_data(self) -> dict:
        """Return all data needed to render the paper trading dashboard."""
        conn = self._connect()
        try:
            accounts = {}
            for strat in ALL_STRATEGIES:
                row = self._latest_account(conn, strat)
                accounts[strat] = dict(row) if row else None

            equity_curves = {}
            for strat in ALL_STRATEGIES:
                rows = conn.execute(
                    """SELECT timestamp, equity FROM paper_accounts
                       WHERE strategy_name = ?
                       ORDER BY id DESC LIMIT 100""",
                    (strat,),
                ).fetchall()
                equity_curves[strat] = [
                    {"ts": r["timestamp"], "equity": r["equity"]}
                    for r in reversed(rows)
                ]

            trades = conn.execute(
                """SELECT * FROM paper_trades
                   ORDER BY timestamp DESC, id DESC LIMIT 20"""
            ).fetchall()
            recent_trades = [dict(t) for t in trades]

            total_pnl = {}
            for strat in ALL_STRATEGIES:
                row = self._latest_account(conn, strat)
                total_pnl[strat] = (
                    float(row["realized_pnl_total"] or 0.0) if row else 0.0
                )

            return _json_safe({
                "accounts": accounts,
                "equity_curves": equity_curves,
                "recent_trades": recent_trades,
                "total_pnl_by_strategy": total_pnl,
            })
        finally:
            conn.close()


if __name__ == "__main__":
    import time

    print("[paper_trader] Starting manual tick loop (Ctrl-C to stop)\n")
    pt = PaperTrader()

    while True:
        ts = datetime.now(timezone.utc).isoformat()
        print(f"── tick {ts} ──")
        pt.tick()
        d = pt.get_dashboard_data()
        for strat in ALL_STRATEGIES:
            acct = d["accounts"].get(strat)
            if acct:
                eq = acct["equity"] or 0.0
                pnl = eq - INITIAL_EQUITY
                pos = acct["position_direction"] or "FLAT"
                sign = "+" if pnl >= 0 else ""
                print(
                    f"  {strat:<25} equity=${eq:>10,.2f}  "
                    f"pnl={sign}${pnl:>8,.2f}  pos={pos}"
                )
        print()
        time.sleep(60)
