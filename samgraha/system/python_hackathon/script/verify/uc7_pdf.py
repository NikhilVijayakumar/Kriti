#!/usr/bin/env python3
"""uc7_pdf.py — Verify one PDF per team, correct page count.

Page structure (per export_team_pdfs.py):
  1 team-summary page + 3 pages per domain-with-data (det, sem, summary)
  Fully-audited team: 1 + 3*10 = 31 pages.

PDF filenames use literal team names with spaces (e.g. "Goal GPT.pdf"),
not underscored. Default pdfs_dir: python_hackathon/reports/pdfs/.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

from db import get_conn, list_participants, get_domain_scores


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
    pdfs_dir = args.pdfs_dir or os.path.join(
        os.path.dirname(__file__), "..", "..", "reports", "pdfs"
    )

    participants = list_participants(conn, args.standard)
    errors = []

    for p in participants:
        tname = p["team_name"]
        pdf_path = os.path.join(pdfs_dir, f"{tname}.pdf")

        if not os.path.isfile(pdf_path):
            errors.append(f"{tname}: PDF missing")
            continue
        if os.path.getsize(pdf_path) == 0:
            errors.append(f"{tname}: PDF empty")
            continue

        rows = get_domain_scores(conn, p["id"])
        data_domains = {r["domain"] for r in rows}
        expected_pages = 1 + 3 * len(data_domains)

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
