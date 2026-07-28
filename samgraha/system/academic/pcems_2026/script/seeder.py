"""seeder.py — pcems_2026's seeder for samgraha's MCP activation path.

Reads script/schema/standard.yaml, creates academic_* tables, seeds
domains, scripts, prompts, usecases (with expanded steps), templates,
and custom_data_tables into knowledge.db.

Expected --in envelope: { _samgraha_dir, _knowledge_db }
Returns: {"status": "ok"} on success.

Run by samgraha's activate_standard (seeder.rs), not standalone.
"""
import json
import os
import sqlite3
import sys
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PCEMS_ROOT = SCRIPT_DIR.parent  # pcems_2026/
sys.path.insert(0, str(SCRIPT_DIR / "common"))
from _adapter import parse_step_args, write_envelope
import academic_schema  # noqa: E402

# --- Domain sort orders (from loop.yaml tiers + 00-domain-relationships.md) ---
_DOMAIN_SORT_ORDERS = {
    "introduction": 1,
    "methodology": 2,
    "findings": 3,
    "conclusion": 4,
    "title-and-metadata": 5,
    "references": 6,
}

_DOMAIN_DISPLAY_NAMES = {
    "introduction": "Introduction",
    "methodology": "Methodology",
    "findings": "Findings",
    "conclusion": "Conclusion",
    "title-and-metadata": "Title and Metadata",
    "references": "References",
}

_DOMAIN_WEIGHTS = {
    "introduction": 1.0,
    "methodology": 1.0,
    "findings": 1.0,
    "conclusion": 1.0,
    "title-and-metadata": 1.0,
    "references": 1.0,
}

# --- Usecase step expansion patterns ---
# Each key maps a usecase name pattern to its step list.
# {domain} is substituted at expansion time.
_GENERATION_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather evidence for {domain}",
     "script": "gather-domain-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Generate {domain} section draft",
     "prompt": "generate-{domain}"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist {domain} section draft",
     "script": "persist-section-draft"},
]

_CITATION_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather citations for {domain}",
     "script": "gather-domain-evidence"},
    {"order": 2, "kind": "deterministic",
     "description": "Persist {domain} citations",
     "script": "persist-section-citations"},
    {"order": 3, "kind": "semantic",
     "description": "Audit {domain} citations part for quality",
     "prompt": "semantic-audit-part"},
    {"order": 4, "kind": "deterministic",
     "description": "Persist {domain} citations-part semantic score",
     "script": "persist-domain-semantic-score"},
]

# section-citations-references is a fan-in usecase — collate-references
# reads all other domains' citations and writes the references draft.
# Replaces the generic _CITATION_STEP_TEMPLATES for this one domain only.
_CITATION_REFERENCES_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Collate all citations into references domain draft",
     "script": "collate-references"},
]

_ENRICHMENT_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather {domain} draft for enrichment",
     "script": "gather-domain-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Add citation grounding to {domain}",
     "prompt": "literature-review-pass"},
    {"order": 3, "kind": "semantic",
     "description": "Enrich {domain} with quality improvements",
     "prompt": "section-enrichment"},
    {"order": 4, "kind": "semantic",
     "description": "Audit enriched {domain} for quality issues",
     "prompt": "semantic-audit-part"},
    {"order": 5, "kind": "deterministic",
     "description": "Persist {domain} enrichment-part semantic score",
     "script": "persist-domain-semantic-score"},
    {"order": 6, "kind": "deterministic",
     "description": "Persist enriched {domain} draft",
     "script": "persist-section-draft"},
]

_BUDGET_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Check {domain} word budget",
     "script": "check-word-budget"},
    {"order": 2, "kind": "semantic",
     "description": "Fit {domain} to word budget",
     "prompt": "fit-to-budget"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist budget-fitted {domain} draft",
     "script": "persist-section-draft"},
    {"order": 4, "kind": "semantic",
     "description": "Audit {domain} budget-fit part for quality",
     "prompt": "semantic-audit-part"},
    {"order": 5, "kind": "deterministic",
     "description": "Persist {domain} budget-fit-part semantic score",
     "script": "persist-domain-semantic-score"},
]

_DET_AUDIT_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Run deterministic checks on {domain}",
     "script": "deterministic-audit"},
]

_SEM_AUDIT_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather {domain} evidence for semantic audit",
     "script": "gather-domain-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Score {domain} against rubric",
     "prompt": "semantic-audit"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist {domain} semantic score",
     "script": "persist-domain-semantic-score"},
]

_PLAGIARISM_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather {domain} draft for plagiarism check",
     "script": "gather-plagiarism-context"},
    {"order": 2, "kind": "deterministic",
     "description": "Run fingerprint check on {domain}",
     "script": "deterministic-fingerprint-check"},
    {"order": 3, "kind": "semantic",
     "description": "Audit {domain} for plagiarism patterns",
     "prompt": "plagiarism-fingerprint-audit"},
    {"order": 4, "kind": "semantic",
     "description": "Rewrite flagged spans in {domain}",
     "prompt": "targeted-rewrite"},
    {"order": 5, "kind": "deterministic",
     "description": "Persist {domain} plagiarism findings",
     "script": "persist-plagiarism-findings"},
]

_HUMANIZE_DET_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather {domain} draft for humanize",
     "script": "gather-humanize-context"},
    {"order": 2, "kind": "deterministic",
     "description": "NLP fingerprint fix for {domain}",
     "script": "nlp-fingerprint-fix"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist {domain} humanize pass",
     "script": "persist-humanize-pass"},
]

_HUMANIZE_SEM_STEP_TEMPLATES = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather {domain} draft for LLM humanize",
     "script": "gather-humanize-context"},
    {"order": 2, "kind": "semantic",
     "description": "LLM humanize rewrite for {domain}",
     "prompt": "humanize-section"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist {domain} humanize pass",
     "script": "persist-humanize-pass"},
]

# Map usecase name prefix to step template
_USECASE_STEP_PATTERNS = {
    "generate-section-draft-": _GENERATION_STEP_TEMPLATES,
    "section-citations-": _CITATION_STEP_TEMPLATES,
    "section-enrichment-": _ENRICHMENT_STEP_TEMPLATES,
    "section-budget-fit-": _BUDGET_STEP_TEMPLATES,
    "deterministic-audit-": _DET_AUDIT_STEP_TEMPLATES,
    "semantic-audit-": _SEM_AUDIT_STEP_TEMPLATES,
    "plagiarism-forensic-audit-": _PLAGIARISM_STEP_TEMPLATES,
    "humanize-deterministic-": _HUMANIZE_DET_STEP_TEMPLATES,
    "humanize-semantic-": _HUMANIZE_SEM_STEP_TEMPLATES,
}

# --- Whole-document usecase step templates (exact name match) ---
_NOVELTY_ANALYSIS_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Discover module boundaries in the target repo",
     "script": "discover-modules"},
    {"order": 2, "kind": "deterministic",
     "description": "Gather evidence for each module",
     "script": "gather-module-evidence"},
    {"order": 3, "kind": "semantic",
     "description": "Analyze each module for novelty",
     "prompt": "module-analysis-novelty"},
    {"order": 4, "kind": "deterministic",
     "description": "Persist per-module novelty analysis",
     "script": "persist-module-analysis"},
    {"order": 5, "kind": "deterministic",
     "description": "Gather cross-module evidence",
     "script": "gather-cross-module-evidence"},
    {"order": 6, "kind": "semantic",
     "description": "Cross-module novelty analysis",
     "prompt": "cross-module-analysis-novelty"},
    {"order": 7, "kind": "deterministic",
     "description": "Persist cross-module novelty analysis",
     "script": "persist-cross-module-analysis"},
]

_GAP_ANALYSIS_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Discover module boundaries in the target repo",
     "script": "discover-modules"},
    {"order": 2, "kind": "deterministic",
     "description": "Gather evidence for each module",
     "script": "gather-module-evidence"},
    {"order": 3, "kind": "semantic",
     "description": "Analyze each module for gaps",
     "prompt": "module-analysis-gaps"},
    {"order": 4, "kind": "deterministic",
     "description": "Persist per-module gap analysis",
     "script": "persist-module-analysis"},
    {"order": 5, "kind": "deterministic",
     "description": "Gather cross-module evidence",
     "script": "gather-cross-module-evidence"},
    {"order": 6, "kind": "semantic",
     "description": "Cross-module gap analysis",
     "prompt": "cross-module-analysis-gaps"},
    {"order": 7, "kind": "deterministic",
     "description": "Persist cross-module gap analysis",
     "script": "persist-cross-module-analysis"},
]

_MATHEMATICS_ANALYSIS_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Discover module boundaries in the target repo",
     "script": "discover-modules"},
    {"order": 2, "kind": "deterministic",
     "description": "Gather evidence for each module",
     "script": "gather-module-evidence"},
    {"order": 3, "kind": "semantic",
     "description": "Analyze each module for mathematical formalization",
     "prompt": "module-analysis-mathematics"},
    {"order": 4, "kind": "deterministic",
     "description": "Persist per-module mathematics analysis",
     "script": "persist-module-analysis"},
    {"order": 5, "kind": "deterministic",
     "description": "Gather cross-module evidence",
     "script": "gather-cross-module-evidence"},
    {"order": 6, "kind": "semantic",
     "description": "Cross-module mathematics analysis",
     "prompt": "cross-module-analysis-mathematics"},
    {"order": 7, "kind": "deterministic",
     "description": "Persist cross-module mathematics analysis",
     "script": "persist-cross-module-analysis"},
]

# diagram-architecture-analysis: 3 cross-module passes (architecture,
# dependencies, interactions) instead of 1. Uses INSERT OR IGNORE-idempotent
# discover-modules/gather-module-evidence, safe to re-run independently.
_DIAGRAM_ARCHITECTURE_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Discover module boundaries in the target repo",
     "script": "discover-modules"},
    {"order": 2, "kind": "deterministic",
     "description": "Gather evidence for each module",
     "script": "gather-module-evidence"},
    {"order": 3, "kind": "deterministic",
     "description": "Gather cross-module evidence",
     "script": "gather-cross-module-evidence"},
    {"order": 4, "kind": "semantic",
     "description": "Cross-module architecture analysis",
     "prompt": "cross-module-analysis-architecture"},
    {"order": 5, "kind": "deterministic",
     "description": "Persist cross-module architecture analysis",
     "script": "persist-cross-module-analysis"},
    {"order": 6, "kind": "semantic",
     "description": "Cross-module dependency analysis",
     "prompt": "cross-module-analysis-dependencies"},
    {"order": 7, "kind": "deterministic",
     "description": "Persist cross-module dependency analysis",
     "script": "persist-cross-module-analysis"},
    {"order": 8, "kind": "semantic",
     "description": "Cross-module interaction analysis",
     "prompt": "cross-module-analysis-interactions"},
    {"order": 9, "kind": "deterministic",
     "description": "Persist cross-module interaction analysis",
     "script": "persist-cross-module-analysis"},
]

_DOCS_FIRST_INGESTION_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Discover module structure from docs/paper/{system}/modules/",
     "script": "discover-docs-modules"},
    {"order": 2, "kind": "deterministic",
     "description": "Load pre-existing per-module analysis into DB",
     "script": "load-docs-module-analysis"},
    {"order": 3, "kind": "deterministic",
     "description": "Load pre-existing cross-module analysis into DB",
     "script": "load-docs-cross-module-analysis"},
]

_CROSS_SECTION_AUDIT_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Concatenate all domain section texts for cross-section review",
     "script": "gather-cross-section-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Cross-section consistency review",
     "prompt": "cross-section-semantic-audit"},
]

_DOCUMENT_AUDIT_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Concatenate all domain section texts for whole-document review",
     "script": "gather-document-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Whole-document holistic review",
     "prompt": "document-semantic-audit"},
]

_REVIEWER_SIMULATION_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Concatenate all domain section texts for reviewer simulation",
     "script": "gather-document-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Three-persona reviewer simulation",
     "prompt": "reviewer-simulation"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist reviewer simulation results",
     "script": "persist-reviewer-simulation"},
]

_CALCULATE_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Calculate final scores from semantic + deterministic buckets",
     "script": "calculate"},
]

_RENDER_CHARTS_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Generate chart images from score/audit data",
     "script": "render-charts"},
]

_RENDER_AUDIT_REPORT_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Generate audit report from score/audit/plagiarism results",
     "script": "generate-audit-report"},
    {"order": 2, "kind": "deterministic",
     "description": "Generate chart images for audit report",
     "script": "render-charts"},
]

_RENDER_PAPER_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Rasterize inline mermaid diagrams to PNG",
     "script": "extract-mermaid-images"},
    {"order": 2, "kind": "deterministic",
     "description": "Assemble all domain drafts into one HTML document",
     "script": "assemble-final-document"},
    {"order": 3, "kind": "deterministic",
     "description": "Convert assembled HTML to DOCX via pandoc",
     "script": "render-docx"},
    {"order": 4, "kind": "deterministic",
     "description": "Convert assembled HTML to PDF via Playwright/Chromium",
     "script": "render-pdf"},
]

# references has no dedicated generate-references prompt — per
# 4a-generate-references.md, it uses the generic generate-section prompt
# with template=templates/generation/markdown/references.md.
_REFERENCES_GENERATION_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather evidence for references",
     "script": "gather-domain-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Generate references section draft",
     "prompt": "generate-section"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist references section draft",
     "script": "persist-section-draft"},
]

# Cross-cutting section generation — reads the already-persisted
# academic_cross_module_analysis row and generates polished section prose.
_CROSS_CUTTING_GENERATION_STEPS = [
    {"order": 1, "kind": "deterministic",
     "description": "Gather cross-cutting analysis for {domain}",
     "script": "gather-cross-cutting-evidence"},
    {"order": 2, "kind": "semantic",
     "description": "Generate {domain} section draft from analysis",
     "prompt": "generate-{domain}"},
    {"order": 3, "kind": "deterministic",
     "description": "Persist {domain} section draft",
     "script": "persist-section-draft"},
]

def _make_cross_cutting_steps(domain):
    """Create pre-substituted step list for a cross-cutting generate usecase."""
    return [
        {k: (v.replace("{domain}", domain) if isinstance(v, str) else v)
         for k, v in s.items()}
        for s in _CROSS_CUTTING_GENERATION_STEPS
    ]

# Exact-name match map for whole-document usecases
_WHOLE_DOCUMENT_STEP_MAP = {
    "novelty-analysis": _NOVELTY_ANALYSIS_STEPS,
    "gap-analysis": _GAP_ANALYSIS_STEPS,
    "mathematics-analysis": _MATHEMATICS_ANALYSIS_STEPS,
    "diagram-architecture-analysis": _DIAGRAM_ARCHITECTURE_STEPS,
    "docs-first-ingestion": _DOCS_FIRST_INGESTION_STEPS,
    "cross-section-semantic-audit": _CROSS_SECTION_AUDIT_STEPS,
    "document-semantic-audit": _DOCUMENT_AUDIT_STEPS,
    "reviewer-simulation": _REVIEWER_SIMULATION_STEPS,
    "calculate": _CALCULATE_STEPS,
    "render-charts": _RENDER_CHARTS_STEPS,
    "render-audit-report": _RENDER_AUDIT_REPORT_STEPS,
    "render-paper": _RENDER_PAPER_STEPS,
    "generate-section-draft-references": _REFERENCES_GENERATION_STEPS,
    "generate-section-draft-novelty": _make_cross_cutting_steps("novelty"),
    "generate-section-draft-gaps": _make_cross_cutting_steps("gaps"),
    "generate-section-draft-mathematics": _make_cross_cutting_steps("mathematics"),
}


def _expand_domain_steps(uc_name):
    """Given a usecase name, expand step templates.
    First checks exact-name match for whole-document usecases,
    then special-cases per-domain usecases that need non-default steps,
    then falls back to prefix-based expansion for per-domain usecases."""
    # Exact-name match (whole-document usecases)
    if uc_name in _WHOLE_DOCUMENT_STEP_MAP:
        return list(_WHOLE_DOCUMENT_STEP_MAP[uc_name])
    # Special-case: section-citations-references uses collate-references
    # (fan-in), not the generic citation templates.
    if uc_name == "section-citations-references":
        return list(_CITATION_REFERENCES_STEPS)
    # Prefix-based match (per-domain usecases)
    for prefix, tmpl in _USECASE_STEP_PATTERNS.items():
        if uc_name.startswith(prefix):
            domain = uc_name[len(prefix):]
            return [
                {k: (v.replace("{domain}", domain) if isinstance(v, str) else v)
                 for k, v in s.items()}
                for s in tmpl
            ]
    return []


def _read_prompt_content(location, standard_root):
    """Read prompt file content from the standard's tree.
    location is relative to script/schema/ (the YAML's own directory).
    standard_root is the standard's root directory (where script/schema/ lives).
    Tries relative to the YAML's directory, then falls back to absolute."""
    yaml_dir = standard_root / "script" / "schema"
    loc = Path(location)
    if loc.is_absolute():
        target = loc
    else:
        target = (yaml_dir / location).resolve()
    if target.exists():
        return target.read_text(encoding="utf-8")
    return f"[prompt file not found: {location} -> {target}]"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    seeder_dir = Path(payload.get("_samgraha_dir", "")).parent
    if not seeder_dir.exists():
        seeder_dir = PCEMS_ROOT

    # Load standard.yaml
    yaml_path = SCRIPT_DIR / "schema" / "standard.yaml"
    if not yaml_path.exists():
        write_envelope(out_path, status="error",
                       message=f"standard.yaml not found at {yaml_path}")
        return
    with open(yaml_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    standard = spec.get("name", "pcems_2026")

    conn = academic_schema.get_conn(db_path)

    # 1. Create academic_* tables
    academic_schema.ensure_schema(conn)

    # 2. Seed 6 structural domains + reviewer-simulation + 3 cross-cutting
    # domains into both domain (core FK) and academic_domains.
    # Cross-cutting domains (novelty, gaps, mathematics) get sort_orders
    # in the 90s alongside reviewer-simulation's 99.
    all_domain_keys = list(_DOMAIN_SORT_ORDERS.keys()) + [
        "reviewer-simulation", "novelty", "gaps", "mathematics",
    ]
    all_domain_display = dict(_DOMAIN_DISPLAY_NAMES, **{
        "reviewer-simulation": "Reviewer Simulation",
        "novelty": "Novelty",
        "gaps": "Gaps",
        "mathematics": "Mathematics",
    })
    all_domain_orders = dict(_DOMAIN_SORT_ORDERS, **{
        "reviewer-simulation": 99,
        "novelty": 91,
        "gaps": 92,
        "mathematics": 93,
    })

    # Core domain table (usecase.domain_id FK target)
    for dkey in all_domain_keys:
        conn.execute(
            "INSERT OR IGNORE INTO domain (standard, key, sort_order, description) VALUES (?, ?, ?, ?)",
            (standard, dkey, all_domain_orders[dkey], all_domain_display[dkey]),
        )
    conn.commit()

    # Academic domains (standard's own lookup table)
    domains = [
        (key, all_domain_display[key], all_domain_orders[key], 1.0)
        for key in all_domain_keys
    ]
    academic_schema.seed_domains(conn, domains)

    # 3. Seed templates from system directory
    academic_schema.seed_templates(conn, str(PCEMS_ROOT))

    # 4. Seed visualization types
    academic_schema.seed_visualization_types(conn, [
        ("domain-score-bar", "per_domain", "Bar chart of latest domain scores"),
        ("deterministic-findings-heatmap", "per_domain", "Heatmap of deterministic check pass/fail"),
        ("cross-section-score", "per_paper", "Cross-section consistency score"),
        ("document-review-score", "per_paper", "Document review score"),
        ("pipeline-progress-matrix", "per_paper", "6x9 heatmap of domain x stage pipeline progress"),
        ("section-part-score-comparison", "per_domain", "Grouped bar: citations/enrichment/budget-fit/full scores per domain"),
        ("citation-count-bar", "per_domain", "Stacked bar of in-repo vs literature citation counts per domain"),
        ("budget-fit-gauge", "per_domain", "Per-domain word count vs configured min/max range"),
        ("whole-paper-budget-gauge", "per_paper", "Total word count vs paper-budget.yaml range"),
        ("humanize-pass-chart", "per_domain", "Bar per domain: deterministic-only vs needed-semantic-pass counts"),
    ])

    # 5. Insert scripts from standard.yaml
    script_id_map = {}  # name -> id
    for s in spec.get("scripts", []):
        name = s["name"]
        location = s["location"]
        purpose = s.get("purpose", "")
        # Absolutize location relative to script/schema/
        abs_loc = str((SCRIPT_DIR / location).resolve())
        existing = conn.execute(
            "SELECT id FROM script WHERE standard=? AND name=?",
            (standard, name),
        ).fetchone()
        if existing:
            script_id_map[name] = existing["id"]
        else:
            cur = conn.execute(
                "INSERT INTO script (standard, name, location, purpose) VALUES (?, ?, ?, ?)",
                (standard, name, abs_loc, purpose),
            )
            script_id_map[name] = cur.lastrowid

    # 6. Insert prompts from standard.yaml
    prompt_id_map = {}  # name -> id
    for p in spec.get("prompts", []):
        name = p["name"]
        location = p["location"]
        content = _read_prompt_content(location, PCEMS_ROOT)
        existing = conn.execute(
            "SELECT id FROM prompt WHERE standard=? AND name=?",
            (standard, name),
        ).fetchone()
        if existing:
            prompt_id_map[name] = existing["id"]
        else:
            cur = conn.execute(
                "INSERT INTO prompt (standard, name, content, purpose) VALUES (?, ?, ?, ?)",
                (standard, name, content, f"prompt: {name}"),
            )
            prompt_id_map[name] = cur.lastrowid

    # 7. Insert usecases + steps
    for uc in spec.get("usecases", []):
        uc_name = uc["name"]
        uc_desc = uc.get("description", "")
        steps = uc.get("steps", [])

        # Expand empty steps based on naming pattern
        if not steps:
            steps = _expand_domain_steps(uc_name)

        # Insert usecase
        existing_uc = conn.execute(
            "SELECT id FROM usecase WHERE standard=? AND name=?",
            (standard, uc_name),
        ).fetchone()
        if existing_uc:
            uc_id = existing_uc["id"]
        else:
            # Get domain_id if this is a domain-specific usecase
            domain_id = None
            for dkey in all_domain_keys:
                if dkey in uc_name:
                    row = conn.execute(
                        "SELECT id FROM domain WHERE standard=? AND key=?",
                        (standard, dkey),
                    ).fetchone()
                    if row:
                        domain_id = row["id"]
                    break
            cur = conn.execute(
                "INSERT INTO usecase (standard, name, description, domain_id) VALUES (?, ?, ?, ?)",
                (standard, uc_name, uc_desc, domain_id),
            )
            uc_id = cur.lastrowid

        # Insert steps
        for step in steps:
            order = step["order"]
            kind = step["kind"]
            desc = step.get("description", "")

            existing_step = conn.execute(
                "SELECT id FROM step WHERE usecase_id=? AND step_order=?",
                (uc_id, order),
            ).fetchone()
            if existing_step:
                step_id = existing_step["id"]
            else:
                cur = conn.execute(
                    "INSERT INTO step (usecase_id, step_order, kind, description) VALUES (?, ?, ?, ?)",
                    (uc_id, order, kind, desc),
                )
                step_id = cur.lastrowid

            # Map step to script or prompt
            if kind == "deterministic" and "script" in step:
                sname = step["script"]
                if sname in script_id_map:
                    conn.execute(
                        "INSERT OR IGNORE INTO step_script (step_id, script_id) VALUES (?, ?)",
                        (step_id, script_id_map[sname]),
                    )
            elif kind == "semantic" and "prompt" in step:
                pname = step["prompt"]
                if pname in prompt_id_map:
                    conn.execute(
                        "INSERT OR IGNORE INTO step_prompt (step_id, prompt_id) VALUES (?, ?)",
                        (step_id, prompt_id_map[pname]),
                    )

    conn.commit()

    # 8. Seed calculation dependency edges
    academic_schema.seed_calculation_dependencies(
        conn, _build_calculation_dependency_edges())

    conn.commit()
    conn.close()

    write_envelope(out_path, status="ok",
                   message="pcems_2026 seeder: academic tables created, "
                           "domains/scripts/prompts/usecases seeded")


def _build_calculation_dependency_edges():
    """Calculation dependency edges for pcems_2026's 6 structural domains."""
    edges = []
    for d in _DOMAIN_SORT_ORDERS:
        edges.append(dict(
            calc_path=f"generation/{d}.yaml",
            depends_on_kind="db_table",
            depends_on="academic_narratives",
            consumed_by="check-word-budget,deterministic-audit",
        ))
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
        edges.append(dict(
            calc_path=f"report/semantic/ensemble/{d}.yaml",
            depends_on_kind="db_scope",
            depends_on="academic_semantic_runs.section-full",
            consumed_by=None,
        ))
        for part in ["citations", "enrichment", "budget-fit"]:
            edges.append(dict(
                calc_path=f"report/semantic/ensemble/{d}-{part}.yaml",
                depends_on_kind="db_scope",
                depends_on=f"academic_semantic_runs.section-part.{part}",
                consumed_by=None,
            ))
    # Shared summary files
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


if __name__ == "__main__":
    main()
