import os
import sqlite3
import time
import requests
from datetime import datetime, timezone

GAMMA_URL = "https://gamma-api.polymarket.com/events?slug={slug}"
CLOB_PRICE = "https://clob.polymarket.com/price?token_id={token_id}&side={side}"
CLOB_LAST  = "https://clob.polymarket.com/last-trade-price?token_id={token_id}"
DB_PATH    = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "btc15m.db")
INTERVAL   = 60


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS polymarket_markets (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at      TEXT NOT NULL,
            ticker            TEXT,
            close_time        TEXT,
            up_bid            REAL,
            up_ask            REAL,
            down_bid          REAL,
            down_ask          REAL,
            last_price        REAL,
            volume_24h        REAL
        )
    """)
    conn.commit()


def current_slug():
    ts = int(time.time())
    window = (ts // 900) * 900
    return f"btc-updown-15m-{window}"


def fetch_event(slug):
    resp = requests.get(GAMMA_URL.format(slug=slug), timeout=10)
    resp.raise_for_status()
    events = resp.json()
    if not events:
        return None, None, None, None
    event = events[0]
    markets = event.get("markets", [])
    if not markets:
        return None, None, None, None
    m = markets[0]
    token_ids = __import__("json").loads(m.get("clobTokenIds", "[]"))
    if len(token_ids) < 2:
        return None, None, None, None
    up_token   = token_ids[0]   # "Up" outcome
    down_token = token_ids[1]   # "Down" outcome
    close_time = m.get("endDate") or event.get("endDate")
    volume_24h = m.get("volume24hr")
    return up_token, down_token, close_time, volume_24h


def clob_price(token_id, side):
    resp = requests.get(CLOB_PRICE.format(token_id=token_id, side=side), timeout=10)
    resp.raise_for_status()
    return float(resp.json()["price"])


def last_trade(token_id):
    resp = requests.get(CLOB_LAST.format(token_id=token_id), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return float(data["price"]) if data.get("price") else None


def fetch_row(slug):
    up_token, down_token, close_time, volume_24h = fetch_event(slug)
    if not up_token:
        raise ValueError(f"No active CLOB market for slug {slug}")

    up_bid   = clob_price(up_token,   "buy")
    up_ask   = clob_price(up_token,   "sell")
    down_bid = clob_price(down_token, "buy")
    down_ask = clob_price(down_token, "sell")
    last     = last_trade(up_token)

    return {
        "ticker":     slug,
        "close_time": close_time,
        "up_bid":     up_bid,
        "up_ask":     up_ask,
        "down_bid":   down_bid,
        "down_ask":   down_ask,
        "last_price": last,
        "volume_24h": volume_24h,
    }


def insert_row(conn, collected_at, row):
    conn.execute("""
        INSERT INTO polymarket_markets
            (collected_at, ticker, close_time, up_bid, up_ask,
             down_bid, down_ask, last_price, volume_24h)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        collected_at,
        row["ticker"],
        row["close_time"],
        row["up_bid"],
        row["up_ask"],
        row["down_bid"],
        row["down_ask"],
        row["last_price"],
        row["volume_24h"],
    ))
    conn.commit()


def print_row(collected_at, row):
    print(
        f"[PM {collected_at}] "
        f"ticker={row['ticker']}  "
        f"close={row['close_time']}  "
        f"up_bid={row['up_bid']}  up_ask={row['up_ask']}  "
        f"down_bid={row['down_bid']}  down_ask={row['down_ask']}  "
        f"last={row['last_price']}  vol24h={row['volume_24h']}"
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    print(f"Collecting Polymarket BTC 15m every {INTERVAL}s → {DB_PATH}")

    while True:
        try:
            slug = current_slug()
            row  = fetch_row(slug)
            collected_at = datetime.now(timezone.utc).isoformat()
            insert_row(conn, collected_at, row)
            print_row(collected_at, row)
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
