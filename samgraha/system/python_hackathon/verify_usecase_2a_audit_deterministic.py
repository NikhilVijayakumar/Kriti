#!/usr/bin/env python3
"""verify_usecase_2a_audit_deterministic.py — Verify deterministic scores exist for all domains."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "script"))

from db import get_conn, list_participants, get_domain_scores

ALL_DOMAINS = [
    "infrastructure", "engineering", "testing", "documentation",
    "security", "mlops", "runtime", "team-workflow",
    "data-quality", "ai-explanations",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None, help="Check only this team")
    args = parser.parse_args()

    conn = get_conn(args.db)
    participants = list_participants(conn, args.standard)
    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]

    total = 0
    missing = []
    for p in participants:
        rows = get_domain_scores(conn, p["id"])
        det_domains = {r["domain"] for r in rows if r["kind"] == "deterministic"}
        for d in ALL_DOMAINS:
            total += 1
            if d not in det_domains:
                missing.append((p["team_name"], d))

    if missing:
        print(f"FAIL: {len(ALL_DOMAINS) - len(missing)}/{len(ALL_DOMAINS)} per team")
        for tname, d in missing:
            print(f"  - {tname}: {d}")
        sys.exit(1)
    else:
        print(f"PASS: all {len(ALL_DOMAINS)} domains present per team")
        sys.exit(0)


if __name__ == "__main__":
    main()
