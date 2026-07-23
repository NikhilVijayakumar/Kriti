"""fetch_score_context.py — pre-script opening the narrative-analysis triad
(pre: this -> semantic: analysis/*.md -> post: persist_narrative.py).
Reads exactly what each analysis/*.md's own "## Inputs" section says the
narrative needs — either one team's domain scores (per-domain narrative) or
every team's aggregated scores (the competition-wide leaderboard narrative,
analysis/00-leaderboard.md) — via common/hackathon_schema.py, read-only.

Expected --in payload: {"team_name": str|null, "domain": str|null}
team_name=null means the competition-wide case.
"""
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import hackathon_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    team_name = payload.get("team_name")
    domain = payload.get("domain")
    standard = payload.get("standard", "python_hackathon")

    conn = hackathon_schema.get_conn(db_path)
    try:
        if team_name is None:
            context = hackathon_schema.get_all_scores_as_dict(conn, standard, mode="both")
            write_envelope(out_path, status="ok", message="gathered competition-wide scores",
                           context=context, team_name=None, domain=domain)
            return

        participant = next(
            (p for p in hackathon_schema.list_participants(conn, standard) if p["team_name"] == team_name),
            None,
        )
        if participant is None:
            write_envelope(out_path, status="error", message=f"unknown team_name '{team_name}'")
            return

        profile = hackathon_schema.get_team_profile(conn, participant["id"])
        scores = hackathon_schema.get_domain_scores(conn, participant["id"], domain=domain)
    finally:
        conn.close()

    write_envelope(out_path, status="ok", message=f"gathered scores for {team_name}/{domain or '(all domains)'}",
                   team_profile=profile, scores=scores, team_name=team_name, domain=domain)


if __name__ == "__main__":
    main()
