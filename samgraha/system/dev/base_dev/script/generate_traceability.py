"""generate_traceability.py — Generates traceability sections from relationship data.

Reads tiers.yaml for tier assignments and {NN}-*-relationships.yaml for
traceable_to edges. Generates the tier diagram, upstream/downstream lists,
and non-contradiction rule for each domain's traceability section.

Fully deterministic — no LLM, no external input needed.

Usage:
  python generate_traceability.py --system-root <path> --domain <domain> --out <path>
  python generate_traceability.py --system-root <path> --all --out-dir <path>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_text, resolve_domain, DOMAIN_PREFIX, DOMAIN_NUMS


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tiers(system_root: Path) -> dict[str, Any]:
    """Load tiers.yaml and build lookup structures."""
    tiers_path = system_root / "plan" / "core" / "tiers.yaml"
    data = load_yaml(tiers_path)

    # Build domain -> tier mapping
    domain_tier: dict[str, int] = {}
    for tier_def in data.get("tiers", []):
        tier_num = tier_def["tier"]
        for domain in tier_def.get("domains", []):
            domain_tier[domain] = tier_num

    # Build tier-level relationships
    relationships = data.get("relationships", [])

    return {
        "domain_tier": domain_tier,
        "relationships": relationships,
    }


def load_relationships(system_root: Path, domain: str) -> list[dict]:
    """Load {NN}-*-relationships.yaml for a domain."""
    prefixed = resolve_domain(domain)
    rel_path = system_root / "audit" / "deterministic" / "document" / f"{prefixed}-relationships.yaml"
    if not rel_path.exists():
        return []
    data = load_yaml(rel_path)
    return data.get("relationships", [])


# ---------------------------------------------------------------------------
# Traceability generation
# ---------------------------------------------------------------------------

def get上下游_edges(
    domain: str,
    tier_data: dict[str, Any],
    section_relationships: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Get upstream and downstream edges for a domain's traceability section.

    Returns (upstream, downstream) where each is a list of
    {target_domain, target_section, relationship_type} dicts.
    """
    domain_tier = tier_data["domain_tier"]
    tier_relationships = tier_data["relationships"]
    my_tier = domain_tier.get(domain, 99)

    upstream: list[dict] = []
    downstream: list[dict] = []

    # From section-level traceable_to edges
    for rel in section_relationships:
        if rel.get("from_section") != "traceability":
            continue
        if rel.get("type") != "traceable_to":
            continue

        target_domain = rel.get("target_domain")
        target_section = rel.get("target_section")

        if target_domain is None or target_domain == "null":
            continue  # Skip null entries (no upstream)

        target_tier = domain_tier.get(target_domain, 99)

        edge = {
            "target_domain": target_domain,
            "target_section": target_section or "purpose",
            "relationship_type": "derives_from",
        }

        if target_tier < my_tier:
            upstream.append(edge)
        else:
            downstream.append(edge)

    # From tier-level relationships (supplement section-level)
    seen_pairs: set[tuple[str, str]] = set()
    for edge in upstream + downstream:
        seen_pairs.add((edge["target_domain"], edge["target_section"]))

    # Relationship types that mean "this domain derives from the source"
    DERIVES_TYPES = {"derives", "inspires", "guides", "validates", "requires"}
    # References are citations, not derivation — don't list as upstream
    REFERENCES_TYPES = {"references", "soft_aligns_with", "informs"}

    for rel in tier_relationships:
        from_domain = rel["from"]
        to_domain = rel["to"]
        rel_type = rel.get("type", "derives")

        if rel_type in REFERENCES_TYPES:
            continue  # Skip references/informs/soft_aligns — not derivation edges

        if from_domain == domain:
            # domain -> to_domain: to_domain is downstream
            pair = (to_domain, "purpose")
            if pair not in seen_pairs:
                downstream.append({
                    "target_domain": to_domain,
                    "target_section": "purpose",
                    "relationship_type": rel_type,
                })
                seen_pairs.add(pair)
        elif to_domain == domain:
            # from_domain -> domain: from_domain is upstream
            pair = (from_domain, "purpose")
            if pair not in seen_pairs:
                upstream.append({
                    "target_domain": from_domain,
                    "target_section": "purpose",
                    "relationship_type": rel_type,
                })
                seen_pairs.add(pair)

    return upstream, downstream


def format_tier_name(domain: str) -> str:
    """Format domain name for display in tier diagrams."""
    return domain.replace("-", " ").title()


def generate_traceability_section(
    domain: str,
    tier_data: dict[str, Any],
    section_relationships: list[dict],
) -> str:
    """Generate the full traceability section content for a domain."""
    domain_tier = tier_data["domain_tier"]
    my_tier = domain_tier.get(domain, 99)

    upstream, downstream = get上下游_edges(domain, tier_data, section_relationships)

    lines: list[str] = []

    # --- Tier derivation diagram ---
    lines.append("## Derivation Chain")
    lines.append("")

    # Build the diagram
    # Find all ancestors and descendants
    all_domains = set(domain_tier.keys())

    # Collect all related domains (upstream + downstream), deduplicated
    ancestors = list(dict.fromkeys(e["target_domain"] for e in upstream))
    descendants = list(dict.fromkeys(e["target_domain"] for e in downstream))

    # Group by tier
    tier_groups: dict[int, list[str]] = {}
    seen_domains: set[str] = set()
    for d in ancestors + [domain] + descendants:
        if d in seen_domains:
            continue
        seen_domains.add(d)
        t = domain_tier.get(d, 99)
        tier_groups.setdefault(t, []).append(d)

    # Build ASCII diagram — simple linear chain
    sorted_tiers = sorted(tier_groups.keys())
    for i, tier_num in enumerate(sorted_tiers):
        domains_in_tier = sorted(tier_groups[tier_num])
        # Put current domain first in its tier
        if domain in domains_in_tier:
            domains_in_tier.remove(domain)
            domains_in_tier.insert(0, domain)

        is_last = i == len(sorted_tiers) - 1
        connector = "+--" if is_last else "+--"
        cont = "    " if is_last else "|   "

        for j, d in enumerate(domains_in_tier):
            label = format_tier_name(d)
            if d == domain:
                label = f"{label} (current)"
            tier_label = f"Tier {tier_num}"

            if j == 0 and i == 0:
                lines.append(f"{connector} {tier_label}: {label}")
            elif j == 0:
                lines.append(f"|{cont}{connector} {tier_label}: {label}")
            else:
                lines.append(f"|{cont}    {tier_label}: {label}")

    lines.append("")

    # --- Upstream derivation ---
    if upstream:
        lines.append("## Upstream Derivation")
        lines.append("")
        lines.append("This document derives from the following upstream standards:")
        lines.append("")
        # Deduplicate by domain, keeping the most specific section
        seen_upstream: dict[str, dict] = {}
        for edge in upstream:
            d = edge["target_domain"]
            if d not in seen_upstream:
                seen_upstream[d] = edge
            elif edge["target_section"] != "purpose":
                # Prefer specific section over generic "purpose"
                seen_upstream[d] = edge
        for edge in sorted(seen_upstream.values(), key=lambda e: (domain_tier.get(e["target_domain"], 99), e["target_domain"])):
            target = edge["target_domain"]
            section = edge["target_section"]
            rel_type = edge.get("relationship_type", "derives_from")
            tier_num = domain_tier.get(target, "?")
            label = format_tier_name(target)
            section_label = section.replace("_", " ").title()
            lines.append(f"- **{label}** (Tier {tier_num}) / {section_label} -- `{rel_type}`")
        lines.append("")

    # --- Downstream consumers ---
    if downstream:
        lines.append("## Downstream Consumers")
        lines.append("")
        lines.append("The following standards derive from or reference this document:")
        lines.append("")
        # Deduplicate by domain
        seen_downstream: dict[str, dict] = {}
        for edge in downstream:
            d = edge["target_domain"]
            if d not in seen_downstream:
                seen_downstream[d] = edge
            elif edge["target_section"] != "purpose":
                seen_downstream[d] = edge
        for edge in sorted(seen_downstream.values(), key=lambda e: (domain_tier.get(e["target_domain"], 99), e["target_domain"])):
            target = edge["target_domain"]
            section = edge["target_section"]
            rel_type = edge.get("relationship_type", "derives")
            tier_num = domain_tier.get(target, "?")
            label = format_tier_name(target)
            section_label = section.replace("_", " ").title()
            lines.append(f"- **{label}** (Tier {tier_num}) / {section_label} -- `{rel_type}`")
        lines.append("")

    # --- Non-contradiction rule ---
    lines.append("## Non-Contradiction Rule")
    lines.append("")
    if downstream:
        consumer_names = [format_tier_name(e["target_domain"]) for e in downstream]
        if len(consumer_names) == 1:
            consumers_str = consumer_names[0]
        elif len(consumer_names) == 2:
            consumers_str = f"{consumer_names[0]} and {consumer_names[1]}"
        else:
            consumers_str = ", ".join(consumer_names[:-1]) + f", and {consumer_names[-1]}"
        lines.append(
            f"No downstream document ({consumers_str}) may state a goal, constraint, "
            f"or priority that contradicts the {format_tier_name(domain)}. "
            f"When conflicts arise, the {format_tier_name(domain)} takes precedence."
        )
    else:
        lines.append(
            f"The {format_tier_name(domain)} is a terminal document — no downstream "
            f"standards derive from it. This section documents traceability for reference only."
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section injection into document
# ---------------------------------------------------------------------------

def inject_traceability(
    doc_content: str,
    traceability_content: str,
) -> str:
    """Replace the traceability section in a document with generated content.

    Finds the traceability heading and replaces everything under it
    until the next heading of the same or higher level.
    """
    lines = doc_content.split("\n")
    result: list[str] = []
    in_traceability = False
    traceability_heading_level = 0

    for line in lines:
        stripped = line.strip()

        # Detect traceability heading (## N. Traceability or ## Traceability)
        if stripped.lower().startswith("## ") and "traceability" in stripped.lower():
            in_traceability = True
            traceability_heading_level = len(line) - len(line.lstrip())
            result.append(line)
            result.append("")
            result.append(traceability_content.rstrip())
            result.append("")
            continue

        # If we're in traceability, skip lines until next heading at same or higher level
        if in_traceability:
            if stripped.startswith("#"):
                current_level = len(line) - len(line.lstrip())
                if current_level <= traceability_heading_level:
                    in_traceability = False
                    result.append(line)
            continue

        result.append(line)

    return "\n".join(result)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def generate_traceability_for_domain(
    domain: str,
    tier_data: dict[str, Any],
    relationships: list[dict],
) -> str:
    """Public API: generate traceability section for a domain."""
    return generate_traceability_section(domain, tier_data, relationships)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate traceability sections from relationship data")
    parser.add_argument("--system-root", required=True, help="Path to base_dev system directory")
    parser.add_argument("--domain", help="Single domain to generate (e.g. vision)")
    parser.add_argument("--all", action="store_true", help="Generate for all domains")
    parser.add_argument("--out", help="Output file path (single domain mode)")
    parser.add_argument("--out-dir", help="Output directory (all-domains mode)")
    parser.add_argument("--doc", help="Existing document to inject into (optional)")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    tier_data = load_tiers(system_root)

    if args.all:
        out_dir = Path(args.out_dir) if args.out_dir else system_root / "test_traceability"
        out_dir.mkdir(parents=True, exist_ok=True)

        generated = 0
        for domain in sorted(DOMAIN_PREFIX.keys()):
            prefixed = resolve_domain(domain)
            section_rels = load_relationships(system_root, domain)

            # Check if this domain has a traceability section
            has_traceability = any(
                r.get("from_section") == "traceability"
                for r in section_rels
            )
            if not has_traceability:
                continue

            content = generate_traceability_section(domain, tier_data, section_rels)
            out_path = out_dir / f"{prefixed}-traceability.md"
            write_text(out_path, content)
            generated += 1
            print(f"  Generated: {prefixed}-traceability.md")

        print(f"\n{generated} traceability sections generated to {out_dir}")

    elif args.domain:
        section_rels = load_relationships(system_root, args.domain)
        content = generate_traceability_section(args.domain, tier_data, section_rels)

        if args.doc:
            # Inject into existing document
            doc_path = Path(args.doc)
            doc_content = doc_path.read_text(encoding="utf-8")
            updated = inject_traceability(doc_content, content)
            write_text(doc_path, updated)
            print(f"Injected traceability into {doc_path}")
        elif args.out:
            write_text(Path(args.out), content)
            print(f"Written to {args.out}")
        else:
            print(content)

    else:
        parser.error("Must specify --domain or --all")


if __name__ == "__main__":
    main()
