"""persist_section_draft.py — post-script for generate/cite/enrich/
budget-fit/polish/humanize stages. Persists section content to
academic_narratives + narrative_sections.

Expected --in payload: {paper_id: int, domain: str, stage: str, iteration: int,
  sections: [{heading: str, text: str}], model: str, validated: bool,
  budget_cap_pct: float (optional), budget_cap_against_stage: str (optional)}

budget_cap_pct/budget_cap_against_stage are how content-detail-polish's
10% growth cap (base_academic-usecase-atomicity-proposal.md §5) is
enforced — generic to any stage transition, not polish-specific. When
both are set, a write growing the domain's word count by more than
budget_cap_pct% over its word count at budget_cap_against_stage is
rejected (status=error, not persisted) instead of silently written.
"""
import re
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _word_count(sections):
    text = " ".join(s.get("text", "") for s in sections)
    return len(re.findall(r"\b\w+\b", text))


def _narrative_word_count(conn, narrative_id):
    rows = conn.execute(
        "SELECT text FROM academic_narrative_sections WHERE narrative_id=?",
        (narrative_id,),
    ).fetchall()
    return sum(len(re.findall(r"\b\w+\b", r["text"] or "")) for r in rows)


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    stage = payload.get("stage", "generate")
    iteration = payload.get("iteration", 0)
    sections = payload.get("sections", [])
    model = payload.get("model", "")
    validated = payload.get("validated", False)
    cap_pct = payload.get("budget_cap_pct")
    cap_against_stage = payload.get("budget_cap_against_stage")

    conn = academic_schema.get_conn(db_path)
    try:
        if cap_pct is not None and cap_against_stage:
            baseline = academic_schema.get_narrative(conn, paper_id, domain, stage=cap_against_stage)
            if baseline:
                baseline_wc = _narrative_word_count(conn, baseline["id"])
                new_wc = _word_count(sections)
                if baseline_wc and new_wc > baseline_wc * (1 + cap_pct / 100):
                    write_envelope(
                        out_path, status="error",
                        message=(f"{stage} draft for {domain} is {new_wc} words vs "
                                 f"{baseline_wc} at {cap_against_stage} — exceeds {cap_pct}% "
                                 f"growth cap, not persisted"),
                        paper_id=paper_id, domain=domain, stage=stage,
                        word_count=new_wc, baseline_word_count=baseline_wc,
                    )
                    return

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
