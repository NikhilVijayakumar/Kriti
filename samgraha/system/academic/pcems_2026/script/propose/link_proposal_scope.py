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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _phase_map import get_phase_domain_keys, get_standard_suffix  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        scope_domains = get_phase_domain_keys(phase)
        if phase == "fix":
            write_envelope(out_path, status="ok",
                           message="fix proposals have no phase-wide scope")
            return

        standard_suffix = get_standard_suffix(phase)
        usecase_name = f"persist-proposal-{standard_suffix}"
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
            domain_id_row = conn.execute(
                "SELECT id FROM academic_domains WHERE key=?",
                (dk,)).fetchone()
            if not domain_id_row:
                continue
            domain_id = domain_id_row["id"]

            usecase_name_dk = f"generate-section-{dk}-{standard_suffix}"
            step_id_dk = academic_schema.get_persist_proposal_step_id(
                conn, usecase_name_dk)
            if not step_id_dk:
                continue

            conn.execute(
                "INSERT INTO academic_proposal_scope "
                "(proposal_id, domain_id, domain_key, phase, phase_number, "
                " usecase_name, step_id, created_at) "
                "VALUES (?,?,?,?,?,?,?,datetime('now'))",
                (proposal_id, domain_id, dk, phase, i + 1,
                 usecase_name_dk, step_id_dk))
            rows_written += 1

        conn.commit()
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"linked {rows_written} scope rows for "
                           f"proposal_id={proposal_id}, phase={phase}")


if __name__ == "__main__":
    main()
