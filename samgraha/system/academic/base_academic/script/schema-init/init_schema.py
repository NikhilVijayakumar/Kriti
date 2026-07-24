"""init_schema.py — creates base_academic's own tables in knowledge.db
and seeds domains + templates. Idempotent — safe to run more than once.
"""
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    standard = payload.get("standard", "base_academic")

    conn = academic_schema.get_conn(db_path)

    # Seed domains from the concrete system's domain list if provided in payload
    domains_list = payload.get("domains")
    if domains_list:
        academic_schema.seed_domains(conn, domains_list)

    # Seed templates from the system directory
    system_dir = str(SCRIPTS_DIR / "..")
    academic_schema.seed_templates(conn, system_dir)

    # Seed visualization types
    academic_schema.seed_visualization_types(conn, [
        ("domain-score-bar", "per_domain", "Bar chart of latest domain scores"),
        ("deterministic-findings-heatmap", "per_domain", "Heatmap of deterministic check pass/fail"),
        ("cross-section-score", "per_paper", "Cross-section consistency score"),
        ("document-review-score", "per_paper", "Document review score"),
    ])

    conn.close()

    write_envelope(out_path, status="ok",
                   message="academic tables created, domains/templates seeded",
                   tables=["academic_papers", "academic_repos", "academic_domains",
                            "academic_modules", "academic_module_analysis",
                            "academic_cross_module_analysis", "academic_narratives",
                            "academic_narrative_sections", "academic_semantic_runs",
                            "academic_semantic_dimension_scores", "academic_semantic_findings",
                            "academic_plagiarism_findings", "academic_humanize_passes",
                            "academic_templates", "academic_score_history",
                            "academic_deterministic_findings",
                            "academic_visualization_types", "academic_visualizations",
                            "academic_report_history"])


if __name__ == "__main__":
    main()
