"""
Flask dashboard for quant-os v2.

Three tabs:
  Live      → current market state + open hedged arbs
  Arb       → hedged_cross_arb deep-dive (distribution, persistence, min_edge slider)
  Backtest  → unified backtester, strategy-agnostic

All text is monospace, colors are a single accent (#1D9E75 teal) + muted red
(#A32D2D) for losses. See templates/index.html for the UI.
"""

import math
import os
import sqlite3
import sys
import threading
import time
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from agents.strategies.hedged_cross_arb import (  # noqa: E402
    DEFAULT_DOLLAR_SIZE_PER_LEG,
    DEFAULT_MIN_EDGE,
    HedgedArbTrader,
    evaluate_arb,
)
from agents.orchestration.paper_trader import PaperTrader  # noqa: E402
from research_db import ensure_research_schema  # noqa: E402
from agents.backtesting.unified_backtester import (  # noqa: E402
    AVAILABLE_STRATEGIES,
    BACKTEST_CACHE,
    MonteCarloBacktester,
    run as unified_run,
)

DB_PATH  = os.path.join(BASE_DIR, "data", "btc15m.db")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

APP_START = datetime.now(timezone.utc).isoformat()

_DASH_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(_DASH_DIR, "templates"))

_paper_trader      = PaperTrader(db_path=DB_PATH)
_hedged_arb_trader = HedgedArbTrader(db_path=DB_PATH)


def _daemon_loop() -> None:
    while True:
        for fn, label in ((_paper_trader.tick, "paper_trader"),
                          (_hedged_arb_trader.tick, "hedged_arb_trader")):
            try:
                fn()
            except Exception as exc:
                print(f"[dashboard] {label}.tick error: {exc}")
        time.sleep(60)


for _fn, _label in ((_paper_trader.tick, "paper_trader"),
                    (_hedged_arb_trader.tick, "hedged_arb_trader")):
    try:
        _fn()
    except Exception as exc:
        print(f"[dashboard] initial {_label}.tick error: {exc}")
threading.Thread(target=_daemon_loop, daemon=True).start()


# ── JSON safety helpers ────────────────────────────────────────────────────────

def _safe(obj):
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: _safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe(v) for v in obj]
    return obj


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_research_schema(conn)
    return conn


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ── LIVE tab ──────────────────────────────────────────────────────────────────

@app.route("/api/live/overview")
def api_live_overview():
    """
    Top-strip metrics: current cross-exchange spread, open positions, today's
    P&L across strategies, capital deployed vs idle (based on hedged arb
    $ outstanding vs $10k baseline).
    """
    conn = get_db()
    try:
        joint = conn.execute("""
            SELECT (k.yes_bid_dollars + k.yes_ask_dollars)/2.0 AS k_mid,
                   (p.up_bid + p.up_ask)/2.0                   AS p_mid,
                   k.collected_at, k.close_time
              FROM markets k
              JOIN polymarket_markets p ON p.close_time = k.close_time
             WHERE k.yes_bid_dollars IS NOT NULL
               AND p.up_bid          IS NOT NULL
             ORDER BY k.collected_at DESC LIMIT 1
        """).fetchone()

        spread_cents = (
            round((joint["k_mid"] - joint["p_mid"]) * 100, 2)
            if joint else None
        )
        close_time = joint["close_time"] if joint else None

        # Open hedged arbs
        open_ct = conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(locked_pnl), 0)"
            "  FROM hedged_arb_trades WHERE status = 'open'"
        ).fetchone()
        n_open      = int(open_ct[0] or 0)
        locked_open = float(open_ct[1] or 0.0)

        deployed = conn.execute(
            """SELECT COALESCE(SUM(kalshi_entry_price * kalshi_contracts +
                                   poly_entry_price   * poly_contracts), 0)
                 FROM hedged_arb_trades WHERE status = 'open'"""
        ).fetchone()[0]
        deployed = float(deployed or 0.0)

        # Today's P&L = realized hedged arbs + realized paper_trades (from UTC midnight)
        today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00")
        arb_pnl = conn.execute(
            """SELECT COALESCE(SUM(realized_pnl), 0) FROM hedged_arb_trades
                WHERE status='resolved' AND closed_at >= ?""",
            (today_utc,),
        ).fetchone()[0]
        paper_pnl = conn.execute(
            """SELECT COALESCE(SUM(pnl), 0) FROM paper_trades
                WHERE timestamp >= ?""",
            (today_utc,),
        ).fetchone()[0]
        today_pnl = round(float(arb_pnl or 0) + float(paper_pnl or 0), 2)

        # Paper trader account equity (sum across strategies)
        paper_equity = 0.0
        for strat in ("spread_arb", "momentum_fade"):
            r = conn.execute(
                "SELECT equity FROM paper_accounts WHERE strategy_name = ?"
                "  ORDER BY id DESC LIMIT 1",
                (strat,),
            ).fetchone()
            if r:
                paper_equity += float(r["equity"] or 0.0)
    finally:
        conn.close()

    return jsonify(_safe({
        "cross_spread_cents":  spread_cents,
        "active_close_time":   close_time,
        "open_hedge_count":    n_open,
        "locked_pnl_open":     round(locked_open, 2),
        "deployed_usd":        round(deployed, 2),
        "paper_equity_total":  round(paper_equity, 2),
        "today_pnl_usd":       today_pnl,
        "now_utc":             datetime.now(timezone.utc).isoformat(),
    }))


@app.route("/api/live/orderbook")
def api_live_orderbook():
    """
    Top-of-book bid/ask for Kalshi and Polymarket for the active window.
    Returns the single best price only (what the exchange APIs expose); the
    'top 3 levels' request in the spec can't be served without CLOB depth
    feeds we don't collect, so we return the one canonical tick plus the
    computed best-edge for both hedge directions.
    """
    conn = get_db()
    try:
        k = conn.execute("""
            SELECT ticker, close_time, yes_bid_dollars, yes_ask_dollars,
                   no_bid_dollars, no_ask_dollars, collected_at
              FROM markets
             WHERE yes_ask_dollars IS NOT NULL
             ORDER BY collected_at DESC LIMIT 1
        """).fetchone()
        p = conn.execute("""
            SELECT ticker, close_time, up_bid, up_ask, down_bid, down_ask,
                   collected_at
              FROM polymarket_markets
             WHERE close_time = ?
               AND up_ask IS NOT NULL
             ORDER BY collected_at DESC LIMIT 1
        """, (k["close_time"],)).fetchone() if k else None
    finally:
        conn.close()

    sig = None
    if k and p:
        sig_obj = evaluate_arb(
            kalshi_yes_ask=k["yes_ask_dollars"],
            kalshi_no_ask=k["no_ask_dollars"],
            poly_up_ask=p["up_ask"],
            poly_down_ask=p["down_ask"],
            min_edge=0.0,
        )
        if sig_obj is not None:
            sig = {
                "direction":       sig_obj.direction,
                "kalshi_side":     sig_obj.kalshi_side,
                "kalshi_price":    round(sig_obj.kalshi_price, 4),
                "poly_side":       sig_obj.poly_side,
                "poly_price":      round(sig_obj.poly_price, 4),
                "net_edge_cents":  round(sig_obj.net_edge * 100, 2),
                "gross_edge_cents":round(sig_obj.gross_edge * 100, 2),
                "contracts":       sig_obj.contracts,
                "locked_pnl":      round(sig_obj.locked_pnl, 2),
            }

    return jsonify(_safe({
        "kalshi":     dict(k) if k else None,
        "polymarket": dict(p) if p else None,
        "arb_signal": sig,
    }))


@app.route("/api/live/hedged")
def api_live_hedged():
    """Open hedged arb trades + last 20 resolved."""
    return jsonify(_safe(_hedged_arb_trader.get_dashboard_data()))


@app.route("/api/live/spread-history")
def api_live_spread_history():
    """Recent cross-exchange spread path for the sparkline (last N ticks)."""
    n = request.args.get("n", 120, type=int)
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT k.collected_at,
                   ((k.yes_bid_dollars + k.yes_ask_dollars)/2.0
                  - (p.up_bid + p.up_ask)/2.0) AS spread
              FROM markets k
              JOIN polymarket_markets p
                ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
                 = strftime('%Y-%m-%dT%H:%M', p.collected_at)
             WHERE k.yes_bid_dollars IS NOT NULL
               AND p.up_bid          IS NOT NULL
             ORDER BY k.collected_at DESC LIMIT ?
        """, (n,)).fetchall()
    finally:
        conn.close()
    data = [{"ts": r["collected_at"], "spread_cents": round(r["spread"] * 100, 3)}
            for r in reversed(rows)]
    return jsonify(data)


# ── ARB tab ───────────────────────────────────────────────────────────────────

@app.route("/api/arb/histogram")
def api_arb_histogram():
    """Net-edge distribution across every historical joint tick (0.5¢ buckets)."""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT k.yes_ask_dollars, k.no_ask_dollars,
                   p.up_ask, p.down_ask
              FROM markets k
              JOIN polymarket_markets p ON p.close_time = k.close_time
             WHERE k.yes_ask_dollars IS NOT NULL
               AND k.no_ask_dollars  IS NOT NULL
               AND p.up_ask          IS NOT NULL
               AND p.down_ask        IS NOT NULL
        """).fetchall()
    finally:
        conn.close()

    bucket_size = 0.005                          # 0.5¢
    hist: dict[float, int] = {}
    for r in rows:
        sig = evaluate_arb(
            kalshi_yes_ask=r["yes_ask_dollars"],
            kalshi_no_ask=r["no_ask_dollars"],
            poly_up_ask=r["up_ask"],
            poly_down_ask=r["down_ask"],
            min_edge=-10.0,
        )
        if sig is None:
            continue
        bucket = round(round(sig.net_edge / bucket_size) * bucket_size, 4)
        hist[bucket] = hist.get(bucket, 0) + 1

    buckets = sorted(hist.keys())
    return jsonify({
        "buckets_cents": [round(b * 100, 2) for b in buckets],
        "counts":        [hist[b]           for b in buckets],
        "total_ticks":   len(rows),
    })


@app.route("/api/arb/persistence")
def api_arb_persistence():
    """
    For each close_time window, measure how many consecutive ticks had a
    ≥ min_edge opportunity before the spread collapsed. Returns the
    distribution of run-lengths (in 60s ticks) — a short run means the
    opportunity was fleeting.
    """
    min_edge = request.args.get("min_edge", 0.01, type=float)
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT k.close_time, k.collected_at,
                   k.yes_ask_dollars, k.no_ask_dollars,
                   p.up_ask, p.down_ask
              FROM markets k
              JOIN polymarket_markets p ON p.close_time = k.close_time
             WHERE k.yes_ask_dollars IS NOT NULL
               AND k.no_ask_dollars  IS NOT NULL
               AND p.up_ask          IS NOT NULL
               AND p.down_ask        IS NOT NULL
             ORDER BY k.close_time, k.collected_at
        """).fetchall()
    finally:
        conn.close()

    run_lengths: list[int] = []
    current_window: str | None = None
    run = 0
    for r in rows:
        ct = r["close_time"]
        if ct != current_window:
            if run > 0:
                run_lengths.append(run)
            current_window = ct
            run = 0
        sig = evaluate_arb(
            kalshi_yes_ask=r["yes_ask_dollars"],
            kalshi_no_ask=r["no_ask_dollars"],
            poly_up_ask=r["up_ask"],
            poly_down_ask=r["down_ask"],
            min_edge=min_edge,
        )
        if sig is not None:
            run += 1
        else:
            if run > 0:
                run_lengths.append(run)
            run = 0
    if run > 0:
        run_lengths.append(run)

    # Bucket by run-length
    dist: dict[int, int] = {}
    for r in run_lengths:
        dist[r] = dist.get(r, 0) + 1
    sorted_keys = sorted(dist.keys())
    return jsonify({
        "run_lengths_ticks": sorted_keys,
        "counts":            [dist[k] for k in sorted_keys],
        "n_runs":            len(run_lengths),
        "min_edge":          min_edge,
    })


@app.route("/api/arb/daily-pnl")
def api_arb_daily_pnl():
    """Realized P&L per UTC day since the strategy went live."""
    conn = get_db()
    try:
        rows = conn.execute("""
            SELECT substr(closed_at, 1, 10)                AS day,
                   ROUND(SUM(COALESCE(realized_pnl, 0)),4) AS pnl,
                   COUNT(*)                                AS n_trades
              FROM hedged_arb_trades
             WHERE status = 'resolved'
             GROUP BY day
             ORDER BY day ASC
        """).fetchall()
    finally:
        conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/arb/top-trades")
def api_arb_top_trades():
    """Top 10 biggest arbs from the last 7 days, by locked_pnl."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT id, opened_at, close_time, direction, kalshi_side, kalshi_entry_price,
                      poly_side, poly_entry_price, kalshi_contracts,
                      gross_edge, net_edge_at_entry, fees_paid,
                      locked_pnl, realized_pnl, status
                 FROM hedged_arb_trades
                WHERE opened_at >= ?
                ORDER BY locked_pnl DESC
                LIMIT 10""",
            (cutoff,),
        ).fetchall()
    finally:
        conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/arb/live-backtest")
def api_arb_live_backtest():
    """
    Recruiter showcase: re-run the hedged_cross_arb historical backtest with
    the user's min_edge. Returns trimmed summary (no full trade list) since
    the client only needs the headline numbers for the slider.
    """
    min_edge = request.args.get("min_edge", 0.01, type=float)
    size     = request.args.get("dollar_size", DEFAULT_DOLLAR_SIZE_PER_LEG, type=float)
    result = unified_run(
        "hedged_cross_arb",
        min_edge=min_edge,
        dollar_size_per_leg=size,
        persist=False,
    )
    trimmed = {
        k: v for k, v in result.items()
        if k not in ("trades", "equity_curve", "edge_histogram")
    }
    return jsonify(_safe(trimmed))


# ── BACKTEST tab ──────────────────────────────────────────────────────────────

_mc_backtester = MonteCarloBacktester()


@app.route("/api/backtest/strategies")
def api_backtest_strategies():
    return jsonify({
        "available": AVAILABLE_STRATEGIES,
        "default":   "hedged_cross_arb",
    })


@app.route("/api/backtest/run")
def api_backtest_run():
    """
    Unified backtest endpoint. Query params:
        strategy       one of AVAILABLE_STRATEGIES
        min_edge       (hedged_cross_arb only)
        dollar_size    (hedged_cross_arb only)
        n              MC simulations (spread_arb / momentum_fade)
        lookback       rows (spread_arb / momentum_fade)
    """
    strategy = request.args.get("strategy", "hedged_cross_arb")
    if strategy not in AVAILABLE_STRATEGIES:
        return jsonify({"error": f"Unknown strategy. Available: {AVAILABLE_STRATEGIES}"}), 400

    params = {}
    if strategy == "hedged_cross_arb":
        params["min_edge"]            = request.args.get("min_edge", 0.01, type=float)
        params["dollar_size_per_leg"] = request.args.get("dollar_size", 500.0, type=float)
        params["persist"]             = bool(request.args.get("persist", 0, type=int))
    elif strategy in ("spread_arb", "momentum_fade"):
        params["n_simulations"] = request.args.get("n", 500, type=int)
        params["lookback_rows"] = request.args.get("lookback", 250, type=int)

    try:
        result = unified_run(strategy, **params)
    except Exception as exc:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(exc)}), 500
    return jsonify(_safe(result))


@app.route("/api/backtest/<strategy>")
def api_backtest_legacy(strategy):
    """Legacy async endpoint preserved for the MC strategies' fan chart."""
    if strategy not in ("spread_arb", "momentum_fade"):
        return jsonify({"error": "legacy endpoint supports only spread_arb / momentum_fade"}), 400
    n        = request.args.get("n",        500, type=int)
    lookback = request.args.get("lookback", 250, type=int)
    refresh  = request.args.get("refresh",  0,   type=int)
    cached = BACKTEST_CACHE.get(strategy)
    if refresh or cached is None:
        _mc_backtester.run_async(strategy, n_simulations=n, lookback_rows=lookback)
        return jsonify({"strategy": strategy, "status": "running"})
    return jsonify(_safe(cached))


# ── Collection health (stays — small, useful, shown in Live header) ───────────

@app.route("/api/health")
def api_health():
    conn = get_db()
    now      = datetime.now(timezone.utc)
    try:
        def stats(table):
            last = conn.execute(
                f"SELECT collected_at FROM {table} ORDER BY collected_at DESC LIMIT 1"
            ).fetchone()
            last_ts = last[0] if last else None
            seconds_since = None
            if last_ts:
                try:
                    dt = datetime.fromisoformat(last_ts)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    seconds_since = round((now - dt).total_seconds())
                except Exception:
                    pass
            status = (
                "offline" if seconds_since is None else
                "ok"      if seconds_since < 180   else
                "stale"   if seconds_since < 600   else
                "offline"
            )
            return {"status": status, "last_row": last_ts,
                    "seconds_since": seconds_since}
        return jsonify({
            "kalshi":      stats("markets"),
            "polymarket":  stats("polymarket_markets"),
            "now_utc":     now.isoformat(),
        })
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5050, use_reloader=False)
