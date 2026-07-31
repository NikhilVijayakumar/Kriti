"""persist_target_section_assignments.py — det step, writes the LLM's
target_section assignments back into the 4 map tables + section
citations. Last step of Step 1's assign-target-sections usecase.

Expected --in payload: {paper_id: int, assignments: [{kind, id, target_section}]}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import academic_schema  # noqa: E402

_MAP_TABLES = {
    "table": "academic_table_map",
    "figure": "academic_figure_map",
    "equation": "academic_equation_map",
    "algorithm": "academic_algorithm_map",
}


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    assignments = payload.get("assignments", [])

    conn = academic_schema.get_conn(db_path)
    try:
        updated = 0
        skipped = 0
        for a in assignments:
            kind = a.get("kind")
            row_id = a.get("id")
            target_section = a.get("target_section")
            if not (kind and row_id and target_section):
                skipped += 1
                continue

            if kind == "citation":
                domain_id = academic_schema.get_domain_id(conn, target_section)
                if domain_id is None:
                    skipped += 1
                    continue
                conn.execute(
                    "UPDATE academic_section_citations SET domain_id=? "
                    "WHERE id=? AND paper_id=?",
                    (domain_id, row_id, paper_id),
                )
                updated += 1
                continue

            table = _MAP_TABLES.get(kind)
            if not table:
                skipped += 1
                continue
            conn.execute(
                f"UPDATE {table} SET target_section=? WHERE id=? AND paper_id=?",
                (target_section, row_id, paper_id),
            )
            updated += 1

        conn.commit()
    finally:
        conn.close()

    write_envelope(
        out_path, status="ok",
        message=f"assigned target_section for {updated} assets ({skipped} skipped)",
        paper_id=paper_id, updated=updated, skipped=skipped,
    )


if __name__ == "__main__":
    main()
