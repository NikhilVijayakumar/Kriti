"""
audit_security.py - Powers the Security domain deterministic audit.
Runs bandit for SAST, checks for hardcoded secrets, detects vulnerable patterns.
"""
import subprocess
import json
import argparse
import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root

# Path to our default configs
DEFAULT_CONFIGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")

SECRET_PATTERNS = [
    re.compile(r'(?i)(api_key|secret|password|token)\s*=\s*["\'][^"\']{6,}["\']'),
    re.compile(r'(?i)OPENAI_API_KEY\s*=\s*["\'][^"\']+["\']'),
    re.compile(r'(?i)sk-[A-Za-z0-9]{32,}'),
]


def _scan_for_secrets(repo_path):
    """Walk the repo looking for hardcoded secrets in Python/env files."""
    findings = []
    extensions = [".py", ".env", ".yaml", ".yml", ".toml", ".json", ".cfg"]
    for root, _, files in os.walk(repo_path):
        # Skip hidden dirs and venvs
        parts = root.split(os.sep)
        if any(p.startswith(".") or p in ("venv", ".venv", "__pycache__") for p in parts):
            continue
        for fname in files:
            if not any(fname.endswith(ext) for ext in extensions):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        for pat in SECRET_PATTERNS:
                            if pat.search(line):
                                findings.append({
                                    "file": os.path.relpath(fpath, repo_path),
                                    "line": lineno,
                                    "match": line.strip()[:80]
                                })
            except (OSError, PermissionError):
                pass
    return findings


def _detect_team_config(repo_path):
    """Detect if team has their own bandit config."""
    config_files = [".bandit", "pyproject.toml"]
    for fname in config_files:
        path = os.path.join(repo_path, fname)
        if os.path.exists(path):
            if fname == "pyproject.toml":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if "tool.bandit" in content:
                        return True, path
                except OSError:
                    pass
            else:
                return True, path
    return False, None


def run_security_audit(repo_path):
    """
    Checks for security tooling, runs bandit, and scans for hardcoded secrets.
    """
    repo_path = resolve_code_root(repo_path)
    
    # Detect team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path)
    
    result = {
        "bandit_config_present": False,
        "bandit_team_config": has_team_cfg,
        "bandit_executed": False,
        "bandit_high_severity_issues": 0,
        "bandit_medium_severity_issues": 0,
        "bandit_low_severity_issues": 0,
        "bandit_total_issues": 0,
        "bandit_issue_types": {},
        "hardcoded_secrets_found": 0,
        "secret_findings": [],
        "error": None
    }

    # Config presence - check team config first, then our default
    if has_team_cfg:
        result["bandit_config_present"] = True
    else:
        # Check our default config
        default_cfg = os.path.join(DEFAULT_CONFIGS_DIR, ".bandit")
        if os.path.exists(default_cfg):
            result["bandit_config_present"] = True

    # Secret scan
    secrets = _scan_for_secrets(repo_path)
    result["hardcoded_secrets_found"] = len(secrets)
    result["secret_findings"] = secrets[:5]

    # Run bandit
    try:
        # Use our config if team doesn't have one
        cmd = [sys.executable, "-m", "bandit", "-r", repo_path, "-f", "json", "-q"]
        if not has_team_cfg:
            default_cfg = os.path.join(DEFAULT_CONFIGS_DIR, ".bandit")
            if os.path.exists(default_cfg):
                cmd = [sys.executable, "-m", "bandit", "-r", repo_path, "-f", "json", "-q", "-c", default_cfg]
        
        proc = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=60
        )
        result["bandit_executed"] = True
        try:
            report = json.loads(proc.stdout)
            issue_types = {}
            for issue in report.get("results", []):
                sev = issue.get("issue_severity", "").upper()
                issue_type = issue.get("issue_text", "unknown")
                if sev == "HIGH":
                    result["bandit_high_severity_issues"] += 1
                elif sev == "MEDIUM":
                    result["bandit_medium_severity_issues"] += 1
                elif sev == "LOW":
                    result["bandit_low_severity_issues"] += 1
                result["bandit_total_issues"] += 1
                
                # Count by issue type
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            
            result["bandit_issue_types"] = issue_types
        except json.JSONDecodeError:
            result["error"] = "bandit JSON parse failed"
    except FileNotFoundError:
        result["error"] = "bandit not installed in environment"
    except subprocess.TimeoutExpired:
        result["error"] = "bandit timed out after 60 seconds"

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    print(json.dumps(run_security_audit(args.repo), indent=2))
