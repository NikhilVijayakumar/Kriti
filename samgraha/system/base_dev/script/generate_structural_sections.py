"""generate_structural_sections.py -- Generates structural section skeletons.

For sections whose format is deterministic but content needs input:
constraints, dependencies, non-goals, external-dependencies, runtime-constraints,
architectural-constraints, security-considerations, performance-considerations,
extension-points.

Generates the table structure with correct columns, source attribution,
and downstream impact mapping from relationship data. Content cells are
left as TODO markers for LLM/human fill.

Usage:
  python generate_structural_sections.py --system-root <path> --domain <domain> --section <section> --out <path>
  python generate_structural_sections.py --system-root <path> --all --out-dir <path>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_text, resolve_domain, DOMAIN_PREFIX


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tiers(system_root: Path) -> dict[str, Any]:
    """Load tiers.yaml."""
    tiers_path = system_root / "plan" / "core" / "tiers.yaml"
    return load_yaml(tiers_path)


def load_relationships(system_root: Path, domain: str) -> list[dict]:
    """Load {NN}-*-relationships.yaml for a domain."""
    prefixed = resolve_domain(domain)
    rel_path = system_root / "audit" / "deterministic" / "document" / f"{prefixed}-relationships.yaml"
    if not rel_path.exists():
        return []
    data = load_yaml(rel_path)
    return data.get("relationships", [])


def format_tier_name(domain: str) -> str:
    """Format domain name for display."""
    return domain.replace("-", " ").title()


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------

def generate_constraints_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate a constraints section skeleton.

    Reads constrains/derives_from edges to determine:
    - Which upstream domains provide constraint sources
    - Which downstream domains are affected
    """
    domain_tier = {}
    for tier_def in tier_data.get("tiers", []):
        for d in tier_def.get("domains", []):
            domain_tier[d] = tier_def["tier"]

    # Find constraint-related edges
    upstream_sources: list[dict] = []
    downstream_impacts: list[dict] = []

    for rel in relationships:
        rel_type = rel.get("type", "")
        from_section = rel.get("from_section", "")
        target_domain = rel.get("target_domain")

        if target_domain is None or target_domain == "null":
            continue

        # Constraints section derives from upstream
        if from_section == "constraints" and rel_type in ("derives_from", "constrains"):
            if domain_tier.get(target_domain, 99) < domain_tier.get(domain, 99):
                upstream_sources.append({
                    "domain": target_domain,
                    "section": rel.get("target_section", "constraints"),
                })
            else:
                downstream_impacts.append({
                    "domain": target_domain,
                    "section": rel.get("target_section", "constraints"),
                })

    lines: list[str] = []

    if upstream_sources:
        lines.append("## Constraint Sources")
        lines.append("")
        lines.append("The following upstream standards provide constraint sources:")
        lines.append("")
        for src in sorted(upstream_sources, key=lambda s: domain_tier.get(s["domain"], 99)):
            label = format_tier_name(src["domain"])
            section = src["section"].replace("_", " ").title()
            lines.append(f"- **{label}** / {section}")
        lines.append("")

    # Generate constraint table
    lines.append("## Constraints")
    lines.append("")
    lines.append("| # | Category | Statement | Source | Enforcement | Impact |")
    lines.append("|---|----------|-----------|--------|-------------|--------|")

    # Generate placeholder rows based on constraint categories
    categories = ["Regulatory", "Business", "Technical", "Platform"]
    for i, cat in enumerate(categories, 1):
        source_ref = ""
        if upstream_sources:
            src = upstream_sources[0]
            source_ref = f"{format_tier_name(src['domain'])} / {src['section'].replace('_', ' ').title()}"

        impact_refs = ""
        if downstream_impacts:
            impact_refs = ", ".join(format_tier_name(d["domain"]) for d in downstream_impacts[:3])

        lines.append(
            f"| C-{i:03d} | {cat} | <!-- TODO: {cat.lower()} constraint statement --> "
            f"| {source_ref or '<!-- TODO: source -->'} | binding | "
            f"{impact_refs or '<!-- TODO: impacted domains -->'} |"
        )

    lines.append("")

    if downstream_impacts:
        lines.append("## Downstream Impact")
        lines.append("")
        lines.append("The following standards are affected by these constraints:")
        lines.append("")
        for imp in sorted(downstream_impacts, key=lambda d: domain_tier.get(d["domain"], 99)):
            label = format_tier_name(imp["domain"])
            section = imp["section"].replace("_", " ").title()
            lines.append(f"- **{label}** / {section}")
        lines.append("")

    return "\n".join(lines)


def generate_dependencies_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate a dependencies section skeleton."""
    lines: list[str] = []

    lines.append("## Dependencies")
    lines.append("")
    lines.append("| # | Dependency | Nature | Required | Source | Behavior if Unavailable |")
    lines.append("|---|-----------|--------|----------|--------|------------------------|")

    for i in range(1, 4):
        lines.append(
            f"| D-{i:03d} | <!-- TODO: dependency name --> | "
            f"<!-- TODO: functional/data/ui --> | yes | "
            f"<!-- TODO: source document --> | "
            f"<!-- TODO: fallback behavior --> |"
        )

    lines.append("")
    return "\n".join(lines)


def generate_non_goals_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate a non-goals section skeleton."""
    domain_tier = {}
    for tier_def in tier_data.get("tiers", []):
        for d in tier_def.get("domains", []):
            domain_tier[d] = tier_def["tier"]

    # Find which domains own related sections
    related_domains = set()
    for rel in relationships:
        target = rel.get("target_domain")
        if target and target != "null":
            related_domains.add(target)

    lines: list[str] = []

    lines.append("## Non-Goals")
    lines.append("")
    lines.append("The following are explicitly out of scope for this document:")
    lines.append("")

    for i in range(1, 4):
        owning = "<!-- TODO: owning standard -->"
        if related_domains:
            # Pick the most relevant domain
            candidates = sorted(related_domains, key=lambda d: domain_tier.get(d, 99))
            owning = format_tier_name(candidates[0]) if candidates else owning

        lines.append(
            f"- **NG-{i:03d}**: <!-- TODO: non-goal statement --> "
            f"(owned by {owning})"
        )

    lines.append("")
    return "\n".join(lines)


def generate_external_dependencies_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate external-dependencies section for feature-technical."""
    lines: list[str] = []

    lines.append("## External Dependencies")
    lines.append("")

    # Find external-context references
    ext_refs = [
        rel for rel in relationships
        if rel.get("target_domain") == "external-context"
        or rel.get("from_section") == "external_dependencies"
    ]

    for i in range(1, 4):
        lines.append(f"### Dependency {i}")
        lines.append("")
        lines.append(f"- **External System**: <!-- TODO: name of external system -->")
        lines.append(f"- **Role**: <!-- TODO: what this system provides -->")
        lines.append(f"- **Nature of Integration**: <!-- TODO: API/file/stream/batch -->")
        lines.append(f"- **Constraints**: <!-- TODO: rate limits, auth requirements -->")
        lines.append(f"- **Reference**: External Context (08) / <!-- TODO: section -->")
        lines.append("")

    return "\n".join(lines)


def generate_runtime_constraints_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate runtime-constraints section for feature-technical."""
    # Find upstream constraint sources
    constraint_sources = [
        rel for rel in relationships
        if rel.get("from_section") == "runtime_constraints"
        and rel.get("type") == "derives_from"
    ]

    lines: list[str] = []

    lines.append("## Runtime Constraints")
    lines.append("")

    if constraint_sources:
        lines.append("Derived from:")
        lines.append("")
        for src in constraint_sources:
            target = src.get("target_domain", "")
            section = src.get("target_section", "constraints")
            if target:
                lines.append(f"- {format_tier_name(target)} / {section.replace('_', ' ').title()}")
        lines.append("")

    for i in range(1, 4):
        lines.append(f"### Constraint {i}")
        lines.append("")
        lines.append(f"- **Statement**: <!-- TODO: runtime constraint statement -->")
        lines.append(f"- **Threshold**: <!-- TODO: measurable threshold -->")
        lines.append(f"- **Source**: <!-- TODO: upstream standard reference -->")
        lines.append(f"- **Verifiability**: <!-- TODO: how to verify -->")
        lines.append("")

    return "\n".join(lines)


def generate_architectural_constraints_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate architectural-constraints section for feature-technical."""
    lines: list[str] = []

    lines.append("## Architectural Constraints")
    lines.append("")
    lines.append("Derived from Architecture (05) principles and component model:")
    lines.append("")

    for i in range(1, 4):
        lines.append(f"### Constraint {i}")
        lines.append("")
        lines.append(f"- **Architecture Principle**: <!-- TODO: reference to Architecture principle -->")
        lines.append(f"- **Feature Application**: <!-- TODO: how this applies to the feature -->")
        lines.append(f"- **Rationale**: <!-- TODO: why this constraint exists -->")
        lines.append("")

    return "\n".join(lines)


def generate_security_considerations_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate security-considerations section for feature-technical."""
    lines: list[str] = []

    lines.append("## Security Considerations")
    lines.append("")

    sections = [
        ("Security Boundary", "Where does this feature sit relative to security boundaries?"),
        ("Authentication", "How does this feature authenticate users/systems?"),
        ("Authorization", "What permissions does this feature require?"),
        ("Sensitive Data", "What sensitive data does this feature handle?"),
    ]

    for title, prompt in sections:
        lines.append(f"### {title}")
        lines.append("")
        lines.append(f"<!-- {prompt} -->")
        lines.append(f"<!-- TODO: {title.lower()} details -->")
        lines.append("")

    return "\n".join(lines)


def generate_performance_considerations_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate performance-considerations section for feature-technical."""
    lines: list[str] = []

    lines.append("## Performance Considerations")
    lines.append("")
    lines.append("Derived from Architecture / Operational Readiness and Runtime Constraints:")
    lines.append("")

    lines.append("| # | Metric | Threshold | Source | Verification |")
    lines.append("|---|--------|-----------|--------|--------------|")

    for i in range(1, 4):
        lines.append(
            f"| P-{i:03d} | <!-- TODO: metric name --> | "
            f"<!-- TODO: threshold value --> | "
            f"<!-- TODO: Architecture/External Context --> | "
            f"<!-- TODO: how to verify --> |"
        )

    lines.append("")
    return "\n".join(lines)


def generate_extension_points_section(
    domain: str,
    relationships: list[dict],
    tier_data: dict[str, Any],
) -> str:
    """Generate extension-points section for feature-technical."""
    lines: list[str] = []

    lines.append("## Extension Points")
    lines.append("")

    for i in range(1, 4):
        lines.append(f"### Extension Point {i}")
        lines.append("")
        lines.append(f"- **Type**: <!-- TODO: plugin/hook/event/configuration -->")
        lines.append(f"- **Description**: <!-- TODO: what this extension point enables -->")
        lines.append(f"- **Constraints**: <!-- TODO: limitations on extension -->")
        lines.append(f"- **Reference**: Architecture (05) / Component Model")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section registry
# ---------------------------------------------------------------------------

SECTION_GENERATORS = {
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

# Map domain -> list of structural sections to generate
DOMAIN_STRUCTURAL_SECTIONS = {
    "security": ["constraints"],
    "feature": ["constraints", "dependencies", "non_goals"],
    "architecture": ["constraints"],
    "design": ["constraints"],
    "engineering": ["constraints"],
    "external-context": ["constraints", "dependencies"],
    "feature-design": ["constraints", "non_goals"],
    "feature-technical": [
        "external-dependencies",
        "runtime-constraints",
        "architectural-constraints",
        "security-considerations",
        "performance-considerations",
        "extension-points",
    ],
    "prototype": ["constraints"],
}


# ---------------------------------------------------------------------------
# Section injection
# ---------------------------------------------------------------------------

def inject_section(
    doc_content: str,
    section_name: str,
    generated_content: str,
) -> str:
    """Replace a section in a document with generated content.

    Finds the heading matching section_name and replaces content
    until the next heading of the same or higher level.
    """
    lines = doc_content.split("\n")
    result: list[str] = []
    in_section = False
    section_heading_level = 0

    # Normalize section name for matching
    normalized = section_name.replace("_", "-").lower()

    for line in lines:
        stripped = line.strip()

        # Detect section heading
        if stripped.lower().startswith("## "):
            heading_text = stripped[3:].strip().lower()
            # Match section name (e.g., "07-constraints" or "constraints")
            if normalized in heading_text or heading_text.endswith(normalized):
                in_section = True
                section_heading_level = len(line) - len(line.lstrip())
                result.append(line)
                result.append("")
                result.append(generated_content.rstrip())
                result.append("")
                continue

        # If in section, skip until next heading at same or higher level
        if in_section:
            if stripped.startswith("#"):
                current_level = len(line) - len(line.lstrip())
                if current_level <= section_heading_level:
                    in_section = False
                    result.append(line)
            continue

        result.append(line)

    return "\n".join(result)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate structural section skeletons")
    parser.add_argument("--system-root", required=True, help="Path to base_dev system directory")
    parser.add_argument("--domain", help="Single domain to generate")
    parser.add_argument("--section", help="Single section to generate (domain required)")
    parser.add_argument("--all", action="store_true", help="Generate for all domains")
    parser.add_argument("--out", help="Output file path (single section mode)")
    parser.add_argument("--out-dir", help="Output directory (all-domains mode)")
    parser.add_argument("--doc", help="Existing document to inject into (optional)")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    tier_data = load_tiers(system_root)

    if args.all:
        out_dir = Path(args.out_dir) if args.out_dir else system_root / "test_structural"
        out_dir.mkdir(parents=True, exist_ok=True)

        generated = 0
        for domain, sections in sorted(DOMAIN_STRUCTURAL_SECTIONS.items()):
            prefixed = resolve_domain(domain)
            relationships = load_relationships(system_root, domain)

            for section_name in sections:
                generator = SECTION_GENERATORS.get(section_name)
                if not generator:
                    continue

                content = generator(domain, relationships, tier_data)
                out_path = out_dir / f"{prefixed}-{section_name}.md"
                write_text(out_path, content)
                generated += 1
                print(f"  Generated: {prefixed}-{section_name}.md")

        print(f"\n{generated} structural sections generated to {out_dir}")

    elif args.domain and args.section:
        relationships = load_relationships(system_root, args.domain)
        generator = SECTION_GENERATORS.get(args.section)
        if not generator:
            print(f"Unknown section: {args.section}")
            print(f"Available: {', '.join(SECTION_GENERATORS.keys())}")
            sys.exit(1)

        content = generator(args.domain, relationships, tier_data)

        if args.doc:
            doc_path = Path(args.doc)
            doc_content = doc_path.read_text(encoding="utf-8")
            updated = inject_section(doc_content, args.section, content)
            write_text(doc_path, updated)
            print(f"Injected {args.section} into {doc_path}")
        elif args.out:
            write_text(Path(args.out), content)
            print(f"Written to {args.out}")
        else:
            print(content)

    else:
        parser.error("Must specify --all or --domain + --section")


if __name__ == "__main__":
    main()
