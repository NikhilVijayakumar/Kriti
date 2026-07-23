"""persist_narrative.py — post-script closing the narrative-analysis triad
(pre: fetch_score_context.py -> semantic: analysis/*.md -> post: this).
Persists the calling agent's narrative sections into hackathon_narratives
(python_hackathon's own table, see common/hackathon_schema.py) via
upsert_narrative(). team_id/domain are genuinely nullable here — the
competition-wide narrative (analysis/00-leaderboard.md) is team_name=null,
domain=null, which the old semantic_reports.domain NOT NULL constraint could
never store (see hackathon_schema.py's module docstring).

Expected --in payload: {"team_name": str|null, "domain": str|null,
"sections": [{"heading": str, "text": str}, ...], "model": str} — matches
each analysis/*.md's own "## Output Schema" section, plus which model wrote
the narrative (hackathon_narratives.model, for backtrace).
"""
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import hackathon_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    team_name = payload.get("team_name")
    domain = payload.get("domain")
    sections = payload["sections"]
    model = payload.get("model")
    standard = payload.get("standard", "python_hackathon")

    conn = hackathon_schema.get_conn(db_path)
    try:
        participant_id = None
        if team_name is not None:
            participant = next(
                (p for p in hackathon_schema.list_participants(conn, standard) if p["team_name"] == team_name),
                None,
            )
            if participant is None:
                write_envelope(out_path, status="error", message=f"unknown team_name '{team_name}'")
                return
            participant_id = participant["id"]
        hackathon_schema.upsert_narrative(conn, participant_id, domain, sections, model=model)
    finally:
        conn.close()

    write_envelope(out_path, status="ok", message=f"persisted narrative for {team_name or '(competition-wide)'}/{domain or '(none)'}")


if __name__ == "__main__":
    main()
