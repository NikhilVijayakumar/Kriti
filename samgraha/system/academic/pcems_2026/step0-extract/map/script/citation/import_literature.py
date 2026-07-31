"""import_literature.py — seed academic_literature_citation table from a
curated markdown bibliography file (format: "**[N]** Author... (Year). Title.
*Venue*."). Idempotent — re-running updates existing entries by cite_key.

Expected --in payload: {paper_id: int, bibliography_path?: str}
If bibliography_path omitted, defaults to
pcems_2026/reference/literature/bodha-references.md
"""
import json
import os
import re
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402

PCEMS_ROOT = _Path(__file__).resolve().parent.parent.parent
DEFAULT_BIB_PATH = PCEMS_ROOT / "reference" / "literature" / "bodha-references.md"

# Main entry pattern: **[N]** Authors... (YYYY). Rest.
_ENTRY_RE = re.compile(
    r'\*\*\[(\d+)\]\*\*\s+'       # **[N]**
    r'(.+?)\s+'                   # authors
    r'\((\d{4})\)[\.\:]\s*'       # (YYYY).
    r'(.+)$',                     # rest (title + venue + DOI)
    re.DOTALL,
)


def _slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def _parse_rest(text):
    """Parse the rest portion of a reference entry into (title, venue, doi)."""
    text = text.strip()
    doi = ""
    doi_m = re.search(r'(https?://\S+)', text)
    if doi_m:
        doi = doi_m.group(1).rstrip('.')
        text = text[:doi_m.start()].strip()

    venue = ""
    venue_m = re.search(r'\*\s*(.+?)\s*\*', text)
    if venue_m:
        venue = venue_m.group(1).strip().rstrip(',')
        text = text[:venue_m.start()].strip()

    title = text.strip().rstrip('.')
    return title, venue, doi


def _make_cite_key(authors, year, existing_keys):
    """Build a unique cite_key from first author's last name + initial + year.
    Appends a suffix if the key already exists."""
    first_author = authors.split(",")[0].strip()
    first_author = re.sub(r'[^a-zA-Z\s-]', '', first_author).strip()
    parts = first_author.split()
    first_word = parts[0] if parts else "unknown"
    first_initial = parts[1][0].lower() if len(parts) > 1 else ""
    base = _slugify(f"{first_word}-{first_initial}-{year}")
    cite_key = base
    suffix = 2
    while cite_key in existing_keys:
        cite_key = f"{base}-{suffix}"
        suffix += 1
    existing_keys.add(cite_key)
    return cite_key


def _parse_entry(line, existing_keys=None):
    """Parse a single "**[N]** Author..." line into a dict or None."""
    if existing_keys is None:
        existing_keys = set()
    line = line.strip()
    if not line:
        return None
    m = _ENTRY_RE.match(line)
    if not m:
        return None
    number = int(m.group(1))
    authors = m.group(2).strip().rstrip('.')
    year = m.group(3)
    rest = m.group(4)
    title, venue, doi = _parse_rest(rest)
    cite_key = _make_cite_key(authors, year, existing_keys)
    return {
        "cite_key": cite_key,
        "number": number,
        "authors": authors,
        "year": year,
        "title": title,
        "venue": venue,
        "doi": doi,
        "raw_markdown": line,
    }


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    bib_path = payload.get("bibliography_path")
    if bib_path:
        src = _Path(bib_path)
    else:
        src = DEFAULT_BIB_PATH

    if not src.is_file():
        write_envelope(out_path, status="error",
                       message=f"bibliography file not found: {src}")
        return

    text = src.read_text(encoding="utf-8")

    conn = academic_schema.get_conn(db_path)
    try:
        # Pre-populate existing cite_keys from DB for idempotent re-runs
        existing_db_keys = set()
        for r in conn.execute(
            "SELECT cite_key FROM academic_literature_citation WHERE paper_id=?",
            (paper_id,),
        ).fetchall():
            existing_db_keys.add(r["cite_key"])

        entries = []
        errors = []
        parse_keys = set(existing_db_keys)  # track unique keys during parse
        for line in text.splitlines():
            parsed = _parse_entry(line, parse_keys)
            if parsed:
                entries.append(parsed)
            elif line.strip() and not line.strip().startswith("#") and not line.strip().startswith("["):
                errors.append(line.strip()[:80])

        inserted = 0
        updated = 0
        for entry in entries:
            existing = conn.execute(
                "SELECT id FROM academic_literature_citation "
                "WHERE paper_id=? AND cite_key=?",
                (paper_id, entry["cite_key"]),
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE academic_literature_citation SET "
                    "number=?, authors=?, year=?, title=?, venue=?, doi=?, "
                    "raw_markdown=?, created_at=? "
                    "WHERE id=?",
                    (entry["number"], entry["authors"], entry["year"],
                     entry["title"], entry["venue"], entry["doi"],
                     entry["raw_markdown"], academic_schema.now_iso(),
                     existing["id"]),
                )
                updated += 1
            else:
                conn.execute(
                    "INSERT INTO academic_literature_citation "
                    "(paper_id, cite_key, number, authors, year, title, venue, doi, raw_markdown, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (paper_id, entry["cite_key"], entry["number"],
                     entry["authors"], entry["year"], entry["title"],
                     entry["venue"], entry["doi"], entry["raw_markdown"],
                     academic_schema.now_iso()),
                )
                inserted += 1
        conn.commit()
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"imported {len(entries)} literature citations "
                           f"({inserted} new, {updated} updated) for paper {paper_id}",
                   paper_id=paper_id, entry_count=len(entries),
                   inserted=inserted, updated=updated,
                   parse_errors=len(errors))


if __name__ == "__main__":
    main()
