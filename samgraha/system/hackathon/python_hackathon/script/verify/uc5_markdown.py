#!/usr/bin/env python3
"""uc5_markdown.py — Verify markdown output and chart PNGs exist."""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

from db import get_conn, list_participants, get_domain_scores, get_canonical_domains

ALL_DOMAINS = get_canonical_domains()

# dir_name prefix -> (canonical domain, hyphenated template-filename prefix)
_DIR_NAMES = [
    "01-infrastructure", "02-engineering", "03-testing",
    "04-documentation", "05-security", "06-mlops",
    "07-runtime", "08-team-workflow", "09-data-quality",
    "10-ai-explanations",
]
DOMAIN_TO_PREFIX = {
    dn.split("-", 1)[1].replace("-", "_"): dn.split("-", 1)[1]
    for dn in _DIR_NAMES
}


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
    reports_dir = args.reports_dir or os.path.join(
        os.path.dirname(__file__), "..", "..", "reports"
    )

    participants = list_participants(conn, args.standard)
    errors = []

    lb_path = os.path.join(reports_dir, "global-leaderboard.md")
    if not os.path.isfile(lb_path):
        errors.append("global-leaderboard.md missing")
    elif os.path.getsize(lb_path) == 0:
        errors.append("global-leaderboard.md empty")
    else:
        tokens = check_md_tokens(lb_path)
        if tokens:
            errors.append(f"global-leaderboard.md has unrendered tokens: {tokens[:3]}")

    # Charts always generated regardless of data completeness: one
    # rank-distribution per canonical domain, domain-weights (static),
    # one radar per registered team.
    charts_dir = os.path.join(reports_dir, "charts")
    expected_charts = [f"{d}-rank-distribution.png" for d in ALL_DOMAINS]
    expected_charts.append("domain-weights.png")
    for p in participants:
        expected_charts.append(f"{p['team_name']}-radar.png")

    for cname in expected_charts:
        cpath = os.path.join(charts_dir, cname)
        if not os.path.isfile(cpath):
            errors.append(f"Chart missing: {cname}")
        elif os.path.getsize(cpath) == 0:
            errors.append(f"Chart empty: {cname}")

    for p in participants:
        tname = p["team_name"]
        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}

        for d in ALL_DOMAINS:
            if d not in data_domains:
                continue
            prefix = DOMAIN_TO_PREFIX[d]
            for kind in ("deterministic", "semantic", "summary"):
                fname = f"{tname}-{prefix}-{kind}.md"
                fpath = os.path.join(reports_dir, fname)
                if not os.path.isfile(fpath):
                    errors.append(f"{tname}/{d}/{kind}: MD missing")
                elif os.path.getsize(fpath) == 0:
                    errors.append(f"{tname}/{d}/{kind}: MD empty")
                else:
                    tokens = check_md_tokens(fpath)
                    if tokens:
                        errors.append(f"{tname}/{d}/{kind}: unrendered tokens {tokens[:2]}")

        summary_path = os.path.join(reports_dir, f"{tname}-summary.md")
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
