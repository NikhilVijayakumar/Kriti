"""approve_proposal.py — the one human-decision step in the standard.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional),
   reject: bool (optional, default False), reason: str (optional)}

Flips the latest pending proposal for (paper_id, phase, scope_domain)
to approved (or rejected with reason). Idempotent: re-running against
an already-decided row is a no-op, reported in the envelope.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    domain_id = payload.get("scope_domain_id")
    reject = payload.get("reject", False)
    reason = payload.get("reason", "")
    conn = academic_schema.get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT id, status FROM academic_proposals "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
            "AND is_latest=1",
            (payload["paper_id"], phase, domain_id)).fetchone()
        if not row:
            write_envelope(out_path, status="error",
                           message=f"no proposal for phase={phase}")
            return
        if row["status"] != "pending":
            write_envelope(out_path, status="ok",
                           message=f"already decided: status={row['status']}")
            return
        new_status = "rejected" if reject else "approved"
        conn.execute(
            "UPDATE academic_proposals SET status=?, decided_at=datetime('now'), "
            "user_comment = CASE WHEN ? THEN ? ELSE user_comment END "
            "WHERE id=?",
            (new_status, reject, reason, row["id"]))
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"phase={phase} {new_status}")


if __name__ == "__main__":
    main()
