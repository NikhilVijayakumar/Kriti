"""gather_cross_cutting_evidence.py — pre-script for cross-cutting section
generation usecases (generate-section-draft-{novelty,gaps,mathematics}).

Reads the already-persisted academic_cross_module_analysis row for the
requested analysis_kind and returns it as context for the LLM prompt.

Expected --in payload: {paper_id: int, analysis_kind: str}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    analysis_kind = payload["analysis_kind"]

    conn = academic_schema.get_conn(db_path)
    try:
        row = academic_schema.get_cross_module_analysis(
            conn, paper_id, analysis_kind=analysis_kind)
        if not row or not row.get("content"):
            write_envelope(out_path, status="error",
                           message=f"no cross_module_analysis for kind={analysis_kind}",
                           paper_id=paper_id, analysis_kind=analysis_kind)
            return

        write_envelope(out_path, status="ok",
                       message=f"gathered {analysis_kind} cross-cutting evidence",
                       paper_id=paper_id, analysis_kind=analysis_kind,
                       analysis_docs=row["content"])
    finally:
        conn.close()


if __name__ == "__main__":
    main()
