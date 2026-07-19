"""plan_generation.py — Renders PLAN.md per the author guide's §5.2.

Reads tiers.yaml, loop.yaml, and system.yaml to produce a human-readable
PLAN.md that describes the execution plan for a given use case.

Usage:
  python plan_generation.py --system-root <path> --use-case <case> --out <path>
  python plan_generation.py --system-root <path> --use-case <case> --out <path> --existing-docs <list>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from _common import load_yaml, write_text, ALL_DOMAINS, DOMAIN_NUMS, utc_now_iso


# ---------------------------------------------------------------------------
# Custom template filters
# ---------------------------------------------------------------------------

def _format_domain(domain: str) -> str:
    """Format a domain name for display in the template."""
    return f"`{domain}`"


# ---------------------------------------------------------------------------
# Plan generation
# ---------------------------------------------------------------------------

def generate_plan(
    system_root: Path,
    use_case: str,
    existing_docs: list[str] | None = None,
) -> str:
    """Generate a PLAN.md for the given use case.

    Args:
        system_root: Path to the system directory.
        use_case: One of repo_new/case_1, repo_new/case_2,
                  repo_existing/case_1, repo_existing/case_2.
        existing_docs: List of domain names that already have documentation.
    """
    system = load_yaml(system_root / "system.yaml")
    tiers_data = load_yaml(system_root / "plan" / "core" / "tiers.yaml")
    loop = load_yaml(system_root / "plan" / "core" / "loop.yaml")

    domains = system.get("domains", ALL_DOMAINS)
    drops = system.get("drops", [])
    active_domains = [d for d in domains if d not in drops]

    active_short_names = {d.split("-", 1)[1] if "-" in d else d for d in active_domains}
    drops_short_names = {d.split("-", 1)[1] if "-" in d else d for d in drops}

    if existing_docs is None:
        existing_docs = []

    # Build tier data for template
    tier_data = tiers_data.get("tiers", [])
    relationships = tiers_data.get("relationships", [])

    # Determine within-tier ordering
    ordering_map = {}
    for item in loop.get("within_tier_ordering", []):
        ordering_map[item["tier"]] = item

    # Build structured tier list for template
    tiers = []
    for idx, tier_info in enumerate(tier_data):
        tier_num = tier_info["tier"]
        tier_domains = [d for d in tier_info["domains"]
                        if d in active_short_names and d not in drops_short_names]

        if not tier_domains:
            continue

        # Upstream dependencies for this tier
        upstream_deps = []
        for rel in relationships:
            if rel["to"] in tier_domains:
                rel_type = rel["type"]
                gating = "strict" if rel_type in ("inspires", "derives", "guides",
                                                    "validates", "requires") else "none"
                upstream_deps.append({
                    "from": rel["from"],
                    "to": rel["to"],
                    "type": rel_type,
                    "gating": gating,
                })

        # Path selection per domain
        domain_paths = {}
        for domain in tier_domains:
            if domain in existing_docs:
                path = "Path B (audit→fix)"
                phases = ["validate", "calculate", "report", "fix"]
            else:
                path = "Path A (generate)"
                phases = ["scaffold", "content", "validate", "calculate", "report", "fix"]
            domain_paths[domain] = {"path": path, "phases": phases}

        tiers.append({
            "num": tier_num,
            "domains": tier_domains,
            "ordering": ordering_map.get(tier_num),
            "upstream_deps": upstream_deps,
            "domain_paths": domain_paths,
            "is_last": idx == len(tier_data) - 1,
        })

    # Threshold info
    threshold = loop.get("threshold", {})

    # Render template
    template_dir = system_root / "templates" / "plan"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        keep_trailing_newline=True,
    )
    env.filters["format_domain"] = _format_domain

    template = env.get_template("PLAN.md.j2")

    return template.render(
        system_name=system.get("name", "unknown"),
        use_case=use_case,
        generated_at=utc_now_iso(),
        abstract=system.get("abstract", False),
        active_domain_count=len(active_domains),
        drops=drops,
        threshold_score=threshold.get("score", "acceptable_minimum"),
        threshold_rating=threshold.get("rating", "Acceptable"),
        max_iterations=loop.get("max_iterations", 5),
        fallback=loop.get("fallback", "human_review"),
        tiers=tiers,
        special_cases=loop.get("special_cases", {}),
        total_tiers=len(tiers),
        relationship_count=len(relationships),
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PLAN.md for a use case")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--use-case", required=True,
                        help="Use case (e.g. repo_new/case_1_no_documentation)")
    parser.add_argument("--out", required=True, help="Output PLAN.md path")
    parser.add_argument("--existing-docs", nargs="*", default=[],
                        help="Domains that already have documentation")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    plan = generate_plan(system_root, args.use_case, args.existing_docs)
    write_text(Path(args.out), plan)
    print(f"Plan written to {args.out}")


if __name__ == "__main__":
    main()
