"""persist_plagiarism_findings.py — post-script for plagiarism-forensic-audit
triads. Persists PASS/FAIL + flagged spans.

Expected --in payload: {paper_id: int, domain: str, verdict: str,
  flagged_spans: list, model: str}
"""
import json
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    verdict = payload["verdict"]
    flagged_spans = payload.get("flagged_spans", [])
    model = payload.get("model", "")

    # Determine run_number (increment from previous)
    conn = academic_schema.get_conn(db_path)
    try:
        prev = academic_schema.get_plagiarism_finding(conn, paper_id, domain)
        run_number = (prev["run_number"] + 1) if prev else 1
        academic_schema.upsert_plagiarism_finding(
            conn, paper_id, domain, run_number, verdict,
            flagged_spans=flagged_spans, model=model,
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"plagiarism {verdict} for {domain} (run={run_number}, spans={len(flagged_spans)})",
                   paper_id=paper_id, domain=domain, verdict=verdict,
                   run_number=run_number, flagged_spans=flagged_spans)


if __name__ == "__main__":
    main()
