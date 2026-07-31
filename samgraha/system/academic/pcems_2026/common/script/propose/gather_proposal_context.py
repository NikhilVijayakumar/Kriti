"""gather_proposal_context.py — det step, first in every propose-* chain.

Gathers the context needed to draft a proposal: upstream analyses,
domain lists, rubric info, failing findings, or redraft context.

Expected --in payload:
  {paper_id: int, phase: str, commit_sha: str,
   scope_domain_id: int (optional, fix only),
   user_comment: str (optional, fix/user-request only),
   models: list (optional, audit only)}
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import academic_schema  # noqa: E402

import yaml  # noqa: E402

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_BASE = os.path.normpath(os.path.join(_SCRIPT_DIR, "..", ".."))
_CALC_GEN_DIR = os.path.join(_REPO_BASE, "calculation", "generation")
_RUBRIC_DIR = os.path.join(_REPO_BASE, "audit", "semantic", "document")

_PER_DOMAIN_REPORT_KINDS = [
    "deterministic", "semantic-full", "semantic-part",
    "plagiarism", "humanize", "summary",
]


def _load_paper_meta(conn, paper_id):
    """Shared by all four branches — title, fetched once per invocation."""
    return conn.execute(
        "SELECT title FROM academic_papers WHERE id=?", (paper_id,)).fetchone()


def _redraft_context(conn, paper_id, phase, scope_domain_id):
    """If the latest row for this (phase, scope_domain) is rejected,
    surface it for the redraft (§6a)."""
    import json
    row = conn.execute(
        "SELECT content_md, user_comment, iteration "
        "FROM academic_proposal_review "
        "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
        "AND is_latest=1 AND review_status='rejected'",
        (paper_id, phase, scope_domain_id)).fetchone()
    return dict(row) if row else None


def _load_generation_rules(domain_key):
    """calculation/generation/{domain}.yaml's checks — same file
    check_word_budget.py and deterministic_audit.py already read."""
    path = os.path.join(_CALC_GEN_DIR, f"{domain_key}.yaml")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    checks = data.get("checks", [])
    wc = next((c.get("config", {}) for c in checks
               if c.get("rule") == "word_count_in_range"), None)
    return {
        "word_min": wc.get("min") if wc else None,
        "word_max": wc.get("max") if wc else None,
        "check_count": len(checks),
        "critical_count": sum(1 for c in checks if c.get("severity") == "critical"),
        "check_names": [c.get("name", c.get("id", "")) for c in checks],
    }


def _load_semantic_rubric(domain_key):
    """audit/semantic/document/{domain}.md — the file prompt/semantic-
    audit/semantic-audit.md names as its rubric source.  Counts criterion
    rows matching the ``| C* |`` table convention used by concrete
    systems' rubric files.  Returns None if the file is absent (the audit
    itself would fail the same way at run time)."""
    path = os.path.join(_RUBRIC_DIR, f"{domain_key}.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    criterion_count = len(re.findall(r"^\|\s*C\d+", text, re.MULTILINE))
    if criterion_count == 0:
        criterion_count = text.count("\n- **C")
    return {"criterion_count": criterion_count, "rubric_path": path}


def _gather_generation_context(conn, paper_id):
    """Gather upstream analysis summaries + domain list for generation proposal."""
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]

    analyses = {}
    for kind in ("novelty", "gaps", "mathematics", "architecture", "figures", "tables"):
        row = conn.execute(
            "SELECT content FROM academic_cross_module_analysis "
            "WHERE paper_id=? AND analysis_kind=? "
            "ORDER BY created_at DESC LIMIT 1", (paper_id, kind)).fetchone()
        analyses[kind] = row["content"] if row else "(none yet)"

    domain_details = []
    for key in domains:
        domain_id_row = conn.execute(
            "SELECT id FROM academic_domains WHERE key=?", (key,)).fetchone()
        if not domain_id_row:
            continue
        stage_row = conn.execute(
            "SELECT stage FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY iteration DESC LIMIT 1",
            (paper_id, domain_id_row["id"])).fetchone()
        stage = stage_row["stage"] if stage_row else "not started"
        rules = _load_generation_rules(key)
        domain_details.append({
            "domain_key": key,
            "stage": stage,
            "word_min": rules["word_min"] if rules else None,
            "word_max": rules["word_max"] if rules else None,
            "check_count": rules["check_count"] if rules else 0,
            "critical_count": rules["critical_count"] if rules else 0,
        })

    return {
        "domains": domain_details,
        "novelty_summary": analyses.get("novelty", ""),
        "gaps_summary": analyses.get("gaps", ""),
        "math_summary": analyses.get("mathematics", ""),
        "diagram_summary": analyses.get("architecture", ""),
        "figures_summary": analyses.get("figures", ""),
        "tables_summary": analyses.get("tables", ""),
    }


def _gather_audit_context(conn, paper_id, models=None):
    """Gather generated domains + rubric info for audit proposal."""
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]

    domain_details = []
    for key in domains:
        rules = _load_generation_rules(key)
        rubric = _load_semantic_rubric(key)
        domain_details.append({
            "domain_key": key,
            "det_rule_count": rules["check_count"] if rules else 0,
            "det_critical_count": rules["critical_count"] if rules else 0,
            "rubric_criterion_count": rubric["criterion_count"] if rubric else 0,
            "rubric_found": rubric is not None,
        })

    return {"domains": domain_details, "models": models or ["default"]}


def _gather_report_context(conn, paper_id):
    """Gather latest score + forward-looking report counts for report
    proposal. render-charts/render-audit-report/render-paper are 100%
    deterministic (chevron templates + DB data, no LLM step anywhere in
    that chain, confirmed against standard.yaml — render-paper doesn't
    even have a script registered yet, per plan/usecase/6c-render-paper.md's
    "planned, not yet built"). A report proposal has nothing for a model
    to judge — every fact in it is already computed here — so this
    function builds `summary`/`content_md` itself instead of staging a
    semantic step to restate the same numbers in prose. propose-report
    is deterministic-only (3 steps: gather/persist/render, no prompt) —
    see standard.yaml and run_full_workflow.py's _checkpoint()."""
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]

    score_row = conn.execute(
        "SELECT final_score, score_band FROM academic_score_history "
        "WHERE paper_id=? AND domain_id IS NULL "
        "ORDER BY calculated_at DESC LIMIT 1", (paper_id,)).fetchone()

    domain_count = len(domains)
    per_domain_kind_count = len(_PER_DOMAIN_REPORT_KINDS)
    whole_run_reports = ["pipeline-progress", "whole-paper-summary"]
    final_score = score_row["final_score"] if score_row else None
    score_band = score_row["score_band"] if score_row else None

    # Layer 4 — reviewer-simulation runs after the pre-submission audits,
    # its verdict belongs on the same "about to render" gate as the
    # calculated score so a human sees both before approving.
    rs_row = conn.execute(
        "SELECT overall_score, reasoning FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=(SELECT id FROM academic_domains "
        "WHERE key='reviewer-simulation') ORDER BY run_number DESC LIMIT 1",
        (paper_id,)).fetchone()
    reviewer_sim_score = rs_row["overall_score"] if rs_row else None
    # reasoning holds "Decision: X (overall_score=N/30)" — see
    # persist_reviewer_simulation.py's _reshape().
    reviewer_sim_decision = rs_row["reasoning"] if rs_row else "not yet run"

    computed = {
        "current_final_score": final_score,
        "current_score_band": score_band,
        "domain_count": domain_count,
        "per_domain_kind_count": per_domain_kind_count,
        "total_domain_reports": domain_count * per_domain_kind_count,
        "whole_run_reports": whole_run_reports,
        "reviewer_simulation_score": reviewer_sim_score,
        "reviewer_simulation_decision": reviewer_sim_decision,
    }
    score_label = f"{final_score} ({score_band})" if score_row else "not yet calculated"
    summary = (f"Score {score_label} — {reviewer_sim_decision} — will (re)render "
               f"{computed['total_domain_reports']} domain reports "
               f"({domain_count} domains × {per_domain_kind_count} kinds) "
               f"+ {len(whole_run_reports)} whole-run reports "
               f"({', '.join(whole_run_reports)}).")

    return {"computed_context": computed, "summary": summary, "content_md": summary}


def _gather_fix_context(conn, paper_id, domain_id, user_comment):
    """Gather failing findings or user comment for fix proposal.
    domain_id is the already-resolved academic_domains.id (request_fix.py
    resolves the key -> id itself, exact-match-or-error — see script/
    propose/request_fix.py's _resolve_domain()), not a raw key string."""
    target_domain = None
    if domain_id:
        row = conn.execute(
            "SELECT id, key FROM academic_domains WHERE id=?",
            (domain_id,)).fetchone()
        if row:
            target_domain = {"id": row["id"], "key": row["key"]}

    triggering_findings = []
    if target_domain:
        finding_row = conn.execute(
            "SELECT findings FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? AND verdict='FAIL' "
            "ORDER BY created_at DESC LIMIT 1",
            (paper_id, target_domain["id"])).fetchone()
        if finding_row:
            all_checks = json.loads(finding_row["findings"])
            triggering_findings = [c for c in all_checks
                                   if not c.get("passed")]

    return {
        "target_domain": target_domain,
        "user_comment": user_comment,
        "triggering_findings": triggering_findings,
        "triggering_finding_count": len(triggering_findings),
    }


def _gather_step0_fix_context(conn, paper_id, step0_finding_id):
    """Gather context for fixing a Step 0 claim finding.
    Resolves the target directly from academic_step0_claim_findings.id,
    bypassing the domain-based path (Step 0 claims have no manuscript-domain)."""
    row = conn.execute(
        "SELECT * FROM academic_step0_claim_findings WHERE id=?",
        (step0_finding_id,)).fetchone()
    if not row:
        return {"error": f"step0_finding_id={step0_finding_id} not found"}
    return {
        "table_name": row["table_name"],
        "row_id": row["row_id"],
        "check_kind": row["check_kind"],
        "verdict": row["verdict"],
        "evidence_note": row["evidence_note"],
        "finding_id": step0_finding_id,
        "module_id": row["module_id"],
    }


_STAGE_PRIORITY = {
    "humanize": 6, "polish": 5, "budget-fit": 4,
    "enrich": 3, "cite": 2, "generate": 1,
}

def _get_latest_narrative_text(conn, paper_id, domain_id):
    """Get the latest-fully-processed narrative text for (paper, domain).
    Returns concatenated heading + text from academic_narrative_sections,
    ordered by sort_order, for the narrative row with the highest stage
    priority and highest iteration within that stage."""
    rows = conn.execute(
        "SELECT n.id, n.stage, n.iteration "
        "FROM academic_narratives n "
        "WHERE n.paper_id=? AND n.domain_id=? "
        "ORDER BY "
        "  CASE n.stage "
        "    WHEN 'humanize' THEN 6 WHEN 'polish' THEN 5 "
        "    WHEN 'budget-fit' THEN 4 WHEN 'enrich' THEN 3 "
        "    WHEN 'cite' THEN 2 WHEN 'generate' THEN 1 "
        "  END DESC, n.iteration DESC "
        "LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    if not rows:
        return None
    sections = conn.execute(
        "SELECT heading, text FROM academic_narrative_sections "
        "WHERE narrative_id=? ORDER BY sort_order",
        (rows["id"],),
    ).fetchall()
    parts = []
    for s in sections:
        heading = s["heading"].strip()
        text = s["text"].strip()
        if heading:
            parts.append(f"## {heading}")
        if text:
            parts.append(text)
    return "\n\n".join(parts) if parts else None


def _get_domain_id(conn, domain_key):
    row = conn.execute(
        "SELECT id FROM academic_domains WHERE key=?", (domain_key,)).fetchone()
    return row["id"] if row else None


def _gather_input_context(repo_root):
    """Gather repo file tree and input scaffold for the input proposal.
    Scans docs/ for candidate source folders, reads metadata + spec
    templates so the LLM has real context to propose weights."""
    repo_root_str = str(repo_root)
    docs_dir = os.path.join(repo_root_str, "docs")
    candidate_sources = {}
    if os.path.isdir(docs_dir):
        for entry in sorted(os.listdir(docs_dir)):
            epath = os.path.join(docs_dir, entry)
            if os.path.isdir(epath):
                files = []
                for root, dirs, fnames in os.walk(epath):
                    dirs[:] = [d for d in dirs
                               if not d.startswith(".") and d != "__pycache__"]
                    for f in fnames:
                        if f.endswith((".md", ".yaml", ".rst", ".txt")):
                            rel = os.path.relpath(os.path.join(root, f), docs_dir)
                            files.append(rel)
                if files:
                    candidate_sources[entry] = files

    # Read the metadata scaffold from step0-extract/input/templates/
    # so the LLM prompt has the expected metadata shape.
    meta_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "step0-extract", "input", "templates", "metadata.yaml")
    meta_scaffold = ""
    if os.path.isfile(meta_path):
        with open(meta_path) as f:
            meta_scaffold = f.read()

    return {
        "candidate_dirs": list(candidate_sources.keys()),
        "candidate_sources": candidate_sources,
        "metadata_scaffold": meta_scaffold,
    }


_MAP_KIND_EXTENSIONS = {
    "novelty": (),
    "gaps": (),
    "mathematics": (".tex", ".sty"),
    "figures": (".png", ".jpg", ".jpeg", ".svg", ".gif"),
    "tables": (),  # tables live inside .md tables, no dedicated extension
    "algorithms": (),
    "references": (".bib", ".biblatex"),
}

_MAP_KIND_DOC_KEYWORDS = {
    "novelty": ("novel", "original", "contribution", "innovation", "first"),
    "gaps": ("gap", "limitation", "open problem", "unaddressed", "challenge"),
    "mathematics": ("equation", "formula", "math", "mathematical"),
    "figures": ("figure", "fig", "visualization", "chart", "plot"),
    "tables": ("table", "results", "evaluation", "comparison"),
    "algorithms": ("algorithm", "pseudocode", "procedure", "method"),
    "references": ("references", "bibliography", "related work", "citations"),
}


def _gather_map_context(repo_root, map_kind):
    """Gather candidate source files for a map-kind proposal.
    Scans docs/paper/ for files matching the map kind's extensions or
    content keywords, so the LLM has real source material to propose
    entries from."""
    repo_root_str = str(repo_root)
    docs_paper = os.path.join(repo_root_str, "docs", "paper")
    candidates = []
    extensions = _MAP_KIND_EXTENSIONS.get(map_kind, ())
    keywords = _MAP_KIND_DOC_KEYWORDS.get(map_kind, ())

    if os.path.isdir(docs_paper):
        for root, dirs, files in os.walk(docs_paper):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(root, f), docs_paper)
                # Match by extension
                if extensions and any(f.lower().endswith(ext) for ext in extensions):
                    candidates.append(rel)
                # Match by keyword in filename
                elif keywords and any(kw in f.lower() for kw in keywords):
                    candidates.append(rel)

    # Read first 4KB of each candidate to give the LLM actual content
    file_snippets = []
    for cand in candidates[:20]:
        fpath = os.path.join(docs_paper, cand)
        try:
            with open(fpath, encoding="utf-8", errors="replace") as fh:
                content = fh.read(4000)
        except Exception:
            content = "[unreadable]"
        file_snippets.append({"path": cand, "content": content})

    return {
        "map_kind": map_kind,
        "candidate_files": candidates,
        "file_snippets": file_snippets,
    }


def _gather_section_context(conn, paper_id, scope_domain_id):
    """Gather domain-specific context for a section proposal.
    When scope_domain_id is set: single domain.
    When None: all 6 structural domains (batched propose-section mode)."""
    structural_domains = [
        "title-and-metadata", "introduction", "methodology",
        "findings", "conclusion", "references",
    ]

    domain_keys = []
    if scope_domain_id:
        row = conn.execute(
            "SELECT key FROM academic_domains WHERE id=?",
            (scope_domain_id,)).fetchone()
        if row:
            domain_keys = [row["key"]]
    else:
        domain_keys = structural_domains

    domain_list = []
    for dk in domain_keys:
        did = _get_domain_id(conn, dk)
        draft_text = _get_latest_narrative_text(conn, paper_id, did) if did else None

        map_entries = []
        if did:
            for table, kind, label_col in [
                ("academic_figure_map", "figure", "caption"),
                ("academic_table_map", "table", "caption"),
                ("academic_equation_map", "equation", "latex"),
                ("academic_algorithm_map", "algorithm", "name"),
            ]:
                rows = conn.execute(
                    f"SELECT map_key, target_section, {label_col} AS label "
                    f"FROM {table} WHERE paper_id=? AND target_section=?",
                    (paper_id, dk)).fetchall()
                for r in rows:
                    map_entries.append({
                        "map_key": r["map_key"],
                        "kind": kind,
                        "label": r["label"],
                    })
            # Citations query by domain_id (no target_section column)
            cite_rows = conn.execute(
                "SELECT citation FROM academic_section_citations "
                "WHERE paper_id=? AND domain_id=?",
                (paper_id, did)).fetchall()
            for r in cite_rows:
                map_entries.append({
                    "map_key": None,
                    "kind": "citation",
                    "label": r["citation"],
                })

        domain_list.append({
            "domain_key": dk,
            "existing_draft": draft_text or "",
            "map_entries": map_entries,
        })

    # Gather Step 0 cross-module analysis summaries — informs section
    # generation with source-code evidence (novelty, gaps, mathematics,
    # architecture, figures, tables).  section-map.yaml documents which
    # analysis kinds map to which target sections for further filtering.
    analysis_summaries = {}
    for kind in (
        "novelty", "gaps", "mathematics", "architecture",
        "dependencies", "interactions", "figures", "tables",
    ):
        row = conn.execute(
            "SELECT content FROM academic_cross_module_analysis "
            "WHERE paper_id=? AND analysis_kind=? "
            "ORDER BY created_at DESC LIMIT 1",
            (paper_id, kind),
        ).fetchone()
        analysis_summaries[kind] = row["content"] if row else ""

    return {
        "domains": domain_list,
        "domain_count": len(domain_list),
        "analysis_summaries": analysis_summaries,
    }


def _gather_module_registry(conn, paper_id):
    """Pull all modules for this paper with their full column data."""
    rows = conn.execute(
        "SELECT id, module_name, module_path, role, interest_weight, reason, "
        "existing_draft_publisher, existing_draft_status, existing_draft_path, sort_order "
        "FROM academic_modules WHERE paper_id=? ORDER BY sort_order",
        (paper_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        meta = _load_paper_meta(conn, payload["paper_id"])
        redraft = _redraft_context(conn, payload["paper_id"], phase,
                                    payload.get("scope_domain_id"))
        if redraft and redraft["iteration"] >= 5:
            write_envelope(out_path, status="error",
                           message="proposal rejected 5 times — escalate to human_review")
            return
        if phase == "input":
            context = _gather_input_context(repo_root)
        elif phase == "map":
            context = _gather_map_context(
                repo_root, payload.get("map_kind", ""))
        elif phase == "section":
            context = _gather_section_context(
                conn, payload["paper_id"], payload.get("scope_domain_id"))
        elif phase == "generation":
            context = _gather_generation_context(conn, payload["paper_id"])
        elif phase == "audit":
            context = _gather_audit_context(conn, payload["paper_id"],
                                             payload.get("models"))
        elif phase == "report":
            context = _gather_report_context(conn, payload["paper_id"])
        elif phase == "fix" and payload.get("step0_finding_id"):
            context = _gather_step0_fix_context(conn, payload["paper_id"],
                                                 payload["step0_finding_id"])
        elif phase == "fix":
            context = _gather_fix_context(conn, payload["paper_id"],
                                           payload.get("scope_domain_id"),
                                           payload.get("user_comment", ""))
        else:
            write_envelope(out_path, status="error",
                           message=f"unknown phase: {phase}")
            return
        context["paper_title"] = meta["title"] if meta else ""
        context["redraft_of"] = redraft
        context["iteration"] = (redraft["iteration"] + 1) if redraft else 0
        context["module_registry"] = _gather_module_registry(conn, payload["paper_id"])
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"gathered {phase} context",
                   **context)


if __name__ == "__main__":
    main()
