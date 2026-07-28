"""init_schema.py — creates pcems_2026's own copy of the shared academic_*
tables in knowledge.db and seeds domains + templates. Idempotent — safe to
run more than once. Forked from base_academic/script/schema-init/
init_schema.py.
"""
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

# Domains that have aggregation/domain/*.yaml + ensemble/*.yaml files.
# Generated from the directory listing — not hand-maintained.
_AGGREGATION_DOMAINS = [
    "title-and-metadata", "introduction", "methodology",
    "findings", "conclusion", "references",
]

# Ensemble part kinds (each domain has a base + these three variants).
_ENSEMBLE_PARTS = ["citations", "enrichment", "budget-fit"]


def _build_calculation_dependency_edges():
    """Generate the full calculation dependency edge list from the domain
    list and shared report files. One set of rows total (standard-level
    metadata, not per-paper)."""
    edges = []
    for d in _AGGREGATION_DOMAINS:
        # generation/{d}.yaml reads academic_narratives — two real readers,
        # one row (consumed_by is a comma-joined list, sorted to match
        # audit_calculation_wiring.py's join convention, not two competing
        # rows for the same edge — schema/23's comment explains why).
        edges.append(dict(
            calc_path=f"generation/{d}.yaml",
            depends_on_kind="db_table",
            depends_on="academic_narratives",
            consumed_by="check-word-budget,deterministic-audit",
        ))
        # report/aggregation/domain/{d}.yaml depends on generation + semantic blend
        edges.append(dict(
            calc_path=f"report/aggregation/domain/{d}.yaml",
            depends_on_kind="calc_file",
            depends_on=f"generation/{d}.yaml",
            consumed_by=None,
        ))
        edges.append(dict(
            calc_path=f"report/aggregation/domain/{d}.yaml",
            depends_on_kind="calc_file",
            depends_on="report/semantic/full-part-blend.yaml",
            consumed_by=None,
        ))
        # report/semantic/ensemble/{d}.yaml reads academic_semantic_runs
        edges.append(dict(
            calc_path=f"report/semantic/ensemble/{d}.yaml",
            depends_on_kind="db_scope",
            depends_on="academic_semantic_runs.section-full",
            consumed_by=None,
        ))
        # part-level ensembles
        for part in _ENSEMBLE_PARTS:
            edges.append(dict(
                calc_path=f"report/semantic/ensemble/{d}-{part}.yaml",
                depends_on_kind="db_scope",
                depends_on=f"academic_semantic_runs.section-part.{part}",
                consumed_by=None,
            ))
    # Shared summary/report files
    edges.append(dict(
        calc_path="report/summary/final_score.yaml",
        depends_on_kind="db_scope",
        depends_on="academic_semantic_runs.section-full",
        consumed_by="calculate",
    ))
    edges.append(dict(
        calc_path="report/summary/final_score.yaml",
        depends_on_kind="db_table",
        depends_on="academic_deterministic_findings",
        consumed_by="calculate",
    ))
    edges.append(dict(
        calc_path="report/semantic/full-part-blend.yaml",
        depends_on_kind="db_scope",
        depends_on="academic_semantic_runs.section-full",
        consumed_by=None,
    ))
    edges.append(dict(
        calc_path="report/semantic/full-part-blend.yaml",
        depends_on_kind="calc_file",
        depends_on="report/semantic/section-parts.yaml",
        consumed_by=None,
    ))
    return edges


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    standard = payload.get("standard", "pcems_2026")

    conn = academic_schema.get_conn(db_path)

    # Run ALTER TABLE migrations for columns/indexes added after original DDL
    academic_schema.ensure_schema(conn)

    # Seed domains from the concrete system's domain list if provided in payload
    domains_list = payload.get("domains")
    if domains_list:
        academic_schema.seed_domains(conn, domains_list)

    # Seed cross-cutting audit domains (not per-section, used by
    # cross-section-semantic-audit, document-semantic-audit, and
    # reviewer-simulation usecases that store results with a domain key).
    academic_schema.seed_domains(conn, [
        ("reviewer-simulation", "Reviewer Simulation", 99, 1.0),
    ])

    # Seed templates from the system directory
    system_dir = str(SCRIPTS_DIR / "..")
    academic_schema.seed_templates(conn, system_dir)

    # Seed visualization types
    academic_schema.seed_visualization_types(conn, [
        ("domain-score-bar", "per_domain", "Bar chart of latest domain scores"),
        ("deterministic-findings-heatmap", "per_domain", "Heatmap of deterministic check pass/fail"),
        ("cross-section-score", "per_paper", "Cross-section consistency score"),
        ("document-review-score", "per_paper", "Document review score"),
        ("pipeline-progress-matrix", "per_paper", "12x9 heatmap of domain x stage pipeline progress"),
        ("section-part-score-comparison", "per_domain", "Grouped bar: citations/enrichment/budget-fit/full scores per domain"),
        ("citation-count-bar", "per_domain", "Stacked bar of in-repo vs literature citation counts per domain"),
        ("budget-fit-gauge", "per_domain", "Per-domain word count vs configured min/max range"),
        ("whole-paper-budget-gauge", "per_paper", "Total word count vs paper-budget.yaml range"),
        ("humanize-pass-chart", "per_domain", "Bar per domain: deterministic-only vs needed-semantic-pass counts"),
    ])

    # Seed calculation dependency graph
    academic_schema.seed_calculation_dependencies(
        conn, _build_calculation_dependency_edges())

    conn.close()

    write_envelope(out_path, status="ok",
                   message="academic tables created, domains/templates/calc-deps seeded",
                   tables=["academic_papers", "academic_repos", "academic_domains",
                            "academic_modules", "academic_module_analysis",
                            "academic_cross_module_analysis", "academic_narratives",
                            "academic_narrative_sections", "academic_semantic_runs",
                            "academic_semantic_dimension_scores", "academic_semantic_findings",
                            "academic_plagiarism_findings", "academic_humanize_passes",
                            "academic_templates", "academic_score_history",
                            "academic_deterministic_findings",
                            "academic_visualization_types", "academic_visualizations",
                            "academic_report_history", "academic_section_citations",
                            "academic_proposals", "academic_calculation_dependencies"])


if __name__ == "__main__":
    main()
