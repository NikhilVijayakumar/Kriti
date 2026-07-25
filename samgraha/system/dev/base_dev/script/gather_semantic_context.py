"""gather_semantic_context.py — Pre-script for semantic audit phases (§21).

Reads validate.py's check results and deterministic rule evaluation results
for a domain, extracts relevant metrics, and formats them as a "Supporting
Evidence" block. This grounds the semantic audit judgment in actual measured
data rather than relying solely on prose descriptions.

Usage:
  python gather_semantic_context.py --system-root <path> --domain <domain> --out-dir <path> --out <path>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_json, utc_now_iso


# ---------------------------------------------------------------------------
# Check → domain mapping (from mapping.yaml)
# ---------------------------------------------------------------------------

def load_check_mappings(system_root: Path) -> dict[str, list[dict]]:
    """Load mapping.yaml and build {domain -> [check entries]} index."""
    mapping_path = system_root / "script" / "mapping.yaml"
    if not mapping_path.exists():
        return {}

    mapping = load_yaml(mapping_path)
    domain_checks: dict[str, list[dict]] = {}

    for entry in mapping.get("mappings", []):
        check_name = entry["check"]
        check_domain = entry["domain"]
        category = entry.get("category", "A")
        consumed_by = entry.get("consumed_by", [])

        # Map to domains that consume this check
        for consumer in consumed_by:
            target_domain = consumer.get("domain", "")
            if target_domain not in domain_checks:
                domain_checks[target_domain] = []
            domain_checks[target_domain].append({
                "check": check_name,
                "source_domain": check_domain,
                "category": category,
                "audit_type": consumer.get("audit_type", "deterministic"),
                "rule_id": consumer.get("rule_id", consumer.get("criterion_id", "")),
            })

    return domain_checks


# ---------------------------------------------------------------------------
# Context extraction
# ---------------------------------------------------------------------------

def extract_check_metrics(
    validation_results: dict[str, Any],
    check_name: str,
) -> dict[str, Any] | None:
    """Extract metrics from a specific check's validation results."""
    for finding in validation_results.get("findings", []):
        if finding.get("check") == check_name:
            return {
                "status": finding.get("status", "unknown"),
                "metrics": finding.get("metrics", {}),
                "evidence": finding.get("evidence", []),
            }
    return None


def extract_rule_eval_metrics(
    eval_results: dict[str, Any],
    rule_id: str,
) -> dict[str, Any] | None:
    """Extract evaluation metrics for a specific rule."""
    # Check document-level rules
    for rule in eval_results.get("doc_rules", []):
        if rule.get("id") == rule_id:
            return {
                "passed": rule.get("passed", False),
                "evidence": rule.get("evidence", {}),
            }

    # Check section-level rules
    for section_name, rules in eval_results.get("sec_rules", {}).items():
        for rule in rules:
            if rule.get("id") == rule_id:
                return {
                    "passed": rule.get("passed", False),
                    "section": section_name,
                    "evidence": rule.get("evidence", {}),
                }

    return None


def build_supporting_evidence(
    system_root: Path,
    domain: str,
    out_dir: Path,
) -> dict[str, Any]:
    """Build a Supporting Evidence block for the semantic audit.

    Gathers metrics from:
    1. validate.py's check results (script-backed checks)
    2. evaluate_rules.py's deterministic rule evaluation results
    3. score_history.json for trend data
    """
    evidence_blocks: list[dict] = []

    # 1. Load check → domain mappings
    domain_checks = load_check_mappings(system_root)
    checks_for_domain = domain_checks.get(domain, [])

    # 2. Load validation results if available
    validation_path = out_dir / f"{domain}-validation.json"
    validation_results: dict[str, Any] = {}
    if validation_path.exists():
        from _common import load_json
        validation_results = load_json(validation_path)

    # 3. Load deterministic evaluation results if available
    det_eval_path = out_dir / f"{domain}-det-eval.json"
    det_eval_results: dict[str, Any] = {}
    if det_eval_path.exists():
        from _common import load_json
        det_eval_results = load_json(det_eval_path)

    # 4. Gather evidence for each relevant check
    for check_entry in checks_for_domain:
        check_name = check_entry["check"]
        rule_id = check_entry["rule_id"]
        audit_type = check_entry["audit_type"]

        # Extract from validation results (check metrics)
        check_metrics = extract_check_metrics(validation_results, check_name)
        if check_metrics:
            block: dict[str, Any] = {
                "source": "deterministic_check",
                "check": check_name,
                "status": check_metrics["status"],
                "metrics": check_metrics["metrics"],
            }
            if check_metrics.get("evidence"):
                block["evidence_summary"] = "; ".join(
                    str(e)[:200] for e in check_metrics["evidence"][:3]
                )
            evidence_blocks.append(block)

        # Extract from rule evaluation (for deterministic rules)
        if audit_type == "deterministic" and det_eval_results:
            rule_metrics = extract_rule_eval_metrics(det_eval_results, rule_id)
            if rule_metrics:
                evidence_blocks.append({
                    "source": "deterministic_rule",
                    "rule_id": rule_id,
                    "passed": rule_metrics["passed"],
                    "evidence": rule_metrics.get("evidence", {}),
                })

    # 5. Load score history for trend context
    history_path = out_dir / "score_history.json"
    if history_path.exists():
        from _common import load_json
        history = load_json(history_path)
        domain_history = [h for h in history if h.get("domain") == domain]
        if domain_history:
            latest = domain_history[-1]
            evidence_blocks.append({
                "source": "score_history",
                "previous_score": latest.get("final_score", 0),
                "previous_band": latest.get("band", "N/A"),
                "trend": latest.get("trend_direction", "baseline"),
            })

    # 6. Build the context block
    context = {
        "domain": domain,
        "gathered_at": utc_now_iso(),
        "supporting_evidence": evidence_blocks,
        "total_checks": len(checks_for_domain),
        "checks_with_results": sum(
            1 for e in evidence_blocks if e.get("source") == "deterministic_check"
        ),
        "summary": _build_summary_text(evidence_blocks),
    }

    return context


def _build_summary_text(evidence_blocks: list[dict]) -> str:
    """Build a human-readable summary of the evidence."""
    lines: list[str] = []

    # Count by source
    check_results = [e for e in evidence_blocks if e.get("source") == "deterministic_check"]
    rule_results = [e for e in evidence_blocks if e.get("source") == "deterministic_rule"]
    history_results = [e for e in evidence_blocks if e.get("source") == "score_history"]

    if check_results:
        passed = sum(1 for e in check_results if e.get("status") == "pass")
        failed = sum(1 for e in check_results if e.get("status") == "fail")
        errors = sum(1 for e in check_results if e.get("status") == "error")
        lines.append(f"Script checks: {passed} passed, {failed} failed, {errors} errors "
                     f"(of {len(check_results)} relevant checks)")

    if rule_results:
        passed = sum(1 for e in rule_results if e.get("passed"))
        failed = sum(1 for e in rule_results if not e.get("passed"))
        lines.append(f"Deterministic rules: {passed} passed, {failed} failed")

    if history_results:
        prev = history_results[0]
        lines.append(f"Previous score: {prev.get('previous_score', 'N/A')} "
                     f"({prev.get('previous_band', 'N/A')})")

    return "; ".join(lines) if lines else "No supporting evidence available"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gather supporting evidence for semantic audit (§21)"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--out-dir", required=True, help="Directory with validation/eval results")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    out_dir = Path(args.out_dir)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    context = build_supporting_evidence(system_root, args.domain, out_dir)
    write_json(Path(args.out), context)

    # Print summary
    evidence = context["supporting_evidence"]
    print(f"Gathered {len(evidence)} evidence blocks for {args.domain}")
    print(f"Summary: {context['summary']}")


if __name__ == "__main__":
    main()
