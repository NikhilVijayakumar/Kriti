"""gather_plagiarism_context.py — pre-script for plagiarism-forensic-audit
triads. Gathers current draft text.

Expected --in payload: {paper_id: int, domain: str}
"""
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

    conn = academic_schema.get_conn(db_path)
    try:
        draft = academic_schema.get_narrative(conn, paper_id, domain)
        plagiarism = academic_schema.get_plagiarism_finding(conn, paper_id, domain)
    finally:
        conn.close()

    context = {
        "current_draft": draft or [],
        "domain": domain,
        "previous_verdict": plagiarism["verdict"] if plagiarism else None,
        "previous_run": plagiarism["run_number"] if plagiarism else 0,
    }

    write_envelope(out_path, status="ok",
                   message=f"gathered plagiarism context for {domain}",
                   context=context)


if __name__ == "__main__":
    main()
