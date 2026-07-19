"""render_usecase_docs.py — Generates plan/usecase/ prose from tiers.yaml + loop.yaml.

Replaces hand-authored usecase files with mechanically generated output
from the same data init.py executes against. One source of truth.

Usage:
  python render_usecase_docs.py --system-root <path>
  python render_usecase_docs.py --system-root <path> --dry-run
  python render_usecase_docs.py --system-root <path> --out-dir <path>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_text, utc_now_iso, ALL_DOMAINS


# ---------------------------------------------------------------------------
# Use case definitions (mirrors init.py's USE_CASE_MAP)
# ---------------------------------------------------------------------------

USE_CASES = {
    "repo_new/case_1_no_documentation": {
        "has_code": False,
        "has_docs": False,
        "description": "New repo, no code, no docs — only a product idea as input",
        "path_default": "A",
    },
    "repo_new/case_2_has_documentation": {
        "has_code": False,
        "has_docs": True,
        "description": "New repo, some pre-existing docs",
        "path_default": "B",
    },
    "repo_existing/case_1_no_documentation": {
        "has_code": True,
        "has_docs": False,
        "description": "Existing repo with code, no docs",
        "path_default": "A",
    },
    "repo_existing/case_2_has_documentation": {
        "has_code": True,
        "has_docs": True,
        "description": "Existing repo, existing docs",
        "path_default": "B",
    },
}


# ---------------------------------------------------------------------------
# Document generation
# ---------------------------------------------------------------------------

def generate_tier_generation_md(
    tier_num: int,
    tier_domains: list[str],
    case_info: dict[str, Any],
    loop: dict[str, Any],
    relationships: list[dict],
    domain_drops: list[str],
) -> str:
    """Generate 01-generation.md for a tier (Path A: scaffold→content→audit→fix)."""
    lines = [
        f"# Tier {tier_num} — Generation (Path A)",
        "",
        f"**Use case:** {case_info['description']}",
        f"**Path:** A (generate from scratch — no existing documentation)",
        "",
        "## Domains",
        "",
    ]

    for d in tier_domains:
        lines.append(f"- `{d}`")

    lines.extend([
        "",
        "## Pipeline per Domain",
        "",
        "Each domain in this tier follows the Path A pipeline:",
        "",
        "1. **Scaffold** (`scripts/scaffold.py`) — read template, emit heading skeleton to `{domain}.md`",
        "2. **Content-fill** (semantic) — LLM writes prose per section, filling TODO placeholders",
        "3. **Post-hook: compile** — ingest into knowledge.db (when built)",
        "4. **Evaluate rules** (`scripts/evaluate_rules.py`) — evaluate deterministic rules against document",
        "5. **Evaluate semantic** (`scripts/evaluate_semantic.py`) — heuristic semantic criteria evaluation",
        "   - Pre-script: `scripts/gather_semantic_context.py` — gather check metrics as grounding evidence",
        "6. **Calculate** (`scripts/calculate.py`) — compute 4-bucket score from evaluated results",
        "7. **Report** (`scripts/report.py`) — render markdown report from templates",
        "8. **Analyze** (`scripts/analyze.py`) — generate structured fix plan, save to `{domain}-fix-plan.json`",
        "9. **Visualize** (`scripts/visualize.py`) — generate 8 PNG charts",
        "10. **Report HTML** (`scripts/report_html.py`) — render self-contained HTML report with embedded charts",
        "11. **Fix** (semantic, conditional) — only if score < threshold; re-fill content, re-audit",
        "",
    ])

    # Upstream dependencies
    upstream = [r for r in relationships if r["to"] in tier_domains]
    if upstream:
        lines.extend(["## Upstream Dependencies", ""])
        for r in upstream:
            gating = "strict" if r["type"] in ("inspires", "derives", "guides",
                                                 "validates", "requires") else "none"
            lines.append(f"- `{r['from']}` —{r['type']}→ `{r['to']}` (tier-gating: {gating})")
        lines.append("")

    # Within-tier ordering
    ordering = loop.get("within_tier_ordering", [])
    tier_ordering = [o for o in ordering if o.get("tier") == tier_num]
    if tier_ordering:
        lines.extend(["## Within-Tier Ordering", ""])
        for o in tier_ordering:
            lines.append(f"- `{o['from']}` must complete before `{o['to']}` starts")
        lines.append("")

    # Tier gate
    threshold = loop.get("threshold", {}).get("rating", "Acceptable")
    lines.extend([
        "## Tier Gate",
        "",
        f"All domains in tier {tier_num} must reach `{threshold}` before tier {tier_num + 1} starts.",
        "",
        "## Domain-Specific Notes",
        "",
    ])

    for d in tier_domains:
        lines.append(f"### {d}")
        lines.append("")
        if d in domain_drops:
            lines.append(f"> **Dropped** — not active for this system.")
        else:
            lines.append(f"- Scaffold reads `templates/generation/document/{d}.md` + `templates/generation/section/{d}/*.md`")
            lines.append(f"- Content-fill uses upstream context from completed tiers")
            lines.append(f"- Validate runs against `audit/deterministic/document/{d}.yaml` + section rules")
            lines.append(f"- Score persisted to `score_history.json` for cross-run trends")
        lines.append("")

    return "\n".join(lines)


def generate_tier_audit_md(
    tier_num: int,
    tier_domains: list[str],
    case_info: dict[str, Any],
    loop: dict[str, Any],
    relationships: list[dict],
    domain_drops: list[str],
) -> str:
    """Generate 02-audit.md for a tier (Path B: audit→fix, docs already exist)."""
    lines = [
        f"# Tier {tier_num} — Audit (Path B)",
        "",
        f"**Use case:** {case_info['description']}",
        f"**Path:** B (audit existing documentation — docs already present)",
        "",
        "## Domains",
        "",
    ]

    for d in tier_domains:
        lines.append(f"- `{d}`")

    lines.extend([
        "",
        "## Pipeline per Domain",
        "",
        "Each domain in this tier follows the Path B pipeline (no scaffold/content phase):",
        "",
        "1. **Pre-hook: staleness check** — skip if doc unchanged since last audit",
        "2. **Evaluate rules** (`scripts/evaluate_rules.py`) — evaluate deterministic rules against existing docs",
        "3. **Evaluate semantic** (`scripts/evaluate_semantic.py`) — heuristic semantic criteria evaluation",
        "   - Pre-script: `scripts/gather_semantic_context.py` — gather check metrics as grounding evidence",
        "4. **Validate** (`scripts/validate.py`) — run 18 deterministic check scripts",
        "5. **Calculate** (`scripts/calculate.py`) — compute 4-bucket score from evaluated results",
        "6. **Report** (`scripts/report.py`) — render markdown report",
        "7. **Analyze** (`scripts/analyze.py`) — generate structured fix plan",
        "8. **Visualize** (`scripts/visualize.py`) — generate 8 PNG charts",
        "9. **Report HTML** (`scripts/report_html.py`) — render self-contained HTML report",
        "10. **Fix** (semantic, conditional) — only if score < threshold; modify existing sections",
        "",
    ])

    # Upstream dependencies (same as generation)
    upstream = [r for r in relationships if r["to"] in tier_domains]
    if upstream:
        lines.extend(["## Upstream Dependencies", ""])
        for r in upstream:
            gating = "strict" if r["type"] in ("inspires", "derives", "guides",
                                                 "validates", "requires") else "none"
            lines.append(f"- `{r['from']}` —{r['type']}→ `{r['to']}` (tier-gating: {gating})")
        lines.append("")

    # Tier gate
    threshold = loop.get("threshold", {}).get("rating", "Acceptable")
    lines.extend([
        "## Tier Gate",
        "",
        f"All domains in tier {tier_num} must reach `{threshold}` before tier {tier_num + 1} starts.",
        "",
        "## Domain-Specific Notes",
        "",
    ])

    for d in tier_domains:
        lines.append(f"### {d}")
        lines.append("")
        if d in domain_drops:
            lines.append(f"> **Dropped** — not active for this system.")
        else:
            lines.append(f"- Existing doc detected at `docs/{d}.md` or `{d}.md`")
            lines.append(f"- Validate runs same checks as Path A but against existing content")
            lines.append(f"- Fix phase modifies existing sections in-place (not full re-generation)")
        lines.append("")

    return "\n".join(lines)


def generate_tier_fix_md(
    tier_num: int,
    tier_domains: list[str],
    case_info: dict[str, Any],
    loop: dict[str, Any],
    domain_drops: list[str],
) -> str:
    """Generate 03-fix.md for a tier (fix loop details)."""
    max_iter = loop.get("max_iterations", 5)
    fallback = loop.get("fallback", "human_review")
    threshold = loop.get("threshold", {}).get("rating", "Acceptable")

    lines = [
        f"# Tier {tier_num} — Fix Loop",
        "",
        f"**Use case:** {case_info['description']}",
        f"**Max iterations:** {max_iter}",
        f"**Threshold:** `{threshold}`",
        f"**Fallback:** {fallback}",
        "",
        "## Fix Procedure",
        "",
        "For each domain in this tier that scores below threshold:",
        "",
        "1. Identify failing sections from audit findings",
        "2. Re-run content-fill with expanded context (all completed domains)",
        "3. Re-validate and re-calculate",
        "4. Repeat until threshold met or max iterations reached",
        "5. If max iterations exceeded: flag for human review",
        "",
        "## Domains",
        "",
    ]

    for d in tier_domains:
        lines.append(f"- `{d}`")

    lines.extend([
        "",
        "## Iteration Tracking",
        "",
        "Each iteration is logged to console with:",
        "- Current score vs threshold",
        "- Which sections were re-filled",
        "- Re-scored result after fix",
        "",
        "Score history persisted to `score_history.json` after each successful calculate.",
        "",
    ])

    return "\n".join(lines)


def generate_tier_analyze_md(
    tier_num: int,
    tier_domains: list[str],
    case_info: dict[str, Any],
    loop: dict[str, Any],
    domain_drops: list[str],
) -> str:
    """Generate 04-analyze.md for a tier (analysis & fix-plan confirmation)."""
    threshold = loop.get("threshold", {}).get("rating", "Acceptable")

    lines = [
        f"# Tier {tier_num} — Analysis & Fix Plan",
        "",
        f"**Use case:** {case_info['description']}",
        f"**Threshold:** `{threshold}`",
        "",
        "## What This Phase Does",
        "",
        "After scores are calculated and reports rendered, the analyze phase",
        "reads all evaluation results and produces a structured fix plan.",
        "The fix plan identifies:",
        "- Which domains/sections are failing",
        "- Why they are failing (specific rule/criterion violations)",
        "- Whether the fix should be section-level or whole-document",
        "- Prioritized list of fixes by severity and score impact",
        "",
        "## Script",
        "",
        "`scripts/analyze.py` — reads `{domain}-scores.json`, `{domain}-validation.json`,",
        "`{domain}-det-eval.json`, and `{domain}-sem-eval.json` from the output directory.",
        "Produces `{domain}-fix-plan.json`.",
        "",
        "## Fix Plan Structure",
        "",
        "```json",
        "{",
        '  "domain": "01-vision",',
        '  "status": "fix_needed",',
        '  "final_score": 45.5,',
        '  "threshold": "Acceptable",',
        '  "fix_scope": "section_level",',
        '  "fix_scope_reason": "3 sections failing",',
        '  "fixes": [',
        "    {",
        '      "priority": 1,',
        '      "type": "error",',
        '      "source": "deterministic_rule",',
        '      "id": "vis-doc-001",',
        '      "scope": "document",',
        '      "message": "Missing sections: problem, solution"',
        "    }",
        "  ]",
        "}",
        "```",
        "",
        "## Fix Scope Decision",
        "",
        "- **Section-level**: ≤5 sections failing, targeted fixes to specific sections",
        "- **Whole-document**: >5 sections failing or >15 section-level findings — regenerate from scratch",
        "- **Document-level**: only document-wide issues (e.g. technology references)",
        "",
        "## Confirmation Checkpoint",
        "",
        "After the fix plan is generated, it is presented to the user via the",
        "rendered HTML report. The user can:",
        "- **Approve** the plan as-is",
        "- **Edit** scope (e.g. 'also fix this section' / 'skip that one')",
        "- **Reject** the plan entirely (falls back to human review)",
        "",
        "The fix phase executes ONLY the confirmed plan.",
        "",
        "## Domains",
        "",
    ]

    for d in tier_domains:
        lines.append(f"- `{d}`")

    lines.extend([
        "",
        "## Outputs",
        "",
        "Per domain in this tier:",
        "- `{domain}-fix-plan.json` — structured fix plan",
        "- Reviewed via HTML report before fix phase executes",
        "",
    ])

    return "\n".join(lines)

def render_usecase_docs(
    system_root: Path,
    out_dir: Path | None = None,
    dry_run: bool = False,
) -> int:
    """Generate all usecase prose files. Returns count of files written."""
    tiers_data = load_yaml(system_root / "plan" / "core" / "tiers.yaml")
    loop = load_yaml(system_root / "plan" / "core" / "loop.yaml")
    system = load_yaml(system_root / "system.yaml")

    tiers = tiers_data.get("tiers", [])
    relationships = tiers_data.get("relationships", [])
    drops = system.get("drops", [])
    drop_short = {d.split("-", 1)[1] if "-" in d else d for d in drops}

    if out_dir is None:
        out_dir = system_root / "plan" / "usecase"

    written = 0

    for case_key, case_info in USE_CASES.items():
        case_dir = out_dir / case_key.replace("/", "/")

        for tier_info in tiers:
            tier_num = tier_info["tier"]
            tier_domains = [d for d in tier_info["domains"] if d not in drop_short]
            tier_dir = case_dir / f"tier_{tier_num}"
            tier_dir.mkdir(parents=True, exist_ok=True)

            gen_md = generate_tier_generation_md(
                tier_num, tier_domains, case_info, loop, relationships, drops,
            )
            audit_md = generate_tier_audit_md(
                tier_num, tier_domains, case_info, loop, relationships, drops,
            )
            fix_md = generate_tier_fix_md(
                tier_num, tier_domains, case_info, loop, drops,
            )
            analyze_md = generate_tier_analyze_md(
                tier_num, tier_domains, case_info, loop, drops,
            )

            if not dry_run:
                write_text(tier_dir / "01-generation.md", gen_md)
                write_text(tier_dir / "02-audit.md", audit_md)
                write_text(tier_dir / "03-fix.md", fix_md)
                write_text(tier_dir / "04-analyze.md", analyze_md)
                written += 4
            else:
                print(f"  [dry-run] {case_key}/tier_{tier_num}/: "
                      f"01-generation.md, 02-audit.md, 03-fix.md, 04-analyze.md")

    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate plan/usecase/ prose from tiers.yaml + loop.yaml"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--out-dir", help="Output directory (default: plan/usecase/)")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir) if args.out_dir else None
    written = render_usecase_docs(system_root, out_dir, args.dry_run)

    if not args.dry_run:
        print(f"Generated {written} usecase prose files")
    else:
        print("Dry run complete — no files written")


if __name__ == "__main__":
    main()
