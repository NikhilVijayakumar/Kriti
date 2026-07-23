"""init_schema.py — creates python_hackathon's own tables (see
common/hackathon_schema.py's module docstring for the full list) in
knowledge.db, and seeds the reference/lookup rows every other script depends
on: hackathon_domains (from weights.yaml + calculation/aggregation/domain/*.yaml),
hackathon_templates (from templates/reports/**), hackathon_visualization_types
(from render_charts.py's known chart functions). This is the python-script
equivalent of samgraha's own schema/knowledge/*.sql — samgraha never creates
or migrates a standard's own tables, so the standard supplies its own
creation+seed step instead. Idempotent throughout — safe to run more than
once (every other script also calls ensure_schema() defensively on connect).
"""
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import hackathon_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    conn = hackathon_schema.get_conn(db_path)  # get_conn() calls ensure_schema()
    hackathon_schema.seed_domains(conn, str(SCRIPTS_DIR))
    hackathon_schema.seed_templates(conn, str(SCRIPTS_DIR))
    hackathon_schema.seed_visualization_types(conn)
    conn.close()

    write_envelope(out_path, status="ok",
                   message="tables created, domains/templates/visualization_types seeded",
                   tables=["hackathon_teams", "hackathon_domains",
                           "hackathon_deterministic_scores", "hackathon_semantic_runs",
                           "hackathon_semantic_dimension_scores", "hackathon_semantic_findings",
                           "hackathon_narratives", "hackathon_narrative_sections",
                           "hackathon_templates", "hackathon_visualization_types",
                           "hackathon_visualizations"])


if __name__ == "__main__":
    main()
