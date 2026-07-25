"""persist_section_citations.py — post-script for section-citations triads.
Persists citations to academic_section_citations.

Expected --in payload: {paper_id: int, domain: str, source_kind: str,
  citations: [str], model: str}
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
    source_kind = payload.get("source_kind", "in-repo")
    citations = payload.get("citations", [])

    conn = academic_schema.get_conn(db_path)
    try:
        for citation in citations:
            academic_schema.insert_section_citation(
                conn, paper_id, domain, source_kind, citation,
            )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"persisted {len(citations)} {source_kind} citations for {domain}",
                   paper_id=paper_id, domain=domain, source_kind=source_kind,
                   citation_count=len(citations))


if __name__ == "__main__":
    main()
