"""gather_cross_module_evidence.py — pre-script for cross-module analysis
triads. Aggregates every module's analysis + repo-wide import graph.

Expected --in payload: {paper_id: int}
"""
import os
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def build_import_graph(module_analyses):
    graph = {}
    for mod_name, analyses in module_analyses.items():
        all_imports = set()
        for analysis in analyses:
            content = analysis.get("content", "")
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    all_imports.add(line)
        graph[mod_name] = sorted(all_imports)
    return graph


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        modules = academic_schema.get_modules(conn, paper_id)
        module_analyses = {}
        for mod in modules:
            analyses = academic_schema.get_module_analysis(conn, mod["id"])
            module_analyses[mod["module_name"]] = analyses
    finally:
        conn.close()

    import_graph = build_import_graph(module_analyses)

    all_summaries = {}
    for mod_name, analyses in module_analyses.items():
        for a in analyses:
            if a["analysis_kind"] == "summary":
                all_summaries[mod_name] = a["content"]

    write_envelope(out_path, status="ok",
                   message=f"aggregated evidence from {len(modules)} modules",
                   module_analyses={k: [{"kind": a["analysis_kind"], "content": a["content"][:2000]}
                                        for a in v if a["content"]]
                                    for k, v in module_analyses.items()},
                   import_graph=import_graph,
                   summaries=all_summaries)


if __name__ == "__main__":
    main()
