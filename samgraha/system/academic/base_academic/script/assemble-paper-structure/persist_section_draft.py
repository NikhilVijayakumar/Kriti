"""persist_section_draft.py — post-script for draft/generate/deepen/humanize
triads. Persists section content to academic_narratives + narrative_sections.

Expected --in payload: {paper_id: int, domain: str, stage: str, iteration: int,
  sections: [{heading: str, text: str}], model: str, validated: bool}
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
    stage = payload.get("stage", "generate")
    iteration = payload.get("iteration", 0)
    sections = payload.get("sections", [])
    model = payload.get("model", "")
    validated = payload.get("validated", False)

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_narrative(
            conn, paper_id, domain, sections,
            stage=stage, iteration=iteration, validated=validated, model=model,
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"persisted {stage} draft for {domain} iter={iteration} ({len(sections)} sections)",
                   paper_id=paper_id, domain=domain, stage=stage, iteration=iteration)


if __name__ == "__main__":
    main()
