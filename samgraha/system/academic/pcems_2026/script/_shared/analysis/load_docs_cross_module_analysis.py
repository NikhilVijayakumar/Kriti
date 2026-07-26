"""load_docs_cross_module_analysis.py — load pre-existing cross-module
analysis markdown files into academic_cross_module_analysis.

Reads from the _cross_module* pseudo-modules discover_docs_modules.py
already registered (one per docs system that has a cross_module/ dir,
plus _cross_module/_cross_library when combining several systems) rather
than re-deriving paths from a system name.

academic_cross_module_analysis is keyed uniquely per (paper_id,
analysis_kind) — assemble-final-document.py's CROSS_CUTTING_TARGETS looks
up that exact bare key (novelty, gaps, mathematics, tables, figures) to
weave content into the final paper, so the key can't be renamed per
source. When combining several systems each contribute a "novelty.md",
etc.: this merges them into one block per analysis_kind (each source's
content under its own heading) and upserts once, instead of the last
system silently overwriting the others' content (upsert_cross_module_
analysis is a true overwrite-by-key, not an accumulator).

File naming convention: {analysis_kind}.md → analysis_kind
  novelty.md       → "novelty"
  architecture.md  → "architecture"
  interactions.md  → "interactions"
  mathematics.md   → "mathematics"
  patterns.md      → "patterns"
  dependencies.md  → "dependencies"
  gaps.md          → "gaps"
  consistency_check.md → "consistency_check"

Expected --in payload: {paper_id: int}
"""
import sqlite3
import sys as _sys
from collections import defaultdict
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _source_label(module_name):
    if "/" not in module_name:
        return "cross_module"
    return module_name.split("/", 1)[1]  # "_cross_module/Bodha" -> "Bodha"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        modules = academic_schema.get_modules(conn, paper_id)
    finally:
        conn.close()

    cross_pseudo_modules = [m for m in modules
                            if m["module_name"].startswith("_cross_module")]

    if not cross_pseudo_modules:
        write_envelope(out_path, status="ok",
                       message="no cross_module directory found, nothing to load",
                       loaded=0)
        return

    # analysis_kind -> [(source_label, content), ...], merged across every
    # contributing system before a single upsert per kind.
    by_kind = defaultdict(list)
    multi_source = len(cross_pseudo_modules) > 1

    for mod in cross_pseudo_modules:
        cross_dir = _Path(mod["module_path"])
        if not cross_dir.is_dir():
            continue
        label = _source_label(mod["module_name"])
        for md_file in sorted(cross_dir.glob("*.md")):
            kind = md_file.stem
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if not content.strip():
                continue
            by_kind[kind].append((label, content, str(md_file)))

    loaded = 0
    skipped_kinds = []
    conn = academic_schema.get_conn(db_path)
    try:
        for kind, entries in by_kind.items():
            if multi_source and len(entries) > 1:
                merged = "\n\n".join(
                    f"## Source: {label}\n\n{content}" for label, content, _ in entries)
                file_path = ";".join(fp for _, _, fp in entries)
            else:
                _, merged, file_path = entries[0]

            try:
                academic_schema.upsert_cross_module_analysis(
                    conn, paper_id, kind, merged,
                    model="docs-ingestion",
                    file_path=file_path,
                )
                loaded += 1
            except sqlite3.IntegrityError:
                # analysis_kind not in academic_cross_module_analysis's CHECK
                # constraint (architecture/dependencies/interactions/
                # patterns/gaps/mathematics/novelty only) — e.g. Bodha's
                # cross_module/ has a consistency_check.md this schema
                # doesn't have a column value for. Skip rather than crash
                # the whole load over one extra file; still reachable via
                # gather_domain_evidence's raw docs/paper/** scan for
                # generation triads even though it won't sit in this table.
                skipped_kinds.append(kind)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"loaded {loaded} cross-module analysis kinds from docs "
                           f"({'combined ' + str(len(cross_pseudo_modules)) + ' sources' if multi_source else '1 source'})"
                           + (f"; skipped (not in schema): {', '.join(skipped_kinds)}" if skipped_kinds else ""),
                   loaded=loaded,
                   kinds=sorted(by_kind.keys()),
                   skipped_kinds=skipped_kinds)


if __name__ == "__main__":
    main()
