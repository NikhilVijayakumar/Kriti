"""gather_cross_section_evidence.py — concatenate all structural domains'
latest drafts in _master-schema.yaml order for cross-section review.
"""
import json
import os
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

SCHEMA_YAML = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "..", "templates", "generation",
                           "markdown", "_master-schema.yaml")


def _load_section_order():
    """Load section order from _master-schema.yaml."""
    try:
        import yaml
    except ImportError:
        return []
    with open(SCHEMA_YAML) as f:
        data = yaml.safe_load(f)
    return data.get("sections", [])


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")

    if not paper_id:
        write_envelope(out_path, status="error", message="missing paper_id")
        return

    conn = academic_schema.get_conn(db_path)
    try:
        section_order = _load_section_order()
        if not section_order:
            write_envelope(out_path, status="error",
                           message="could not load section order")
            return

        parts = []
        for section in section_order:
            row = conn.execute(
                "SELECT draft_text FROM academic_narratives "
                "WHERE paper_id=? AND domain_key=? "
                "ORDER BY iteration DESC LIMIT 1",
                (paper_id, section),
            ).fetchone()
            if row and row["draft_text"]:
                parts.append(f"## {section}\n\n{row['draft_text']}")
            else:
                parts.append(f"## {section}\n\n[NOT YET GENERATED]")

        concatenated = "\n\n---\n\n".join(parts)
        write_envelope(out_path, status="ok",
                       message=f"concatenated {len(parts)} sections",
                       document_text=concatenated,
                       section_count=len(parts))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
