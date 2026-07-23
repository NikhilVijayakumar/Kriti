"""persist_cross_module_analysis.py — post-script for cross-module analysis
triads. Persists to academic_cross_module_analysis + writes to disk.

Expected --in payload: {paper_id: int, analysis_kind: str, content: str,
  model: str, file_path: str}
"""
import os
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    analysis_kind = payload["analysis_kind"]
    content = payload.get("content", "")
    model = payload.get("model", "")
    file_path = payload.get("file_path", "")

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_cross_module_analysis(
            conn, paper_id, analysis_kind, content, model=model, file_path=file_path,
        )
    finally:
        conn.close()

    if file_path and content:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    write_envelope(out_path, status="ok",
                   message=f"persisted cross-module {analysis_kind}",
                   paper_id=paper_id, analysis_kind=analysis_kind)


if __name__ == "__main__":
    main()
