"""evaluate_rules.py — Evaluates deterministic audit rules against document content.

Reads audit/deterministic/{document,section}/{domain}.yaml rule definitions,
dispatches on evidence.type, checks the actual document, and produces
{id, weight, mandatory, passed, evidence} per rule. This is the evaluator
that bridges between raw rule definitions and calculate.py's formulas (§20).

Usage:
  python evaluate_rules.py --system-root <path> --domain <path> --doc <path> --out <path>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_json, utc_now_iso, resolve_domain


# ---------------------------------------------------------------------------
# Technology keyword lists for keyword_absence checks
# ---------------------------------------------------------------------------

TECH_KEYWORDS: dict[str, list[str]] = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c\\+\\+", "rust",
        "golang", "ruby", "php", "swift", "kotlin", "scala", "haskell",
        "clojure", "elixir", "perl", "r\\b", "matlab", "fortran", "cobol",
        "c#", "objective-c", "dart", "lua", "perl", "racket",
    ],
    "frameworks": [
        "react", "vue", "angular", "svelte", "next\\.js", "nuxt",
        "django", "flask", "fastapi", "spring", "rails", "laravel",
        "express", "nestjs", "ember", "backbone", "jquery",
        "tensorflow", "pytorch", "keras", "scikit-learn",
    ],
    "libraries": [
        "numpy", "pandas", "matplotlib", "requests", "axios",
        "lodash", "moment", "webpack", "babel", "eslint",
        "pytest", "jest", "mocha", "cypress", "selenium",
    ],
    "database_schemas": [
        "postgres", "mysql", "mongodb", "redis", "elasticsearch",
        "sqlite", "cassandra", "dynamodb", "cosmos",
        "sql\\s+table", "database\\s+schema", "migration",
    ],
    "protocols": [
        "grpc", "graphql", "rest\\s+api", "websocket", "mqtt",
        "amqp", "thrift", "protobuf", "avro",
    ],
}


# ---------------------------------------------------------------------------
# Document section parsing
# ---------------------------------------------------------------------------

def parse_document_sections(content: str) -> dict[str, str]:
    """Parse markdown into {heading: body_content} mapping.

    Extracts ## level headings and their content until the next ## heading.
    Also records the heading text in lowercase for semantic type matching.
    """
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in content.split("\n"):
        heading_match = re.match(r"^##\s+(.+)$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def build_heading_to_semantic_type(system_root: Path, domain: str) -> dict[str, str]:
    """Map section template filenames to semantic_type values.

    Reads templates/generation/section/{domain}/ to build a mapping
    like {"01-purpose.md": "purpose", "02-vision_statement.md": "vision_statement"}.
    """
    section_dir = system_root / "templates" / "generation" / "section" / domain
    mapping: dict[str, str] = {}

    if not section_dir.is_dir():
        return mapping

    for sec_file in sorted(section_dir.glob("*.md")):
        # Extract the semantic type from the filename
        # e.g. "01-purpose.md" -> "purpose", "02-vision_statement.md" -> "vision_statement"
        stem = sec_file.stem
        # Remove leading number prefix
        name_part = re.sub(r"^\d+[-_]", "", stem)
        # Normalize: replace underscores with hyphens for matching
        semantic_type = name_part.replace("_", "-")
        mapping[stem] = semantic_type

    return mapping


def find_sections_by_semantic_type(
    sections: dict[str, str],
    heading_to_type: dict[str, str],
    semantic_type: str,
) -> list[str]:
    """Find section contents matching a given semantic_type."""
    results: list[str] = []
    for heading, content in sections.items():
        # Check if any template maps to this semantic_type
        for template_name, stype in heading_to_type.items():
            if stype == semantic_type:
                # Check if heading contains the template's title words
                template_words = set(
                    w.lower() for w in re.split(r"[-_\s]+", template_name)
                    if w and not w.isdigit()
                )
                heading_words = set(
                    w.lower() for w in re.split(r"[-_\s]+", heading)
                    if w and not w.isdigit()
                )
                if template_words & heading_words:
                    results.append(content)
                    break
    return results


# ---------------------------------------------------------------------------
# Evidence type evaluators
# ---------------------------------------------------------------------------

def eval_section_presence(
    rule: dict,
    sections: dict[str, str],
    heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check if required sections exist in the document."""
    evidence = rule.get("evidence", {})

    # Check by required_semantic_types (document-level)
    required_types = evidence.get("required_semantic_types", [])
    if required_types:
        found_types: set[str] = set()
        for heading, content in sections.items():
            for template_name, stype in heading_to_type.items():
                if stype in required_types:
                    template_words = set(
                        w.lower() for w in re.split(r"[-_\s]+", template_name)
                        if w and not w.isdigit()
                    )
                    heading_words = set(
                        w.lower() for w in re.split(r"[-_\s]+", heading)
                        if w and not w.isdigit()
                    )
                    if template_words & heading_words:
                        found_types.add(stype)

        missing = [t for t in required_types if t not in found_types]
        if missing:
            return False, f"Missing sections: {', '.join(missing)}"
        return True, f"All {len(required_types)} required sections present"

    # Check by single semantic_type (section-level)
    semantic_type = evidence.get("semantic_type")
    if semantic_type:
        matching = find_sections_by_semantic_type(sections, heading_to_type, semantic_type)
        if not matching:
            return False, f"Missing required section: {semantic_type}"
        return True, f"Section '{semantic_type}' found"

    return True, "No section_presence criteria to check"


def eval_section_content(
    rule: dict,
    sections: dict[str, str],
    heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check if sections have non-empty content."""
    evidence = rule.get("evidence", {})
    check = evidence.get("check", "non_empty")

    if check == "non_empty":
        empty_sections: list[str] = []
        for heading, content in sections.items():
            # Skip non-content sections (title, upstream context, etc.)
            if heading.lower() in ("upstream context",):
                continue
            stripped = content.strip()
            # Consider empty if only contains TODO markers or is blank
            if not stripped or stripped.startswith("<!-- TODO:"):
                empty_sections.append(heading)

        if empty_sections:
            return False, f"{len(empty_sections)} section(s) empty: {', '.join(empty_sections[:5])}"
        return True, f"All {len(sections)} sections have content"

    return True, f"Unknown content check type: {check}"


def eval_content_check(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check if document content contains expected keywords or patterns."""
    evidence = rule.get("evidence", {})
    all_content = "\n".join(sections.values()).lower()

    keywords = evidence.get("keywords", [])
    patterns = evidence.get("patterns", [])

    if keywords:
        found = [kw for kw in keywords if kw.lower() in all_content]
        if not found:
            return False, f"None of the expected keywords found: {keywords}"
        return True, f"Found {len(found)}/{len(keywords)} expected keywords"

    if patterns:
        found = [p for p in patterns if re.search(p, all_content, re.IGNORECASE)]
        if not found:
            return False, f"None of the expected patterns found: {patterns}"
        return True, f"Found {len(found)}/{len(patterns)} expected patterns"

    return True, "No content_check criteria"


def eval_keyword_absence(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check that forbidden technology keywords are absent from the document."""
    evidence = rule.get("evidence", {})
    all_content = "\n".join(sections.values()).lower()

    # Check by categories
    categories = evidence.get("categories", [])
    if categories:
        violations: list[str] = []
        for cat in categories:
            keywords = TECH_KEYWORDS.get(cat, [])
            for kw in keywords:
                if re.search(rf"\b{kw}\b", all_content):
                    violations.append(f"{cat}: '{kw}'")
        if violations:
            return False, f"Technology references found: {'; '.join(violations[:5])}"
        return True, "No technology references found"

    # Check by explicit keywords
    keywords = evidence.get("keywords", [])
    if keywords:
        found = [kw for kw in keywords if kw.lower() in all_content]
        if found:
            return False, f"Forbidden keywords found: {', '.join(found[:5])}"
        return True, "No forbidden keywords found"

    return True, "No keyword_absence criteria"


def eval_relationship_absence(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check that forbidden relationship directions are absent."""
    # This is a structural check — for standalone docs, relationships are
    # expressed as cross-references (## Related, ## Traceability sections).
    # A forbidden direction means the doc should NOT claim derives_from, etc.
    evidence = rule.get("evidence", {})
    forbidden = evidence.get("forbidden_direction", "")

    # Check traceability/related sections for forbidden patterns
    trace_content = ""
    for heading, content in sections.items():
        if any(kw in heading.lower() for kw in ("traceability", "related", "derivation")):
            trace_content += content.lower()

    if forbidden and forbidden.replace("_", " ") in trace_content:
        return False, f"Forbidden relationship direction found: {forbidden}"
    return True, f"No forbidden relationship direction: {forbidden}"


def eval_cross_reference(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check for expected cross-references to other domains."""
    evidence = rule.get("evidence", {})
    expected = evidence.get("expected", [])

    all_content = "\n".join(sections.values()).lower()

    missing: list[str] = []
    found: list[str] = []
    for ref in expected:
        domain = ref.get("domain", "")
        # Check if domain name appears in the document
        if domain.lower() in all_content:
            found.append(domain)
        else:
            missing.append(domain)

    if missing and expected:
        return False, f"Missing cross-references to: {', '.join(missing)}"
    return True, f"Cross-references present: {', '.join(found) if found else 'none expected'}"


def eval_heading_analysis(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Analyze headings for single-concern focus."""
    evidence = rule.get("evidence", {})
    check = evidence.get("check", "single_concern")

    if check == "single_concern":
        # A simple heuristic: if the document has too many top-level sections
        # with unrelated topic words, it may cover multiple concerns
        content_headings = [
            h for h in sections.keys()
            if h.lower() not in ("upstream context", "related", "traceability")
        ]
        if len(content_headings) <= 12:
            return True, f"Single concern (document has {len(content_headings)} content sections)"
        return True, f"Unclear ({len(content_headings)} sections — manual review recommended)"

    return True, f"Unknown heading_analysis check: {check}"


def eval_content_deduplication(
    rule: dict,
    sections: dict[str, str],
    _heading_to_type: dict[str, str],
) -> tuple[bool, str]:
    """Check for duplicate content within the document."""
    evidence = rule.get("evidence", {})
    scope = evidence.get("scope", "within_document")

    if scope == "within_document":
        # Simple dedup: check for repeated sentences across sections
        all_sentences: list[str] = []
        duplicates: list[str] = []
        for heading, content in sections.items():
            for sentence in re.split(r"[.!?]+", content):
                s = sentence.strip().lower()
                if len(s) > 30:  # Only check meaningful sentences
                    if s in all_sentences:
                        duplicates.append(s[:60])
                    all_sentences.append(s)

        if duplicates:
            return False, f"{len(duplicates)} duplicate sentence(s) found"
        return True, "No duplicate content detected"

    return True, f"Unknown dedup scope: {scope}"


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

EVIDENCE_EVALUATORS: dict[str, Any] = {
    "section_presence": eval_section_presence,
    "section_content": eval_section_content,
    "content_check": eval_content_check,
    "keyword_absence": eval_keyword_absence,
    "relationship_absence": eval_relationship_absence,
    "cross_reference": eval_cross_reference,
    "heading_analysis": eval_heading_analysis,
    "content_deduplication": eval_content_deduplication,
}


# ---------------------------------------------------------------------------
# Main evaluator
# ---------------------------------------------------------------------------

def evaluate_rules(
    system_root: Path,
    domain: str,
    doc_content: str,
) -> dict[str, Any]:
    """Evaluate all deterministic rules for a domain against a document.

    Returns a dict with document-level and section-level evaluated rules,
    each with {id, weight, mandatory, passed, evidence} fields.
    """
    audit_root = system_root / "audit"
    sections = parse_document_sections(doc_content)
    heading_to_type = build_heading_to_semantic_type(system_root, domain)

    # --- Document-level rules ---
    prefixed_domain = resolve_domain(domain)
    det_doc_path = audit_root / "deterministic" / "document" / f"{prefixed_domain}.yaml"
    det_doc_rules: list[dict] = []
    if det_doc_path.exists():
        data = load_yaml(det_doc_path)
        det_doc_rules = data.get("rules", [])

    evaluated_doc_rules: list[dict] = []
    for rule in det_doc_rules:
        evidence_type = rule.get("evidence", {}).get("type", "")
        evaluator = EVIDENCE_EVALUATORS.get(evidence_type)

        if evaluator:
            passed, message = evaluator(rule, sections, heading_to_type)
        else:
            # Unknown evidence type — pass by default (don't penalize)
            passed = True
            message = f"Unknown evidence type: {evidence_type} — passed by default"

        evaluated_doc_rules.append({
            "id": rule["id"],
            "description": rule.get("description", ""),
            "weight": rule.get("weight", 1.0),
            "mandatory": rule.get("mandatory", False),
            "severity": rule.get("severity", "warning"),
            "passed": passed,
            "evidence": {
                "type": evidence_type,
                "message": message,
            },
        })

    # --- Section-level rules ---
    det_sec_dir = audit_root / "deterministic" / "section" / prefixed_domain
    evaluated_sec_rules: dict[str, list[dict]] = {}

    if det_sec_dir.is_dir():
        for yaml_file in sorted(det_sec_dir.glob("*.yaml")):
            data = load_yaml(yaml_file)
            section_rules = data.get("rules", [])
            section_name = yaml_file.stem

            evaluated_sec: list[dict] = []
            for rule in section_rules:
                evidence_type = rule.get("evidence", {}).get("type", "")
                evaluator = EVIDENCE_EVALUATORS.get(evidence_type)

                if evaluator:
                    passed, message = evaluator(rule, sections, heading_to_type)
                else:
                    passed = True
                    message = f"Unknown evidence type: {evidence_type} — passed by default"

                evaluated_sec.append({
                    "id": rule["id"],
                    "description": rule.get("description", ""),
                    "weight": rule.get("weight", 1.0),
                    "mandatory": rule.get("mandatory", False),
                    "severity": rule.get("severity", "warning"),
                    "passed": passed,
                    "evidence": {
                        "type": evidence_type,
                        "message": message,
                    },
                })

            evaluated_sec_rules[section_name] = evaluated_sec

    return {
        "domain": domain,
        "evaluated_at": utc_now_iso(),
        "doc_rules": evaluated_doc_rules,
        "sec_rules": evaluated_sec_rules,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate deterministic audit rules against a document"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--doc", required=True, help="Path to the document to evaluate")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    doc_path = Path(args.doc)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)
    if not doc_path.is_file():
        print(f"Error: document not found: {doc_path}", file=sys.stderr)
        sys.exit(1)

    doc_content = doc_path.read_text(encoding="utf-8")
    result = evaluate_rules(system_root, args.domain, doc_content)

    write_json(Path(args.out), result)

    # Summary
    doc_total = len(result["doc_rules"])
    doc_passed = sum(1 for r in result["doc_rules"] if r["passed"])
    sec_total = sum(len(rules) for rules in result["sec_rules"].values())
    sec_passed = sum(
        sum(1 for r in rules if r["passed"])
        for rules in result["sec_rules"].values()
    )
    print(f"Document rules: {doc_passed}/{doc_total} passed")
    print(f"Section rules: {sec_passed}/{sec_total} passed")
    print(f"Total: {doc_passed + sec_passed}/{doc_total + sec_total} passed")


if __name__ == "__main__":
    main()
