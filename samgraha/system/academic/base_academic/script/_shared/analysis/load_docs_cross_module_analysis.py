"""load_docs_cross_module_analysis.py — load pre-existing cross-module
analysis markdown files from docs/paper/{system}/cross_module/ into
academic_cross_module_analysis.

File naming convention: {analysis_kind}.md → analysis_kind
  novelty.md       → "novelty"
  architecture.md  → "architecture"
  interactions.md  → "interactions"
  mathematics.md   → "mathematics"
  patterns.md      → "patterns"
  dependencies.md  → "dependencies"
  gaps.md          → "gaps"

Expected --in payload: {paper_id: int, standard: str}
"""
import os
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _find_cross_module_dir(repo_root, system):
    candidates = [
        repo_root / "docs" / "paper" / system / "cross_module",
        repo_root / "docs" / "paper" / "cross_module",
    ]
    for path in candidates:
        if path.is_dir():
            return path
    return None


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    standard = payload.get("standard", "base_academic")

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
    finally:
        conn.close()

    repo_root_path = _Path(paper["repo_root"]) if paper else repo_root
    cross_dir = _find_cross_module_dir(repo_root_path, standard)

    if not cross_dir:
        write_envelope(out_path, status="ok",
                       message="no cross_module directory found, nothing to load",
                       loaded=0)
        return

    loaded = 0
    loaded_kinds = []

    conn = academic_schema.get_conn(db_path)
    try:
        for md_file in sorted(cross_dir.glob("*.md")):
            kind = md_file.stem
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if not content.strip():
                continue

            academic_schema.upsert_cross_module_analysis(
                conn, paper_id, kind, content,
                model="docs-ingestion",
                file_path=str(md_file),
            )
            loaded += 1
            loaded_kinds.append(kind)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"loaded {loaded} cross-module analysis files from docs",
                   loaded=loaded,
                   kinds=sorted(set(loaded_kinds)))


if __name__ == "__main__":
    main()
