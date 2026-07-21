"""
run_reporting.py — Report-time pipeline: load from DB, z-score, leaderboard, render.

Usage:
  python run_reporting.py --standard python_hackathon
  python run_reporting.py --standard python_hackathon --output-dir ./reports
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "common"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "usecase-3-calculate"))

from db import get_conn, get_all_scores_as_dict, list_participants, get_domain_scores
from statistics import run_z_adjustment
from leaderboard import _load_weights, build_leaderboard, render_leaderboard_md
from render_reports import render_all, build_chart_spec, render_html_all

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


def main():
    parser = argparse.ArgumentParser(
        description="Report-time pipeline: DB -> z-score -> leaderboard -> markdown"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--output-dir", default=None, help="Output directory for reports (default: reports/)")
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both",
                        help="det=ignore semantic scores, sem=ignore deterministic, both=default")
    args = parser.parse_args()

    conn = get_conn(args.db)
    weights_cfg = _load_weights(WEIGHTS_FILE)

    # Load aggregated scores from DB
    aggregated = get_all_scores_as_dict(conn, args.standard, mode=args.mode)
    if not aggregated:
        print("No scores found in DB. Run run_hackathon.py first.")
        return

    print(f"Loaded {len(aggregated)} participants from DB")

    # Phase 2: Z-score adjustment
    print("Running Z-score adjustment...")
    domain_stats, adjusted_scores = run_z_adjustment(aggregated)

    # Phase 3: Build leaderboard
    print("Building leaderboard...")
    results = build_leaderboard(adjusted_scores, weights_cfg)

    # Output directory
    out_dir = args.output_dir or os.path.join(SYSTEM_DIR, "reports")
    os.makedirs(out_dir, exist_ok=True)

    # Write leaderboard JSON
    lb_json_path = os.path.join(out_dir, "leaderboard.json")
    with open(lb_json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Leaderboard JSON -> {lb_json_path}")

    # Write leaderboard markdown
    lb_md_path = os.path.join(out_dir, "leaderboard.md")
    md = render_leaderboard_md(results, weights_cfg)
    with open(lb_md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Leaderboard MD   -> {lb_md_path}")

    # Write domain stats
    stats_path = os.path.join(out_dir, "domain_stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(domain_stats, f, indent=2)
    print(f"Domain stats     -> {stats_path}")

    # Render all markdown reports
    print("\nRendering markdown reports...")
    render_all(conn, args.standard, out_dir, results, domain_stats, adjusted_scores, weights_cfg)

    # Generate charts
    print("\nGenerating charts...")
    chart_spec = build_chart_spec(conn, results, domain_stats, adjusted_scores, weights_cfg)
    from render_charts import generate_charts
    charts_dir = os.path.join(out_dir, "charts")
    generate_charts(chart_spec, charts_dir)

    # Render HTML reports (standalone, with embedded charts)
    print("\nRendering HTML reports...")
    render_html_all(conn, args.standard, out_dir, results, domain_stats,
                    adjusted_scores, weights_cfg, charts_dir)

    # Print summary
    print(f"\n{'='*50}")
    print(f"{'RANK':<6} {'TEAM':<30} {'SCORE':>6}")
    print(f"{'='*50}")
    medals = {1: "\U0001f947", 2: "\U0001f948", 3: "\U0001f949"}
    for r in results:
        m = medals.get(r["rank"], "  ")
        print(f"{m} {r['rank']:<4} {r['team']:<30} {r['final_score']:>6}/{weights_cfg['final_scale']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
