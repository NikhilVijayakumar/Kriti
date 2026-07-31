"""classify_citations.py — deterministic classification of extracted citation
markers into in-repo vs literature. Reads the output of gather_domain_evidence
(mode='citation'), matches each marker against academic_literature_citation,
and writes classified results for persist_section_citations to consume.

Runs as an additional deterministic step between gather-domain-evidence and
persist-section-citations in the section-citations-* usecase chain.

Expected --in payload: {paper_id: int, domain: str, markers: [str]}
"""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def _normalise(s):
    """Normalise a citation string for fuzzy matching."""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    return s.strip()


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    markers = payload.get("markers", [])

    conn = academic_schema.get_conn(db_path)
    try:
        lit_rows = conn.execute(
            "SELECT cite_key, authors, year, title FROM academic_literature_citation "
            "WHERE paper_id=?",
            (paper_id,),
        ).fetchall()

        # Build lookup from normalised author/title/year -> cite_key
        lit_lookup = {}
        for row in lit_rows:
            key = _normalise(f"{row['authors']} {row['year']}")
            lit_lookup[key] = row["cite_key"]
            title_key = _normalise(row["title"])
            lit_lookup[title_key] = row["cite_key"]

        classified = {"in_repo": [], "literature": []}
        for marker in markers:
            normalised = _normalise(marker)
            matched_key = None
            for lookup_key, cite_key in lit_lookup.items():
                if normalised in lookup_key or lookup_key in normalised:
                    matched_key = cite_key
                    break
            if matched_key:
                classified["literature"].append({
                    "source_kind": "literature",
                    "citation": marker,
                    "cite_key": matched_key,
                })
            else:
                classified["in_repo"].append({
                    "source_kind": "in-repo",
                    "citation": marker,
                })
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"classified {len(markers)} markers for {domain}: "
                           f"{len(classified['literature'])} literature, "
                           f"{len(classified['in_repo'])} in-repo",
                   paper_id=paper_id, domain=domain,
                   classified=classified,
                   total_markers=len(markers),
                   literature_count=len(classified["literature"]),
                   in_repo_count=len(classified["in_repo"]))


if __name__ == "__main__":
    main()
