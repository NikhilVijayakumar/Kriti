#!/usr/bin/env python3
"""verify_usecase_4_analysis.py — Verify narrative rows exist for all data-holding combos."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "script"))

from db import get_conn, list_participants, get_domain_scores, get_narrative

ALL_DOMAINS = [
    "infrastructure", "engineering", "testing", "documentation",
    "security", "mlops", "runtime", "team-workflow",
    "data-quality", "ai-explanations",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    args = parser.parse_args()

    conn = get_conn(args.db)
    participants = list_participants(conn, args.standard)

    errors = []
    # Check per-team per-domain narratives
    for p in participants:
        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}
        for d in data_domains:
            narrative = get_narrative(conn, p["id"], d)
            if not narrative:
                errors.append(f"{p['team_name']}: missing narrative for {d}")

    # Check competition-wide narrative exists
    comp_wide = get_narrative(conn, None, None)
    if not comp_wide:
        errors.append("Competition-wide narrative missing")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors[:10]:
            print(f"  - {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        sys.exit(1)
    else:
        print("PASS: all narratives present")
        sys.exit(0)


if __name__ == "__main__":
    main()
