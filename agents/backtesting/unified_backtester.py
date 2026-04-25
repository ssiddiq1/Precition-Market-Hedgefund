"""
unified_backtester.py — single backtester engine for every strategy.

Dispatches by strategy name. Each dispatcher returns a dict with a common
shape (see RESULT_SCHEMA below) so the dashboard can render any strategy's
output without strategy-specific branches.

Strategies:
    spread_arb, momentum_fade     → Monte Carlo block-bootstrap (legacy)
    hedged_cross_arb              → deterministic historical walk
    ml_probability_threshold,
    cross_market_rf               → ML forward-prediction walk (reads
                                    paper_model_predictions + labels)

The old backtester.py and monte_carlo.py continue to exist as thin shims
that re-export from this module for CLI compatibility.
"""

from __future__ import annotations

import os
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Optional

import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH  = os.path.join(BASE_DIR, "data", "btc15m.db")

# ── MC backtester constants (shared with historical spread_arb/momentum_fade) ─
SLIPPAGE        = 0.0015
INITIAL_EQUITY  = 10_000.0
ALLOC_BASE      = 500.0
MIN_CONFIDENCE  = 0.50
BLOCK_SIZE      = 4

# Thread-safe module-level result cache (used by the Backtest tab for async runs)
BACKTEST_CACHE: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()


# ══════════════════════════════════════════════════════════════════════════════
# Shared evaluator helpers (ported from the v1 backtester.py)
# ══════════════════════════════════════════════════════════════════════════════

def _eval_spread_arb(row: dict) -> dict | None:
    yb, ya = row.get("yes_bid_dollars"), row.get("yes_ask_dollars")
    ub, ua = row.get("up_bid"),          row.get("up_ask")
    if None in (yb, ya, ub, ua):
        return None
    k_mid, p_mid = (yb + ya) / 2.0, (ub + ua) / 2.0
    spread = k_mid - p_mid
    if abs(spread) <= 0.03:
        return None
    entry = ua if spread > 0 else ya
    return {
        "direction":   "YES",
        "entry_price": entry,
        "confidence":  min(abs(spread) / 0.10, 1.0),
    }


def _eval_momentum_fade(recent4: list[dict]) -> dict | None:
    if len(recent4) < 4:
        return None
    first_ub, last_ub = recent4[0].get("up_bid"), recent4[-1].get("up_bid")
    if first_ub is None or last_ub is None:
        return None
    delta = last_ub - first_ub
    if abs(delta) <= 0.08:
        return None
    if delta > 0:
        entry = recent4[-1].get("down_bid") or (1.0 - last_ub)
        return {"direction": "NO",  "entry_price": entry, "confidence": min(abs(delta) / 0.15, 1.0)}
    entry = recent4[-1].get("up_ask") or last_ub
    return {"direction": "YES", "entry_price": entry, "confidence": min(abs(delta) / 0.15, 1.0)}


def _momentum_fade_window(rows: list[dict], i: int) -> dict | None:
    target_ct = rows[i].get("close_time")
    if not target_ct:
        return None
    window = [r for r in rows[max(0, i - 3): i + 1] if r.get("close_time") == target_ct]
    if len(window) < 4:
        return None
    return _eval_momentum_fade(window)


_MC_EVALUATORS = {
    "spread_arb":    lambda rows, i: _eval_spread_arb(rows[i]),
    "momentum_fade": _momentum_fade_window,
}

MC_VALID_STRATEGIES = list(_MC_EVALUATORS)


# ══════════════════════════════════════════════════════════════════════════════
# Monte Carlo bootstrap engine
# ══════════════════════════════════════════════════════════════════════════════

class MonteCarloBacktester:
    """
    Block-bootstrap Monte Carlo backtester for rule-based strategies with
    continuous confidence signals. Paths are built from historical joined
    Kalshi/Polymarket ticks; PnL uses a binary-contract proxy based on the
    next tick's last_price_dollars.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _load_rows(self, lookback: int) -> list[dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT k.collected_at, k.close_time,
                   k.yes_bid_dollars, k.yes_ask_dollars,
                   k.no_bid_dollars,  k.no_ask_dollars,
                   k.last_price_dollars, k.volume_24h_fp,
                   p.up_bid, p.up_ask, p.down_bid, p.down_ask,
                   p.last_price AS poly_last_price, p.volume_24h
              FROM markets k
              JOIN polymarket_markets p
                ON strftime('%Y-%m-%dT%H:%M', k.collected_at)
                 = strftime('%Y-%m-%dT%H:%M', p.collected_at)
             WHERE k.yes_bid_dollars BETWEEN 0.05 AND 0.95
               AND k.yes_ask_dollars BETWEEN 0.05 AND 0.95
               AND p.up_bid          BETWEEN 0.05 AND 0.95
               AND p.up_ask          BETWEEN 0.05 AND 0.95
             ORDER BY k.collected_at DESC LIMIT ?
        """, (lookback,)).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]

    def _block_bootstrap(self, rows: list[dict]) -> list[dict]:
        n      = len(rows)
        blocks = [rows[i: i + BLOCK_SIZE] for i in range(n - BLOCK_SIZE + 1)]
        if not blocks:
            return rows[:]
        n_blocks = (n + BLOCK_SIZE - 1) // BLOCK_SIZE
        chosen   = np.random.randint(0, len(blocks), size=n_blocks)
        path: list[dict] = []
        for idx in chosen:
            path.extend(blocks[int(idx)])
        return path[:n]

    def _simulate_path(self, rows: list[dict], eval_fn) -> tuple[list[float], list[float]]:
        equity = INITIAL_EQUITY
        curve  = [equity]
        pnls: list[float] = []
        for i in range(len(rows) - 1):
            sig = eval_fn(rows, i)
            if sig is None or sig.get("confidence", 0) <= MIN_CONFIDENCE:
                curve.append(equity); continue
            entry_raw = sig.get("entry_price")
            if entry_raw is None or entry_raw <= 0:
                curve.append(equity); continue
            entry_adj = entry_raw * (1.0 + SLIPPAGE)
            allocated = min(sig["confidence"] * ALLOC_BASE, equity)
            if allocated <= 0:
                curve.append(equity); continue
            next_last = rows[i + 1].get("last_price_dollars") or 0.5
            resolved_yes = next_last >= 0.5
            won = (resolved_yes and sig["direction"] == "YES") or (not resolved_yes and sig["direction"] == "NO")
            raw_pnl = allocated * (1.0 - entry_adj) if won else allocated * (-entry_adj)
            pnl = max(min(raw_pnl, allocated), -allocated)
            equity = max(equity + pnl, 0.0)
            pnls.append(pnl); curve.append(equity)
        return curve, pnls

    @staticmethod
    def _max_drawdown(curve: list[float]) -> float:
        peak, mdd = curve[0] if curve else INITIAL_EQUITY, 0.0
        for e in curve:
            if e > peak:
                peak = e
            if peak > 0:
                dd = (peak - e) / peak
                if dd > mdd:
                    mdd = dd
        return mdd

    def run(
        self,
        strategy_name: str,
        n_simulations: int = 500,
        lookback_rows: int = 200,
    ) -> dict:
        if strategy_name not in _MC_EVALUATORS:
            err = {"strategy": strategy_name,
                   "error": f"Unknown strategy '{strategy_name}'. Valid: {MC_VALID_STRATEGIES}"}
            with _CACHE_LOCK:
                BACKTEST_CACHE[strategy_name] = err
            return err

        rows = self._load_rows(lookback_rows)
        if len(rows) < BLOCK_SIZE * 2:
            err = {"strategy": strategy_name,
                   "error": f"Only {len(rows)} joined rows (need ≥ {BLOCK_SIZE*2}).",
                   "n_rows_available": len(rows)}
            with _CACHE_LOCK:
                BACKTEST_CACHE[strategy_name] = err
            return err

        eval_fn = _MC_EVALUATORS[strategy_name]
        final_eqs, dds, pnls_all, wins, sampled = [], [], [], [], []
        sample_every = max(1, n_simulations // 50)
        for sim_i in range(n_simulations):
            path = self._block_bootstrap(rows)
            curve, pnls = self._simulate_path(path, eval_fn)
            final_eqs.append(curve[-1])
            dds.append(self._max_drawdown(curve))
            pnls_all.extend(pnls)
            wins.extend(1 if p > 0 else 0 for p in pnls)
            if sim_i % sample_every == 0:
                sampled.append(curve)

        fe, dd, pnl_arr = np.array(final_eqs), np.array(dds), np.array(pnls_all)
        pnl_std = float(np.std(pnl_arr))
        sharpe = float(np.mean(pnl_arr) / pnl_std * np.sqrt(252)) if pnl_std > 0 and len(pnl_arr) else 0.0
        win_rate = float(np.mean(wins)) if wins else 0.0

        result = {
            "strategy":            strategy_name,
            "engine":              "monte_carlo_block_bootstrap",
            "n_simulations":       n_simulations,
            "n_rows":              len(rows),
            "n_trades_total":      len(pnls_all),
            "median_final_equity": round(float(np.median(fe)), 2),
            "p10_equity":          round(float(np.percentile(fe, 10)), 2),
            "p90_equity":          round(float(np.percentile(fe, 90)), 2),
            "max_drawdown_median": round(float(np.median(dd)), 4),
            "win_rate":            round(win_rate, 4),
            "sharpe":              round(sharpe, 4),
            "equity_paths":        [p for p in sampled[:50]],
            "run_at":              datetime.now(timezone.utc).isoformat(),
            "status":              "done",
        }

        with _CACHE_LOCK:
            BACKTEST_CACHE[strategy_name] = result
        return result

    def run_async(
        self,
        strategy_name: str,
        n_simulations: int = 500,
        lookback_rows: int = 200,
    ) -> Optional[threading.Thread]:
        with _CACHE_LOCK:
            BACKTEST_CACHE[strategy_name] = {"strategy": strategy_name, "status": "running"}

        def _worker():
            try:
                self.run(strategy_name, n_simulations, lookback_rows)
            except Exception as exc:
                import traceback
                with _CACHE_LOCK:
                    BACKTEST_CACHE[strategy_name] = {
                        "strategy": strategy_name, "status": "error",
                        "error": str(exc), "traceback": traceback.format_exc(),
                    }

        t = threading.Thread(target=_worker, daemon=True, name=f"mc-backtest-{strategy_name}")
        t.start()
        return t


# ══════════════════════════════════════════════════════════════════════════════
# Dispatch: unified.run(strategy, **kwargs) → dict
# ══════════════════════════════════════════════════════════════════════════════

def _run_hedged_cross_arb(db_path: str, **params) -> dict:
    from hedged_arb_backtest import run_backtest  # local import to avoid cycle
    min_edge = float(params.get("min_edge", 0.01))
    size     = float(params.get("dollar_size_per_leg", 500.0))
    return run_backtest(
        db_path=db_path,
        min_edge=min_edge,
        dollar_size_per_leg=size,
        persist=bool(params.get("persist", False)),
    )


def _run_mc(db_path: str, strategy: str, **params) -> dict:
    n        = int(params.get("n_simulations", 500))
    lookback = int(params.get("lookback_rows",  200))
    return MonteCarloBacktester(db_path).run(strategy, n_simulations=n, lookback_rows=lookback)


def _run_ml(db_path: str, strategy: str, **params) -> dict:
    """Summary read of paper_model_predictions for an ML strategy."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """SELECT prediction_timestamp, target_timestamp, prob_up, action,
                      position, status, actual_direction, pnl, cumulative_pnl
                 FROM paper_model_predictions
                WHERE strategy_name = ?
                ORDER BY target_timestamp ASC""",
            (strategy,),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return {"strategy": strategy, "engine": "ml_forward_walk",
                "error": f"No paper_model_predictions for '{strategy}'.",
                "n_predictions": 0}

    resolved = [r for r in rows if r["status"] == "resolved" and r["pnl"] is not None]
    pnls  = [float(r["pnl"]) for r in resolved]
    wins  = sum(1 for p in pnls if p > 0)
    total = sum(pnls)
    return {
        "strategy":         strategy,
        "engine":           "ml_forward_walk",
        "n_predictions":    len(rows),
        "n_resolved":       len(resolved),
        "cumulative_pnl":   round(total, 4),
        "win_rate":         round(wins / len(resolved), 4) if resolved else None,
        "recent":           [dict(r) for r in rows[-20:]],
        "run_at":           datetime.now(timezone.utc).isoformat(),
    }


_DISPATCH = {
    "hedged_cross_arb":         lambda db, **p: _run_hedged_cross_arb(db, **p),
    "spread_arb":               lambda db, **p: _run_mc(db, "spread_arb",    **p),
    "momentum_fade":            lambda db, **p: _run_mc(db, "momentum_fade", **p),
    "ml_probability_threshold": lambda db, **p: _run_ml(db, "ml_probability_threshold", **p),
    "cross_market_rf":          lambda db, **p: _run_ml(db, "cross_market_rf",          **p),
}

AVAILABLE_STRATEGIES = list(_DISPATCH.keys())


def run(strategy: str, db_path: str = DB_PATH, **params) -> dict:
    fn = _DISPATCH.get(strategy)
    if fn is None:
        return {"strategy": strategy,
                "error": f"Unknown strategy. Available: {AVAILABLE_STRATEGIES}"}
    return fn(db_path, **params)


# ── CLI smoke test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse, json as _json
    ap = argparse.ArgumentParser(description="Unified backtester")
    ap.add_argument("strategy", choices=AVAILABLE_STRATEGIES)
    ap.add_argument("--n",        type=int, default=500)
    ap.add_argument("--lookback", type=int, default=200)
    ap.add_argument("--min-edge", type=float, default=0.01)
    ap.add_argument("--size",     type=float, default=500.0)
    args = ap.parse_args()
    result = run(
        args.strategy,
        n_simulations=args.n, lookback_rows=args.lookback,
        min_edge=args.min_edge, dollar_size_per_leg=args.size,
    )
    trimmed = {k: v for k, v in result.items()
               if k not in ("equity_paths", "trades", "equity_curve", "edge_histogram", "recent")}
    print(_json.dumps(trimmed, indent=2, default=str))
