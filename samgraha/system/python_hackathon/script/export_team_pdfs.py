"""
export_team_pdfs.py — Merge per-team HTML reports into one PDF each.

Usage:
  python export_team_pdfs.py --reports-dir ../reports/html
  python export_team_pdfs.py --reports-dir ../reports/html --team "Goal GPT"
  python export_team_pdfs.py --reports-dir ../reports/html --output-dir ../reports/pdfs
"""
import argparse
import glob
import json
import os
import tempfile
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

load_dotenv()


def _load_team_names():
    """Read known team names from TEAMS_JSON env path."""
    teams_path = os.environ.get("PYTHON_HACKATHON_TEAMS_JSON", "")
    if not teams_path or not os.path.isfile(teams_path):
        return None
    with open(teams_path, "r", encoding="utf-8") as f:
        teams = json.load(f)
    return [t["team_name"] for t in teams if t.get("team_name")]


def collect_team_files(html_dir):
    """Group HTML files into {team_name: [summary, domain*]}.

    Files:
      global-leaderboard.html          (standalone, not in team PDFs)
      {team}-summary.html              team summary
      {team}-{domain}-{kind}.html      domain pages (30 per team)

    Anchors on team names from teams.json so hyphenated domain names
    (ai-explanations, team-workflow, data-quality) are never ambiguous.
    """
    all_files = sorted(glob.glob(os.path.join(html_dir, "*.html")))

    known_names = _load_team_names()
    if known_names is None:
        # Fallback: derive from {team}-summary.html files
        import re
        known_names = []
        for fp in all_files:
            basename = os.path.basename(fp)
            m = re.match(r"^(.+)-summary\.html$", basename)
            if m:
                known_names.append(m.group(1))

    team_files = {name: [] for name in known_names}

    # Categorize files by known team prefix (longest first to avoid collisions)
    for fp in all_files:
        basename = os.path.basename(fp)
        if basename == "global-leaderboard.html":
            continue
        for name in sorted(team_files, key=len, reverse=True):
            if basename.startswith(name + "-") or basename == name + "-summary.html":
                team_files[name].append(fp)
                break

    # Sort: team summary first, then domain pages alphabetically
    for team_name in team_files:
        pages = team_files[team_name]
        summary_file = os.path.join(html_dir, f"{team_name}-summary.html")
        summary = [summary_file] if summary_file in pages else []
        domain = sorted(f for f in pages if f not in summary)
        team_files[team_name] = summary + domain

    return {k: v for k, v in team_files.items() if v}


def html_to_pdf_batch(html_paths, output_path, timeout=30000):
    """Render a list of HTML files into a single merged PDF using Playwright."""
    if not html_paths:
        return

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_pdfs = []

            for i, html_path in enumerate(html_paths):
                file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
                page.goto(file_url, wait_until="networkidle", timeout=timeout)
                page.wait_for_timeout(500)

                temp_pdf = os.path.join(tmpdir, f"page_{i:03d}.pdf")
                page.pdf(
                    path=temp_pdf,
                    format="A4",
                    print_background=True,
                    margin={"top": "16mm", "bottom": "16mm",
                            "left": "12mm", "right": "12mm"},
                )
                temp_pdfs.append(temp_pdf)

            browser.close()

            writer = PdfWriter()
            for pdf_path in temp_pdfs:
                writer.append(pdf_path)
            with open(output_path, "wb") as f:
                writer.write(f)


def main():
    parser = argparse.ArgumentParser(
        description="Merge per-team HTML reports into one PDF each"
    )
    parser.add_argument("--reports-dir", required=True,
                        help="Path to reports/html/ directory")
    parser.add_argument("--team", default=None,
                        help="Process only this team (default: all teams)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory for PDFs (default: reports/pdfs/)")
    args = parser.parse_args()

    html_dir = os.path.abspath(args.reports_dir)
    if not os.path.isdir(html_dir):
        print(f"Error: {html_dir} is not a directory")
        return

    out_dir = args.output_dir or os.path.join(
        os.path.dirname(html_dir), "pdfs"
    )
    os.makedirs(out_dir, exist_ok=True)

    team_files = collect_team_files(html_dir)
    if not team_files:
        print(f"No team HTML files found in {html_dir}")
        return

    if args.team:
        if args.team not in team_files:
            print(f"Team '{args.team}' not found. Available: {', '.join(sorted(team_files))}")
            return
        team_files = {args.team: team_files[args.team]}

    print(f"Generating PDFs for {len(team_files)} team(s)...")

    for team_name, html_paths in sorted(team_files.items()):
        pdf_path = os.path.join(out_dir, f"{team_name}.pdf")
        print(f"  {team_name}: {len(html_paths)} pages -> {pdf_path}")
        html_to_pdf_batch(html_paths, pdf_path)

    print(f"\nDone. PDFs written to {out_dir}")


if __name__ == "__main__":
    main()
