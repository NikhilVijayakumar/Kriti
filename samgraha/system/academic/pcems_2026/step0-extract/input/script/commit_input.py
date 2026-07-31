import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema

import yaml

_METADATA_PATH = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", "templates", "input", "metadata.yaml"))

def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    conn = academic_schema.get_conn(db_path)
    try:
        # Gate: verify an approved proposal exists
        row = conn.execute(
            "SELECT 1 FROM academic_proposal_review "
            "WHERE paper_id=? AND phase='input' AND is_latest=1 AND review_status='approved' "
            "LIMIT 1", (paper_id,)).fetchone()
        if not row:
            write_envelope(out_path, status="error",
                           message="no approved input proposal — run propose-input + approve first")
            return

        # Read the user-edited metadata.yaml directly
        if not os.path.isfile(_METADATA_PATH):
            write_envelope(out_path, status="error",
                           message=f"metadata file not found: {meta_path}")
            return

        with open(meta_path, encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        if not isinstance(meta, dict):
            write_envelope(out_path, status="error",
                           message="metadata.yaml is empty or invalid")
            return

        # Persist each top-level key via set_paper_metadata
        for key, value in meta.items():
            if value is not None:
                academic_schema.set_paper_metadata(conn, paper_id, key, value)

        # Update paper title from metadata
        paper_data = meta.get("paper", {})
        if isinstance(paper_data, dict) and paper_data.get("title"):
            conn.execute(
                "UPDATE academic_papers SET title=?, updated_at=? WHERE id=?",
                (paper_data["title"], academic_schema.now_iso(), paper_id))
            conn.commit()
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"committed input metadata from templates/input/metadata.yaml for paper {paper_id}")

if __name__ == "__main__":
    main()
