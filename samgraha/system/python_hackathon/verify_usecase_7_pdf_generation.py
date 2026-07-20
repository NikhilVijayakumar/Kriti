#!/usr/bin/env python3
"""verify_usecase_7_pdf_generation.py — Verify one PDF per team, correct page count."""
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


def count_pdf_pages(path):
    from pypdf import PdfReader
    return len(PdfReader(path).pages)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--pdfs-dir", default=None)
    args = parser.parse_args()

    conn = get_conn(args.db)
    pdfs_dir = args.pdfs_dir or os.path.join(os.path.dirname(__file__), "..", "pdfs")

    participants = list_participants(conn, args.standard)
    errors = []

    for p in participants:
        tname = p["team_name"]
        pdf_path = os.path.join(pdfs_dir, f"{tname.replace(' ', '_')}.pdf")

        if not os.path.isfile(pdf_path):
            errors.append(f"{tname}: PDF missing")
            continue
        if os.path.getsize(pdf_path) == 0:
            errors.append(f"{tname}: PDF empty")
            continue

        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}
        # Summary page always present, each data domain = 1 page
        expected_pages = 1 + len(data_domains)

        try:
            actual = count_pdf_pages(pdf_path)
        except Exception as e:
            errors.append(f"{tname}: PDF unreadable ({e})")
            continue

        if actual != expected_pages:
            errors.append(f"{tname}: expected {expected_pages} pages, got {actual}")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"PASS: {len(participants)} PDFs verified")
        sys.exit(0)


if __name__ == "__main__":
    main()
