#!/usr/bin/env python3
"""verify_usecase_1_init.py — Verify DB exists, schema correct, all teams registered."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "script"))

from db import get_conn, list_participants


def check_standard(conn, standard):
    errors = []
    # Check tables exist
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name IN ('standard_participants','standard_domain_scores','standard_narratives')"
    ).fetchall()
    found = {t["name"] for t in tables}
    for t in ("standard_participants", "standard_domain_scores", "standard_narratives"):
        if t not in found:
            errors.append(f"Missing table: {t}")

    # Check teams registered
    participants = list_participants(conn, standard)
    if not participants:
        errors.append("No participants registered for this standard")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    args = parser.parse_args()

    conn = get_conn(args.db)
    errors = check_standard(conn, args.standard)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        count = len(list_participants(conn, args.standard))
        print(f"PASS: {count} participants, schema OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
