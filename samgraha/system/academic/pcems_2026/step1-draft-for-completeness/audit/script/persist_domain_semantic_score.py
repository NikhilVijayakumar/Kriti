"""persist_domain_semantic_score.py — post-script for semantic-audit triads.
Persists the agent's per-domain semantic score.

Expected --in payload: {paper_id: int, domain: str, model: str,
  result: {overall_score: number, dimension_scores: {...}, reasoning: str,
           strengths: [...], weaknesses: [...], recommendations: [...]},
  scope: str (optional, default "section-full"),
  part_kind: str (optional, default None — only for scope="section-part")}
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
    domain = payload["domain"]
    model = payload.get("model", "")
    commit_sha = payload.get("commit_sha", "")
    result = payload["result"]
    score = result["overall_score"]
    scope = payload.get("scope", "section-full")
    part_kind = payload.get("part_kind")

    if scope not in ("section-full", "section-part"):
        scope = "section-full"
    if scope != "section-part":
        part_kind = None
    elif part_kind not in ("citations", "enrichment", "budget-fit", None):
        part_kind = None

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_semantic_score(
            conn, paper_id, domain, model, score, result,
            scope=scope, part_kind=part_kind, commit_sha=commit_sha)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"persisted semantic score for {domain}: {score}",
                   paper_id=paper_id, domain=domain, score=score)


if __name__ == "__main__":
    main()
