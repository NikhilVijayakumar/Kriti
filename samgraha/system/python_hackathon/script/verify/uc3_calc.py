#!/usr/bin/env python3
"""uc3_calc.py — Verify leaderboard output has one entry per team, no None fields."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "usecase-3-calculate"))

from db import get_conn, get_all_scores_as_dict, list_participants
from statistics import run_z_adjustment
from leaderboard import _load_weights, build_leaderboard

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both")
    args = parser.parse_args()

    conn = get_conn(args.db)
    weights_cfg = _load_weights(WEIGHTS_FILE)

    aggregated = get_all_scores_as_dict(conn, args.standard, mode=args.mode)
    if not aggregated:
        print("FAIL: no scores in DB")
        sys.exit(1)

    domain_stats, adjusted_scores = run_z_adjustment(aggregated)
    results = build_leaderboard(adjusted_scores, weights_cfg)

    registered = {p["team_name"] for p in list_participants(conn, args.standard)}
    lb_teams = {r["team"] for r in results}

    errors = []
    if registered != lb_teams:
        missing = registered - lb_teams
        extra = lb_teams - registered
        if missing:
            errors.append(f"Missing from leaderboard: {missing}")
        if extra:
            errors.append(f"Extra in leaderboard (not registered): {extra}")

    for r in results:
        if r.get("final_score") is None:
            errors.append(f"{r['team']}: final_score is None")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"PASS: {len(results)} teams, all fields present")
        sys.exit(0)


if __name__ == "__main__":
    main()
