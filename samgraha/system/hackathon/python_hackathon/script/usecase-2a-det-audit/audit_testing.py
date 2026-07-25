"""
audit_testing.py - Powers the Testing domain deterministic audit.
Discovers test files, runs pytest with coverage, parses results.
"""
import subprocess
import json
import argparse
import os
import sys
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root


def _check_module_installed(module_name):
    """Check if a Python module is available via import."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {module_name}"],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_testing_audit(repo_path):
    """
    Discovers test configurations and executes pytest to collect pass/fail/coverage.
    """
    repo_path = resolve_code_root(repo_path)
    result = {
        "tests_directory_present": False,
        "pytest_config_present": False,
        "pytest_executed": False,
        "tests_passed": False,
        "total_tests": 0,
        "failed_tests": 0,
        "coverage_pct": None,
        "json_report_used": False,
        "coverage_used": False,
        "data_skipped": [],
        "error": None,
    }

    # 1. Structural checks
    for name in ["tests", "test"]:
        if os.path.isdir(os.path.join(repo_path, name)):
            result["tests_directory_present"] = True
            break

    for candidate in [
        os.path.join(repo_path, "pytest.ini"),
        os.path.join(repo_path, "setup.cfg"),
    ]:
        if os.path.exists(candidate):
            result["pytest_config_present"] = True
            break

    pyproject_path = os.path.join(repo_path, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, "r", encoding="utf-8") as f:
            if "tool.pytest" in f.read():
                result["pytest_config_present"] = True

    # 2. Detect optional plugins before running pytest
    has_json_report = _check_module_installed("pytest_jsonreport")
    has_cov = _check_module_installed("pytest_cov")

    if not has_json_report:
        result["data_skipped"].append(
            "pytest-json-report not installed — per-test breakdown unavailable"
        )
    if not has_cov:
        result["data_skipped"].append(
            "pytest-cov not installed — coverage data unavailable"
        )

    # 3. Build pytest command dynamically
    # Use -c /dev/null to avoid picking up parent directory's pyproject.toml
    cmd = [sys.executable, "-m", "pytest", "--tb=no", "-q", "-c", "/dev/null"]
    
    # Use a temp file for JSON report to avoid mixing with stdout
    json_report_path = os.path.join(repo_path, ".pytest_json_report.json")
    if has_json_report:
        cmd += ["--json-report", f"--json-report-file={json_report_path}"]
    if has_cov:
        cmd += ["--cov=.", "--cov-report=json:-"]

    # 4. Execute pytest
    try:
        proc = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["pytest_executed"] = True

        stdout = proc.stdout
        stderr = proc.stderr

        # Parse JSON report (test counts) if the plugin produced output
        if has_json_report and os.path.exists(json_report_path):
            try:
                with open(json_report_path, "r", encoding="utf-8") as f:
                    report = json.load(f)
                summary = report.get("summary", {})
                result["total_tests"] = summary.get("total", 0)
                result["failed_tests"] = summary.get("failed", 0)
                result["tests_passed"] = (
                    result["failed_tests"] == 0 and result["total_tests"] > 0
                )
                result["json_report_used"] = True
                
                # Parse coverage if pytest-cov produced JSON
                if has_cov:
                    try:
                        cov_report = report.get("coverage", {})
                        cov_total = cov_report.get("totals", {}).get("percent_covered")
                        if cov_total is not None:
                            result["coverage_pct"] = round(cov_total, 2)
                            result["coverage_used"] = True
                    except (KeyError, TypeError):
                        result["data_skipped"].append(
                            "Coverage JSON present but unparseable"
                        )
            except (json.JSONDecodeError, KeyError, OSError) as e:
                result["tests_passed"] = proc.returncode == 0
                result["data_skipped"].append(
                    f"JSON report error: {e}"
                )
            finally:
                # Clean up temp file
                try:
                    os.remove(json_report_path)
                except OSError:
                    pass
        else:
            # No JSON report plugin; parse -q output for a rough count
            result["tests_passed"] = proc.returncode == 0
            for line in reversed(stdout.strip().splitlines()):
                # Typical pytest -q summary: "5 passed, 1 failed in 0.30s"
                tokens = line.split()
                if tokens and tokens[-1].startswith("in"):
                    # e.g. "3 passed, 1 failed in 0.12s"
                    for i, t in enumerate(tokens):
                        if t == "passed":
                            try:
                                result["total_tests"] += int(tokens[i - 1])
                            except (ValueError, IndexError):
                                pass
                        if t == "failed":
                            try:
                                result["failed_tests"] += int(tokens[i - 1])
                            except (ValueError, IndexError):
                                pass
                    break

    except FileNotFoundError:
        result["error"] = "pytest not installed in environment"
    except subprocess.TimeoutExpired:
        result["error"] = "pytest timed out after 120 seconds"

    # 5. Print summary to stderr (stdout reserved for JSON output)
    print(f"[audit_testing] pytest executed: {result['pytest_executed']}", file=sys.stderr)
    print(f"[audit_testing] JSON report: {'used' if result['json_report_used'] else 'skipped'}", file=sys.stderr)
    print(f"[audit_testing] Coverage: {'used' if result['coverage_used'] else 'skipped'}", file=sys.stderr)
    if result["data_skipped"]:
        for msg in result["data_skipped"]:
            print(f"[audit_testing] SKIP: {msg}", file=sys.stderr)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    print(json.dumps(run_testing_audit(args.repo), indent=2))
