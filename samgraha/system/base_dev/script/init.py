"""init.py — Orchestration engine for the base_dev documentation pipeline.

Reads tiers.yaml and loop.yaml, determines use case (Path A vs Path B per domain),
and executes the tier-by-tier pipeline: scaffold→structural→content→validate→calculate→report→fix.

Usage:
  python init.py --system-root <path> --repo-root <path> --use-case <case> --out-dir <path>
  python init.py --system-root <path> --repo-root <path> --use-case <case> --out-dir <path> --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import re

from _common import load_yaml, load_json, read_text, write_json, write_text, compute_fingerprint, utc_now_iso, ALL_DOMAINS

# Import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from scaffold import (
    generate_document, load_upstream_context, extract_template_skeleton,
    extract_section_heading,
)
from validate import validate
from calculate import calculate_all
from report import render_report, render_trend_and_narrative
from evaluate_rules import evaluate_rules
from evaluate_semantic import evaluate_all_semantic, evaluate_semantic_document
from gather_semantic_context import build_supporting_evidence
from analyze import analyze_domain
from generate_traceability import generate_traceability_for_domain
from generate_structural_sections import (
    generate_constraints_section,
    generate_dependencies_section,
    generate_non_goals_section,
    generate_external_dependencies_section,
    generate_runtime_constraints_section,
    generate_architectural_constraints_section,
    generate_security_considerations_section,
    generate_performance_considerations_section,
    generate_extension_points_section,
    inject_section,
    DOMAIN_STRUCTURAL_SECTIONS,
)


# ---------------------------------------------------------------------------
# Pre/post script hooks (§13)
# ---------------------------------------------------------------------------

def run_pre_script(
    hook_name: str,
    system_root: Path,
    domain: str,
    domain_out: Path,
    doc_file: Path | None = None,
) -> bool:
    """Run a pre-script hook before a phase.

    Returns True if the phase should proceed, False to skip (e.g. doc unchanged).
    Currently implements staleness checking: if the doc file hasn't changed
    since the last audit, skip re-validation.
    """
    if hook_name == "check_section_changed" and doc_file:
        # Check if doc file has been modified since last validation
        validation_json = domain_out / f"{domain}-validation.json"
        if validation_json.exists():
            try:
                prev = json.loads(validation_json.read_text(encoding="utf-8"))
                prev_fingerprint = prev.get("repo_fingerprint", "")
                current_fingerprint = compute_fingerprint(doc_file.parent)
                if prev_fingerprint == current_fingerprint:
                    print(f"  Pre-hook: {domain} unchanged since last audit — skipping")
                    return False
            except (json.JSONDecodeError, KeyError):
                pass
    return True


def run_post_script(
    hook_name: str,
    system_root: Path,
    domain: str,
    domain_out: Path,
    doc_file: Path | None = None,
) -> None:
    """Run a post-script hook after a phase.

    Currently a structured extension point. When compile_hook.py is built
    (§14), this is where it would be called to ingest the doc into knowledge.db.
    """
    if hook_name == "compile" and doc_file:
        # Future: call compile_hook.py to ingest doc_file into knowledge.db
        # For now, record that compilation would happen here
        pass


# ---------------------------------------------------------------------------
# Score history persistence (§15)
# ---------------------------------------------------------------------------

def append_score_history(
    history_path: Path,
    domain: str,
    scores: dict[str, Any],
    git_revision: str = "",
) -> None:
    """Append a score entry to the append-only history store.

    Creates the history file if it doesn't exist. Each entry captures
    {domain, timestamp, final_score, band, git_revision} for cross-run
    trend analysis.
    """
    entry = {
        "domain": domain,
        "timestamp": utc_now_iso(),
        "final_score": scores.get("final_score", {}).get("score", 0),
        "band": scores.get("score_bands", {}).get("rating", "N/A"),
        "git_revision": git_revision,
        "model": scores.get("model", "heuristic-v1"),
        "deterministic_whole": scores.get("deterministic_whole", {}).get("score", 0),
        "deterministic_section": scores.get("deterministic_section", {}).get("score", 0),
        "semantic_whole": scores.get("semantic_whole", {}).get("score", 0),
        "semantic_section": scores.get("semantic_section", {}).get("score", 0),
    }

    history: list[dict] = []
    if history_path.exists():
        try:
            history = json.loads(history_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            history = []

    history.append(entry)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")


def load_score_history(history_path: Path) -> list[dict]:
    """Load the full score history for trend analysis."""
    if not history_path.exists():
        return []
    try:
        return json.loads(history_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return []


# ---------------------------------------------------------------------------
# Use case parsing
# ---------------------------------------------------------------------------

USE_CASE_MAP = {
    "repo_new/case_1_no_documentation": {
        "has_code": False,
        "has_docs": False,
        "description": "New repo, no code, no docs — only a product idea as input",
    },
    "repo_new/case_2_has_documentation": {
        "has_code": False,
        "has_docs": True,
        "description": "New repo, some pre-existing docs",
    },
    "repo_existing/case_1_no_documentation": {
        "has_code": True,
        "has_docs": False,
        "description": "Existing repo with code, no docs",
    },
    "repo_existing/case_2_has_documentation": {
        "has_code": True,
        "has_docs": True,
        "description": "Existing repo, existing docs",
    },
}


def detect_existing_docs(repo_root: Path, docs_root: Path | None, domains: list[str]) -> list[str]:
    """Detect which domains already have documentation files."""
    existing: list[str] = []

    search_root = docs_root or repo_root
    for domain in domains:
        # Check for any file starting with the domain prefix
        domain_prefix = domain.split("-", 1)[0] if "-" in domain else domain
        domain_name = domain.split("-", 1)[1] if "-" in domain else domain

        for md_file in search_root.glob(f"{domain_prefix}-{domain_name}*.md"):
            if md_file.is_file():
                existing.append(domain)
                break

        # Also check docs/ directory
        if not existing or existing[-1] != domain:
            docs_dir = repo_root / "docs"
            if docs_dir.is_dir():
                for md_file in docs_dir.glob(f"{domain_prefix}-{domain_name}*.md"):
                    if md_file.is_file():
                        existing.append(domain)
                        break

    return existing


# ---------------------------------------------------------------------------
# Pipeline phases
# ---------------------------------------------------------------------------

def phase_scaffold(
    system_root: Path,
    repo_root: Path,
    domain: str,
    out_dir: Path,
    context: dict[str, str] | None,
) -> Path:
    """Generate scaffold for a domain."""
    out_path = out_dir / f"{domain}.md"
    content = generate_document(system_root, domain, context)
    write_text(out_path, content)
    return out_path


def phase_validate(
    system_root: Path,
    repo_root: Path,
    docs_root: Path | None,
    domain: str,
    out_dir: Path,
) -> dict[str, Any]:
    """Run validation checks for a domain."""
    out_path = out_dir / f"{domain}-validation.json"
    result = validate(system_root, repo_root, docs_root, domain)
    write_json(out_path, result)
    return result


def phase_calculate(
    system_root: Path,
    domain: str,
    out_dir: Path,
    previous_report: Path | None = None,
    score_history: list[dict] | None = None,
) -> dict[str, Any]:
    """Calculate scores for a domain."""
    out_path = out_dir / f"{domain}-scores.json"
    result = calculate_all(system_root, domain)

    # Apply trend from score history (§15) — cross-run comparison
    if score_history:
        # Find the most recent entry for this domain
        domain_history = [h for h in score_history if h.get("domain") == domain]
        if domain_history:
            prev = domain_history[-1]
            from calculate import trend_comparison
            result["trend"] = trend_comparison(
                result["final_score"]["score"],
                prev.get("final_score", 0),
            )
    elif previous_report and previous_report.exists():
        # Fallback: single-file comparison (legacy)
        from calculate import load_previous_scores, trend_comparison
        prev_scores = load_previous_scores(previous_report)
        if "final_score" in prev_scores:
            result["trend"] = trend_comparison(
                result["final_score"]["score"],
                prev_scores["final_score"],
            )

    write_json(out_path, result)
    return result


def phase_report(
    system_root: Path,
    domain: str,
    scores: dict[str, Any],
    out_dir: Path,
    trend_json: Path | None = None,
    narrative_json: Path | None = None,
) -> Path:
    """Render reports for a domain."""
    reports: list[str] = []

    # Deterministic document report
    det_doc_report = render_report(system_root, domain, scores, "deterministic", "document")
    det_doc_path = out_dir / f"{domain}-det-doc-report.md"
    write_text(det_doc_path, det_doc_report)
    reports.append(str(det_doc_path))

    # Deterministic section report
    det_sec_report = render_report(system_root, domain, scores, "deterministic", "section")
    det_sec_path = out_dir / f"{domain}-det-sec-report.md"
    write_text(det_sec_path, det_sec_report)
    reports.append(str(det_sec_path))

    # Semantic document report
    sem_doc_report = render_report(system_root, domain, scores, "semantic", "document")
    sem_doc_path = out_dir / f"{domain}-sem-doc-report.md"
    write_text(sem_doc_path, sem_doc_report)
    reports.append(str(sem_doc_path))

    # Semantic section report
    sem_sec_report = render_report(system_root, domain, scores, "semantic", "section")
    sem_sec_path = out_dir / f"{domain}-sem-sec-report.md"
    write_text(sem_sec_path, sem_sec_report)
    reports.append(str(sem_sec_path))

    # Trend table + narrative (§6.5 + §9)
    trend = None
    if trend_json and trend_json.exists():
        trend = load_json(trend_json)
    narrative = None
    if narrative_json and narrative_json.exists():
        narrative = load_json(narrative_json)

    trend_narrative_md = render_trend_and_narrative(trend, narrative)
    if trend_narrative_md.strip():
        tn_path = out_dir / f"{domain}-trend-narrative.md"
        write_text(tn_path, trend_narrative_md)
        reports.append(str(tn_path))

    return det_doc_path  # Return primary report path


def phase_evaluate_rules(
    system_root: Path,
    domain: str,
    doc_file: Path,
    out_dir: Path,
) -> dict[str, Any]:
    """Evaluate deterministic rules against the document (§20)."""
    det_eval_path = out_dir / f"{domain}-det-eval.json"
    doc_content = doc_file.read_text(encoding="utf-8")
    result = evaluate_rules(system_root, domain, doc_content)
    write_json(det_eval_path, result)
    return result


def phase_evaluate_semantic(
    system_root: Path,
    domain: str,
    doc_file: Path,
    out_dir: Path,
    context_path: Path | None = None,
) -> dict[str, Any]:
    """Evaluate semantic criteria against the document (§20)."""
    sem_eval_path = out_dir / f"{domain}-sem-eval.json"
    doc_content = doc_file.read_text(encoding="utf-8")

    context = None
    if context_path and context_path.exists():
        from _common import load_json
        context = load_json(context_path)

    result = evaluate_all_semantic(system_root, domain, doc_content, context)
    write_json(sem_eval_path, result)
    return result


def phase_analyze(
    system_root: Path,
    domain: str,
    out_dir: Path,
    threshold: str = "Acceptable",
) -> dict[str, Any]:
    """Analyze scores and generate fix plan (§22)."""
    fix_plan_path = out_dir / f"{domain}-fix-plan.json"
    result = analyze_domain(system_root, domain, out_dir, threshold)
    write_json(fix_plan_path, result)
    return result


def phase_analyze_trend(
    system_root: Path,
    domain: str,
    out_dir: Path,
    score_history: list[dict] | None = None,
) -> dict[str, Any] | None:
    """Run multi-window trend analysis (§6.5). Produces {domain}-trend.json.

    Reads the existing score_history.json via load_score_history().
    Returns the trend dict, or None on error.
    """
    try:
        from analyze_trend import analyze_trend, load_history
    except ImportError:
        print(f"  Analyze trend: skipped (import error)")
        return None

    scores_path = out_dir / f"{domain}-scores.json"
    if not scores_path.exists():
        print(f"  Analyze trend: skipped (no scores file)")
        return None

    scores = json.loads(scores_path.read_text(encoding="utf-8"))

    # Use passed history or load from file
    if score_history is not None:
        history = [e for e in score_history if e.get("domain") == domain]
    else:
        history_path = out_dir.parent / "score_history.json"
        history = load_history(history_path, domain) if history_path.exists() else []

    result = analyze_trend(scores, history)
    trend_path = out_dir / f"{domain}-trend.json"
    write_json(trend_path, result)
    return result


def phase_visualize(
    system_root: Path,
    domain: str,
    out_dir: Path,
    history_path: Path | None = None,
    viz_plan: list[str] | None = None,
) -> None:
    """Generate visualization charts (§19)."""
    try:
        from visualize import generate_all_charts
        scores_path = out_dir / f"{domain}-scores.json"
        charts_out = out_dir / "charts"
        generate_all_charts(
            system_root, out_dir, charts_out, scores_path,
            viz_plan=viz_plan,
            history_path=history_path,
        )
    except ImportError:
        print(f"  Visualize: skipped (matplotlib not available)")
    except Exception as e:
        print(f"  Visualize: error — {e}")


def phase_report_html(
    system_root: Path,
    domain: str,
    out_dir: Path,
) -> Path | None:
    """Generate HTML report with embedded charts (§19)."""
    try:
        from report_html import generate_html_report
        charts_dir = out_dir / "charts"
        html_path = out_dir / f"{domain}-report.html"
        generate_html_report(system_root, out_dir, charts_dir, html_path, scores_json=None)
        return html_path
    except ImportError:
        print(f"  Report HTML: skipped (missing dependencies)")
        return None
    except Exception as e:
        print(f"  Report HTML: error — {e}")
        return None


def check_threshold(scores: dict[str, Any], threshold: str) -> bool:
    """Check if scores meet the threshold."""
    final_score = scores.get("final_score", {}).get("score", 0)
    rating = scores.get("score_bands", {}).get("rating", "Needs Improvement")

    # Threshold mapping
    threshold_scores = {
        "Excellent": 95,
        "Very Good": 90,
        "Good": 80,
        "Acceptable": 70,
        "Needs Improvement": 0,
    }

    min_score = threshold_scores.get(threshold, 70)
    return final_score >= min_score


# ---------------------------------------------------------------------------
# Tier execution
# ---------------------------------------------------------------------------

def execute_tier(
    system_root: Path,
    repo_root: Path,
    docs_root: Path | None,
    tier_num: int,
    tier_domains: list[str],
    loop_config: dict[str, Any],
    completed_domains: list[str],
    out_dir: Path,
    existing_docs: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, dict[str, Any]]:
    """Execute a single tier's pipeline for all its domains.

    Returns a dict mapping domain name to its final scores.
    """
    if existing_docs is None:
        existing_docs = []
    threshold = loop_config.get("threshold", {}).get("rating", "Acceptable")
    max_iterations = loop_config.get("max_iterations", 5)
    ordering = loop_config.get("within_tier_ordering", [])
    score_history_path = out_dir / "score_history.json"

    # Determine domain execution order within tier
    ordered_domains = _resolve_within_tier_order(tier_domains, tier_num, ordering)

    domain_results: dict[str, dict[str, Any]] = {}
    tier_out = out_dir / f"tier_{tier_num}"
    tier_out.mkdir(parents=True, exist_ok=True)

    for domain in ordered_domains:
        domain_out = tier_out / domain
        domain_out.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Tier {tier_num} — Domain: {domain}")
        print(f"{'='*60}")

        # Load upstream context
        context = None
        if completed_domains:
            context_dir = out_dir.parent  # Parent of all tier outputs
            context = load_upstream_context(context_dir, completed_domains)

        # Phase 1: Scaffold (Path A only — if no existing docs)
        doc_file = None
        if domain not in existing_docs:
            if not dry_run:
                doc_file = phase_scaffold(system_root, repo_root, domain, domain_out, context)
                print(f"  Scaffold: {doc_file}")
            else:
                print(f"  Scaffold: [dry-run] would generate {domain}.md")

        # Phase 2: Structural generation — inject traceability + constraint skeletons
        if not dry_run and doc_file:
            from generate_traceability import load_tiers as load_tiers_trace, load_relationships as load_rel_trace
            from generate_structural_sections import load_tiers as load_tiers_struct, load_relationships as load_rel_struct

            # Inject traceability sections
            trace_tiers = load_tiers_trace(system_root)
            trace_rels = load_rel_trace(system_root, domain)
            trace_content = generate_traceability_for_domain(domain, trace_tiers, trace_rels)
            doc_content = read_text(doc_file)
            updated = inject_section(doc_content, "traceability", trace_content)
            write_text(doc_file, updated)
            print(f"  Structural: injected traceability")

            # Inject constraint/dependency/non-goal skeletons
            struct_tiers = load_tiers_struct(system_root)
            struct_rels = load_rel_struct(system_root, domain)
            struct_sections = DOMAIN_STRUCTURAL_SECTIONS.get(domain, [])
            for section_name in struct_sections:
                generator_map = {
                    "constraints": generate_constraints_section,
                    "dependencies": generate_dependencies_section,
                    "non_goals": generate_non_goals_section,
                    "external-dependencies": generate_external_dependencies_section,
                    "runtime-constraints": generate_runtime_constraints_section,
                    "architectural-constraints": generate_architectural_constraints_section,
                    "security-considerations": generate_security_considerations_section,
                    "performance-considerations": generate_performance_considerations_section,
                    "extension-points": generate_extension_points_section,
                }
                gen_fn = generator_map.get(section_name)
                if gen_fn:
                    content = gen_fn(domain, struct_rels, struct_tiers)
                    doc_content = read_text(doc_file)
                    updated = inject_section(doc_content, section_name, content)
                    write_text(doc_file, updated)
            if struct_sections:
                print(f"  Structural: injected {len(struct_sections)} constraint/dependency skeletons")

        # Phase 3: Content fill — replace TODO placeholders with upstream-derived content
        if not dry_run and doc_file:
            filled_content = content_fill(system_root, domain, read_text(doc_file), context)
            write_text(doc_file, filled_content)
            run_post_script("compile", system_root, domain, domain_out, doc_file)
            print(f"  Content: filled TODO placeholders from upstream context")

        # Phase 4: Evaluate deterministic rules (§20)
        det_eval = None
        if not dry_run and doc_file:
            det_eval = phase_evaluate_rules(system_root, domain, doc_file, domain_out)
            doc_passed = sum(1 for r in det_eval.get("doc_rules", []) if r.get("passed"))
            doc_total = len(det_eval.get("doc_rules", []))
            sec_passed = sum(
                sum(1 for r in rules if r.get("passed"))
                for rules in det_eval.get("sec_rules", {}).values()
            )
            sec_total = sum(len(rules) for rules in det_eval.get("sec_rules", {}).values())
            print(f"  Evaluate rules: doc {doc_passed}/{doc_total}, sec {sec_passed}/{sec_total}")

        # Phase 5: Gather semantic context (§21) + Evaluate semantic (§20)
        sem_eval = None
        if not dry_run and doc_file:
            # Gather supporting evidence for semantic audit
            evidence_path = domain_out / f"{domain}-semantic-context.json"
            evidence = build_supporting_evidence(system_root, domain, domain_out)
            write_json(evidence_path, evidence)
            print(f"  Semantic context: {evidence['summary'][:80]}")

            # Evaluate semantic criteria
            sem_eval = phase_evaluate_semantic(
                system_root, domain, doc_file, domain_out, evidence_path,
            )
            doc_crit = sem_eval.get("document", {}).get("criteria", [])
            doc_crit_passed = sum(1 for c in doc_crit if c.get("passed"))
            print(f"  Evaluate semantic: doc {doc_crit_passed}/{len(doc_crit)} criteria")

        # Phase 6: Validate (check scripts)
        validation = None
        if not dry_run:
            should_validate = run_pre_script(
                "check_section_changed", system_root, domain, domain_out, doc_file,
            )
            if should_validate:
                validation = phase_validate(system_root, repo_root, docs_root, domain, domain_out)
                print(f"  Validate: {validation['summary']['passed']} passed, "
                      f"{validation['summary']['failed']} failed")
            else:
                print(f"  Validate: skipped (unchanged since last audit)")

        # Phase 6: Calculate (reads evaluated results via out_dir)
        scores = None
        if not dry_run:
            previous_report = domain_out / f"{domain}-det-doc-report.md"
            history = load_score_history(score_history_path)
            scores = phase_calculate(system_root, domain, domain_out, previous_report, history)
            print(f"  Calculate: score={scores['final_score']['score']}, "
                  f"rating={scores['score_bands']['rating']}")

            # Persist score to history (§15)
            git_rev = compute_fingerprint(out_dir)
            append_score_history(score_history_path, domain, scores, git_rev)

        # Phase 6.5: Trend analysis (§6.5)
        trend = None
        if not dry_run and scores:
            history = load_score_history(score_history_path)
            trend = phase_analyze_trend(system_root, domain, domain_out, history)
            if trend:
                print(f"  Trend: {trend['vs_last_run']['direction']}, "
                      f"vs_last_run={trend['vs_last_run']['delta']:+.1f}")

        # Phase 7: Report
        if not dry_run and scores:
            trend_path = domain_out / f"{domain}-trend.json"
            narrative_path = domain_out / f"{domain}-narrative.json"
            report_path = phase_report(
                system_root, domain, scores, domain_out,
                trend_json=trend_path if trend_path.exists() else None,
                narrative_json=narrative_path if narrative_path.exists() else None,
            )
            print(f"  Report: {report_path}")

        # Phase 8: Analyze — generate fix plan (§22)
        fix_plan = None
        if not dry_run and scores:
            fix_plan = phase_analyze(system_root, domain, domain_out, threshold)
            print(f"  Analyze: {fix_plan['status']} — {fix_plan.get('fix_scope', 'N/A')}")

        # Phase 9: Fix loop (only if below threshold)
        if not dry_run and scores:
            iteration = 0
            while (not check_threshold(scores, threshold) and
                   iteration < max_iterations):
                iteration += 1
                print(f"  Fix iteration {iteration}/{max_iterations} — "
                      f"score {scores['final_score']['score']} < threshold")

                # Re-run content fill with accumulated context from all completed domains
                if doc_file:
                    expanded_context = dict(context) if context else {}
                    for cd in completed_domains:
                        for md in out_dir.rglob(f"{cd}*.md"):
                            if md.is_file() and cd not in expanded_context:
                                expanded_context[cd] = md.read_text(encoding="utf-8")
                    filled = content_fill(system_root, domain, read_text(doc_file), expanded_context)
                    write_text(doc_file, filled)
                    run_post_script("compile", system_root, domain, domain_out, doc_file)
                    print(f"  Fix: re-filled content with expanded context")

                # Re-evaluate after fix
                if doc_file:
                    det_eval = phase_evaluate_rules(system_root, domain, doc_file, domain_out)
                    evidence_path = domain_out / f"{domain}-semantic-context.json"
                    evidence = build_supporting_evidence(system_root, domain, domain_out)
                    write_json(evidence_path, evidence)
                    sem_eval = phase_evaluate_semantic(
                        system_root, domain, doc_file, domain_out, evidence_path,
                    )

                # Re-validate after fix
                validation = phase_validate(system_root, repo_root, docs_root, domain, domain_out)
                history = load_score_history(score_history_path)
                scores = phase_calculate(system_root, domain, domain_out, score_history=history)
                report_path = phase_report(system_root, domain, scores, domain_out)
                fix_plan = phase_analyze(system_root, domain, domain_out, threshold)
                print(f"  Re-scored: {scores['final_score']['score']}")

            if iteration >= max_iterations:
                print(f"  WARNING: Max iterations reached for {domain} — "
                      f"flagging for human review")

        # Phase 10: Visualize (§19)
        if not dry_run:
            phase_visualize(system_root, domain, domain_out, history_path=score_history_path)

        # Phase 11: HTML Report (§19)
        if not dry_run:
            html_path = phase_report_html(system_root, domain, domain_out)
            if html_path:
                print(f"  HTML report: {html_path}")

        # Store results
        if not dry_run and scores:
            domain_results[domain] = scores
            completed_domains.append(domain)
        else:
            domain_results[domain] = {"final_score": {"score": 0}, "score_bands": {"rating": "N/A"}}

    return domain_results


def _resolve_within_tier_order(
    domains: list[str],
    tier_num: int,
    ordering: list[dict],
) -> list[str]:
    """Resolve domain execution order within a tier based on ordering constraints."""
    for item in ordering:
        if item.get("tier") == tier_num:
            from_domain = item.get("from")
            to_domain = item.get("to")
            if from_domain in domains and to_domain in domains:
                # Ensure from comes before to
                result = []
                for d in domains:
                    if d == to_domain:
                        if from_domain not in result:
                            result.append(from_domain)
                        result.append(d)
                    elif d != from_domain:
                        result.append(d)
                return result

    return domains


def content_fill(
    system_root: Path,
    domain: str,
    doc_content: str,
    context: dict[str, str] | None,
) -> str:
    """Fill scaffolded TODO placeholders with content derived from upstream context.

    Reads the scaffolded document, finds <!-- TODO: Fill in ... --> markers,
    and replaces them with relevant excerpts from upstream domain documents.
    Falls back to a generic placeholder note when no relevant context exists.
    """
    if not context:
        return doc_content

    # Build a flat corpus of upstream content for relevance matching
    corpus: list[tuple[str, str]] = []  # (domain_name, paragraph)
    for ctx_domain, ctx_content in context.items():
        for para in _extract_paragraphs(ctx_content):
            if len(para) > 20:
                corpus.append((ctx_domain, para))

    def _replace_todo(match: re.Match) -> str:
        placeholder_desc = match.group(1).strip()
        # Extract the section name from the placeholder (e.g. "01-vision/01-purpose")
        parts = placeholder_desc.split("/")
        section_key = parts[-1].replace("-", " ").lower() if parts else ""

        # Find most relevant paragraphs by keyword overlap
        keywords = set(section_key.split())
        scored: list[tuple[int, str, str]] = []
        for ctx_domain, para in corpus:
            para_lower = para.lower()
            score = sum(1 for kw in keywords if kw in para_lower)
            if score > 0:
                scored.append((score, ctx_domain, para))

        scored.sort(key=lambda x: x[0], reverse=True)

        if scored:
            # Take top 2 most relevant paragraphs
            lines = []
            for _, src_domain, para in scored[:2]:
                lines.append(f"> **Source ({src_domain}):** {para[:300]}")
            return "\n".join(lines)
        else:
            return f"<!-- TODO: {placeholder_desc} — no relevant upstream context found -->"

    return re.sub(r"<!-- TODO: (.+?) -->", _replace_todo, doc_content)


def _extract_paragraphs(content: str) -> list[str]:
    """Extract non-heading, non-empty paragraphs from markdown."""
    paragraphs: list[str] = []
    current: list[str] = []

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if stripped.startswith("#"):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if stripped.startswith(">") or stripped.startswith("---") or stripped.startswith("<!--"):
            continue
        current.append(stripped)

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs


def _get_existing_docs() -> list[str]:
    """Stub — replaced by wired existing_docs parameter in execute_tier."""
    return []


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    system_root: Path,
    repo_root: Path,
    use_case: str,
    out_dir: Path,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Execute the full documentation pipeline for a use case."""
    if use_case not in USE_CASE_MAP:
        raise ValueError(f"Unknown use case: {use_case}. "
                        f"Valid: {list(USE_CASE_MAP.keys())}")

    case_info = USE_CASE_MAP[use_case]
    system = load_yaml(system_root / "system.yaml")
    tiers = load_yaml(system_root / "plan" / "core" / "tiers.yaml")
    loop = load_yaml(system_root / "plan" / "core" / "loop.yaml")

    # Resolve active domains
    domains = system.get("domains", ALL_DOMAINS)
    drops = system.get("drops", [])
    active_domains = [d for d in domains if d not in drops]

    # tiers.yaml uses short names (e.g. "vision"), system.yaml uses full (e.g. "01-vision")
    active_short_names = {d.split("-", 1)[1] if "-" in d else d for d in active_domains}
    drops_short_names = {d.split("-", 1)[1] if "-" in d else d for d in drops}

    # Detect existing docs for Path B
    existing_docs = []
    if case_info["has_docs"]:
        existing_docs = detect_existing_docs(repo_root, None, active_domains)

    # Prepare output directory
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate plan
    from plan_generation import generate_plan
    plan_content = generate_plan(system_root, use_case, existing_docs)
    write_text(out_dir / "PLAN.md", plan_content)

    print(f"Pipeline: {use_case}")
    print(f"Description: {case_info['description']}")
    print(f"Active domains: {len(active_domains)}")
    print(f"Existing docs (Path B): {len(existing_docs)}")
    print(f"Output: {out_dir}")
    print()

    # Execute tiers
    completed_domains: list[str] = []
    all_results: dict[str, Any] = {
        "use_case": use_case,
        "started_at": utc_now_iso(),
        "tiers": {},
    }

    for tier_info in tiers.get("tiers", []):
        tier_num = tier_info["tier"]
        tier_domains = [d for d in tier_info["domains"]
                       if d in active_short_names and d not in drops_short_names]

        if not tier_domains:
            continue

        tier_results = execute_tier(
            system_root, repo_root, None,
            tier_num, tier_domains, loop,
            completed_domains, out_dir, existing_docs, dry_run,
        )

        all_results["tiers"][f"tier_{tier_num}"] = {
            "domains": tier_domains,
            "results": {
                d: {
                    "score": r.get("final_score", {}).get("score", 0),
                    "rating": r.get("score_bands", {}).get("rating", "N/A"),
                }
                for d, r in tier_results.items()
            },
        }

        # Tier gate check
        if not dry_run:
            threshold = loop.get("threshold", {}).get("rating", "Acceptable")
            all_pass = all(
                check_threshold(tier_results[d], threshold)
                for d in tier_domains
                if d in tier_results
            )
            if not all_pass:
                print(f"\n!!! TIER {tier_num} GATE: NOT ALL DOMAINS PASS — "
                      f"blocking next tier")
                break

    all_results["completed_at"] = utc_now_iso()

    # Write summary
    write_json(out_dir / "results.json", all_results)

    print(f"\n{'='*60}")
    print(f"Pipeline complete: {len(completed_domains)} domains processed")
    print(f"Results: {out_dir / 'results.json'}")
    print(f"Plan: {out_dir / 'PLAN.md'}")

    return all_results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute the documentation pipeline for a use case"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--repo-root", required=True, help="Repository root")
    parser.add_argument("--use-case", required=True,
                        help="Use case (e.g. repo_new/case_1_no_documentation)")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan without executing")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    repo_root = Path(args.repo_root)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)
    if not repo_root.is_dir():
        print(f"Error: repo-root not found: {repo_root}", file=sys.stderr)
        sys.exit(1)

    run_pipeline(
        system_root, repo_root, args.use_case,
        Path(args.out_dir), args.dry_run,
    )


if __name__ == "__main__":
    main()
