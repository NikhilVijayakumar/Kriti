#!/usr/bin/env python3
"""verify_usecase_6_html_report.py — Verify HTML output files exist and have no issues."""
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

EMPTY_B64_RE = re.compile(r'base64,"')


def check_html_tokens(path):
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

    # Check global leaderboard
    lb_path = os.path.join(reports_dir, "global-leaderboard.html")
    if not os.path.isfile(lb_path):
        errors.append("global-leaderboard.html missing")
    elif os.path.getsize(lb_path) == 0:
        errors.append("global-leaderboard.html empty")
    else:
        tokens = check_html_tokens(lb_path)
        if tokens:
            errors.append(f"global-leaderboard.html: unrendered tokens {tokens[:3]}")

    for p in participants:
        tname = p["team_name"]
        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}

        for d in ALL_DOMAINS:
            if d not in data_domains:
                continue
            for kind in ("deterministic", "semantic", "summary"):
                fname = f"{tname.replace(' ', '_')}-{d}-{kind}.html"
                fpath = os.path.join(reports_dir, fname)
                if not os.path.isfile(fpath):
                    errors.append(f"{tname}/{d}/{kind}: HTML missing")
                elif os.path.getsize(fpath) == 0:
                    errors.append(f"{tname}/{d}/{kind}: HTML empty")
                else:
                    tokens = check_html_tokens(fpath)
                    if tokens:
                        errors.append(f"{tname}/{d}/{kind}: unrendered tokens {tokens[:2]}")
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    empty_hits = EMPTY_B64_RE.findall(content)
                    if empty_hits:
                        errors.append(f"{tname}/{d}/{kind}: {len(empty_hits)} empty base64 payloads")

        summary_fname = f"{tname.replace(' ', '_')}-team-final-summary.html"
        summary_path = os.path.join(reports_dir, summary_fname)
        if not os.path.isfile(summary_path):
            errors.append(f"{tname}: team-final-summary.html missing")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors[:15]:
            print(f"  - {e}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more")
        sys.exit(1)
    else:
        print(f"PASS: HTML reports OK for {len(participants)} teams")
        sys.exit(0)


if __name__ == "__main__":
    main()
