"""
evaluate_rules.py — Evaluate raw audit facts against deterministic rules.

Loads audit/deterministic/document/{domain}.yaml rules, compares each rule's
condition against the audit script's raw output, and computes a 0-100 score
using calculation/deterministic/document.yaml's weighted_pass_rate formula.
"""
import os
import re
import yaml
import glob as globmod

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
RULES_DIR = os.path.join(SYSTEM_DIR, "audit", "deterministic", "document")
AGG_DIR = os.path.join(SYSTEM_DIR, "calculation", "aggregation", "domain")

# Explicit rule-ID -> evidence-key mappings for cases where the rule's target
# doesn't match the audit script's output key naming convention.
RULE_EVIDENCE_MAP = {
    # documentation domain
    "doc-001": "readme_present",
    "doc-002": "readme_has_installation_section",
    "doc-003": "local_links_valid",
}


def _domain_dirname(domain_name):
    """Map a domain name like 'team-workflow' or 'team_workflow' to its directory prefix like '08-team-workflow'."""
    matches = globmod.glob(os.path.join(RULES_DIR, f"*-{domain_name.replace('_', '-')}.yaml"))
    if matches:
        return os.path.splitext(os.path.basename(matches[0]))[0]
    return None


def load_rules(domain):
    """Load the rule YAML for a domain. Returns (domain_dirname, rules_list, meta)."""
    dirname = _domain_dirname(domain)
    if not dirname:
        return None, [], {}
    path = os.path.join(RULES_DIR, f"{dirname}.yaml")
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return dirname, cfg.get("rules", []), cfg


def _evaluate_condition(rule, evidence):
    """
    Evaluate a single rule against raw audit evidence.

    Evidence types supported:
      file_presence: bool key matching target, OR extensions/directories/patterns variants
      git_history: nested keys checked via 'check' path
      tool_execution: numeric value compared to threshold
      config_analysis: bool key matching target
      dependency_presence: list in evidence matching packages, or bool key matching target
      regex_match: list/count in evidence
      section_presence: check section headings in evidence
      link_validation: check link validity in evidence
      script_output: navigate nested check path and compare to expected
    Returns (passed: bool, detail: str).
    """
    rule_id = rule.get("id", "")

    # Check explicit rule-to-evidence mapping first
    if rule_id in RULE_EVIDENCE_MAP:
        ev_key = RULE_EVIDENCE_MAP[rule_id]
        val = evidence.get(ev_key)
        if val is not None:
            if isinstance(val, bool):
                return val, f"{rule_id}: {ev_key}={val}"
            return bool(val), f"{rule_id}: {ev_key}={val}"

    ev = rule.get("evidence", {})
    ev_type = ev.get("type", "")
    check = ev.get("check", "")
    target = ev.get("target", "")

    if ev_type == "file_presence":
        # Standard: check if target key is truthy in evidence
        if target and target in evidence:
            val = evidence[target]
            return bool(val), f"{target}: {'present' if val else 'missing'}"
        # Fuzzy match: target "uv.lock" may map to evidence key "uv_lock_present"
        # (evidence keys are always snake_case, so normalize case too --
        # target "Dockerfile" must still match evidence key "dockerfile_present")
        if target:
            normalized = target.replace(".", "_").replace("-", "_").lower()
            for suffix in ("_present", ""):
                key = normalized + suffix
                if key in evidence:
                    val = evidence[key]
                    return bool(val), f"{target}: {'present' if val else 'missing'}"
        # Targets variant (runtime): check if any of multiple targets exist
        targets = ev.get("targets", [])
        if targets:
            found = []
            for t in targets:
                if t in evidence and evidence[t]:
                    found.append(t)
                else:
                    # Fuzzy match for each target
                    norm = t.replace(".", "_").replace("-", "_")
                    for suffix in ("_present", ""):
                        if norm + suffix in evidence and evidence[norm + suffix]:
                            found.append(t)
                            break
            return len(found) > 0, f"entrypoints: {', '.join(found) if found else 'none found'}"
        # Extensions variant (data-quality): check data_files_found
        if "extensions" in ev:
            val = evidence.get("data_files_found", False)
            return bool(val), f"data files: {'found' if val else 'missing'}"
        # Directories variant (data-quality): check data_directory_present
        if "directories" in ev:
            val = evidence.get("data_directory_present", False)
            return bool(val), f"data directory: {'found' if val else 'missing'}"
        # Patterns variant (ai-explanations): check prompt_files_found
        if "patterns" in ev:
            count = evidence.get("prompt_file_count", 0)
            return count > 0, f"prompt files: {count} found"
        # Fallback
        val = evidence.get(target, False)
        return bool(val), f"{target}: {val}"

    if ev_type == "git_history":
        parts = check.split(".")
        obj = evidence
        for p in parts:
            if isinstance(obj, dict):
                obj = obj.get(p)
            else:
                return False, f"Path {'.'.join(parts)} not found in evidence"
        return bool(obj), f"{'.'.join(parts)}: {obj}"

    if ev_type == "tool_execution":
        val = evidence.get(target, 0)
        if val is None:
            # Tool didn't run (e.g. pylint_score is null when pylint wasn't
            # configured) -- treat as "no measurement", which fails a
            # threshold check the same as an explicit 0 would.
            val = 0
        threshold = ev.get("threshold", 0)
        op = ev.get("op", "gte")
        if op == "gte":
            passed = float(val) >= float(threshold)
        elif op == "lte":
            passed = float(val) <= float(threshold)
        elif op == "eq":
            passed = float(val) == float(threshold)
        else:
            passed = bool(val)
        return passed, f"{target}: {val} (threshold: {threshold})"

    if ev_type == "config_analysis":
        val = evidence.get(target, False)
        return bool(val), f"{target}: {'configured' if val else 'not configured'}"

    if ev_type == "dependency_presence":
        # Standard: check if target key is truthy
        if target and target in evidence:
            val = evidence[target]
            return bool(val), f"{target}: {'found' if val else 'not found'}"
        # Packages variant (ai-explanations): check llm_dependencies_found
        if "packages" in ev:
            found = evidence.get("llm_dependencies_found", [])
            return len(found) > 0, f"LLM deps: {len(found)} found ({', '.join(found[:5])})"
        val = evidence.get(target, False)
        return bool(val), f"{target}: {val}"

    if ev_type == "regex_match":
        # Patterns variant: search the rule's own patterns against readme_text
        # (target is typically "README.md" -- a filename, not an evidence key,
        # so this must be checked before the "target" branch below).
        patterns = ev.get("patterns")
        if patterns and "readme_text" in evidence:
            text = evidence.get("readme_text") or ""
            matched = [p for p in patterns if re.search(p, text, re.IGNORECASE)]
            return len(matched) > 0, f"README patterns matched: {len(matched)}/{len(patterns)} ({', '.join(matched[:3])})"
        # Legacy patterns variant (data-quality): check datahub_url_count
        if patterns:
            count = evidence.get("datahub_url_count", 0)
            return count > 0, f"data-hub URLs: {count} found"
        # Standard: check list/count in evidence
        if target:
            val = evidence.get(target, [])
            passed = len(val) > 0 if isinstance(val, list) else bool(val)
            return passed, f"{target}: {len(val) if isinstance(val, list) else 'found'} matches"
        val = evidence.get(target, [])
        return bool(val), f"{target}: {val}"

    if ev_type == "section_presence":
        # documentation domain: check section headings
        if "required_semantic_types" in ev:
            sections = ev["required_semantic_types"]
            for section_type in sections:
                key = f"readme_has_{section_type}_section"
                if key in evidence:
                    if not evidence[key]:
                        return False, f"README missing '{section_type}' section"
                    return True, f"README has '{section_type}' section"
            # If no matching evidence key, check readme_has_installation_section as fallback
            if evidence.get("readme_has_installation_section"):
                return True, "README has installation section"
            return False, "README missing required sections"
        val = evidence.get(target, False)
        return bool(val), f"{target}: {val}"

    if ev_type == "link_validation":
        # documentation domain: check local links validity
        valid = evidence.get("local_links_valid", True)
        broken = evidence.get("local_links_broken", [])
        if valid:
            return True, "All local links valid"
        return False, f"Broken local links: {', '.join(broken[:5])}"

    if ev_type == "script_output":
        # Navigate nested check path (e.g. "inference.within_time_limit")
        parts = check.split(".")
        obj = evidence
        for p in parts:
            if isinstance(obj, dict):
                obj = obj.get(p)
            else:
                return False, f"Path {'.'.join(parts)} not found in evidence"
        # If expected is specified, compare against it
        if "expected" in ev:
            expected = ev["expected"]
            passed = (obj == expected) if not isinstance(expected, bool) else (bool(obj) == expected)
            return passed, f"{'.'.join(parts)}: {obj} (expected: {expected})"
        # Otherwise, truthy = pass
        return bool(obj), f"{'.'.join(parts)}: {obj}"

    # Fallback: treat evidence key matching target as boolean
    val = evidence.get(target, evidence.get(check, False))
    return bool(val), f"{target or check}: {val}"


def evaluate_domain(domain, evidence):
    """
    Evaluate all rules for a domain against raw audit evidence.

    Returns:
        {
            "domain": str,
            "score": float (0-100),
            "rules": [{"id", "description", "passed", "weight", "mandatory", "severity", "detail"}, ...],
            "total_weight": float,
            "passed_weight": float,
        }
    """
    _, rules, meta = load_rules(domain)
    if not rules:
        return {"domain": domain, "score": 0.0, "rules": [], "total_weight": 0, "passed_weight": 0}

    rule_results = []
    total_weight = 0.0
    passed_weight = 0.0

    for rule in rules:
        weight = rule.get("weight", 1.0)
        mandatory = rule.get("mandatory", False)
        severity = rule.get("severity", "warning")
        total_weight += weight

        passed, detail = _evaluate_condition(rule, evidence)
        if passed:
            passed_weight += weight

        rule_results.append({
            "id": rule["id"],
            "description": rule.get("description", ""),
            "passed": passed,
            "weight": weight,
            "mandatory": mandatory,
            "severity": severity,
            "detail": detail,
        })

    # weighted_pass_rate: 100 * (sum of weights where passed) / (sum of all weights)
    score = round(100.0 * passed_weight / total_weight, 2) if total_weight > 0 else 0.0

    return {
        "domain": domain,
        "score": score,
        "rules": rule_results,
        "total_weight": total_weight,
        "passed_weight": passed_weight,
    }
