"""gather_claim_evidence.py — step 1 of verify-step0-claims.
Gathers all map/analysis rows for a module/paper with their source_evidence + relevance_note.

Expected --in: {paper_id: int, module_name: str (optional)}
Output: {rows: [{table_name, row_id, source_evidence, relevance_note, ...}]}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope
import academic_schema

CLAIM_TABLES = [
    "academic_table_map",
    "academic_figure_map",
    "academic_equation_map",
    "academic_algorithm_map",
    "academic_module_analysis",
]

CROSS_TABLES = [
    "academic_cross_module_analysis",
]


def _fetch_rows(conn, paper_id, module_id):
    rows = []
    for table in CLAIM_TABLES:
        if module_id and table == "academic_module_analysis":
            cur = conn.execute(
                f"SELECT id, source_evidence, relevance_note FROM {table} WHERE module_id=?",
                (module_id,))
        else:
            cur = conn.execute(
                f"SELECT id, source_evidence, relevance_note FROM {table} WHERE paper_id=?",
                (paper_id,))
        for r in cur.fetchall():
            rows.append({
                "table_name": table,
                "row_id": r["id"],
                "source_evidence": r["source_evidence"] or "",
                "relevance_note": r["relevance_note"] or "",
            })
    for table in CROSS_TABLES:
        cur = conn.execute(
            f"SELECT id, source_evidence, relevance_note FROM {table} WHERE paper_id=?",
            (paper_id,))
        for r in cur.fetchall():
            rows.append({
                "table_name": table,
                "row_id": r["id"],
                "source_evidence": r["source_evidence"] or "",
                "relevance_note": r["relevance_note"] or "",
            })
    return rows


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_name = payload.get("module_name")
    conn = academic_schema.get_conn(db_path)
    module_id = None
    if module_name:
        modules = academic_schema.get_modules(conn, paper_id)
        mod = next((m for m in modules if m["module_name"] == module_name), None)
        if mod:
            module_id = mod["id"]
    try:
        rows = _fetch_rows(conn, paper_id, module_id)
    finally:
        conn.close()
    write_envelope(out_path, status="ok",
                   message=f"gathered {len(rows)} claim rows",
                   paper_id=paper_id, module_name=module_name or "",
                   module_id=module_id, rows=rows)


if __name__ == "__main__":
    main()
