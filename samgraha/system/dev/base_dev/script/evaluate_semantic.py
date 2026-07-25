"""evaluate_semantic.py — Heuristic semantic audit evaluator (§20).

Reads audit/semantic/{document,section}/{domain}.md rubric files, parses
scoring criteria, and produces heuristic pass/fail judgments for each criterion
based on document content analysis. This is a deterministic heuristic — real
LLM-based semantic evaluation would be a separate, future enhancement.

Usage:
  python evaluate_semantic.py --system-root <path> --domain <domain> --doc <path> --out <path>
  python evaluate_semantic.py --system-root <path> --domain <domain> --doc <path> --out <path> --context <path>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from _common import load_yaml, write_json, utc_now_iso, resolve_domain


# ---------------------------------------------------------------------------
# Rubric parsing
# ---------------------------------------------------------------------------

def parse_semantic_rubric(content: str) -> dict[str, Any]:
    """Parse a semantic audit markdown file into structured data.

    Returns dict with keys: engineering_intent, audit_objectives,
    red_flags, scoring_criteria (list of {id, weight, score, description}).
    """
    result: dict[str, Any] = {
        "engineering_intent": "",
        "audit_objectives": "",
        "red_flags": "",
        "scoring_criteria": [],
    }

    current_section: str | None = None
    in_table = False
    table_lines: list[str] = []

    for line in content.split("\n"):
        # Detect section headers
        if line.startswith("## "):
            section_name = line[3:].strip().lower().replace(" ", "_")
            current_section = section_name
            in_table = False
            continue

        # Parse scoring criteria table
        if current_section == "scoring_criteria":
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
                        score_parts = cols[2].split("or")
                        max_score = int(score_parts[-1].strip()) if score_parts[-1].strip().isdigit() else 0
                    except (ValueError, IndexError):
                        max_score = 0
                    result["scoring_criteria"].append({
                        "criterion_id": cols[0],
                        "mandatory": mandatory,
                        "max_score": max_score,
                        "description": cols[3] if len(cols) > 3 else "",
                    })
            elif in_table and not line.strip().startswith("|"):
                in_table = False
            continue

        # Collect section content
        if current_section and not in_table:
            if current_section in result and isinstance(result[current_section], str):
                result[current_section] += line + "\n"
            elif current_section in result:
                pass  # Already initialized
            else:
                result[current_section] = line + "\n"

    return result


# ---------------------------------------------------------------------------
# Heuristic evaluation
# ---------------------------------------------------------------------------

def _count_words(text: str) -> int:
    """Count non-trivial words in text."""
    return len([w for w in text.split() if len(w) > 2])


def _has_substantial_content(sections: dict[str, str], min_words: int = 50) -> bool:
    """Check if the document has substantial content (not just headings/TODOs)."""
    total_words = 0
    for heading, content in sections.items():
        if heading.lower() in ("upstream context",):
            continue
        # Remove TODO markers
        clean = re.sub(r"<!--.*?-->", "", content)
        total_words += _count_words(clean)
    return total_words >= min_words


def _check_section_quality(
    section_content: str,
    rubric_objectives: str,
    expected_keywords: list[str],
) -> tuple[bool, float, str]:
    """Check if a section's content aligns with rubric objectives.

    Returns (passed, confidence, evidence_message).
    """
    clean = re.sub(r"<!--.*?-->", "", section_content).strip()
    word_count = _count_words(clean)

    if word_count < 5:
        return False, 0.9, "Section is empty or contains only TODO markers"

    # Check for expected keywords from rubric objectives
    content_lower = clean.lower()
    keyword_hits = sum(1 for kw in expected_keywords if kw.lower() in content_lower)
    keyword_ratio = keyword_hits / max(len(expected_keywords), 1)

    # Check for TODO markers (indicates unfilled content)
    todo_count = len(re.findall(r"<!--\s*TODO", section_content))
    if todo_count > 0:
        return False, 0.8, f"Section contains {todo_count} TODO marker(s)"

    # Heuristic: section passes if it has content and some keyword alignment
    if word_count >= 20 and keyword_ratio > 0.2:
        return True, min(0.7, 0.5 + keyword_ratio * 0.3), f"Content present ({word_count} words, {keyword_hits}/{len(expected_keywords)} keyword matches)"
    elif word_count >= 10:
        return True, 0.5, f"Minimal content ({word_count} words) — confidence low"
    else:
        return False, 0.7, f"Insufficient content ({word_count} words)"


def evaluate_semantic_document(
    system_root: Path,
    domain: str,
    doc_content: str,
    context: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Evaluate semantic criteria for a whole document using heuristics.

    Returns evaluated criteria with {criterion_id, passed, score, confidence, evidence}.
    """
    audit_root = system_root / "audit"
    sem_doc_path = audit_root / "semantic" / "document" / f"{resolve_domain(domain)}.md"

    if not sem_doc_path.exists():
        return {
            "domain": domain,
            "scope": "document",
            "evaluated_at": utc_now_iso(),
            "criteria": [],
            "note": f"No semantic audit file found: {sem_doc_path}",
        }

    rubric_content = sem_doc_path.read_text(encoding="utf-8")
    rubric = parse_semantic_rubric(rubric_content)

    # Parse document sections
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in doc_content.split("\n"):
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

    # Extract keywords from rubric objectives for heuristic matching
    objective_text = (rubric.get("engineering_intent", "") +
                     rubric.get("audit_objectives", "") +
                     rubric.get("expected_quality", ""))
    # Extract meaningful words (3+ chars, not common stopwords)
    stopwords = {"the", "and", "for", "that", "this", "with", "from", "are",
                 "was", "not", "but", "has", "have", "can", "should", "must",
                 "shall", "may", "will", "each", "every", "any", "all", "its",
                 "their", "they", "them", "there", "then", "than", "when",
                 "what", "which", "who", "whom", "how", "where", "why", "being"}
    objective_words = [
        w.lower() for w in re.split(r"[\s,.!?;:()]+", objective_text)
        if len(w) >= 3 and w.lower() not in stopwords
    ]
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_keywords: list[str] = []
    for w in objective_words:
        if w not in seen:
            seen.add(w)
            unique_keywords.append(w)

    # Evaluate each criterion
    evaluated_criteria: list[dict] = []
    for criterion in rubric.get("scoring_criteria", []):
        criterion_id = criterion["criterion_id"]
        max_score = criterion["max_score"]
        mandatory = criterion["mandatory"]

        # Use the criterion description + rubric objectives as keywords
        desc_words = [
            w.lower() for w in re.split(r"[\s,.!?;:()]+", criterion["description"])
            if len(w) >= 3 and w.lower() not in stopwords
        ]
        # Combine rubric-level and criterion-specific keywords
        combined_keywords = unique_keywords[:10] + desc_words[:5]

        # Heuristic: check document quality against this criterion
        has_content = _has_substantial_content(sections)
        if not has_content:
            passed = False
            confidence = 0.9
            evidence_msg = "Document has no substantial content"
        else:
            # Check if any section's content aligns with this criterion
            best_result = (False, 0.0, "No matching sections found")
            for heading, content in sections.items():
                if heading.lower() in ("upstream context",):
                    continue
                p, c, msg = _check_section_quality(content, objective_text, combined_keywords)
                if c > best_result[1]:
                    best_result = (p, c, msg)
            passed, confidence, evidence_msg = best_result

        # Adjust confidence based on mandatory status
        if not passed and mandatory:
            confidence = max(confidence, 0.7)  # Mandatory failures are high confidence

        # Compute score
        score = max_score if passed else 0

        evaluated_criteria.append({
            "criterion_id": criterion_id,
            "passed": passed,
            "score": score,
            "max_score": max_score,
            "mandatory": mandatory,
            "confidence": round(confidence, 2),
            "evidence": {
                "message": evidence_msg,
            },
            "description": criterion["description"],
        })

    return {
        "domain": domain,
        "scope": "document",
        "evaluated_at": utc_now_iso(),
        "criteria": evaluated_criteria,
        "rubric_summary": {
            "engineering_intent": rubric.get("engineering_intent", "")[:200],
            "total_criteria": len(rubric.get("scoring_criteria", [])),
        },
    }


def evaluate_semantic_section(
    system_root: Path,
    domain: str,
    section_name: str,
    section_content: str,
) -> dict[str, Any]:
    """Evaluate semantic criteria for a single section using heuristics."""
    audit_root = system_root / "audit"
    sem_sec_dir = audit_root / "semantic" / "section" / resolve_domain(domain)
    sem_sec_file = sem_sec_dir / section_name / f"{section_name}.md"

    # Also try flat structure: section/{domain}/{section_name}.md
    if not sem_sec_file.exists():
        sem_sec_file = sem_sec_dir / f"{section_name}.md"

    if not sem_sec_file.exists():
        return {
            "section": section_name,
            "scope": "section",
            "evaluated_at": utc_now_iso(),
            "criteria": [],
            "note": f"No semantic section audit file found for {section_name}",
        }

    rubric_content = sem_sec_file.read_text(encoding="utf-8")
    rubric = parse_semantic_rubric(rubric_content)

    # Extract keywords from rubric
    objective_text = (rubric.get("engineering_intent", "") +
                     rubric.get("audit_objectives", ""))
    stopwords = {"the", "and", "for", "that", "this", "with", "from", "are",
                 "was", "not", "but", "has", "have", "can", "should", "must"}
    objective_words = [
        w.lower() for w in re.split(r"[\s,.!?;:()]+", objective_text)
        if len(w) >= 3 and w.lower() not in stopwords
    ]

    evaluated_criteria: list[dict] = []
    for criterion in rubric.get("scoring_criteria", []):
        criterion_id = criterion["criterion_id"]
        max_score = criterion["max_score"]
        mandatory = criterion["mandatory"]

        desc_words = [
            w.lower() for w in re.split(r"[\s,.!?;:()]+", criterion["description"])
            if len(w) >= 3 and w.lower() not in stopwords
        ]
        combined_keywords = objective_words[:10] + desc_words[:5]

        passed, confidence, evidence_msg = _check_section_quality(
            section_content, objective_text, combined_keywords
        )

        score = max_score if passed else 0

        evaluated_criteria.append({
            "criterion_id": criterion_id,
            "passed": passed,
            "score": score,
            "max_score": max_score,
            "mandatory": mandatory,
            "confidence": round(confidence, 2),
            "evidence": {
                "message": evidence_msg,
            },
            "description": criterion["description"],
        })

    return {
        "section": section_name,
        "scope": "section",
        "evaluated_at": utc_now_iso(),
        "criteria": evaluated_criteria,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def evaluate_all_semantic(
    system_root: Path,
    domain: str,
    doc_content: str,
    context: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Evaluate all semantic criteria for a domain (document + sections)."""
    # Document-level
    doc_result = evaluate_semantic_document(system_root, domain, doc_content, context)

    # Section-level
    audit_root = system_root / "audit"
    sem_sec_dir = audit_root / "semantic" / "section" / resolve_domain(domain)
    sec_results: dict[str, dict] = {}

    if sem_sec_dir.is_dir():
        for sec_file in sorted(sem_sec_dir.glob("*.md")):
            section_name = sec_file.stem
            # Extract section content from the document
            sections = _parse_doc_sections(doc_content)
            section_content = sections.get(section_name, "")

            sec_result = evaluate_semantic_section(
                system_root, domain, section_name, section_content,
            )
            sec_results[section_name] = sec_result

    return {
        "domain": domain,
        "evaluated_at": utc_now_iso(),
        "model": "heuristic-v1",
        "document": doc_result,
        "sections": sec_results,
    }


def _parse_doc_sections(content: str) -> dict[str, str]:
    """Parse markdown into {heading_lower: content} mapping."""
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in content.split("\n"):
        heading_match = re.match(r"^##\s+(.+)$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip().lower()
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Heuristic semantic audit evaluator"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--doc", required=True, help="Path to the document to evaluate")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--context", help="Path to context JSON for grounding")
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

    context = None
    if args.context:
        from _common import load_json
        context_path = Path(args.context)
        if context_path.exists():
            context = load_json(context_path)

    result = evaluate_all_semantic(system_root, args.domain, doc_content, context)
    write_json(Path(args.out), result)

    # Summary
    doc_criteria = result["document"].get("criteria", [])
    doc_passed = sum(1 for c in doc_criteria if c["passed"])
    sec_total = sum(
        len(s.get("criteria", [])) for s in result["sections"].values()
    )
    sec_passed = sum(
        sum(1 for c in s.get("criteria", []) if c["passed"])
        for s in result["sections"].values()
    )
    print(f"Semantic document criteria: {doc_passed}/{len(doc_criteria)} passed")
    print(f"Semantic section criteria: {sec_passed}/{sec_total} passed")
    print(f"Total: {doc_passed + sec_passed}/{len(doc_criteria) + sec_total} passed")


if __name__ == "__main__":
    main()
