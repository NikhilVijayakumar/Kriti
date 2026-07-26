"""persist_reviewer_simulation.py — post-script for the reviewer-simulation
triad. Reshapes the 3-persona result into the generic semantic-run shape
(persona -> academic_semantic_dimension_scores, decision folded into
reasoning, per-persona weaknesses/questions/strengths flattened with a
persona prefix) before calling the same upsert_semantic_score() every
other semantic audit uses — reviewer-simulation is stored in
academic_semantic_runs like any other domain, not a bespoke table.

Expected --in payload: {paper_id: int, model: str, commit_sha: str,
  result: {reviewers: [{persona, score, weaknesses, questions, strengths}],
           overall_score: number, decision: str}}
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _reshape(result):
    reviewers = result.get("reviewers", [])
    dimension_scores = {
        r["persona"]: {"score": r.get("score"),
                       "evidence": "; ".join(r.get("weaknesses", []))}
        for r in reviewers if r.get("persona")
    }
    strengths = [f"[{r.get('persona')}] {s}"
                 for r in reviewers for s in r.get("strengths", [])]
    weaknesses = [f"[{r.get('persona')}] {w}"
                  for r in reviewers for w in r.get("weaknesses", [])]
    recommendations = [f"[{r.get('persona')}] {q}"
                       for r in reviewers for q in r.get("questions", [])]
    reasoning = (f"Decision: {result.get('decision', 'Unknown')} "
                 f"(overall_score={result.get('overall_score')}/30)")
    return {
        "overall_score": result.get("overall_score"),
        "reasoning": reasoning,
        "dimension_scores": dimension_scores,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
    }


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    model = payload.get("model", "")
    commit_sha = payload.get("commit_sha", "")
    raw_result = payload["result"]
    reshaped = _reshape(raw_result)
    score = reshaped["overall_score"]

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_semantic_score(
            conn, paper_id, "reviewer-simulation", model, score, reshaped,
            scope="section-full", commit_sha=commit_sha)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"persisted reviewer-simulation: "
                           f"{raw_result.get('decision')} ({score}/30)",
                   paper_id=paper_id, score=score,
                   decision=raw_result.get("decision"))


if __name__ == "__main__":
    main()
