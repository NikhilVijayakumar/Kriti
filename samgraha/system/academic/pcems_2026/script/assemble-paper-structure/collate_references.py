"""collate_references.py — deterministic step for section-citations-references
usecase (fan-in). Reads all academic_section_citations rows for a paper,
deduplicates, formats a bibliography, and writes it as the references
domain's stage='cite' draft.

Gates on all 11 section-citations-{domain} usecases completing first —
hard-fails rather than collating a partial citation list from whichever
domains happened to finish.

If the paper's metadata contains a "bibliography_path" key, external
citations from that file are merged with in-repo citations. File format:
one citation per line (plain text or BibTeX @article/@inproceedings blocks).

Expected --in payload: {paper_id: int}
"""
import json as _json
import re as _re
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _parse_bibtex(text):
    """Extract citation strings from BibTeX @article/@inproceedings/etc. blocks."""
    citations = []
    for match in _re.finditer(
        r'@\w+\{[^,]+,\s*(.*?)\n\}', text, _re.DOTALL
    ):
        block = match.group(1)
        author = _re.search(r'author\s*=\s*\{(.+?)\}', block)
        title = _re.search(r'title\s*=\s*\{(.+?)\}', block)
        year = _re.search(r'year\s*=\s*\{?(\d{4})\}?', block)
        journal = _re.search(r'(?:journal|booktitle)\s*=\s*\{(.+?)\}', block)
        parts = []
        if author:
            parts.append(author.group(1).strip())
        if title:
            parts.append(f'"{title.group(1).strip()}"')
        if journal:
            parts.append(journal.group(1).strip())
        if year:
            parts.append(year.group(1).strip())
        if parts:
            citations.append(", ".join(parts))
    return citations


def _load_external_citations(path_str):
    """Load external citations from a file (plain text or BibTeX)."""
    path = _Path(path_str)
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    if text.lstrip().startswith("@"):
        return _parse_bibtex(text)
    # Plain text: one citation per line, skip blanks and comments
    return [
        line.strip() for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


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

        # Merge external bibliography if provided via metadata
        paper = academic_schema.get_paper(conn, paper_id)
        metadata = {}
        if paper and paper["metadata"]:
            try:
                metadata = _json.loads(paper["metadata"])
            except (TypeError, ValueError):
                pass
        bib_path = metadata.get("bibliography_path")
        if bib_path:
            ext_citations = _load_external_citations(bib_path)
            # Append external citations not already present
            existing = set(deduped)
            for c in ext_citations:
                if c not in existing:
                    deduped.append(c)
                    existing.add(c)

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
