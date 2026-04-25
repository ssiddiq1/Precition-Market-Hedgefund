import argparse
import math
import os
import sqlite3
import time
from datetime import datetime, timedelta, timezone

import requests

try:
    from research_db import DB_PATH, ensure_research_schema, get_conn, utc_now_iso
except ModuleNotFoundError:  # pragma: no cover - CLI path bootstrap
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from research_db import DB_PATH, ensure_research_schema, get_conn, utc_now_iso

COINBASE_URL = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
GRANULARITY_SECONDS = 900
MAX_CANDLES_PER_REQUEST = 300


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def iso_floor_15m(dt: datetime) -> str:
    dt = to_utc(dt).replace(second=0, microsecond=0)
    floored = dt - timedelta(minutes=dt.minute % 15)
    return floored.isoformat()


def init_tables(conn: sqlite3.Connection) -> None:
    ensure_research_schema(conn)


def fetch_coinbase_chunk(start: datetime, end: datetime) -> list[dict]:
    params = {
        "granularity": GRANULARITY_SECONDS,
        "start": to_utc(start).isoformat(),
        "end": to_utc(end).isoformat(),
    }
    resp = requests.get(COINBASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    rows = []
    for item in resp.json():
        ts, low, high, open_, close, volume = item
        rows.append(
            {
                "timestamp": datetime.fromtimestamp(ts, tz=timezone.utc).replace(
                    second=0, microsecond=0
                ).isoformat(),
                "open": float(open_),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": float(volume),
                "source": "coinbase",
            }
        )
    rows.sort(key=lambda r: r["timestamp"])
    return rows


def upsert_ohlcv_rows(conn: sqlite3.Connection, rows: list[dict]) -> int:
    if not rows:
        return 0
    now = utc_now_iso()
    conn.executemany(
        """
        INSERT INTO btc_ohlcv_15m
            (timestamp, open, high, low, close, volume, source, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(timestamp) DO UPDATE SET
            open=excluded.open,
            high=excluded.high,
            low=excluded.low,
            close=excluded.close,
            volume=excluded.volume,
            source=excluded.source,
            updated_at=excluded.updated_at
        """,
        [
            (
                row["timestamp"],
                row["open"],
                row["high"],
                row["low"],
                row["close"],
                row["volume"],
                row["source"],
                now,
                now,
            )
            for row in rows
        ],
    )
    conn.commit()
    return len(rows)


def log_continuity_gaps(conn: sqlite3.Connection, source: str = "coinbase") -> dict:
    rows = conn.execute(
        """
        SELECT timestamp
        FROM btc_ohlcv_15m
        WHERE source = ?
        ORDER BY timestamp ASC
        """,
        (source,),
    ).fetchall()
    conn.execute("DELETE FROM btc_data_quality WHERE source = ? AND issue_type = 'missing_interval'", (source,))
    if len(rows) < 2:
        conn.commit()
        return {"missing_intervals": 0}

    missing = 0
    for idx in range(1, len(rows)):
        prev_ts = datetime.fromisoformat(rows[idx - 1][0])
        curr_ts = datetime.fromisoformat(rows[idx][0])
        delta = curr_ts - prev_ts
        if delta > timedelta(seconds=GRANULARITY_SECONDS):
            step_count = int(delta.total_seconds() // GRANULARITY_SECONDS)
            for step in range(1, step_count):
                expected = prev_ts + timedelta(seconds=GRANULARITY_SECONDS * step)
                conn.execute(
                    """
                    INSERT OR IGNORE INTO btc_data_quality
                        (source, expected_timestamp, issue_type, details, created_at)
                    VALUES (?, ?, 'missing_interval', ?, ?)
                    """,
                    (
                        source,
                        expected.isoformat(),
                        f"Gap between {prev_ts.isoformat()} and {curr_ts.isoformat()}",
                        utc_now_iso(),
                    ),
                )
                missing += 1
    conn.commit()
    return {"missing_intervals": missing}


def infer_default_start(conn: sqlite3.Connection, days: int) -> datetime:
    row = conn.execute(
        "SELECT MAX(timestamp) FROM btc_ohlcv_15m WHERE source = 'coinbase'"
    ).fetchone()
    if row and row[0]:
        return datetime.fromisoformat(row[0]) + timedelta(seconds=GRANULARITY_SECONDS)
    end = datetime.now(timezone.utc)
    return end - timedelta(days=days)


def ingest_range(
    conn: sqlite3.Connection,
    start: datetime,
    end: datetime,
    source: str = "coinbase",
    pause_seconds: float = 0.35,
) -> dict:
    if source != "coinbase":
        raise ValueError(f"Unsupported source '{source}'. Only coinbase is implemented.")

    start = to_utc(start)
    end = to_utc(end)
    total_inserted = 0
    chunk_span = timedelta(seconds=GRANULARITY_SECONDS * MAX_CANDLES_PER_REQUEST)
    chunk_start = start
    while chunk_start < end:
        chunk_end = min(chunk_start + chunk_span, end)
        rows = fetch_coinbase_chunk(chunk_start, chunk_end)
        total_inserted += upsert_ohlcv_rows(conn, rows)
        chunk_start = chunk_end
        if chunk_start < end:
            time.sleep(pause_seconds)

    quality = log_continuity_gaps(conn, source=source)
    coverage = conn.execute(
        """
        SELECT MIN(timestamp), MAX(timestamp), COUNT(*)
        FROM btc_ohlcv_15m
        WHERE source = ?
        """,
        (source,),
    ).fetchone()
    return {
        "source": source,
        "inserted_or_updated": total_inserted,
        "coverage_start": coverage[0] if coverage else None,
        "coverage_end": coverage[1] if coverage else None,
        "row_count": coverage[2] if coverage else 0,
        **quality,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest historical BTC 15m OHLCV data")
    parser.add_argument("--source", default="coinbase", help="Historical source")
    parser.add_argument("--days", type=int, default=60, help="Days to backfill if no explicit start")
    parser.add_argument("--start", help="UTC ISO timestamp start")
    parser.add_argument("--end", help="UTC ISO timestamp end")
    parser.add_argument("--db-path", default=DB_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    os.makedirs(os.path.dirname(args.db_path), exist_ok=True)
    conn = get_conn(args.db_path)
    try:
        init_tables(conn)
        start = datetime.fromisoformat(args.start) if args.start else infer_default_start(conn, args.days)
        end = datetime.fromisoformat(args.end) if args.end else datetime.now(timezone.utc)
        summary = ingest_range(conn, start, end, source=args.source)
    finally:
        conn.close()

    print("Historical BTC ingest complete")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
