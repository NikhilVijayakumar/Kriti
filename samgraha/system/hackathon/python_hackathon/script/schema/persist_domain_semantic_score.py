"""persist_domain_semantic_score.py — post-script closing the semantic-audit
triad (pre: run_domain_evidence.py -> semantic: audit/semantic/document/*
-> post: this). Persists the calling agent's result via upsert_domain_score()
(common/hackathon_schema.py), same call every deterministic audit score
already goes through — internally it normalizes `result` across
hackathon_semantic_runs / hackathon_semantic_dimension_scores /
hackathon_semantic_findings, this script itself doesn't need to know that.

Expected --in payload:
  {"team_name": str, "domain": str, "model": str,
   "result": {"overall_score": number, "dimension_scores": {...},
              "reasoning": str, "strengths": [...], "weaknesses": [...],
              "recommendations": [...]}}
`result` is exactly the JSON shape each semantic-audit prompt's
"## Expected Output" section asks the agent to return.
"""
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import hackathon_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    team_name = payload["team_name"]
    domain = payload["domain"]
    model = payload.get("model", "")
    result = payload["result"]
    score = result["overall_score"]
    standard = payload.get("standard", "python_hackathon")

    conn = hackathon_schema.get_conn(db_path)
    try:
        participant = next(
            (p for p in hackathon_schema.list_participants(conn, standard) if p["team_name"] == team_name),
            None,
        )
        if participant is None:
            write_envelope(out_path, status="error", message=f"unknown team_name '{team_name}'")
            return
        hackathon_schema.upsert_domain_score(conn, participant["id"], domain, "semantic", model, score, result)
    finally:
        conn.close()

    write_envelope(out_path, status="ok", message=f"persisted semantic score for {team_name}/{domain}: {score}")


if __name__ == "__main__":
    main()
