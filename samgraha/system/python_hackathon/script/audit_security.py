"""
audit_security.py - Powers the Security domain deterministic audit.
Runs bandit for SAST, checks for hardcoded secrets, detects vulnerable patterns.
"""
import subprocess
import json
import argparse
import os
import re

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


def run_security_audit(repo_path):
    """
    Checks for security tooling, runs bandit, and scans for hardcoded secrets.
    """
    result = {
        "bandit_config_present": False,
        "bandit_executed": False,
        "bandit_high_severity_issues": 0,
        "bandit_medium_severity_issues": 0,
        "hardcoded_secrets_found": 0,
        "secret_findings": [],
        "error": None
    }

    # Config presence
    for path in [
        os.path.join(repo_path, ".bandit"),
        os.path.join(repo_path, "pyproject.toml")
    ]:
        if os.path.exists(path):
            if path.endswith(".bandit"):
                result["bandit_config_present"] = True
            else:
                with open(path, "r", encoding="utf-8") as f:
                    if "tool.bandit" in f.read():
                        result["bandit_config_present"] = True

    # Secret scan
    secrets = _scan_for_secrets(repo_path)
    result["hardcoded_secrets_found"] = len(secrets)
    result["secret_findings"] = secrets[:5]  # Cap at 5 examples in output

    # Run bandit
    try:
        proc = subprocess.run(
            ["bandit", "-r", repo_path, "-f", "json", "-q"],
            capture_output=True, text=True, timeout=60
        )
        result["bandit_executed"] = True
        try:
            report = json.loads(proc.stdout)
            for issue in report.get("results", []):
                sev = issue.get("issue_severity", "").upper()
                if sev == "HIGH":
                    result["bandit_high_severity_issues"] += 1
                elif sev == "MEDIUM":
                    result["bandit_medium_severity_issues"] += 1
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
