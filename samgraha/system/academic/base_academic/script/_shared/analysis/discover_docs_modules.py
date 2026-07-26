"""discover_docs_modules.py — discover module boundaries from
docs/paper/{system}/modules/ directory structure.

For documentation-first repos (e.g. repos whose primary intellectual
content is under docs/paper/ rather than source packages), this script
replaces discover_modules.py's code-first path.  Each subdirectory of
docs/paper/{system}/modules/ is registered as a module in
academic_modules, plus a _cross_module pseudo-module if
docs/paper/{system}/cross_module/ exists.

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


def _find_docs_modules_dir(repo_root, system):
    """Locate the modules directory under docs/paper/.

    Tries two layouts:
      1. docs/paper/{system}/modules/  (system-specific)
      2. docs/paper/modules/           (system-agnostic)
    """
    candidates = [
        repo_root / "docs" / "paper" / system / "modules",
        repo_root / "docs" / "paper" / "modules",
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
    modules_dir = _find_docs_modules_dir(repo_root_path, standard)

    modules = []
    if modules_dir:
        for entry in sorted(modules_dir.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                modules.append(entry.name)

    # Register modules in DB
    conn = academic_schema.get_conn(db_path)
    try:
        for i, mod_name in enumerate(modules):
            mod_path = str(modules_dir / mod_name)
            academic_schema.upsert_module(conn, paper_id, mod_name, mod_path,
                                          sort_order=i,
                                          metadata={"source": "docs"})

        # Register _cross_module pseudo-module if cross_module/ exists
        has_cross_module = False
        for candidate in [
            repo_root_path / "docs" / "paper" / standard / "cross_module",
            repo_root_path / "docs" / "paper" / "cross_module",
        ]:
            if candidate.is_dir():
                has_cross_module = True
                academic_schema.upsert_module(
                    conn, paper_id, "_cross_module", str(candidate),
                    sort_order=len(modules),
                    metadata={"source": "docs", "kind": "cross_module"},
                )
                modules.append("_cross_module")
                break
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"discovered {len(modules)} docs modules: {', '.join(modules)}",
                   modules=modules, count=len(modules),
                   modules_dir=str(modules_dir) if modules_dir else None)


if __name__ == "__main__":
    main()
