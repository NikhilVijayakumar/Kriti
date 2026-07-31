"""discover_docs_modules.py — discover module boundaries from one or more
docs/paper/{system}/modules/ directory structures.

For documentation-first repos (e.g. repos whose primary intellectual
content is under docs/paper/ rather than source packages), this script
replaces discover_modules.py's code-first path. Each subdirectory of every
given system's modules/ is registered as a module in academic_modules,
plus a _cross_module/{system} pseudo-module per system that has a
cross_module/ dir, and a _cross_module/_cross_library pseudo-module if
docs/paper/cross_library/ exists (whole-system analysis spanning several
dependent subprojects — only meaningful when combining more than one).

A repo can have several dependent, documented subprojects (e.g. Bodha's
Amsha/Bodha/Yantra) — a paper covering just one and a paper covering all
of them are both valid, so this accepts a list rather than assuming one.
When more than one system is given, module names are namespaced
"{system}/{module}" to avoid collisions (two systems can both have a
"monitoring" module) — a single system keeps its plain module name,
unchanged from before this accepted a list.

Expected --in payload: {paper_id: int, docs_systems: [str]}
docs_systems are the target repo's own subproject name(s) under docs/
paper/{name}/modules/ (e.g. Bodha's "Bodha"/"Amsha"/"Yantra") — not the
samgraha standard name (see run_full_workflow.py's resolve_docs_systems(),
which resolves this value before it ever reaches this script). An empty
list means the flat docs/paper/modules/ layout (no subproject segment).
"""
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def _docs_paper_dir(repo_root, system):
    return (repo_root / "docs" / "paper" / system) if system else (repo_root / "docs" / "paper")


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    docs_systems = payload.get("docs_systems") or [None]  # [None] = flat layout
    combining = len([s for s in docs_systems if s]) > 1

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
    finally:
        conn.close()
    repo_root_path = _Path(paper["repo_root"]) if paper else repo_root

    registered = []
    sort_order = 0

    conn = academic_schema.get_conn(db_path)
    try:
        for system in docs_systems:
            base = _docs_paper_dir(repo_root_path, system)
            modules_dir = base / "modules"
            if not modules_dir.is_dir():
                continue
            for entry in sorted(modules_dir.iterdir()):
                if not entry.is_dir() or entry.name.startswith("."):
                    continue
                mod_name = f"{system}/{entry.name}" if combining else entry.name
                academic_schema.upsert_module(
                    conn, paper_id, mod_name, str(entry),
                    sort_order=sort_order, role="primary")
                registered.append(mod_name)
                sort_order += 1

            cross_dir = base / "cross_module"
            if cross_dir.is_dir():
                pseudo = f"_cross_module/{system}" if combining else "_cross_module"
                academic_schema.upsert_module(
                    conn, paper_id, pseudo, str(cross_dir),
                    sort_order=sort_order, role="primary")
                registered.append(pseudo)
                sort_order += 1

        # Whole-system analysis spanning several dependent subprojects —
        # only meaningful (and only loaded) when actually combining more
        # than one, same reasoning a per-system cross_module/ has for one.
        if combining:
            cross_library_dir = repo_root_path / "docs" / "paper" / "cross_library"
            if cross_library_dir.is_dir():
                pseudo = "_cross_module/_cross_library"
                academic_schema.upsert_module(
                    conn, paper_id, pseudo, str(cross_library_dir),
                    sort_order=sort_order, role="primary")
                registered.append(pseudo)
                sort_order += 1
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"discovered {len(registered)} docs modules: {', '.join(registered)}",
                   modules=registered, count=len(registered),
                   docs_systems=[s for s in docs_systems if s])


if __name__ == "__main__":
    main()
