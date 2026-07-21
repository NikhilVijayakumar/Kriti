#!/usr/bin/env python3
"""uc2b_sem.py — Verify at least 1 semantic row per domain per team."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

from db import get_conn, list_participants, get_domain_scores, get_canonical_domains

ALL_DOMAINS = get_canonical_domains()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None)
    args = parser.parse_args()

    conn = get_conn(args.db)
    participants = list_participants(conn, args.standard)
    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]

    missing = []
    total_sem = 0
    for p in participants:
        rows = get_domain_scores(conn, p["id"])
        sem_domains = {r["domain"] for r in rows if r["kind"] == "semantic"}
        total_sem += len(sem_domains)
        for d in ALL_DOMAINS:
            if d not in sem_domains:
                missing.append((p["team_name"], d))

    if missing:
        print(f"FAIL: semantic data missing for {len(missing)} (team, domain) combos")
        for tname, d in missing[:10]:
            print(f"  - {tname}: {d}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
        sys.exit(1)
    else:
        print(f"PASS: >=1 semantic model per domain per team ({total_sem} rows total)")
        sys.exit(0)


if __name__ == "__main__":
    main()
