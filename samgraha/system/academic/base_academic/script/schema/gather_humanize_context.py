"""gather_humanize_context.py — pre-script for humanize triads.
Gathers draft + flagged spans from the latest plagiarism finding.

Expected --in payload: {paper_id: int, domain: str}
"""
import json
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

    flagged_spans = []
    if plagiarism and plagiarism["flagged_spans"]:
        try:
            flagged_spans = json.loads(plagiarism["flagged_spans"])
        except (json.JSONDecodeError, TypeError):
            pass

    latest_humanize = None
    conn = academic_schema.get_conn(db_path)
    try:
        info = academic_schema.get_latest_narrative_info(conn, paper_id, domain)
    finally:
        conn.close()

    context = {
        "current_draft": draft or [],
        "domain": domain,
        "flagged_spans": flagged_spans,
        "current_stage": info[0] if info else "generate",
        "current_iteration": info[1] if info else 0,
    }

    write_envelope(out_path, status="ok",
                   message=f"gathered humanize context for {domain} ({len(flagged_spans)} spans)",
                   context=context)


if __name__ == "__main__":
    main()
