"""
latency_arb.py — paper-trading latency arbitrage agent.

Every 5 seconds:
  1. Polls the Kalshi REST API and writes a snapshot to kalshi_market_snapshots.
  2. Reads BTC spot from btc_feed (websocket-backed, sub-second latency).
  3. Computes fair_value and net_edge via fair_value.py.
  4. Opens a paper position when net_edge > 0.035 AND BTC spot age < 3s.
  5. Closes when net_edge < 0.01 OR position has been held > 90 seconds.

All activity is paper-only. No real orders are placed.
"""

import asyncio
import logging
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _ROOT)
from agents.collectors.btc_feed import get_latest_btc                              # noqa: E402
from agents.pricing.fair_value import get_realized_vol, fair_value as _fv, edge as _edge  # noqa: E402

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(_ROOT, "data", "btc15m.db")

_KALSHI_URL = (
    "https://api.elections.kalshi.com/trade-api/v2/markets"
    "?series_ticker=KXBTC15M&status=open&limit=1"
)
_KALSHI_API_KEY = os.environ.get("KALSHI_API_KEY")
_HEADERS        = {"Authorization": f"Bearer {_KALSHI_API_KEY}"} if _KALSHI_API_KEY else {}

POLL_INTERVAL  = 5.0    # seconds between ticks
ENTRY_EDGE     = 0.035  # minimum net_edge to enter
ENTRY_MAX_AGE  = 3.0    # maximum BTC spot age (seconds) to allow entry
EXIT_EDGE      = 0.01   # close when net_edge falls below this
MAX_HOLD_SEC   = 90.0   # force-close after this many seconds
BANKROLL       = 1_000.0
MAX_KELLY_FRAC = 0.10   # cap Kelly fraction at 10% of bankroll
KALSHI_FEE     = 0.0175

_STRIKE_RE = re.compile(r'-B(\d+(?:\.\d+)?)$')


def _f(v) -> float | None:
    """Cast Kalshi API value (may be str or None) to float."""
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# In-memory position
# ---------------------------------------------------------------------------

@dataclass
class Position:
    db_id:         int
    side:          str      # 'YES' or 'NO'
    entry_price:   float
    fair_at_entry: float
    edge_at_entry: float
    contracts:     float
    dollar_size:   float
    opened_at:     datetime
    strike:        float
    sigma:         float


_position: Optional[Position] = None


# ---------------------------------------------------------------------------
# DB
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS kalshi_market_snapshots (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            snapped_at         TEXT NOT NULL,
            ticker             TEXT,
            close_time         TEXT,
            strike             REAL,
            yes_bid_dollars    REAL,
            yes_ask_dollars    REAL,
            no_bid_dollars     REAL,
            no_ask_dollars     REAL,
            last_price_dollars REAL,
            volume_24h_fp      REAL
        );
        CREATE TABLE IF NOT EXISTS latency_arb_paper_trades (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            opened_at           DATETIME,
            closed_at           DATETIME,
            side                TEXT,
            entry_price         REAL,
            close_price         REAL,
            fair_value_at_entry REAL,
            net_edge_at_entry   REAL,
            contracts           REAL,
            dollar_size         REAL,
            pnl                 REAL,
            status              TEXT
        );
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Kalshi REST helpers
# ---------------------------------------------------------------------------

def _parse_strike(ticker: str, floor_strike=None) -> Optional[float]:
    """Try the -B{strike} ticker suffix first, then the floor_strike API field."""
    m = _STRIKE_RE.search(ticker or "")
    if m:
        return float(m.group(1))
    if floor_strike is not None:
        try:
            return float(floor_strike)
        except (TypeError, ValueError):
            pass
    return None


def _fetch_kalshi() -> Optional[dict]:
    """Hit the Kalshi REST API and return a normalised snapshot dict, or None."""
    try:
        resp = requests.get(_KALSHI_URL, headers=_HEADERS, timeout=5)
        resp.raise_for_status()
        markets = resp.json().get("markets", [])
        if not markets:
            return None
        m = markets[0]
        ticker = m.get("ticker") or ""
        return {
            "ticker":             ticker,
            "close_time":         m.get("close_time"),
            "strike":             _parse_strike(ticker, m.get("floor_strike")),
            "yes_bid_dollars":    _f(m.get("yes_bid_dollars")),
            "yes_ask_dollars":    _f(m.get("yes_ask_dollars")),
            "no_bid_dollars":     _f(m.get("no_bid_dollars")),
            "no_ask_dollars":     _f(m.get("no_ask_dollars")),
            "last_price_dollars": _f(m.get("last_price_dollars")),
            "volume_24h_fp":      _f(m.get("volume_24h_fp")),
        }
    except Exception as exc:
        log.error("Kalshi REST fetch failed: %s", exc)
        return None


def _save_snapshot(conn: sqlite3.Connection, snap: dict) -> None:
    conn.execute("""
        INSERT INTO kalshi_market_snapshots
            (snapped_at, ticker, close_time, strike,
             yes_bid_dollars, yes_ask_dollars,
             no_bid_dollars,  no_ask_dollars,
             last_price_dollars, volume_24h_fp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        snap["ticker"],
        snap["close_time"],
        snap["strike"],
        snap["yes_bid_dollars"],
        snap["yes_ask_dollars"],
        snap["no_bid_dollars"],
        snap["no_ask_dollars"],
        snap["last_price_dollars"],
        snap["volume_24h_fp"],
    ))
    conn.commit()


# ---------------------------------------------------------------------------
# Misc helpers
# ---------------------------------------------------------------------------

def _t_remaining(close_time: Optional[str]) -> Optional[float]:
    try:
        ct = datetime.fromisoformat((close_time or "").replace("Z", "+00:00"))
        return max((ct - datetime.now(timezone.utc)).total_seconds(), 0.0)
    except (ValueError, TypeError):
        return None


def _kelly_size(net_edge: float, yes_ask: float) -> float:
    """Kelly fraction of bankroll, capped at MAX_KELLY_FRAC."""
    denom = 1.0 - yes_ask
    if denom <= 0:
        return 0.0
    frac = min(net_edge / denom, MAX_KELLY_FRAC)
    return max(frac * BANKROLL, 0.0)


# ---------------------------------------------------------------------------
# Trade lifecycle
# ---------------------------------------------------------------------------

def _open(conn: sqlite3.Connection, snap: dict, fv: float, ne: float, sigma: float) -> None:
    global _position

    yes_ask = snap["yes_ask_dollars"]
    yes_bid = snap["yes_bid_dollars"]
    side        = "YES" if fv > yes_ask else "NO"
    entry_price = yes_ask if side == "YES" else (1.0 - yes_bid)

    dollar_size = _kelly_size(ne, yes_ask)
    if dollar_size <= 0:
        log.info("latency_arb: edge present but Kelly size is zero — skipping")
        return

    contracts = dollar_size / entry_price if entry_price > 0 else 0.0
    now = datetime.now(timezone.utc)

    conn.execute("""
        INSERT INTO latency_arb_paper_trades
            (opened_at, side, entry_price, fair_value_at_entry,
             net_edge_at_entry, contracts, dollar_size, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'open')
    """, (now.isoformat(), side, entry_price, fv, ne, contracts, dollar_size))
    conn.commit()

    db_id = conn.execute(
        "SELECT id FROM latency_arb_paper_trades ORDER BY id DESC LIMIT 1"
    ).fetchone()["id"]

    _position = Position(
        db_id=db_id, side=side, entry_price=entry_price,
        fair_at_entry=fv, edge_at_entry=ne,
        contracts=contracts, dollar_size=dollar_size,
        opened_at=now, strike=snap["strike"], sigma=sigma,
    )
    log.info(
        "latency_arb: OPEN %s  entry=%.4f  fair=%.4f  net_edge=%.4f  "
        "size=$%.2f (%.4f contracts)",
        side, entry_price, fv, ne, dollar_size, contracts,
    )


def _close(conn: sqlite3.Connection, close_price: float, reason: str) -> None:
    global _position
    pos = _position
    if pos is None:
        return

    pnl = (
        pos.contracts * (close_price - pos.entry_price)
        if pos.side == "YES"
        else pos.contracts * (pos.entry_price - close_price)
    )

    conn.execute("""
        UPDATE latency_arb_paper_trades
           SET closed_at = ?, close_price = ?, pnl = ?, status = 'closed'
         WHERE id = ?
    """, (datetime.now(timezone.utc).isoformat(), close_price, pnl, pos.db_id))
    conn.commit()

    log.info(
        "latency_arb: CLOSE %s  close_price=%.4f  pnl=%+.4f  reason=%s",
        pos.side, close_price, pnl, reason,
    )
    _position = None


# ---------------------------------------------------------------------------
# Tick
# ---------------------------------------------------------------------------

async def _tick(conn: sqlite3.Connection) -> None:
    global _position

    # 1. Kalshi snapshot
    snap = _fetch_kalshi()
    if snap is None:
        log.info("latency_arb: no Kalshi data this tick — skipping")
        return
    _save_snapshot(conn, snap)

    strike  = snap.get("strike")
    yes_ask = snap.get("yes_ask_dollars")
    yes_bid = snap.get("yes_bid_dollars")

    if strike is None:
        log.warning(
            "latency_arb: cannot parse strike from ticker %r — skipping tick",
            snap.get("ticker"),
        )
        return
    if yes_ask is None or yes_bid is None:
        log.info("latency_arb: missing bid/ask — skipping tick")
        return

    # 2. BTC spot
    try:
        btc = get_latest_btc()
    except Exception as exc:
        log.error("latency_arb: get_latest_btc() failed: %s", exc)
        return

    # 3. Time remaining in the current window
    t_remaining = _t_remaining(snap.get("close_time"))
    if t_remaining is None:
        log.info("latency_arb: cannot parse close_time — skipping tick")
        return

    # 4. Realized volatility
    try:
        sigma = get_realized_vol(DB_PATH)
    except Exception as exc:
        log.warning("latency_arb: get_realized_vol() failed: %s — skipping tick", exc)
        return

    # 5. Pricing
    fv = _fv(btc["price"], strike, t_remaining, sigma)
    ne = _edge(fv, yes_ask, KALSHI_FEE)
    now = datetime.now(timezone.utc)

    # 6. Manage existing position
    if _position is not None:
        hold_sec    = (now - _position.opened_at).total_seconds()
        close_price = yes_ask if _position.side == "YES" else (1.0 - yes_bid)

        if ne < EXIT_EDGE:
            _close(conn, close_price, reason=f"edge_collapsed(ne={ne:.4f})")
        elif hold_sec > MAX_HOLD_SEC:
            _close(conn, close_price, reason=f"timeout({hold_sec:.0f}s)")
        else:
            log.info(
                "latency_arb: HOLD %s  age=%.0fs  net_edge=%.4f  fv=%.4f  btc=$%.2f",
                _position.side, hold_sec, ne, fv, btc["price"],
            )
        return

    # 7. Entry check
    if ne <= ENTRY_EDGE:
        log.info(
            "latency_arb: skip — net_edge=%.4f ≤ %.3f  fv=%.4f  ask=%.4f  btc=$%.2f",
            ne, ENTRY_EDGE, fv, yes_ask, btc["price"],
        )
        return

    if btc["age_seconds"] >= ENTRY_MAX_AGE:
        log.info(
            "latency_arb: skip — BTC spot stale (age=%.1fs ≥ %.0fs)  net_edge=%.4f",
            btc["age_seconds"], ENTRY_MAX_AGE, ne,
        )
        return

    _open(conn, snap, fv, ne, sigma)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    conn = _connect()
    _init_db(conn)
    log.info(
        "latency_arb: daemon started — poll=%.0fs  bankroll=$%.0f  "
        "entry_edge=%.3f  max_hold=%.0fs",
        POLL_INTERVAL, BANKROLL, ENTRY_EDGE, MAX_HOLD_SEC,
    )

    while True:
        t0 = time.monotonic()
        try:
            await _tick(conn)
        except Exception as exc:
            log.error("latency_arb: unhandled tick error: %s", exc, exc_info=True)
        elapsed = time.monotonic() - t0
        await asyncio.sleep(max(0.0, POLL_INTERVAL - elapsed))


if __name__ == "__main__":
    asyncio.run(main())
