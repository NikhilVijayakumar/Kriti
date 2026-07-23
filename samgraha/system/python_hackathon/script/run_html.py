#!/usr/bin/env python3
"""
run_html.py — Generate HTML reports for all teams.

Runs after run_render.py. Produces standalone HTML files with embedded charts.
This is use-case 6.

Usage:
  python run_html.py
  python run_html.py --output-dir ./reports
"""
import argparse
import os
import sys

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))
sys.path.insert(0, os.path.join(_script, "usecase-3-calculate"))

from hackathon_schema import get_conn, get_all_scores_as_dict
from statistics import run_z_adjustment
from leaderboard import _load_weights, build_leaderboard
from render_reports import render_html_all

SYSTEM_DIR = os.path.join(_script, "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML reports for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: reports/)")
    parser.add_argument("--charts-dir", default=None,
                        help="Charts directory (default: reports/charts/)")
    args = parser.parse_args()

    conn = get_conn(args.db)
    weights_cfg = _load_weights(WEIGHTS_FILE)

    aggregated = get_all_scores_as_dict(conn, args.standard, mode=args.mode)
    if not aggregated:
        print("No scores in DB. Run run_det_audit.py first.")
        sys.exit(1)

    domain_stats, adjusted_scores = run_z_adjustment(aggregated)
    results = build_leaderboard(adjusted_scores, weights_cfg)

    out_dir = args.output_dir or os.path.join(SYSTEM_DIR, "reports")
    charts_dir = args.charts_dir or os.path.join(out_dir, "charts")

    print("Rendering HTML reports...")
    render_html_all(conn, args.standard, out_dir, results, domain_stats,
                    adjusted_scores, weights_cfg, charts_dir)

    print(f"\nDone. HTML reports -> {out_dir}")


if __name__ == "__main__":
    main()
