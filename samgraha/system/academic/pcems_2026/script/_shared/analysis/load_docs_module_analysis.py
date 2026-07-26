"""load_docs_module_analysis.py — load pre-existing per-module analysis
markdown files into academic_module_analysis.

For documentation-first repos that already have analysis artifacts on
disk (architecture.md, novelty.md, mathematics.md, gaps.md, summary.md
per module), this script bridges the gap between "docs on disk" and
"rows in the DB" that the downstream generation/audit pipeline depends on.

Reads each module's real directory straight from academic_modules.
module_path (set by discover_docs_modules.py) rather than re-deriving it
from a system name — works the same whether the module came from a single
subproject or several combined ones, since discover already resolved the
real path per module.

File naming convention: {analysis_kind}.md → analysis_kind
  architecture.md → "architecture"
  novelty.md      → "novelty"
  mathematics.md  → "mathematics"
  gaps.md         → "gaps"
  summary.md      → "summary"

Expected --in payload: {paper_id: int}
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        modules = academic_schema.get_modules(conn, paper_id)
    finally:
        conn.close()

    loaded = 0
    loaded_kinds = []
    loaded_modules = []

    conn = academic_schema.get_conn(db_path)
    try:
        for mod in modules:
            if mod["module_name"].startswith("_cross_module"):
                continue  # handled by load_docs_cross_module_analysis

            mod_dir = _Path(mod["module_path"])
            if not mod_dir.is_dir():
                continue

            for md_file in sorted(mod_dir.glob("*.md")):
                kind = md_file.stem
                try:
                    content = md_file.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                if not content.strip():
                    continue

                academic_schema.upsert_module_analysis(
                    conn, mod["id"], kind, content,
                    model="docs-ingestion",
                    file_path=str(md_file),
                )
                loaded += 1
                loaded_kinds.append(kind)
                loaded_modules.append(mod["module_name"])
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"loaded {loaded} analysis files from docs",
                   loaded=loaded,
                   modules=sorted(set(loaded_modules)),
                   kinds=sorted(set(loaded_kinds)))


if __name__ == "__main__":
    main()
