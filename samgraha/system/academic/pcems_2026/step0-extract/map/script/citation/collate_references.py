"""collate_references.py — deterministic step for section-citations-references
usecase (fan-in). Reads academic_literature_citation for the paper, assigns
numbers, and writes the references domain's stage='cite' narrative.

No longer hard-gates on per-domain section-citations-* completeness — logs
outstanding domains as a warning but proceeds with whatever literature
citations are available. In-repo evidence citations stay in
academic_section_citations(source_kind='in-repo') for audit only, never
rendered.

Expected --in payload: {paper_id: int}
"""
import json as _json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        # Warn about outstanding domains but don't hard-block
        seeded = conn.execute(
            "SELECT key FROM academic_domains WHERE key != 'references'"
        ).fetchall()
        seeded_domains = [r["key"] for r in seeded]
        outstanding = []
        for domain in seeded_domains:
            complete, _detail = academic_schema.usecase_status(
                conn, paper_id, f"section-citations-{domain}")
            if not complete:
                outstanding.append(domain)
        warning = ""
        if outstanding:
            warning = (f"WARNING: outstanding section-citations domains: "
                       f"{', '.join(outstanding)} — references will be "
                       f"incomplete")

        # Query literature citations directly — this is the reader-facing list
        lit_rows = academic_schema.get_literature_citations(conn, paper_id)

        # Assign/update numbers stable per cite_key
        ref_entries = []
        for i, row in enumerate(lit_rows):
            number = row["number"] or (i + 1)
            if not row["number"]:
                conn.execute(
                    "UPDATE academic_literature_citation SET number=? WHERE id=?",
                    (number, row["id"]),
                )
            ref_entries.append({"raw_markdown": row["raw_markdown"]})
        conn.commit()

        # Write references narrative as JSON list of raw_markdown dicts
        # This gets consumed by assemble_common.parse_draft_to_context which
        # now detects JSON arrays and preserves structure
        sections = []
        if ref_entries:
            sections = [{
                "heading": "References",
                "text": _json.dumps(ref_entries),
            }]
        academic_schema.upsert_narrative(
            conn, paper_id, "references", sections,
            stage="cite", iteration=0, model="collate_references",
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"collated {len(ref_entries)} literature references "
                           f"for paper {paper_id}. {warning}" if warning
                   else f"collated {len(ref_entries)} literature references "
                        f"for paper {paper_id}",
                   paper_id=paper_id, reference_count=len(ref_entries),
                   outstanding_domains=outstanding if outstanding else None)


if __name__ == "__main__":
    main()
