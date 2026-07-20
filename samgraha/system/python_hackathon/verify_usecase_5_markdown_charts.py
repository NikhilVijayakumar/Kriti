#!/usr/bin/env python3
"""verify_usecase_5_markdown_charts.py — Verify markdown output and chart PNGs exist."""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "script"))

from db import get_conn, list_participants, get_domain_scores

ALL_DOMAINS = [
    "infrastructure", "engineering", "testing", "documentation",
    "security", "mlops", "runtime", "team-workflow",
    "data-quality", "ai-explanations",
]


def check_md_tokens(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return re.findall(r"\{\{[^}]*\}\}", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--reports-dir", default=None)
    args = parser.parse_args()

    conn = get_conn(args.db)
    reports_dir = args.reports_dir or os.path.join(os.path.dirname(__file__), "..", "reports")

    participants = list_participants(conn, args.standard)
    errors = []

    # Check leaderboard.md
    lb_path = os.path.join(reports_dir, "leaderboard.md")
    if not os.path.isfile(lb_path):
        errors.append("leaderboard.md missing")
    elif os.path.getsize(lb_path) == 0:
        errors.append("leaderboard.md empty")
    else:
        tokens = check_md_tokens(lb_path)
        if tokens:
            errors.append(f"leaderboard.md has unrendered tokens: {tokens[:3]}")

    # Check chart PNGs
    charts_dir = os.path.join(reports_dir, "charts")
    expected_charts = [
        "overall-ranking.png",
        "team-comparison.png",
        "team-radar.png",
        "domain-distribution.png",
        "top5-radar.png",
        "score-distribution.png",
        "deterministic-vs-semantic.png",
    ]
    for cname in expected_charts:
        cpath = os.path.join(charts_dir, cname)
        if not os.path.isfile(cpath):
            errors.append(f"Chart missing: {cname}")
        elif os.path.getsize(cpath) == 0:
            errors.append(f"Chart empty: {cname}")

    # Check per-team markdown files
    for p in participants:
        tname = p["team_name"]
        team_dir = os.path.join(reports_dir, tname.replace(" ", "_"))
        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}

        for d in ALL_DOMAINS:
            if d not in data_domains:
                continue
            for kind in ("deterministic", "semantic", "summary"):
                fname = f"{tname.replace(' ', '_')}-{d}-{kind}.md"
                fpath = os.path.join(team_dir, fname)
                if not os.path.isfile(fpath):
                    errors.append(f"{tname}/{d}/{kind}: MD missing")
                elif os.path.getsize(fpath) == 0:
                    errors.append(f"{tname}/{d}/{kind}: MD empty")
                else:
                    tokens = check_md_tokens(fpath)
                    if tokens:
                        errors.append(f"{tname}/{d}/{kind}: unrendered tokens {tokens[:2]}")

        summary_fname = f"{tname.replace(' ', '_')}-team-summary.md"
        summary_path = os.path.join(team_dir, summary_fname)
        if not os.path.isfile(summary_path):
            errors.append(f"{tname}: team-summary.md missing")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors[:15]:
            print(f"  - {e}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more")
        sys.exit(1)
    else:
        print(f"PASS: markdown + charts OK for {len(participants)} teams")
        sys.exit(0)


if __name__ == "__main__":
    main()
