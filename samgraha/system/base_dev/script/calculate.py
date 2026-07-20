"""calculate.py — Implements the 7 scoring formulas from calculation/.

Formulas:
  1. deterministic_document_v1  — weighted_pass_rate (whole doc)
  2. deterministic_section_v1   — weighted_pass_rate per section + average rollup
  3. semantic_document_v1       — sum capped at 100 (whole doc)
  4. semantic_section_v1        — sum capped at 100 per section + average rollup
  5. final_score_v1             — weighted_sum 25/25/25/25
  6. score_bands_v1             — threshold_lookup
  7. trend_v1                   — trend_comparison with tolerance

Usage:
  python calculate.py --system-root <path> --domain <domain> --out <path>
  python calculate.py --system-root <path> --domain <domain> --out <path> --previous-report <path>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from _common import load_yaml, write_json, utc_now_iso, resolve_domain


# ---------------------------------------------------------------------------
# Formula implementations
# ---------------------------------------------------------------------------

def deterministic_document(rules: list[dict]) -> dict[str, Any]:
    """Formula: deterministic_document_v1 — weighted_pass_rate."""
    total_weight = sum(r.get("weight", 0) for r in rules)
    passed_weight = sum(r.get("weight", 0) for r in rules if r.get("passed", False))

    if total_weight == 0:
        score = 0.0
    else:
        score = round(100 * passed_weight / total_weight, 2)

    return {
        "formula": "deterministic_document_v1",
        "score": score,
        "total_weight": total_weight,
        "passed_weight": passed_weight,
        "rules_total": len(rules),
        "rules_passed": sum(1 for r in rules if r.get("passed", False)),
        "rules_failed": sum(1 for r in rules if not r.get("passed", False)),
    }


def deterministic_section(sections: list[dict]) -> dict[str, Any]:
    """Formula: deterministic_section_v1 — per-section weighted_pass_rate + average rollup."""
    section_scores: list[dict] = []

    for sec in sections:
        rules = sec.get("rules", [])
        total_weight = sum(r.get("weight", 0) for r in rules)
        passed_weight = sum(r.get("weight", 0) for r in rules if r.get("passed", False))

        if total_weight == 0:
            score = 0.0
        else:
            score = round(100 * passed_weight / total_weight, 2)

        section_scores.append({
            "section": sec.get("section", "unknown"),
            "score": score,
            "total_weight": total_weight,
            "passed_weight": passed_weight,
            "rules_total": len(rules),
            "rules_passed": sum(1 for r in rules if r.get("passed", False)),
        })

    scores_list = [s["score"] for s in section_scores]
    avg_score = round(sum(scores_list) / len(scores_list), 2) if scores_list else 0.0

    return {
        "formula": "deterministic_section_v1",
        "sections": section_scores,
        "rollup": avg_score,
    }


def semantic_document(criteria: list[dict]) -> dict[str, Any]:
    """Formula: semantic_document_v1 — sum of passed criterion scores, capped at 100."""
    total = 0
    for c in criteria:
        if c.get("passed", False):
            total += c.get("score", 0)

    return {
        "formula": "semantic_document_v1",
        "score": min(100, total),
        "uncapped": total,
        "criteria_total": len(criteria),
        "criteria_passed": sum(1 for c in criteria if c.get("passed", False)),
    }


def semantic_section(sections: list[dict]) -> dict[str, Any]:
    """Formula: semantic_section_v1 — per-section sum capped at 100 + average rollup."""
    section_scores: list[dict] = []

    for sec in sections:
        criteria = sec.get("criteria", [])
        total = 0
        for c in criteria:
            if c.get("passed", False):
                total += c.get("score", 0)

        section_scores.append({
            "section": sec.get("section", "unknown"),
            "score": min(100, total),
            "uncapped": total,
            "criteria_total": len(criteria),
            "criteria_passed": sum(1 for c in criteria if c.get("passed", False)),
        })

    scores_list = [s["score"] for s in section_scores]
    avg_score = round(sum(scores_list) / len(scores_list), 2) if scores_list else 0.0

    return {
        "formula": "semantic_section_v1",
        "sections": section_scores,
        "rollup": avg_score,
    }


def final_score(buckets: dict[str, float]) -> dict[str, Any]:
    """Formula: final_score_v1 — weighted_sum with 25/25/25/25 split."""
    weights = {
        "deterministic_whole": 25,
        "deterministic_section": 25,
        "semantic_whole": 25,
        "semantic_section": 25,
    }

    weighted_sum = 0.0
    breakdown: dict[str, Any] = {}
    for key, weight in weights.items():
        bucket_score = buckets.get(key, 0.0)
        contribution = round(bucket_score / 100 * weight, 4)
        weighted_sum += contribution
        breakdown[key] = {
            "score": bucket_score,
            "weight": weight,
            "contribution": contribution,
        }

    return {
        "formula": "final_score_v1",
        "score": round(weighted_sum, 2),
        "breakdown": breakdown,
    }


def score_bands(score: float) -> dict[str, Any]:
    """Formula: score_bands_v1 — threshold_lookup."""
    bands = [
        {"min": 95, "max": 100, "rating": "Excellent"},
        {"min": 90, "max": 94, "rating": "Very Good"},
        {"min": 80, "max": 89, "rating": "Good"},
        {"min": 70, "max": 79, "rating": "Acceptable"},
        {"min": 0, "max": 69, "rating": "Needs Improvement"},
    ]

    rating = "Needs Improvement"
    for band in bands:
        if band["min"] <= score <= band["max"]:
            rating = band["rating"]
            break

    return {
        "formula": "score_bands_v1",
        "score": score,
        "rating": rating,
        "thresholds": bands,
    }


def trend_comparison(
    current: float,
    previous: float | None,
    tolerance: float = 0.1,
) -> dict[str, Any]:
    """Formula: trend_v1 — trend_comparison with stddev-based tolerance."""
    if previous is None:
        direction = "baseline"
        delta = 0.0
    elif abs(current - previous) <= tolerance:
        direction = "stable"
        delta = round(current - previous, 2)
    elif current > previous:
        direction = "improving"
        delta = round(current - previous, 2)
    else:
        direction = "declining"
        delta = round(current - previous, 2)

    return {
        "formula": "trend_v1",
        "current": current,
        "previous": previous,
        "delta": delta,
        "direction": direction,
        "tolerance": tolerance,
    }


# ---------------------------------------------------------------------------
# Load audit results from disk
# ---------------------------------------------------------------------------

def load_audit_results(
    system_root: Path,
    domain: str,
    out_dir: Path | None = None,
) -> dict[str, Any]:
    """Load deterministic + semantic audit results for a domain.

    Reads evaluated results from out_dir if available (from evaluate_rules.py
    and evaluate_semantic.py). Falls back to raw YAML rule definitions from
    system_root/audit/ when evaluated results don't exist.

    Returns a dict with keys: det_doc, det_sec, sem_doc, sem_sec.
    Each value is a list of rule/criterion dicts with 'passed' field.
    """
    audit_root = system_root / "audit"

    # --- Deterministic document rules ---
    det_doc_rules: list[dict] = []

    # Try evaluated results first (from evaluate_rules.py)
    if out_dir:
        det_eval_path = out_dir / f"{domain}-det-eval.json"
        if det_eval_path.exists():
            from _common import load_json
            eval_data = load_json(det_eval_path)
            det_doc_rules = eval_data.get("doc_rules", [])

    # Fall back to raw YAML rule definitions (§20 bug: no 'passed' field)
    if not det_doc_rules:
        prefixed_domain = resolve_domain(domain)
        det_doc_path = audit_root / "deterministic" / "document" / f"{prefixed_domain}.yaml"
        if det_doc_path.exists():
            data = load_yaml(det_doc_path)
            det_doc_rules = data.get("rules", [])

    # --- Deterministic section rules ---
    det_sec_groups: dict[str, list[dict]] = {}

    # Try evaluated results first
    if out_dir:
        det_eval_path = out_dir / f"{domain}-det-eval.json"
        if det_eval_path.exists():
            from _common import load_json
            eval_data = load_json(det_eval_path)
            det_sec_groups = eval_data.get("sec_rules", {})

    # Fall back to raw YAML
    if not det_sec_groups:
        det_sec_dir = audit_root / "deterministic" / "section" / resolve_domain(domain)
        if det_sec_dir.is_dir():
            for yaml_file in sorted(det_sec_dir.glob("*.yaml")):
                data = load_yaml(yaml_file)
                section_name = yaml_file.stem
                det_sec_groups[section_name] = data.get("rules", [])

    # --- Semantic document criteria ---
    sem_doc_criteria: list[dict] = []

    # Try evaluated results first (from evaluate_semantic.py)
    if out_dir:
        sem_eval_path = out_dir / f"{domain}-sem-eval.json"
        if sem_eval_path.exists():
            from _common import load_json
            eval_data = load_json(sem_eval_path)
            doc_criteria = eval_data.get("document", {}).get("criteria", [])
            # Map to calculate.py's expected format: {criterion_id, passed, score, ...}
            sem_doc_criteria = [
                {
                    "criterion_id": c.get("criterion_id", ""),
                    "passed": c.get("passed", False),
                    "score": c.get("score", 0),
                    "mandatory": c.get("mandatory", False),
                    "description": c.get("description", ""),
                }
                for c in doc_criteria
            ]

    # Fall back to parsing rubric from markdown
    if not sem_doc_criteria:
        sem_doc_path = audit_root / "semantic" / "document" / f"{resolve_domain(domain)}.md"
        if sem_doc_path.exists():
            content = sem_doc_path.read_text(encoding="utf-8")
            sem_doc_criteria = _parse_semantic_criteria(content)

    # --- Semantic section criteria ---
    sem_sec_groups: dict[str, list[dict]] = {}

    # Try evaluated results first
    if out_dir:
        sem_eval_path = out_dir / f"{domain}-sem-eval.json"
        if sem_eval_path.exists():
            from _common import load_json
            eval_data = load_json(sem_eval_path)
            for sec_name, sec_data in eval_data.get("sections", {}).items():
                sec_criteria = sec_data.get("criteria", [])
                sem_sec_groups[sec_name] = [
                    {
                        "criterion_id": c.get("criterion_id", ""),
                        "passed": c.get("passed", False),
                        "score": c.get("score", 0),
                        "mandatory": c.get("mandatory", False),
                        "description": c.get("description", ""),
                    }
                    for c in sec_criteria
                ]

    # Fall back to parsing rubric from markdown
    if not sem_sec_groups:
        sem_sec_dir = audit_root / "semantic" / "section" / resolve_domain(domain)
        if sem_sec_dir.is_dir():
            for md_file in sorted(sem_sec_dir.rglob("*.md")):
                section_name = md_file.stem
                content = md_file.read_text(encoding="utf-8")
                sem_sec_groups[section_name] = _parse_semantic_criteria(content)

    return {
        "det_doc": det_doc_rules,
        "det_sec": det_sec_groups,
        "sem_doc": sem_doc_criteria,
        "sem_sec": sem_sec_groups,
    }


def _parse_semantic_criteria(content: str) -> list[dict]:
    """Parse scoring criteria from a semantic audit markdown file.

    Looks for the | ID | Weight | Score | Description | table.
    """
    import re
    criteria: list[dict] = []
    in_table = False
    for line in content.split("\n"):
        if re.match(r"^\|\s*ID\s*\|", line, re.IGNORECASE):
            in_table = True
            continue
        if in_table and re.match(r"^\|[\s:-]+\|", line):
            continue
        if in_table and line.strip().startswith("|"):
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) >= 3:
                weight_str = cols[1].lower()
                mandatory = weight_str == "mandatory"
                try:
                    score_val = int(cols[2]) if cols[2].isdigit() else 0
                except (ValueError, IndexError):
                    score_val = 0
                criteria.append({
                    "criterion_id": cols[0],
                    "mandatory": mandatory,
                    "score": score_val,
                    "description": cols[3] if len(cols) > 3 else "",
                })
        elif in_table and not line.strip().startswith("|"):
            in_table = False

    return criteria


# ---------------------------------------------------------------------------
# Previous report loading
# ---------------------------------------------------------------------------

def load_previous_scores(report_path: Path) -> dict[str, float]:
    """Load scores from a previous report file for trend comparison."""
    if not report_path.exists():
        return {}

    content = report_path.read_text(encoding="utf-8")
    scores: dict[str, float] = {}

    import re
    # Look for score lines like "| final_score | 85.5 |"
    for match in re.finditer(r"final_score.*?\|\s*(\d+\.?\d*)\s*\|", content):
        try:
            scores["final_score"] = float(match.group(1))
        except ValueError:
            pass

    return scores


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def calculate_all(system_root: Path, domain: str, out_dir: Path | None = None) -> dict[str, Any]:
    """Run all 7 formulas for a domain and return the complete score dict."""
    audit = load_audit_results(system_root, domain, out_dir)

    # 1. Deterministic document
    det_doc = deterministic_document(audit["det_doc"])

    # 2. Deterministic section
    det_sec_input = [
        {"section": name, "rules": rules}
        for name, rules in audit["det_sec"].items()
    ]
    det_sec = deterministic_section(det_sec_input)

    # 3. Semantic document
    sem_doc = semantic_document(audit["sem_doc"])

    # 4. Semantic section
    sem_sec_input = [
        {"section": name, "criteria": criteria}
        for name, criteria in audit["sem_sec"].items()
    ]
    sem_sec = semantic_section(sem_sec_input)

    # 5. Final score
    buckets = {
        "deterministic_whole": det_doc["score"],
        "deterministic_section": det_sec["rollup"],
        "semantic_whole": sem_doc["score"],
        "semantic_section": sem_sec["rollup"],
    }
    final = final_score(buckets)

    # 6. Score bands
    bands = score_bands(final["score"])

    # 7. Trend (placeholder — needs previous report)
    trend = trend_comparison(final["score"], None)

    # Read model attribution from semantic eval (§7 flow)
    model = "heuristic-v1"
    if out_dir:
        sem_eval_path = out_dir / f"{domain}-sem-eval.json"
        if sem_eval_path.exists():
            from _common import load_json
            sem_eval = load_json(sem_eval_path)
            model = sem_eval.get("model", "heuristic-v1")

    return {
        "domain": domain,
        "calculated_at": utc_now_iso(),
        "model": model,
        "deterministic_document": det_doc,
        "deterministic_section": det_sec,
        "semantic_document": sem_doc,
        "semantic_section": sem_sec,
        "final_score": final,
        "score_bands": bands,
        "trend": trend,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate audit scores for a domain")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--out-dir", help="Directory containing evaluated results (for §20 fix)")
    parser.add_argument("--previous-report", help="Previous report for trend comparison")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir) if args.out_dir else None
    result = calculate_all(system_root, args.domain, out_dir)

    # Apply trend if previous report provided
    if args.previous_report:
        prev_path = Path(args.previous_report)
        prev_scores = load_previous_scores(prev_path)
        if "final_score" in prev_scores:
            result["trend"] = trend_comparison(
                result["final_score"]["score"],
                prev_scores["final_score"],
            )

    write_json(Path(args.out), result)


if __name__ == "__main__":
    main()
