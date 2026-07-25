"""collate_references.py — deterministic step for section-citations-references
usecase (fan-in). Reads all academic_section_citations rows for a paper,
deduplicates, formats a bibliography, and writes it as the references
domain's stage='cite' draft.

Gates on all 11 section-citations-{domain} usecases completing first —
hard-fails rather than collating a partial citation list from whichever
domains happened to finish.

Expected --in payload: {paper_id: int}
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

    conn = academic_schema.get_conn(db_path)
    try:
        outstanding = []
        for domain in academic_schema.GENERATED_DOMAINS:
            complete, _detail = academic_schema.usecase_status(
                conn, paper_id, f"section-citations-{domain}")
            if not complete:
                outstanding.append(domain)
        if outstanding:
            write_envelope(out_path, status="error",
                           message=(f"cannot collate references — outstanding: "
                                    f"{', '.join(outstanding)}"),
                           paper_id=paper_id, outstanding=outstanding)
            return

        citations = academic_schema.get_section_citations(conn, paper_id)
        deduped = list(dict.fromkeys(c["citation"] for c in citations))
        sections = []
        if deduped:
            sections = [{"heading": "References", "text": "\n".join(
                f"[{i+1}] {c}" for i, c in enumerate(deduped)
            )}]
        academic_schema.upsert_narrative(
            conn, paper_id, "references", sections,
            stage="cite", iteration=0, model="collate_references",
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"collated {len(deduped)} references for paper {paper_id}",
                   paper_id=paper_id, reference_count=len(deduped))


if __name__ == "__main__":
    main()
