#!/usr/bin/env python3
"""
run_det_audit.py — Run deterministic audits for all (or one) teams.

Reads teams from DB, runs each audit_*.py script against each team's repo,
evaluates rules, stores scores. This is use-case 2a.

Usage:
  python run_det_audit.py
  python run_det_audit.py --team "Goal GPT"
  python run_det_audit.py --db /path/to/hackathon.db
"""
import argparse
import os
import sys

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))

from db import get_conn, list_participants, get_domain_scores
from det_audit import run_domain_audit, DOMAIN_AUDIT_MODULES


def run_team(conn, participant, skip_existing=False):
    """Run deterministic audits for one team. Returns (passed, failed) counts."""
    tname = participant["team_name"]
    repo_path = participant["repo_path"]
    pid = participant["id"]

    if not repo_path or not os.path.isdir(repo_path):
        print(f"  SKIP {tname}: repo_path not found ({repo_path})")
        return 0, 0

    if skip_existing:
        existing = {r["domain"] for r in get_domain_scores(conn, pid)
                    if r["kind"] == "deterministic"}
        if len(existing) >= len(DOMAIN_AUDIT_MODULES):
            print(f"  SKIP {tname}: already has {len(existing)}/{len(DOMAIN_AUDIT_MODULES)} deterministic scores")
            return len(DOMAIN_AUDIT_MODULES), 0

    print(f"\n  {tname} ({repo_path})")
    passed, failed = 0, 0

    for domain in DOMAIN_AUDIT_MODULES:
        score = run_domain_audit(conn, pid, domain, repo_path)
        if score is None:
            failed += 1
        else:
            passed += 1

    return passed, failed


def main():
    parser = argparse.ArgumentParser(
        description="Run deterministic audits for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None, help="Process only this team")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip teams that already have all scores")
    args = parser.parse_args()

    conn = get_conn(args.db)
    participants = list_participants(conn, args.standard)

    if not participants:
        print("No teams registered. Run run_hackathon.py first.")
        sys.exit(1)

    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]
        if not participants:
            print(f"Team '{args.team}' not found")
            sys.exit(1)

    print(f"Running deterministic audits for {len(participants)} team(s)...")
    total_pass, total_fail = 0, 0

    for p in participants:
        passed, failed = run_team(conn, p, args.skip_existing)
        total_pass += passed
        total_fail += failed

    print(f"\n{'='*50}")
    print(f"Done: {total_pass} domains scored, {total_fail} errors")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
