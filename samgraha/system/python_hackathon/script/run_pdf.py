#!/usr/bin/env python3
"""
run_pdf.py — Generate PDF reports for all teams.

Runs after run_html.py. Merges per-team HTML pages into one PDF each.
This is use-case 7.

Usage:
  python run_pdf.py
  python run_pdf.py --team "Goal GPT"
  python run_pdf.py --html-dir ./reports --output-dir ./reports/pdfs
"""
import argparse
import json
import os
import sys

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))

from hackathon_schema import get_conn, list_participants

SYSTEM_DIR = os.path.join(_script, "..")


def _load_team_names():
    teams_path = os.environ.get("PYTHON_HACKATHON_TEAMS_JSON", "")
    if not teams_path or not os.path.isfile(teams_path):
        return None
    with open(teams_path, "r", encoding="utf-8") as f:
        teams = json.load(f)
    return [t["team_name"] for t in teams if t.get("team_name")]


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF reports for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None, help="Process only this team")
    parser.add_argument("--html-dir", default=None,
                        help="HTML reports directory (default: reports/html/)")
    parser.add_argument("--output-dir", default=None,
                        help="PDF output directory (default: reports/pdfs/)")
    args = parser.parse_args()

    conn = get_conn(args.db)
    participants = list_participants(conn, args.standard)

    if not participants:
        print("No teams registered.")
        sys.exit(1)

    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]
        if not participants:
            print(f"Team '{args.team}' not found")
            sys.exit(1)

    reports_dir = os.path.join(SYSTEM_DIR, "reports")
    
    if args.output_dir and not args.html_dir:
        html_dir = os.path.join(os.path.dirname(args.output_dir), "html")
    else:
        html_dir = args.html_dir or os.path.join(reports_dir, "html")
        
    out_dir = args.output_dir or os.path.join(reports_dir, "pdfs")
    os.makedirs(out_dir, exist_ok=True)

    # Import PDF generation from usecase-7-pdf
    pdf_dir = os.path.join(_script, "usecase-7-pdf")
    sys.path.insert(0, pdf_dir)
    from export_team_pdfs import collect_team_files, html_to_pdf_batch

    team_files = collect_team_files(html_dir)
    if not team_files:
        print(f"No team HTML files found in {html_dir}")
        sys.exit(1)

    # Filter to requested teams
    team_names = {p["team_name"] for p in participants}
    team_files = {k: v for k, v in team_files.items() if k in team_names}

    if args.team:
        team_files = {k: v for k, v in team_files.items() if k == args.team}

    print(f"Generating PDFs for {len(team_files)} team(s)...")
    for team_name, html_paths in sorted(team_files.items()):
        pdf_path = os.path.join(out_dir, f"{team_name}.pdf")
        print(f"  {team_name}: {len(html_paths)} pages -> {pdf_path}")
        html_to_pdf_batch(html_paths, pdf_path)

    print(f"\nDone. PDFs -> {out_dir}")


if __name__ == "__main__":
    main()
