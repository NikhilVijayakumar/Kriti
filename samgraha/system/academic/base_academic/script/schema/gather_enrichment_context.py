"""gather_enrichment_context.py — pre-script for enrichment triads
(literature-review, mathematics, figures). Gathers current draft + analysis
docs + citation notes.

Expected --in payload: {paper_id: int, domain: str, enrichment_kind: str}
"""
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    enrichment_kind = payload["enrichment_kind"]

    conn = academic_schema.get_conn(db_path)
    try:
        draft = academic_schema.get_narrative(conn, paper_id, domain)
        latest_info = academic_schema.get_latest_narrative_info(conn, paper_id, domain)
    finally:
        conn.close()

    context = {
        "current_draft": draft or [],
        "domain": domain,
        "enrichment_kind": enrichment_kind,
        "latest_stage": latest_info[0] if latest_info else None,
        "latest_iteration": latest_info[1] if latest_info else 0,
    }

    write_envelope(out_path, status="ok",
                   message=f"gathered enrichment context for {domain}/{enrichment_kind}",
                   context=context)


if __name__ == "__main__":
    main()
