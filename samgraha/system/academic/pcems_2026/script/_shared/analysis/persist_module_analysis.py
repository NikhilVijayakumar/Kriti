"""persist_module_analysis.py — post-script for module analysis triads.
Persists content to academic_module_analysis + writes to docs/paper/{system}/.

Expected --in payload: {paper_id: int, module_name: str, analysis_kind: str,
  content: str, model: str, file_path: str}
"""
import os
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_name = payload["module_name"]
    analysis_kind = payload["analysis_kind"]
    content = payload.get("content", "")
    model = payload.get("model", "")
    file_path = payload.get("file_path", "")

    conn = academic_schema.get_conn(db_path)
    try:
        modules = academic_schema.get_modules(conn, paper_id)
        mod = next((m for m in modules if m["module_name"] == module_name), None)
        if not mod:
            from _adapter import write_envelope as we
            we(out_path, status="error", message=f"unknown module '{module_name}'")
            return
        academic_schema.upsert_module_analysis(
            conn, mod["id"], analysis_kind, content, model=model, file_path=file_path,
        )
    finally:
        conn.close()

    # Write to disk if file_path provided
    if file_path and content:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    write_envelope(out_path, status="ok",
                   message=f"persisted {analysis_kind} for module={module_name}",
                   paper_id=paper_id, module_name=module_name, analysis_kind=analysis_kind)


if __name__ == "__main__":
    main()
