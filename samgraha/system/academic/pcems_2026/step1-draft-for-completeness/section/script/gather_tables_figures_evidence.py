"""gather_tables_figures_evidence.py — pre-script for
generate-section-draft-{tables,figures}.

Unlike novelty/gaps/mathematics, tables and figures have no upstream
module-level analysis usecase and no academic_cross_module_analysis row —
per the domain guide, their checks apply to already-drafted findings text
(tables/figures embedded inline, per CROSS_CUTTING_TARGETS in
assemble_common.py), not repo source code. Evidence is the findings
domain's current best-available draft.

Expected --in payload: {paper_id: int, domain: str ("tables" or "figures")}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR  # noqa: E402
import academic_schema  # noqa: E402
import assemble_common  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]

    conn = academic_schema.get_conn(db_path)
    try:
        draft = assemble_common.get_final_structural_draft(
            academic_schema, conn, paper_id, "findings")
        if not draft:
            # Nothing published yet — fall back to the raw generate-stage
            # draft so tables/figures can still be checked pre-polish.
            draft = academic_schema.get_narrative(conn, paper_id, "findings", stage="generate")
        if not draft:
            write_envelope(out_path, status="error",
                           message="no findings draft to check for tables/figures",
                           paper_id=paper_id, domain=domain)
            return

        write_envelope(out_path, status="ok",
                       message=f"gathered findings draft as {domain} evidence",
                       paper_id=paper_id, domain=domain,
                       findings_draft=draft)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
