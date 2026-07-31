"""extract-tables-figures.py - pulls the tables and figures already
embedded in the findings draft into standalone files, before markdown/
html/docx/pdf assembly runs. The main assembled document still keeps them
inline (that's the "referenced at first mention, not collected at the
end" rule tables/figures are audited against) - these standalone copies
are for reuse/reference/archival, not a replacement for the inline copy.

Tables: contiguous Markdown pipe-table blocks, each captured with its
preceding "**Table N. Title**" caption line if present.
Figures: Markdown image syntax `![alt](path)` - copies the referenced
image file alongside a small .md wrapper with the caption. There are
currently no figures in findings (confirmed by the figures domain audit),
so this produces zero files until the paper actually has one - that's
expected, not a bug.

Expected --in payload: {paper_id: int}
"""
import re as _re
import shutil as _shutil
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import academic_schema  # noqa: E402

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))
import assemble_common  # noqa: E402

_TABLE_CAPTION_RE = _re.compile(r'^\*\*(Table\s+[IVXLCDM]+\.\s*.+?)\*\*\s*$', _re.MULTILINE)
_TABLE_BLOCK_RE = _re.compile(r'(\|.+\|\n)+')
_IMAGE_RE = _re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def _slugify(text):
    text = text.lower().strip()
    text = _re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:60] or "untitled"


def _extract_tables(text):
    """Find each (caption, table_block) pair in reading order. A table
    block is the contiguous run of `| ... |` lines that follows a
    "**Table N. Title**" caption line within a few lines."""
    tables = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = _TABLE_CAPTION_RE.match(lines[i])
        if m:
            caption = m.group(1)
            # scan forward (skipping blank lines) for the table block
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            block_lines = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                block_lines.append(lines[j])
                j += 1
            if block_lines:
                tables.append((caption, "\n".join(block_lines)))
            i = j
        else:
            i += 1
    return tables


def _extract_images(text):
    return [(alt, path) for alt, path in _IMAGE_RE.findall(text)]


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        draft = assemble_common.get_final_structural_draft(
            academic_schema, conn, paper_id, "findings")
        if not draft:
            draft = academic_schema.get_narrative(conn, paper_id, "findings", stage="generate")
    finally:
        conn.close()

    base_dir = repo_root / ".samgraha" / "output" / "draft" / f"paper-{paper_id}"
    tables_dir = base_dir / "tables"
    viz_dir = base_dir / "visualization"

    written_tables = []
    written_figures = []

    if draft:
        full_text = "\n\n".join(s.get("text", "") for s in draft)

        tables = _extract_tables(full_text)
        if tables:
            tables_dir.mkdir(parents=True, exist_ok=True)
            for idx, (caption, block) in enumerate(tables, start=1):
                fname = f"{idx:02d}-{_slugify(caption)}.md"
                fpath = tables_dir / fname
                fpath.write_text(f"**{caption}**\n\n{block}\n", encoding="utf-8")
                written_tables.append(str(fpath))

        images = _extract_images(full_text)
        if images:
            viz_dir.mkdir(parents=True, exist_ok=True)
            for idx, (alt, img_path) in enumerate(images, start=1):
                src = _Path(img_path)
                if not src.is_absolute():
                    src = repo_root / img_path
                if src.is_file():
                    dest = viz_dir / f"{idx:02d}-{src.name}"
                    _shutil.copy2(src, dest)
                    written_figures.append(str(dest))

    write_envelope(
        out_path, status="ok",
        message=f"extracted {len(written_tables)} tables, {len(written_figures)} figures",
        paper_id=paper_id,
        tables=written_tables,
        figures=written_figures,
    )


if __name__ == "__main__":
    main()
