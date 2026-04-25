import logging
import os
import re
import sqlite3
import sys
import time
import requests
from datetime import datetime, timezone

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _ROOT)
from agents.collectors.btc_feed import get_latest_btc                              # noqa: E402
from agents.pricing.fair_value import get_realized_vol, fair_value as _fv, edge as _edge  # noqa: E402

URL = "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTC15M&status=open&limit=1"
DB_PATH = os.path.join(_ROOT, "data", "btc15m.db")
INTERVAL = 60

KALSHI_API_KEY = os.environ.get("KALSHI_API_KEY")
if KALSHI_API_KEY:
    _HEADERS = {"Authorization": f"Bearer {KALSHI_API_KEY}"}
else:
    logging.warning("KALSHI_API_KEY not set — running in unauthenticated mode")
    _HEADERS = {}


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS markets (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at    TEXT NOT NULL,
            ticker          TEXT,
            close_time      TEXT,
            yes_bid_dollars REAL,
            yes_ask_dollars REAL,
            no_bid_dollars  REAL,
            no_ask_dollars  REAL,
            last_price_dollars REAL,
            volume_24h_fp   REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS arb_edge_log (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            ts                   DATETIME NOT NULL,
            btc_spot             REAL,
            btc_spot_age_seconds REAL,
            kalshi_yes_ask       REAL,
            kalshi_strike        REAL,
            t_remaining_seconds  REAL,
            sigma                REAL,
            fair_value           REAL,
            raw_edge             REAL,
            net_edge             REAL,
            kalshi_fee           REAL,
            tradeable            INTEGER
        )
    """)
    conn.commit()


_STRIKE_RE = re.compile(r'-B(\d+(?:\.\d+)?)$')
_KALSHI_FEE = 0.0175


def _parse_strike(ticker: str, floor_strike: float | None = None) -> float | None:
    """Extract numeric strike: try ticker regex first, fall back to floor_strike API field."""
    m = _STRIKE_RE.search(ticker or "")
    if m:
        return float(m.group(1))
    if floor_strike is not None:
        return float(floor_strike)
    return None


def _log_arb_edge(conn, row, collected_at: str) -> None:
    """Compute fair value and edge after a successful Kalshi tick, then insert into arb_edge_log."""
    ticker = row.get("ticker") or ""
    strike = _parse_strike(ticker, floor_strike=row.get("floor_strike"))
    if strike is None:
        logging.warning("collector: cannot parse strike from ticker %r and no floor_strike — skipping arb_edge_log", ticker)
        return

    try:
        btc = get_latest_btc()
    except Exception as exc:
        logging.warning("collector: get_latest_btc() failed: %s — skipping arb_edge_log", exc)
        return

    close_time = row.get("close_time")
    try:
        ct_dt = datetime.fromisoformat((close_time or "").replace("Z", "+00:00"))
        t_remaining = max((ct_dt - datetime.now(timezone.utc)).total_seconds(), 0.0)
    except (ValueError, TypeError):
        logging.warning("collector: cannot parse close_time %r — skipping arb_edge_log", close_time)
        return

    try:
        sigma = get_realized_vol(DB_PATH)
    except Exception as exc:
        logging.warning("collector: get_realized_vol() failed: %s — skipping arb_edge_log", exc)
        return

    yes_ask = row.get("yes_ask_dollars")
    if yes_ask is None:
        return

    fv       = _fv(btc["price"], strike, t_remaining, sigma)
    raw_edge = fv - yes_ask
    net_edge = _edge(fv, yes_ask, _KALSHI_FEE)

    conn.execute("""
        INSERT INTO arb_edge_log
            (ts, btc_spot, btc_spot_age_seconds, kalshi_yes_ask, kalshi_strike,
             t_remaining_seconds, sigma, fair_value, raw_edge, net_edge,
             kalshi_fee, tradeable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        collected_at,
        btc["price"],
        btc["age_seconds"],
        yes_ask,
        strike,
        t_remaining,
        sigma,
        fv,
        raw_edge,
        net_edge,
        _KALSHI_FEE,
        1 if net_edge > 0.035 else 0,
    ))
    conn.commit()


def fetch_market():
    resp = requests.get(URL, headers=_HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    markets = data.get("markets", [])
    if not markets:
        raise ValueError("No markets returned")
    m = markets[0]
    def _f(v):
        try:
            return float(v) if v is not None else None
        except (TypeError, ValueError):
            return None

    return {
        "ticker":             m.get("ticker"),
        "close_time":         m.get("close_time"),
        "yes_bid_dollars":    _f(m.get("yes_bid_dollars")),
        "yes_ask_dollars":    _f(m.get("yes_ask_dollars")),
        "no_bid_dollars":     _f(m.get("no_bid_dollars")),
        "no_ask_dollars":     _f(m.get("no_ask_dollars")),
        "last_price_dollars": _f(m.get("last_price_dollars")),
        "volume_24h_fp":      _f(m.get("volume_24h_fp")),
        "floor_strike":       _f(m.get("floor_strike")),
    }


def insert_row(conn, collected_at, row):
    conn.execute("""
        INSERT INTO markets
            (collected_at, ticker, close_time, yes_bid_dollars, yes_ask_dollars,
             no_bid_dollars, no_ask_dollars, last_price_dollars, volume_24h_fp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        collected_at,
        row["ticker"],
        row["close_time"],
        row["yes_bid_dollars"],
        row["yes_ask_dollars"],
        row["no_bid_dollars"],
        row["no_ask_dollars"],
        row["last_price_dollars"],
        row["volume_24h_fp"],
    ))
    conn.commit()


def print_row(collected_at, row):
    print(
        f"[{collected_at}] "
        f"ticker={row['ticker']}  "
        f"close={row['close_time']}  "
        f"yes_bid={row['yes_bid_dollars']}  yes_ask={row['yes_ask_dollars']}  "
        f"no_bid={row['no_bid_dollars']}  no_ask={row['no_ask_dollars']}  "
        f"last={row['last_price_dollars']}  vol24h={row['volume_24h_fp']}"
    )


def check_spread_zscore(conn, current_spread, window=50):
    """Print an alert if the current bid-ask spread is > 2σ above recent history."""
    rows = conn.execute("""
        SELECT yes_ask_dollars - yes_bid_dollars
        FROM markets
        WHERE yes_bid_dollars IS NOT NULL AND yes_ask_dollars IS NOT NULL
        ORDER BY collected_at DESC
        LIMIT ?
    """, (window,)).fetchall()
    if len(rows) < 10:
        return
    spreads = [r[0] for r in rows]
    mean = sum(spreads) / len(spreads)
    std  = (sum((s - mean) ** 2 for s in spreads) / (len(spreads) - 1)) ** 0.5
    if std == 0:
        return
    z = (current_spread - mean) / std
    if abs(z) > 2.0:
        print(f"  ⚠ SPREAD ALERT: bid-ask spread={current_spread:.4f}  z={z:+.2f}  (mean={mean:.4f} σ={std:.4f})")


def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    print(f"Collecting from Kalshi every {INTERVAL}s → {DB_PATH}")

    while True:
        try:
            row = fetch_market()
            collected_at = datetime.now(timezone.utc).isoformat()
            insert_row(conn, collected_at, row)
            print_row(collected_at, row)
            bid = row["yes_bid_dollars"]
            ask = row["yes_ask_dollars"]
            if bid is not None and ask is not None:
                check_spread_zscore(conn, ask - bid)
            _log_arb_edge(conn, row, collected_at)
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
