"""link_proposal_scope.py — det step, links proposal to domain scope rows.

Runs immediately after persist_proposal.py.  Reads the generic
``proposal`` table to find the most recent proposal linked to the
``persist-proposal`` step execution, then writes
``academic_proposal_scope`` rows for each domain.

Expected --in payload:
  {paper_id: int, phase: str}

This script re-derives the domain list from _phase_map (same source of
truth as persist_proposal.py) because no inter-step state is passed
through the automation layer (seed_standard.rs passes {} to every step).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import academic_schema  # noqa: E402
from _phase_map import get_phase_domain_keys  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        scope_domains = get_phase_domain_keys(phase)
        if phase in ("fix", "input", "map"):
            write_envelope(out_path, status="ok",
                           message=f"proposals have no phase-wide scope")
            return

        # Find the generic proposal row by the persist-proposal step
        usecase_name = f"propose-{phase}"
        step_id = academic_schema.get_persist_proposal_step_id(
            conn, usecase_name)
        if not step_id:
            write_envelope(out_path, status="error",
                           message=f"step_id not found for {usecase_name}")
            return

        proposal_id = academic_schema.get_latest_proposal_id(conn, step_id)
        if not proposal_id:
            write_envelope(out_path, status="error",
                           message=f"no proposal found for step_id={step_id}")
            return

        rows_written = 0
        for i, dk in enumerate(scope_domains):
            # Look up generic domain_id (FK target)
            domain_row = conn.execute(
                "SELECT id FROM domain WHERE standard=? AND key=?",
                ("pcems_2026", dk),
            ).fetchone()
            if not domain_row:
                continue
            domain_id = domain_row["id"]

            # Look up generate-section-draft-{dk} usecase for its ID
            uc_row = conn.execute(
                "SELECT id FROM usecase WHERE standard=? AND name=?",
                ("pcems_2026", f"generate-section-draft-{dk}"),
            ).fetchone()
            if not uc_row:
                continue
            usecase_id = uc_row["id"]

            # Look up a step within that usecase (first available)
            step_row = conn.execute(
                "SELECT s.id FROM step s WHERE s.usecase_id=? "
                "ORDER BY s.step_order LIMIT 1",
                (usecase_id,),
            ).fetchone()
            if not step_row:
                continue
            step_id_dk = step_row["id"]

            conn.execute(
                "INSERT INTO academic_proposal_scope "
                "(proposal_id, domain_id, usecase_id, step_id) "
                "VALUES (?,?,?,?)",
                (proposal_id, domain_id, usecase_id, step_id_dk))
            rows_written += 1

        conn.commit()
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"linked {rows_written} scope rows for "
                           f"proposal_id={proposal_id}, phase={phase}")


if __name__ == "__main__":
    main()
