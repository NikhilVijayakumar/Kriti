"""persist_domain_semantic_score.py — post-script for semantic-audit triads.
Persists the agent's per-domain semantic score.

Expected --in payload: {paper_id: int, domain: str, model: str,
  result: {overall_score: number, dimension_scores: {...}, reasoning: str,
           strengths: [...], weaknesses: [...], recommendations: [...]}}
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    model = payload.get("model", "")
    result = payload["result"]
    score = result["overall_score"]

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_semantic_score(conn, paper_id, domain, model, score, result)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"persisted semantic score for {domain}: {score}",
                   paper_id=paper_id, domain=domain, score=score)


if __name__ == "__main__":
    main()
