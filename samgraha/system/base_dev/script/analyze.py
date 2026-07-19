"""analyze.py — Analysis & fix-plan generator (§22).

Reads calculate.py's scores, validate.py's findings, and evaluation results.
Produces a structured fix plan: which domains/sections are failing, why,
and whether the fix should be section-level or whole-document.

Inserted between report and visualize in the pipeline. The fix plan is
saved to {domain}-fix-plan.json and can be reviewed/edited before the
fix phase executes.

Usage:
  python analyze.py --system-root <path> --domain <domain> --out-dir <path> --out <path>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_json, utc_now_iso


# ---------------------------------------------------------------------------
# Score analysis
# ---------------------------------------------------------------------------

def analyze_scores(
    scores: dict[str, Any],
    threshold: str,
) -> dict[str, Any]:
    """Analyze scores and determine pass/fail status."""
    final_score = scores.get("final_score", {}).get("score", 0)

    threshold_scores = {
        "Excellent": 95,
        "Very Good": 90,
        "Good": 80,
        "Acceptable": 70,
        "Needs Improvement": 0,
    }
    min_score = threshold_scores.get(threshold, 70)
    passes = final_score >= min_score

    # Analyze each bucket
    buckets = {}
    det_doc = scores.get("deterministic_document", {})
    det_sec = scores.get("deterministic_section", {})
    sem_doc = scores.get("semantic_document", {})
    sem_sec = scores.get("semantic_section", {})

    if det_doc:
        buckets["deterministic_document"] = {
            "score": det_doc.get("score", 0),
            "passed_rules": det_doc.get("rules_passed", 0),
            "failed_rules": det_doc.get("rules_failed", 0),
            "total_rules": det_doc.get("rules_total", 0),
        }
    if det_sec:
        sections = det_sec.get("sections", [])
        failing_sections = [s for s in sections if s.get("score", 0) < 70]
        buckets["deterministic_section"] = {
            "score": det_sec.get("rollup", 0),
            "total_sections": len(sections),
            "failing_sections": len(failing_sections),
            "weakest_section": min(sections, key=lambda s: s.get("score", 100)) if sections else None,
        }
    if sem_doc:
        buckets["semantic_document"] = {
            "score": sem_doc.get("score", 0),
            "passed_criteria": sem_doc.get("criteria_passed", 0),
            "total_criteria": sem_doc.get("criteria_total", 0),
        }
    if sem_sec:
        sections = sem_sec.get("sections", [])
        failing_sections = [s for s in sections if s.get("score", 0) < 70]
        buckets["semantic_section"] = {
            "score": sem_sec.get("rollup", 0),
            "total_sections": len(sections),
            "failing_sections": len(failing_sections),
            "weakest_section": min(sections, key=lambda s: s.get("score", 100)) if sections else None,
        }

    return {
        "passes_threshold": passes,
        "final_score": final_score,
        "threshold": threshold,
        "min_score": min_score,
        "buckets": buckets,
    }


# ---------------------------------------------------------------------------
# Finding analysis
# ---------------------------------------------------------------------------

def analyze_findings(
    validation: dict[str, Any],
    det_eval: dict[str, Any] | None,
    sem_eval: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Extract and prioritize findings from validation and evaluation results."""
    findings: list[dict[str, Any]] = []

    # From validation (check-backed findings)
    for f in validation.get("findings", []):
        if f.get("status") in ("fail", "error"):
            findings.append({
                "source": "check",
                "id": f.get("check", "unknown"),
                "severity": "error" if f.get("status") == "error" else "warning",
                "domain": f.get("domain", "unknown"),
                "message": "; ".join(f.get("evidence", ["Check failed"])[:1]),
                "metrics": f.get("metrics", {}),
            })

    # From deterministic evaluation
    if det_eval:
        for rule in det_eval.get("doc_rules", []):
            if not rule.get("passed", True):
                findings.append({
                    "source": "deterministic_rule",
                    "id": rule.get("id", "unknown"),
                    "severity": rule.get("severity", "warning"),
                    "scope": "document",
                    "message": rule.get("evidence", {}).get("message", "Rule failed"),
                })

        for section_name, rules in det_eval.get("sec_rules", {}).items():
            for rule in rules:
                if not rule.get("passed", True):
                    findings.append({
                        "source": "deterministic_rule",
                        "id": rule.get("id", "unknown"),
                        "severity": rule.get("severity", "warning"),
                        "scope": "section",
                        "section": section_name,
                        "message": rule.get("evidence", {}).get("message", "Rule failed"),
                    })

    # From semantic evaluation
    if sem_eval:
        doc_criteria = sem_eval.get("document", {}).get("criteria", [])
        for c in doc_criteria:
            if not c.get("passed", True):
                findings.append({
                    "source": "semantic_criterion",
                    "id": c.get("criterion_id", "unknown"),
                    "severity": "error" if c.get("mandatory") else "warning",
                    "scope": "document",
                    "message": c.get("evidence", {}).get("message", "Criterion not met"),
                    "score_loss": c.get("max_score", 0),
                })

        for sec_name, sec_data in sem_eval.get("sections", {}).items():
            for c in sec_data.get("criteria", []):
                if not c.get("passed", True):
                    findings.append({
                        "source": "semantic_criterion",
                        "id": c.get("criterion_id", "unknown"),
                        "severity": "error" if c.get("mandatory") else "warning",
                        "scope": "section",
                        "section": sec_name,
                        "message": c.get("evidence", {}).get("message", "Criterion not met"),
                        "score_loss": c.get("max_score", 0),
                    })

    # Sort by severity (errors first) then by score_loss (biggest losses first)
    severity_order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (
        severity_order.get(f.get("severity", "info"), 3),
        -f.get("score_loss", 0),
    ))

    return findings


# ---------------------------------------------------------------------------
# Fix plan generation
# ---------------------------------------------------------------------------

def generate_fix_plan(
    domain: str,
    score_analysis: dict[str, Any],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate a structured fix plan from analysis results.

    Determines fix scope (section-level vs whole-document) and
    prioritizes fixes by impact.
    """
    if score_analysis["passes_threshold"]:
        return {
            "domain": domain,
            "status": "no_fix_needed",
            "final_score": score_analysis["final_score"],
            "threshold": score_analysis["threshold"],
            "fixes": [],
            "generated_at": utc_now_iso(),
        }

    # Determine fix scope
    fixes: list[dict[str, Any]] = []

    # Group findings by section
    section_findings: dict[str, list[dict]] = {}
    doc_findings: list[dict] = []

    for f in findings:
        scope = f.get("scope", "document")
        if scope == "section":
            section = f.get("section", "unknown")
            if section not in section_findings:
                section_findings[section] = []
            section_findings[section].append(f)
        else:
            doc_findings.append(f)

    # Determine if section-level or whole-document fix is needed
    # Section-level: fix only the failing sections
    # Whole-document: too many section failures, easier to regenerate
    failing_section_count = len(section_findings)
    total_section_findings = sum(len(fs) for fs in section_findings.values())

    if failing_section_count > 5 or total_section_findings > 15:
        fix_scope = "whole_document"
        reason = (f"{failing_section_count} sections failing, "
                  f"{total_section_findings} total section-level findings — "
                  f"whole-document regeneration recommended")
    elif failing_section_count > 0:
        fix_scope = "section_level"
        reason = (f"{failing_section_count} sections failing — "
                  f"targeted section fixes")
    else:
        fix_scope = "document_level"
        reason = "Document-level issues only"

    # Build fix entries
    # Priority 1: Mandatory errors
    for f in findings:
        if f.get("severity") == "error":
            fixes.append({
                "priority": 1,
                "type": "error",
                "source": f.get("source", "unknown"),
                "id": f.get("id", "unknown"),
                "scope": f.get("scope", "document"),
                "section": f.get("section"),
                "message": f.get("message", ""),
                "estimated_impact": f.get("score_loss", "unknown"),
            })

    # Priority 2: Warnings with score impact
    for f in findings:
        if f.get("severity") == "warning" and f.get("score_loss", 0) > 0:
            fixes.append({
                "priority": 2,
                "type": "warning",
                "source": f.get("source", "unknown"),
                "id": f.get("id", "unknown"),
                "scope": f.get("scope", "document"),
                "section": f.get("section"),
                "message": f.get("message", ""),
                "estimated_impact": f.get("score_loss", 0),
            })

    # Priority 3: Other warnings
    for f in findings:
        if f.get("severity") == "warning" and f.get("score_loss", 0) == 0:
            fixes.append({
                "priority": 3,
                "type": "warning",
                "source": f.get("source", "unknown"),
                "id": f.get("id", "unknown"),
                "scope": f.get("scope", "document"),
                "section": f.get("section"),
                "message": f.get("message", ""),
                "estimated_impact": "low",
            })

    return {
        "domain": domain,
        "status": "fix_needed",
        "final_score": score_analysis["final_score"],
        "threshold": score_analysis["threshold"],
        "fix_scope": fix_scope,
        "fix_scope_reason": reason,
        "total_fixes": len(fixes),
        "error_count": sum(1 for f in fixes if f["type"] == "error"),
        "warning_count": sum(1 for f in fixes if f["type"] == "warning"),
        "failing_sections": list(section_findings.keys()),
        "fixes": fixes,
        "bucket_analysis": score_analysis["buckets"],
        "generated_at": utc_now_iso(),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze_domain(
    system_root: Path,
    domain: str,
    out_dir: Path,
    threshold: str = "Acceptable",
) -> dict[str, Any]:
    """Run full analysis for a domain and produce a fix plan."""
    # Load scores
    scores_path = out_dir / f"{domain}-scores.json"
    scores: dict[str, Any] = {}
    if scores_path.exists():
        from _common import load_json
        scores = load_json(scores_path)

    # Load validation results
    validation_path = out_dir / f"{domain}-validation.json"
    validation: dict[str, Any] = {"findings": []}
    if validation_path.exists():
        from _common import load_json
        validation = load_json(validation_path)

    # Load deterministic evaluation results
    det_eval_path = out_dir / f"{domain}-det-eval.json"
    det_eval: dict[str, Any] | None = None
    if det_eval_path.exists():
        from _common import load_json
        det_eval = load_json(det_eval_path)

    # Load semantic evaluation results
    sem_eval_path = out_dir / f"{domain}-sem-eval.json"
    sem_eval: dict[str, Any] | None = None
    if sem_eval_path.exists():
        from _common import load_json
        sem_eval = load_json(sem_eval_path)

    # Analyze
    score_analysis = analyze_scores(scores, threshold)
    findings = analyze_findings(validation, det_eval, sem_eval)
    fix_plan = generate_fix_plan(domain, score_analysis, findings)

    return fix_plan


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze scores and generate fix plan (§22)"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--out-dir", required=True, help="Directory with scores/validation/eval results")
    parser.add_argument("--out", required=True, help="Output JSON path (fix plan)")
    parser.add_argument("--threshold", default="Acceptable", help="Minimum threshold rating")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    out_dir = Path(args.out_dir)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    fix_plan = analyze_domain(system_root, args.domain, out_dir, args.threshold)
    write_json(Path(args.out), fix_plan)

    # Print summary
    status = fix_plan["status"]
    if status == "no_fix_needed":
        print(f"{args.domain}: PASS — score {fix_plan['final_score']} >= threshold")
    else:
        print(f"{args.domain}: FIX NEEDED — score {fix_plan['final_score']} < threshold")
        print(f"  Scope: {fix_plan['fix_scope']} — {fix_plan['fix_scope_reason']}")
        print(f"  Fixes: {fix_plan['total_fixes']} "
              f"({fix_plan['error_count']} errors, {fix_plan['warning_count']} warnings)")
        if fix_plan.get("failing_sections"):
            print(f"  Failing sections: {', '.join(fix_plan['failing_sections'])}")


if __name__ == "__main__":
    main()
