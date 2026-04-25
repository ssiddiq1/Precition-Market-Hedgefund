"""
calibration.py — probability calibration report for forward paper predictions.

Reads resolved rows from paper_model_predictions and computes:
  - Per-strategy accuracy and mean PnL
  - Calibration table: bucketed mean(prob_up) vs actual win rate

Usage:
    python agents/calibration.py [--db-path PATH] [--strategy NAME] [--buckets N]
"""

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from research_db import DB_PATH, get_conn


def calibration_report(db_path: str, strategy: str | None = None, n_buckets: int = 10) -> None:
    conn = get_conn(db_path)
    try:
        where = "status = 'resolved' AND prob_up IS NOT NULL AND actual_direction IS NOT NULL"
        params: list = []
        if strategy:
            where += " AND strategy_name = ?"
            params.append(strategy)

        rows = conn.execute(
            f"""SELECT strategy_name, prob_up, actual_direction, correct, pnl
                FROM paper_model_predictions
                WHERE {where}
                ORDER BY strategy_name, target_timestamp""",
            params,
        ).fetchall()

        if not rows:
            print("No resolved predictions found — calibration report is empty.")
            return

        # ── Per-strategy summary ──────────────────────────────────────────
        by_strategy: dict[str, list] = {}
        for r in rows:
            by_strategy.setdefault(r["strategy_name"], []).append(r)

        print(f"{'Strategy':<30} {'N':>5} {'Accuracy':>9} {'Mean PnL':>10} {'Total PnL':>10}")
        print("-" * 68)
        for strat, items in sorted(by_strategy.items()):
            n        = len(items)
            accuracy = sum(int(r["correct"] or 0) for r in items) / n
            mean_pnl = sum(float(r["pnl"] or 0.0) for r in items) / n
            total    = sum(float(r["pnl"] or 0.0) for r in items)
            print(f"{strat:<30} {n:>5} {accuracy:>9.3f} {mean_pnl:>10.4f} {total:>10.4f}")

        # ── Calibration table (all strategies combined) ───────────────────
        print()
        print("Calibration (prob_up bucket → actual win rate):")
        bucket_size = 1.0 / n_buckets
        buckets: dict[int, list] = {i: [] for i in range(n_buckets)}
        for r in rows:
            p   = float(r["prob_up"])
            idx = min(int(p / bucket_size), n_buckets - 1)
            buckets[idx].append(int(r["actual_direction"] or 0))

        print(f"  {'Bucket':>14}  {'N':>5}  {'Mean prob':>10}  {'Actual win%':>12}  {'Gap':>8}")
        print("  " + "-" * 56)
        for i in range(n_buckets):
            lo   = i * bucket_size
            hi   = lo + bucket_size
            vals = buckets[i]
            if not vals:
                continue
            mean_prob   = lo + bucket_size / 2
            actual_rate = sum(vals) / len(vals)
            gap         = actual_rate - mean_prob
            bar         = ("+" if gap >= 0 else "") + f"{gap:+.3f}"
            print(
                f"  [{lo:.2f}, {hi:.2f})  {len(vals):>5}  {mean_prob:>10.3f}"
                f"  {actual_rate:>12.3f}  {bar:>8}"
            )

        # ── Brier score ───────────────────────────────────────────────────
        brier = sum(
            (float(r["prob_up"]) - float(r["actual_direction"])) ** 2
            for r in rows
        ) / len(rows)
        print()
        print(f"Brier score (lower = better): {brier:.4f}  (baseline naive=0.25)")

    finally:
        conn.close()


def brier_score_summary(db_path: str, strategy: str | None = None) -> dict:
    """Return {brier_score, n_predictions, baseline_brier} for the API, or brier_score=None if no data."""
    conn = get_conn(db_path)
    try:
        where = "status = 'resolved' AND prob_up IS NOT NULL AND actual_direction IS NOT NULL"
        params: list = []
        if strategy:
            where += " AND strategy_name = ?"
            params.append(strategy)
        rows = conn.execute(
            f"SELECT prob_up, actual_direction FROM paper_model_predictions WHERE {where}",
            params,
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return {"brier_score": None, "n_predictions": 0, "baseline_brier": 0.25}

    brier = sum(
        (float(r["prob_up"]) - float(r["actual_direction"])) ** 2
        for r in rows
    ) / len(rows)
    return {"brier_score": round(brier, 4), "n_predictions": len(rows), "baseline_brier": 0.25}


def reliability_diagram_data(
    db_path: str,
    strategy: str | None = None,
    n_bins: int = 10,
) -> list[dict]:
    """Return per-bin calibration data for a reliability diagram chart.

    Each element: {bin_center, predicted_prob, actual_freq, count}
    Empty bins are omitted.
    """
    conn = get_conn(db_path)
    try:
        where = "status = 'resolved' AND prob_up IS NOT NULL AND actual_direction IS NOT NULL"
        params: list = []
        if strategy:
            where += " AND strategy_name = ?"
            params.append(strategy)
        rows = conn.execute(
            f"SELECT prob_up, actual_direction FROM paper_model_predictions WHERE {where}",
            params,
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return []

    bin_size = 1.0 / n_bins
    bins: dict[int, list[float]] = {i: [] for i in range(n_bins)}
    bins_probs: dict[int, list[float]] = {i: [] for i in range(n_bins)}
    for r in rows:
        p   = float(r["prob_up"])
        idx = min(int(p / bin_size), n_bins - 1)
        bins[idx].append(float(r["actual_direction"] or 0))
        bins_probs[idx].append(p)

    result = []
    for i in range(n_bins):
        lo   = i * bin_size
        hi   = lo + bin_size
        vals = bins[i]
        if not vals:
            continue
        predicted_prob = sum(bins_probs[i]) / len(bins_probs[i])
        result.append({
            "bin_center":     round(lo + bin_size / 2, 3),
            "predicted_prob": round(predicted_prob, 4),
            "actual_freq":    round(sum(vals) / len(vals), 4),
            "count":          len(vals),
        })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Probability calibration report")
    parser.add_argument("--db-path",  default=DB_PATH)
    parser.add_argument("--strategy", default=None, help="Filter to one strategy name")
    parser.add_argument("--buckets",  type=int, default=10)
    args = parser.parse_args()
    calibration_report(args.db_path, args.strategy, args.buckets)


if __name__ == "__main__":
    main()
