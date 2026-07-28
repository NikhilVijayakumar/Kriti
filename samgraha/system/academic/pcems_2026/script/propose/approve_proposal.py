"""approve_proposal.py — human-decision step, writes academic_proposal_review.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional),
   reject: bool (optional, default False), reason: str (optional)}

Writes to academic_proposal_review (linked to generic proposal table).
Idempotent: re-running against an already-reviewed proposal is a no-op.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def _find_proposal(conn, phase):
    """Find the latest generic proposal row for this phase."""
    row = conn.execute(
        "SELECT p.id FROM proposal p "
        "JOIN usecase u ON u.id = p.usecase_id "
        "WHERE u.name=? ORDER BY p.id DESC LIMIT 1",
        (f"propose-{phase}",),
    ).fetchone()
    return row["id"] if row else None


def _get_metadata(conn, proposal_id):
    """Extract metadata_json from the generic proposal."""
    row = conn.execute(
        "SELECT metadata_json FROM proposal WHERE id=?",
        (proposal_id,),
    ).fetchone()
    if not row or not row["metadata_json"]:
        return {}
    import json
    try:
        return json.loads(row["metadata_json"])
    except (json.JSONDecodeError, TypeError):
        return {}


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    domain_id = payload.get("scope_domain_id")
    reject = payload.get("reject", False)
    reason = payload.get("reason", "")
    conn = academic_schema.get_conn(db_path)
    try:
        proposal_id = _find_proposal(conn, phase)
        if not proposal_id:
            write_envelope(out_path, status="error",
                           message=f"no proposal for phase={phase}")
            return

        existing = conn.execute(
            "SELECT id FROM academic_proposal_review "
            "WHERE proposal_id=?",
            (proposal_id,),
        ).fetchone()
        if existing:
            write_envelope(out_path, status="ok",
                           message=f"already decided: review_id={existing['id']}")
            return

        meta = _get_metadata(conn, proposal_id)
        # Supersede any prior pending reviews for this (paper, phase, scope)
        conn.execute(
            "UPDATE academic_proposal_review SET is_latest=0"
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ?",
            (payload["paper_id"], phase, domain_id))
        review_status = "rejected" if reject else "approved"
        conn.execute(
            "INSERT INTO academic_proposal_review "
            "(proposal_id, paper_id, phase, scope_domain_id, review_status, "
            " source, user_comment, iteration, summary, content_md, "
            " computed_context) "
            "VALUES (?,?,?,?,?,'approve-proposal',?,?,?,?,?)",
            (proposal_id, payload["paper_id"], phase, domain_id,
             review_status, reason,
             meta.get("iteration", 0),
             meta.get("summary", ""),
             meta.get("content_md", ""),
             meta.get("computed_context")))
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"phase={phase} {review_status}")


if __name__ == "__main__":
    main()
