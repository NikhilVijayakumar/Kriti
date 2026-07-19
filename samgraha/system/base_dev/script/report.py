"""report.py — Renders audit report templates using calculated scores.

Reads templates/audit/{type}/{scope}/{domain}-report.md and substitutes
score data from calculate.py's output.

Usage:
  python report.py --system-root <path> --domain <domain> --scores <path> --out <path>
  python report.py --system-root <path> --domain <domain> --scores <path> --out <path> --type deterministic
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from _common import load_json, read_text, write_text, load_yaml


# ---------------------------------------------------------------------------
# Template substitution
# ---------------------------------------------------------------------------

def substitute_template(template: str, data: dict[str, Any]) -> str:
    """Substitute {{variable}} placeholders in a template with data values.

    Supports:
      - {{variable}} — direct substitution
      - {{variable | default('fallback')}} — with default
      - Nested dot notation: {{final_score.score}}
    """
    result = template

    def resolve_value(path: str, data: dict) -> Any:
        """Resolve a dotted path against a data dict."""
        parts = path.strip().split(".")
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def replace_match(m: re.Match) -> str:
        expr = m.group(1).strip()

        # Check for default filter
        default_match = re.match(r"(.+?)\s*\|\s*default\(['\"](.+?)['\"]\)", expr)
        if default_match:
            path = default_match.group(1).strip()
            fallback = default_match.group(2)
            value = resolve_value(path, data)
            return str(value) if value is not None else fallback

        # Simple path resolution
        value = resolve_value(expr, data)
        if value is None:
            return m.group(0)  # Leave unresolved
        return str(value)

    result = re.sub(r"\{\{(.+?)\}\}", replace_match, result)
    return result


def render_rule_table(rules: list[dict], rule_data: dict[str, Any]) -> str:
    """Render a rule table row from audit data."""
    rows: list[str] = []
    for rule in rules:
        rule_id = rule.get("id", "unknown")
        passed = rule.get("passed", False)
        weight = rule.get("weight", 0)
        status_icon = "PASS" if passed else "FAIL"
        rows.append(f"| {rule_id} | {status_icon} | {weight} | |")

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_report(
    system_root: Path,
    domain: str,
    scores: dict[str, Any],
    report_type: str = "deterministic",
    scope: str = "document",
) -> str:
    """Render a report for a domain using the appropriate template."""
    template_dir = system_root / "templates" / "audit" / report_type / scope
    template_path = template_dir / f"{domain}-report.md"

    if not template_path.exists():
        # Try fallback to summary template
        summary_dir = system_root / "templates" / "audit" / "summary"
        template_path = summary_dir / f"{domain}-report.md"

    if not template_path.exists():
        return _generate_fallback_report(domain, scores, report_type, scope)

    template = read_text(template_path)
    return substitute_template(template, scores)


def _generate_fallback_report(
    domain: str,
    scores: dict[str, Any],
    report_type: str,
    scope: str,
) -> str:
    """Generate a fallback report when no template exists."""
    lines = [
        f"# {report_type.title()} {scope.title()} Report — {domain}",
        "",
        f"Generated at: {scores.get('calculated_at', 'unknown')}",
        "",
    ]

    if report_type == "deterministic":
        if scope == "document":
            det = scores.get("deterministic_document", {})
            lines.extend([
                "## Document Score",
                "",
                f"| Metric | Value |",
                f"|--------|-------|",
                f"| Score | {det.get('score', 0)} |",
                f"| Rules Total | {det.get('rules_total', 0)} |",
                f"| Rules Passed | {det.get('rules_passed', 0)} |",
                f"| Rules Failed | {det.get('rules_failed', 0)} |",
                "",
            ])
        else:
            det = scores.get("deterministic_section", {})
            lines.extend([
                "## Section Scores",
                "",
                "| Section | Score | Rules Passed | Rules Total |",
                "|---------|-------|-------------|-------------|",
            ])
            for sec in det.get("sections", []):
                lines.append(
                    f"| {sec['section']} | {sec['score']} | "
                    f"{sec.get('rules_passed', 0)} | {sec.get('rules_total', 0)} |"
                )
            lines.extend(["", f"**Rollup (average):** {det.get('rollup', 0)}", ""])

    elif report_type == "semantic":
        if scope == "document":
            sem = scores.get("semantic_document", {})
            lines.extend([
                "## Document Score",
                "",
                f"| Metric | Value |",
                f"|--------|-------|",
                f"| Score | {sem.get('score', 0)} |",
                f"| Criteria Total | {sem.get('criteria_total', 0)} |",
                f"| Criteria Passed | {sem.get('criteria_passed', 0)} |",
                "",
            ])
        else:
            sem = scores.get("semantic_section", {})
            lines.extend([
                "## Section Scores",
                "",
                "| Section | Score | Criteria Passed | Criteria Total |",
                "|---------|-------|----------------|----------------|",
            ])
            for sec in sem.get("sections", []):
                lines.append(
                    f"| {sec['section']} | {sec['score']} | "
                    f"{sec.get('criteria_passed', 0)} | {sec.get('criteria_total', 0)} |"
                )
            lines.extend(["", f"**Rollup (average):** {sem.get('rollup', 0)}", ""])

    # Add final score and bands
    final = scores.get("final_score", {})
    bands = scores.get("score_bands", {})
    trend = scores.get("trend", {})

    lines.extend([
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Final Score | {final.get('score', 0)} |",
        f"| Rating | {bands.get('rating', 'unknown')} |",
        f"| Trend | {trend.get('direction', 'baseline')} |",
        f"| Delta | {trend.get('delta', 0)} |",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Render audit report from scores")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--scores", required=True, help="Path to scores JSON from calculate.py")
    parser.add_argument("--out", required=True, help="Output report path (.md)")
    parser.add_argument("--type", default="deterministic",
                        choices=["deterministic", "semantic", "summary"],
                        help="Report type")
    parser.add_argument("--scope", default="document",
                        choices=["document", "section"],
                        help="Report scope")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    scores_path = Path(args.scores)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)
    if not scores_path.exists():
        print(f"Error: scores file not found: {scores_path}", file=sys.stderr)
        sys.exit(1)

    scores = load_json(scores_path)
    report = render_report(system_root, args.domain, scores, args.type, args.scope)

    write_text(Path(args.out), report)
    print(f"Report written to {args.out}")


if __name__ == "__main__":
    main()
