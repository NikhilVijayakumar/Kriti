"""gather_keyword_evidence.py — det step, first in build-keyword-map chain.

Gathers per-module approved analysis content (novelty, gaps, mathematics,
figures, tables) plus the paper's declared classification.keywords.
Output is fed to the semantic module-keyword-map prompt for keyword
identification with evidence.

Expected --in payload:
  {paper_id: int, module_id: int}
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
import academic_schema  # noqa: E402


_EVIDENCE_KINDS = (
    "novelty", "gaps", "mathematics", "architecture",
    "dependencies", "interactions", "figures", "tables",
)


def _get_module_name(conn, module_id):
    row = conn.execute(
        "SELECT name FROM academic_modules WHERE id=?", (module_id,)).fetchone()
    return row["name"] if row else f"module-{module_id}"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_id = payload.get("module_id")

    conn = academic_schema.get_conn(db_path)
    try:
        module_name = _get_module_name(conn, module_id) if module_id else "paper-wide"

        # Gather per-module analysis content
        analysis = {}
        for kind in _EVIDENCE_KINDS:
            if module_id:
                row = conn.execute(
                    "SELECT content FROM academic_module_analysis "
                    "WHERE paper_id=? AND module_id=? AND analysis_kind=? "
                    "ORDER BY created_at DESC LIMIT 1",
                    (paper_id, module_id, kind),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT content FROM academic_cross_module_analysis "
                    "WHERE paper_id=? AND analysis_kind=? "
                    "ORDER BY created_at DESC LIMIT 1",
                    (paper_id, kind),
                ).fetchone()
            analysis[kind] = row["content"] if row else ""

        # Gather declared keywords from academic_papers.metadata
        paper = academic_schema.get_paper(conn, paper_id)
        declared_keywords = []
        if paper and paper["metadata"]:
            try:
                meta = json.loads(paper["metadata"])
                declared_keywords = (
                    meta.get("classification", {}).get("keywords", [])
                    or meta.get("keywords", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        # Gather module info for reference
        modules = []
        if not module_id:
            rows = conn.execute(
                "SELECT id, name FROM academic_modules WHERE paper_id=? ORDER BY id",
                (paper_id,),
            ).fetchall()
            modules = [{"id": r["id"], "name": r["name"]} for r in rows]

    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"gathered keyword evidence for {module_name}",
                   module_id=module_id,
                   module_name=module_name,
                   analysis_summaries=analysis,
                   declared_keywords=declared_keywords,
                   modules=modules)


if __name__ == "__main__":
    main()
