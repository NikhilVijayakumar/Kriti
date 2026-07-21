#!/usr/bin/env python3
"""
run_calculate.py — Run scoring calculation for all teams.

Loads scores from DB, runs z-score adjustment, builds leaderboard.
This is use-case 3.

Usage:
  python run_calculate.py
  python run_calculate.py --mode det
  python run_calculate.py --output-dir ./reports
"""
import argparse
import json
import os
import sys

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))
sys.path.insert(0, os.path.join(_script, "usecase-3-calculate"))

from db import get_conn, get_all_scores_as_dict, list_participants
from statistics import run_z_adjustment
from leaderboard import _load_weights, build_leaderboard, render_leaderboard_md

SYSTEM_DIR = os.path.join(_script, "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


def main():
    parser = argparse.ArgumentParser(
        description="Run scoring calculation for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both",
                        help="det=ignore semantic, sem=ignore deterministic, both=default")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: reports/)")
    args = parser.parse_args()

    conn = get_conn(args.db)
    weights_cfg = _load_weights(WEIGHTS_FILE)

    # Load scores
    aggregated = get_all_scores_as_dict(conn, args.standard, mode=args.mode)
    if not aggregated:
        print("No scores in DB. Run run_det_audit.py first.")
        sys.exit(1)

    print(f"Loaded {len(aggregated)} teams from DB")

    # Z-score adjustment
    print("Running z-score adjustment...")
    domain_stats, adjusted_scores = run_z_adjustment(aggregated)

    # Build leaderboard
    print("Building leaderboard...")
    results = build_leaderboard(adjusted_scores, weights_cfg)

    # Output directory
    out_dir = args.output_dir or os.path.join(SYSTEM_DIR, "reports")
    os.makedirs(out_dir, exist_ok=True)

    # Write outputs
    lb_json = os.path.join(out_dir, "leaderboard.json")
    with open(lb_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"  leaderboard.json -> {lb_json}")

    lb_md = os.path.join(out_dir, "leaderboard.md")
    with open(lb_md, "w", encoding="utf-8") as f:
        f.write(render_leaderboard_md(results, weights_cfg))
    print(f"  leaderboard.md   -> {lb_md}")

    stats_path = os.path.join(out_dir, "domain_stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(domain_stats, f, indent=2)
    print(f"  domain_stats.json -> {stats_path}")

    # Print summary
    print(f"\n{'='*50}")
    print(f"{'RANK':<6} {'TEAM':<30} {'SCORE':>6}")
    print(f"{'='*50}")
    medals = {1: "#1", 2: "#2", 3: "#3"}
    for r in results:
        m = medals.get(r["rank"], "  ")
        print(f" {m} {r['rank']:<4} {r['team']:<30} {r['final_score']:>6}/{weights_cfg['final_scale']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
