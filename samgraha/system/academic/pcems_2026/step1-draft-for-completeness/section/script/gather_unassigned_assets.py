"""gather_unassigned_assets.py — det step, gathers Step-0-extracted
assets that don't have a target_section (or domain_id, for citations)
assigned yet, plus the analysis-section-map.yaml reference guidance.

Step 0 extracts data without deciding which manuscript section it
belongs in; this is the first step of Step 1's own assignment usecase,
which decides that before generation consumes any entry.

Expected --in payload: {paper_id: int}
"""
import os
import sys
import yaml
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

_REFERENCE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "analysis-section-map.yaml")


def _load_reference():
    if not os.path.isfile(_REFERENCE_PATH):
        return {}
    with open(_REFERENCE_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("analysis_kind_sections", {})


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    conn = academic_schema.get_conn(db_path)
    try:
        unassigned = {}
        for kind, table in _MAP_TABLES.items():
            rows = conn.execute(
                f"SELECT id, map_key, caption, source_evidence FROM {table} "
                "WHERE paper_id=? AND target_section IS NULL",
                (paper_id,),
            ).fetchall()
            unassigned[kind] = [dict(r) for r in rows]

        citation_rows = conn.execute(
            "SELECT id, citation, source_kind FROM academic_section_citations "
            "WHERE paper_id=? AND domain_id IS NULL",
            (paper_id,),
        ).fetchall()
        unassigned["citation"] = [dict(r) for r in citation_rows]

        structural_domains = [r["key"] for r in conn.execute(
            "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]
    finally:
        conn.close()

    total = sum(len(v) for v in unassigned.values())
    write_envelope(
        out_path, status="ok",
        message=f"gathered {total} unassigned assets for paper {paper_id}",
        paper_id=paper_id,
        unassigned=unassigned,
        structural_domains=structural_domains,
        reference_guidance=_load_reference(),
    )


if __name__ == "__main__":
    main()
