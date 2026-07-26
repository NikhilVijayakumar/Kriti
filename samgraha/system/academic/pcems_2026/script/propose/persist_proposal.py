"""persist_proposal.py — append-only insert of a proposal row.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional),
   source: str, commit_sha: str, summary: str, content_md: str,
   user_comment: str (optional), iteration: int (optional, default 0),
   computed_context: dict (optional — domains, findings, scores, etc.)}

Appends a new row with status='pending'. Flips the previous is_latest=1
row to is_latest=0 (and status='superseded' if it was still pending).
Decided rows (approved/rejected) are immutable — only is_latest changes.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    conn = academic_schema.get_conn(db_path)
    try:
        # §3/§6a: only a still-pending previous row gets rewritten to
        # 'superseded' — a decided (approved/rejected) row's status is
        # immutable history, is_latest is the only column that changes.
        conn.execute(
            "UPDATE academic_proposals SET is_latest=0, "
            "status = CASE WHEN status='pending' THEN 'superseded' "
            "ELSE status END "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
            "AND is_latest=1",
            (payload["paper_id"], payload["phase"],
             payload.get("scope_domain_id")))
        conn.execute(
            "INSERT INTO academic_proposals "
            "(paper_id, phase, scope_domain_id, source, status, commit_sha, "
            " iteration, summary, content_md, user_comment, metadata, "
            " is_latest, created_at) "
            "VALUES (?,?,?,?,'pending',?,?,?,?,?,?,1,datetime('now'))",
            (payload["paper_id"], payload["phase"],
             payload.get("scope_domain_id"),
             payload["source"], payload["commit_sha"],
             payload.get("iteration", 0),
             payload["summary"], payload["content_md"],
             payload.get("user_comment", ""),
             json.dumps(payload.get("computed_context"))))
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok",
                   message=f"proposal drafted, phase={payload['phase']}")


if __name__ == "__main__":
    main()
