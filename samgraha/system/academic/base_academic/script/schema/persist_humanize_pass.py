"""persist_humanize_pass.py — post-script for humanize triads.
Persists rewrite result + change summary + risk flags.

Expected --in payload: {paper_id: int, domain: str, iteration: int,
  change_summary: str, risk_flags: list, sections: [{heading, text}], model: str}
"""
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    iteration = payload.get("iteration", 0)
    change_summary = payload.get("change_summary", "")
    risk_flags = payload.get("risk_flags", [])
    sections = payload.get("sections", [])
    model = payload.get("model", "")

    conn = academic_schema.get_conn(db_path)
    try:
        # Persist the humanize pass record
        academic_schema.upsert_humanize_pass(
            conn, paper_id, domain, iteration, change_summary,
            risk_flags=risk_flags, model=model,
        )
        # Also persist the rewritten section as a new narrative iteration
        academic_schema.upsert_narrative(
            conn, paper_id, domain, sections,
            stage="humanize", iteration=iteration, model=model,
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"humanized {domain} iter={iteration} ({len(sections)} sections, {len(risk_flags)} risk flags)",
                   paper_id=paper_id, domain=domain, iteration=iteration,
                   risk_flags=risk_flags)


if __name__ == "__main__":
    main()
