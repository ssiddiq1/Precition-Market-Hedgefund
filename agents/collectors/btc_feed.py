"""
Real-time BTC/USD price feed via Coinbase Advanced Trade websocket.

Auto-starts a background daemon thread on import. Falls back to a REST poll
of the Coinbase v2 spot endpoint when the websocket has been dark for > 5s.
"""

import json
import logging
import threading
import time
from datetime import datetime, timezone

import requests
import websocket

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Public state
# ---------------------------------------------------------------------------
LATEST_BTC_PRICE: float | None = None
LATEST_BTC_TIMESTAMP: datetime | None = None
_state_lock = threading.Lock()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_WS_URL = "wss://advanced-trade-api.coinbase.com/ws"
_SUBSCRIBE_MSG = json.dumps({
    "type": "subscribe",
    "product_ids": ["BTC-USD"],
    "channel": "ticker",
})
_REST_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
_FALLBACK_THRESHOLD = 5.0   # seconds of websocket silence before REST kicks in
_BACKOFF_MAX = 30.0          # seconds


def get_latest_btc() -> dict:
    """Return the most recent BTC/USD price.

    Returns a dict with:
        price        (float)    - latest BTC/USD price
        timestamp    (datetime) - UTC datetime of the last update
        age_seconds  (float)    - seconds since the last update

    Falls back to the Coinbase REST spot endpoint if the cached value is stale
    (older than _FALLBACK_THRESHOLD) or not yet populated.
    """
    with _state_lock:
        price = LATEST_BTC_PRICE
        ts = LATEST_BTC_TIMESTAMP

    now = datetime.now(timezone.utc)
    age = (now - ts).total_seconds() if ts else float("inf")

    if price is None or age > _FALLBACK_THRESHOLD:
        price, ts = _rest_fetch()
        age = (datetime.now(timezone.utc) - ts).total_seconds()

    return {"price": price, "timestamp": ts, "age_seconds": age}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _set_price(price: float, ts: datetime) -> None:
    global LATEST_BTC_PRICE, LATEST_BTC_TIMESTAMP
    with _state_lock:
        LATEST_BTC_PRICE = price
        LATEST_BTC_TIMESTAMP = ts


def _rest_fetch() -> tuple[float, datetime]:
    """Poll the Coinbase v2 REST endpoint for the current BTC/USD spot price."""
    try:
        resp = requests.get(_REST_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        price = float(data["data"]["amount"])
        ts = datetime.now(timezone.utc)
        log.debug("REST fallback: BTC/USD = %.2f", price)
        _set_price(price, ts)
        return price, ts
    except Exception as exc:
        log.error("REST fallback failed: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Websocket callbacks
# ---------------------------------------------------------------------------

def _on_open(ws: websocket.WebSocketApp) -> None:
    log.info("Coinbase WS connected — subscribing to BTC-USD ticker")
    ws.send(_SUBSCRIBE_MSG)


def _on_message(ws: websocket.WebSocketApp, raw: str) -> None:  # noqa: ARG001
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        return

    # The Advanced Trade API wraps ticks inside an "events" list.
    if msg.get("channel") != "ticker":
        return

    for event in msg.get("events", []):
        for tick in event.get("ticks", []):
            raw_price = tick.get("price")
            if raw_price is None:
                continue
            try:
                price = float(raw_price)
            except (TypeError, ValueError):
                continue
            ts = datetime.now(timezone.utc)
            _set_price(price, ts)
            log.debug("WS tick: BTC/USD = %.2f at %s", price, ts.isoformat())


def _on_error(ws: websocket.WebSocketApp, error: Exception) -> None:  # noqa: ARG001
    log.error("Coinbase WS error: %s", error)


def _on_close(
    ws: websocket.WebSocketApp,  # noqa: ARG001
    close_status_code: int | None,
    close_msg: str | None,
) -> None:
    log.warning(
        "Coinbase WS disconnected (code=%s msg=%s)",
        close_status_code,
        close_msg,
    )


# ---------------------------------------------------------------------------
# Background thread
# ---------------------------------------------------------------------------

def _run_forever() -> None:
    """Connect and reconnect with exponential backoff."""
    delay = 1.0
    while True:
        log.info("Connecting to Coinbase WS: %s", _WS_URL)
        ws = websocket.WebSocketApp(
            _WS_URL,
            on_open=_on_open,
            on_message=_on_message,
            on_error=_on_error,
            on_close=_on_close,
        )
        ws.run_forever(ping_interval=20, ping_timeout=10)
        # run_forever returns when the connection closes
        log.info("Reconnecting in %.1fs …", delay)
        time.sleep(delay)
        delay = min(delay * 2, _BACKOFF_MAX)


def _start_feed() -> None:
    t = threading.Thread(target=_run_forever, name="btc-feed", daemon=True)
    t.start()
    log.info("BTC feed daemon thread started")


# Auto-start on import
_start_feed()
