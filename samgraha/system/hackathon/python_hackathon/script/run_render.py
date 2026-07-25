#!/usr/bin/env python3
"""
run_render.py — Generate markdown reports + charts for all teams.

Runs after run_calculate.py. Produces markdown templates and PNG charts.
This covers use-case 5 (markdown + visualization).

Usage:
  python run_render.py
  python run_render.py --output-dir ./reports
"""
import argparse
import json
import os
import sys

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))
sys.path.insert(0, os.path.join(_script, "usecase-3-calculate"))

from hackathon_schema import get_conn, get_all_scores_as_dict, list_participants, record_visualization
from statistics import run_z_adjustment
from leaderboard import _load_weights, build_leaderboard
from render_reports import render_all, build_chart_spec
from render_charts import generate_charts

SYSTEM_DIR = os.path.join(_script, "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown reports + charts for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: reports/)")
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
    os.makedirs(out_dir, exist_ok=True)

    # Render markdown reports
    print("Rendering markdown reports...")
    render_all(conn, args.standard, out_dir, results, domain_stats,
               adjusted_scores, weights_cfg)

    # Generate charts
    print("Generating charts...")
    chart_spec = build_chart_spec(conn, results, domain_stats,
                                  adjusted_scores, weights_cfg)
    charts_dir = os.path.join(out_dir, "charts")
    written = generate_charts(chart_spec, charts_dir)

    # Record every chart actually generated, for backtrace — a future run
    # can check hackathon_schema.get_visualization() before re-rendering.
    team_ids = {p["team_name"]: p["id"] for p in list_participants(conn, args.standard)}
    for w in written:
        team_id = team_ids.get(w["team_name"]) if w["team_name"] else None
        record_visualization(conn, w["chart_key"], w["file_path"], team_id=team_id, domain_key=w["domain_key"])

    print(f"\nDone. Reports -> {out_dir}")


if __name__ == "__main__":
    main()
