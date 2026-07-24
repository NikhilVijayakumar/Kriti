"""deterministic_audit.py — runs deterministic mechanical checks against a
domain's draft, per calculation/deterministic/{domain}.yaml rules.
Records findings in academic_deterministic_findings.
"""
import json
import os
import re
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

DETERMINISTIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "calculation", "deterministic")


def _load_rules(domain_key):
    """Load deterministic rules for a domain from YAML."""
    yaml_path = os.path.join(DETERMINISTIC_DIR, f"{domain_key}.yaml")
    if not os.path.isfile(yaml_path):
        return None, f"rules not found: {yaml_path}"
    try:
        import yaml
    except ImportError:
        return None, "pyyaml not installed"
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f), None


def _get_domain_draft(conn, paper_id, domain_key):
    """Get the latest draft text for a domain."""
    domain_id = academic_schema.get_domain_id(conn, domain_key)
    if domain_id is None:
        return None
    row = conn.execute(
        "SELECT id FROM academic_narratives "
        "WHERE paper_id=? AND domain_id=? ORDER BY iteration DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    if not row:
        return None
    sections = conn.execute(
        "SELECT heading, text FROM academic_narrative_sections "
        "WHERE narrative_id=? ORDER BY sort_order",
        (row["id"],),
    ).fetchall()
    return "\n\n".join(f"## {s['heading']}\n\n{s['text']}" for s in sections)


def _check_regex(pattern, text, flags=0):
    """Check if a regex pattern matches in text."""
    return bool(re.search(pattern, text, flags))


def _check_word_count(text, min_words=0, max_words=None):
    """Check word count bounds."""
    wc = len(re.findall(r'\S+', text))
    if wc < min_words:
        return False, f"word count {wc} < minimum {min_words}"
    if max_words and wc > max_words:
        return False, f"word count {wc} > maximum {max_words}"
    return True, f"word count {wc}"


def _check_no_placeholders(text):
    """Check for unfilled template markers."""
    patterns = [r'\bTODO\b', r'\bXXX\b', r'\[Author\s*Name\]', r'\[Insert',
                r'\[TBD\]', r'\[FIXME\]', r'\{TODO\}']
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return False, f"placeholder found: {re.search(pat, text, re.IGNORECASE).group()}"
    return True, "no placeholders"


def _check_contains_number(text):
    """Check that text contains at least one numeric value."""
    return bool(re.search(r'\d+\.?\d*', text)), "contains numbers" if re.search(r'\d+\.?\d*', text) else "no numbers found"


def _check_citation_markers(text):
    """Count citation markers in text."""
    # Matches [1], [2,3], [1-5], (Author, 2024), etc.
    numbered = len(re.findall(r'\[\d+(?:[,;\s\-–]\d+)*\]', text))
    author_year = len(re.findall(r'\([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-z]+))?,\s*\d{4}[a-z]?\)', text))
    return numbered + author_year


def _check_mermaid_diagram(text):
    """Check for mermaid code block."""
    return bool(re.search(r'```mermaid', text))


def _check_equations(text):
    """Check for equation blocks."""
    return bool(re.search(r'\$\$.*?\$\$|\\begin\{equation|\\\[.*?\\\]', text, re.DOTALL))


def _check_pseudocode(text):
    """Check for pseudocode or algorithm blocks."""
    patterns = [r'\\begin\{algorithm', r'```pseudo', r'```algorithm',
                r'\*\*Algorithm\s*\d', r'**Input:', r'**Output:']
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def _check_list_items(text, min_items=1):
    """Check for bulleted or numbered list items."""
    items = re.findall(r'^\s*[-*+]\s|^\s*\d+[.)]\s', text, re.MULTILINE)
    return len(items) >= min_items, f"{len(items)} list items found"


def _run_check(check, text, draft_texts=None):
    """Run a single deterministic check against the draft text.
    Returns (passed: bool, detail: str)."""
    check_id = check.get("id", "unknown")
    rule = check.get("rule", "")
    draft_texts = draft_texts or {}

    try:
        if rule == "word_count_in_range":
            cfg = check.get("config", {})
            return _check_word_count(text, cfg.get("min", 0), cfg.get("max"))
        elif rule == "no_placeholders":
            return _check_no_placeholders(text)
        elif rule == "contains_number":
            return _check_contains_number(text)
        elif rule == "contains_mermaid_diagram":
            return _check_mermaid_diagram(text), "mermaid diagram present" if _check_mermaid_diagram(text) else "no mermaid diagram"
        elif rule == "contains_pseudocode":
            return _check_pseudocode(text), "pseudocode present" if _check_pseudocode(text) else "no pseudocode"
        elif rule == "contains_equation":
            return _check_equations(text), "equations present" if _check_equations(text) else "no equations"
        elif rule == "min_citation_count":
            min_count = check.get("config", {}).get("min", 1)
            count = _check_citation_markers(text)
            return count >= min_count, f"{count} citations found (minimum {min_count})"
        elif rule == "regex_match":
            pattern = check.get("config", {}).get("pattern", "")
            return _check_regex(pattern, text), f"pattern {'found' if _check_regex(pattern, text) else 'not found'}: {pattern}"
        elif rule == "regex_absent":
            pattern = check.get("config", {}).get("pattern", "")
            return not _check_regex(pattern, text), f"forbidden pattern {'found' if _check_regex(pattern, text) else 'absent'}: {pattern}"
        elif rule == "min_list_items":
            min_items = check.get("config", {}).get("min", 1)
            return _check_list_items(text, min_items)
        elif rule == "cross_reference_numbers":
            other_domain = check.get("config", {}).get("other_domain", "")
            other_text = draft_texts.get(other_domain, "")
            if not other_text:
                return True, f"cross-reference skipped: {other_domain} draft not available"
            nums_in_draft = set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', text))
            nums_in_other = set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', other_text))
            mismatches = nums_in_draft - nums_in_other
            if mismatches:
                return False, f"numbers in draft not in {other_domain}: {mismatches}"
            return True, "all numbers cross-referenced"
        elif rule == "no_new_results":
            results_text = draft_texts.get("results", "")
            if not results_text:
                return True, "cross-reference skipped: results draft not available"
            new_nums = set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', text)) - set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', results_text))
            if new_nums:
                return False, f"new numbers not in results: {new_nums}"
            return True, "no new results"
        elif rule == "length_proportion":
            other_domain = check.get("config", {}).get("compare_to", "")
            max_ratio = check.get("config", {}).get("max_ratio", 1.5)
            other_text = draft_texts.get(other_domain, "")
            if not other_text:
                return True, f"proportion check skipped: {other_domain} not available"
            my_wc = len(re.findall(r'\S+', text))
            other_wc = len(re.findall(r'\S+', other_text))
            if other_wc > 0 and my_wc / other_wc > max_ratio:
                return False, f"length ratio {my_wc/other_wc:.1f} exceeds {max_ratio} vs {other_domain}"
            return True, f"length proportion OK ({my_wc}/{other_wc})"
        elif rule == "no_citations":
            count = _check_citation_markers(text)
            return count == 0, f"{count} citations found (expected 0)"
        elif rule == "severity_tagged":
            # Check that gaps have severity markers
            severity_pattern = r'(?i)(?:HIGH|MEDIUM|LOW|CRITICAL)\s*[:\-]'
            matches = re.findall(severity_pattern, text)
            return len(matches) > 0, f"{len(matches)} severity-tagged items"
        else:
            return True, f"unknown rule '{rule}' — passed by default"
    except Exception as e:
        return False, f"check error: {e}"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")
    domain_key = payload.get("domain")

    if not paper_id or not domain_key:
        write_envelope(out_path, status="error",
                       message="missing paper_id or domain in input")
        return

    # Load rules
    rules, err = _load_rules(domain_key)
    if err:
        write_envelope(out_path, status="error", message=err)
        return

    checks = rules.get("checks", []) if rules else []
    if not checks:
        write_envelope(out_path, status="ok",
                       message=f"no deterministic checks defined for {domain_key}",
                       verdict="PASS", findings=[])
        return

    conn = academic_schema.get_conn(db_path)
    try:
        # Get this domain's draft
        draft_text = _get_domain_draft(conn, paper_id, domain_key)
        if not draft_text:
            write_envelope(out_path, status="error",
                           message=f"no draft found for {domain_key}")
            return

        # Get other domains' drafts for cross-reference checks
        draft_texts = {}
        for other_domain in ("abstract", "results", "introduction", "conclusion"):
            other_text = _get_domain_draft(conn, paper_id, other_domain)
            if other_text:
                draft_texts[other_domain] = other_text

        # Run all checks
        findings = []
        all_passed = True
        for check in checks:
            passed, detail = _run_check(check, draft_text, draft_texts)
            findings.append({
                "check_id": check.get("id", "unknown"),
                "rule": check.get("rule", "unknown"),
                "passed": passed,
                "detail": detail,
                "severity": check.get("severity", "warning"),
            })
            if not passed and check.get("severity") in ("critical", "error"):
                all_passed = False

        verdict = "PASS" if all_passed else "FAIL"

        # Record findings
        academic_schema.record_deterministic_findings(
            conn, paper_id, domain_key, verdict, findings
        )

        write_envelope(out_path, status="ok",
                       message=f"deterministic audit {domain_key}: {verdict}",
                       verdict=verdict, findings=findings)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
