#!/usr/bin/env python3
"""uc6_html.py — Verify HTML output files exist and have no issues."""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

from db import get_conn, list_participants, get_domain_scores, get_canonical_domains

ALL_DOMAINS = get_canonical_domains()

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
    reports_dir = args.reports_dir or os.path.join(
        os.path.dirname(__file__), "..", "..", "reports", "html"
    )

    participants = list_participants(conn, args.standard)
    errors = []

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
            prefix = DOMAIN_TO_PREFIX[d]
            for kind in ("deterministic", "semantic", "summary"):
                fname = f"{tname}-{prefix}-{kind}.html"
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

        summary_path = os.path.join(reports_dir, f"{tname}-summary.html")
        if not os.path.isfile(summary_path):
            errors.append(f"{tname}: team-summary.html missing")

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
