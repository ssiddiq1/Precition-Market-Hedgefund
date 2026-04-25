"""
Fair-value pricing for Kalshi BTC 15-minute binary YES contracts.

All functions are pure math — no network calls, no btc_feed dependency.
"""

import math
import sqlite3


# ---------------------------------------------------------------------------
# Core pricing
# ---------------------------------------------------------------------------

def fair_value(
    spot: float,
    strike: float,
    t_remaining_seconds: float,
    sigma: float,
) -> float:
    """Black-Scholes binary (digital) call probability.

    P(YES) = N((spot - strike) / (sigma * sqrt(T)))
    where T = t_remaining_seconds / 900 (fraction of a 15-min window).

    Returns a probability clamped to [0.01, 0.99].
    If t_remaining_seconds <= 0, returns the intrinsic value (1.0 or 0.0).
    """
    if t_remaining_seconds <= 0:
        return 1.0 if spot > strike else 0.0

    T = t_remaining_seconds / 900.0
    d = (spot - strike) / (sigma * math.sqrt(T))
    prob = _norm_cdf(d)
    return max(0.01, min(0.99, prob))


# ---------------------------------------------------------------------------
# Realized volatility from historical candles
# ---------------------------------------------------------------------------

def get_realized_vol(db_path: str, n_candles: int = 20) -> float:
    """Compute per-candle (15-min) realized vol from the last n_candles closes.

    Reads `close` from `btc_ohlcv_15m`, ordered by timestamp descending,
    then computes std(log(close[i] / close[i-1])).

    Returns sigma as a per-15-min-candle standard deviation of log returns —
    ready to plug straight into fair_value().
    """
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT close FROM btc_ohlcv_15m
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (n_candles,),
        ).fetchall()
    finally:
        conn.close()

    closes = [r[0] for r in rows]
    if len(closes) < 2:
        raise ValueError(
            f"Need at least 2 candles to compute vol; got {len(closes)}"
        )

    # Reverse so closes are chronologically oldest-first before computing returns
    closes = closes[::-1]
    log_returns = [
        math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))
    ]

    mean = sum(log_returns) / len(log_returns)
    variance = sum((r - mean) ** 2 for r in log_returns) / (len(log_returns) - 1)
    return math.sqrt(variance)


# ---------------------------------------------------------------------------
# Edge calculation
# ---------------------------------------------------------------------------

def edge(fair: float, market_ask: float, kalshi_fee: float = 0.0175) -> float:
    """Return the edge of buying the YES contract at market_ask.

    edge = fair - market_ask - kalshi_fee
    Positive means the trade is favorable before sizing / risk constraints.
    """
    return fair - market_ask - kalshi_fee


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _norm_cdf(x: float) -> float:
    """Standard normal CDF via math.erfc (no scipy dependency)."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Hardcoded test inputs
    SPOT = 83_500.0
    STRIKE = 84_000.0
    T_REMAINING = 450.0   # 7.5 minutes left in the window
    SIGMA = 0.0035         # ~0.35% per 15-min candle (realistic for BTC)
    MARKET_ASK = 0.38

    fv = fair_value(SPOT, STRIKE, T_REMAINING, SIGMA)
    e = edge(fv, MARKET_ASK)

    print(f"Spot:          ${SPOT:,.2f}")
    print(f"Strike:        ${STRIKE:,.2f}")
    print(f"T remaining:   {T_REMAINING:.0f}s  ({T_REMAINING/60:.1f} min)")
    print(f"Sigma (15m):   {SIGMA:.4f}  ({SIGMA*100:.2f}%)")
    print(f"Fair value:    {fv:.4f}  ({fv*100:.2f}¢)")
    print(f"Market ask:    {MARKET_ASK:.4f}  ({MARKET_ASK*100:.2f}¢)")
    print(f"Edge:          {e:+.4f}  ({e*100:+.2f}¢)")
    print()

    # Boundary cases
    print("--- Boundary checks ---")
    print(f"Expired, spot > strike: {fair_value(84_001, 84_000, 0,   SIGMA)}")
    print(f"Expired, spot < strike: {fair_value(83_999, 84_000, 0,   SIGMA)}")
    print(f"ATM, half window:       {fair_value(84_000, 84_000, 450, SIGMA):.4f}")
    print(f"Deep ITM clamp:         {fair_value(90_000, 84_000, 450, SIGMA):.4f}")
    print(f"Deep OTM clamp:         {fair_value(70_000, 84_000, 450, SIGMA):.4f}")
