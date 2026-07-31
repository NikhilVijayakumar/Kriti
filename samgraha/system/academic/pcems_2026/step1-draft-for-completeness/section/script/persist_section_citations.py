"""persist_section_citations.py — post-script for section-citations triads.
Persists citations to academic_section_citations.

Supports source_kind='auto' — matches each citation marker against
academic_literature_citation to classify as 'literature' or 'in-repo'.

Expected --in payload: {paper_id: int, domain: str, source_kind: str,
  citations: [str], model: str}
"""
import re as _re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def _normalise(s):
    s = s.lower().strip()
    s = _re.sub(r'[^a-z0-9\s]', '', s)
    return s.strip()


def _classify_citations(conn, paper_id, citations):
    """Classify citations as 'literature' or 'in-repo' by matching against
    academic_literature_citation. Returns list of (citation, source_kind)."""
    lit_rows = conn.execute(
        "SELECT cite_key, authors, year, title FROM academic_literature_citation "
        "WHERE paper_id=?",
        (paper_id,),
    ).fetchall()
    lit_lookup = {}
    for row in lit_rows:
        key = _normalise(f"{row['authors']} {row['year']}")
        lit_lookup[key] = row["cite_key"]
        title_key = _normalise(row["title"])
        lit_lookup[title_key] = row["cite_key"]

    results = []
    for citation in citations:
        normalised = _normalise(citation)
        matched = False
        for lookup_key, cite_key in lit_lookup.items():
            if normalised in lookup_key or lookup_key in normalised:
                results.append((citation, "literature"))
                matched = True
                break
        if not matched:
            results.append((citation, "in-repo"))
    return results


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    source_kind = payload.get("source_kind", "in-repo")
    citations = payload.get("citations", [])

    conn = academic_schema.get_conn(db_path)
    try:
        if source_kind == "auto":
            classified = _classify_citations(conn, paper_id, citations)
            for citation, kind in classified:
                academic_schema.insert_section_citation(
                    conn, paper_id, domain, kind, citation,
                )
            lit_count = sum(1 for _, k in classified if k == "literature")
            repo_count = sum(1 for _, k in classified if k == "in-repo")
            message = (f"auto-classified {len(classified)} citations for {domain}: "
                       f"{lit_count} literature, {repo_count} in-repo")
        else:
            for citation in citations:
                academic_schema.insert_section_citation(
                    conn, paper_id, domain, source_kind, citation,
                )
            message = f"persisted {len(citations)} {source_kind} citations for {domain}"
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=message,
                   paper_id=paper_id, domain=domain, source_kind=source_kind,
                   citation_count=len(citations))


if __name__ == "__main__":
    main()
