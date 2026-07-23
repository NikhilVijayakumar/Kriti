import subprocess
import json
import argparse
import os
import sys
import glob
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root


SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".mypy_cache",
             ".pytest_cache", ".tox", ".eggs", "*.egg-info", ".eggs"}

# Path to our default configs
DEFAULT_CONFIGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")


def _run_tool(cmd, timeout=60):
    """Run a tool command, return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return -1, "", "tool not available"


def _check_cicd_content(repo_path):
    """
    Check for CI/CD files with real pipeline content (on: triggers, jobs: blocks).
    Returns dict with cicd_real_content (bool), cicd_files_found (list), cicd_stubs (list).
    """
    real_files = []
    stub_files = []

    # GitHub Actions
    workflows_dir = os.path.join(repo_path, ".github", "workflows")
    if os.path.isdir(workflows_dir):
        for f in os.listdir(workflows_dir):
            if not f.endswith((".yml", ".yaml")):
                continue
            path = os.path.join(workflows_dir, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
            except OSError:
                continue
            has_trigger = bool(re.search(r"^\s*on\s*:", content, re.MULTILINE))
            has_jobs = bool(re.search(r"^\s*jobs\s*:", content, re.MULTILINE))
            if has_trigger and has_jobs:
                real_files.append(os.path.relpath(path, repo_path))
            else:
                stub_files.append(os.path.relpath(path, repo_path))

    # GitLab CI
    gitlab_ci = os.path.join(repo_path, ".gitlab-ci.yml")
    if os.path.isfile(gitlab_ci):
        try:
            with open(gitlab_ci, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            has_trigger = bool(re.search(r"^\s*(on|rules|only|except)\s*:", content, re.MULTILINE))
            has_jobs = bool(re.search(r"^\s*jobs\s*:", content, re.MULTILINE)) or bool(
                re.search(r"^[a-zA-Z_][a-zA-Z0-9_-]*\s*:", content, re.MULTILINE)
            )
            if has_trigger or has_jobs:
                real_files.append(os.path.relpath(gitlab_ci, repo_path))
            else:
                stub_files.append(os.path.relpath(gitlab_ci, repo_path))
        except OSError:
            pass

    return {
        "cicd_real_content": len(real_files) > 0,
        "cicd_files_found": real_files,
        "cicd_stubs": stub_files,
    }


def _count_top_level_dirs(repo_path):
    """
    Count top-level directories (excluding hidden dirs and known non-structure dirs).
    """
    count = 0
    for entry in os.listdir(repo_path):
        full = os.path.join(repo_path, entry)
        if not os.path.isdir(full):
            continue
        if entry.startswith("."):
            continue
        if entry in SKIP_DIRS:
            continue
        if entry.endswith(".egg-info"):
            continue
        count += 1
    return count


def _detect_team_config(repo_path, tool_name):
    """
    Detect if team has their own config for a tool.
    Returns (has_config: bool, config_path: str or None)
    """
    config_files = {
        "radon": ["radon.cfg", "pyproject.toml"],
        "mypy": ["mypy.ini", "mypy.cfg", "pyproject.toml", "pyrightconfig.json"],
        "pylint": [".pylintrc", "pylintrc", "pyproject.toml"],
        "flake8": [".flake8", "setup.cfg", "pyproject.toml"],
        "black": ["pyproject.toml"],
        "isort": [".isort.cfg", "setup.cfg", "pyproject.toml"],
    }
    
    for fname in config_files.get(tool_name, []):
        path = os.path.join(repo_path, fname)
        if os.path.exists(path):
            # For pyproject.toml, check if it has the tool section
            if fname == "pyproject.toml":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if f"tool.{tool_name}" in content:
                        return True, path
                except OSError:
                    pass
            else:
                return True, path
    return False, None


def _run_radon(repo_path):
    """Run radon for cyclomatic complexity analysis."""
    result = {
        "radon_config_found": False,
        "radon_team_config": False,
        "radon_executed": False,
        "radon_complexity": None,
        "radon_high_complexity_count": 0,
        "radon_avg_complexity": 0,
        "radon_grade": "A",
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "radon")
    result["radon_team_config"] = has_team_cfg
    
    # Check for our default config
    default_cfg = os.path.join(DEFAULT_CONFIGS_DIR, "radon.cfg")
    if os.path.exists(default_cfg):
        result["radon_config_found"] = True
    elif has_team_cfg:
        result["radon_config_found"] = True
    
    # Run radon
    rc, stdout, _ = _run_tool(
        [sys.executable, "-m", "radon", "cc", repo_path, "-j", "--no-assert"],
        timeout=60,
    )
    if rc == 0 and stdout.strip():
        try:
            data = json.loads(stdout)
            high_complexity = []
            total_complexity = 0
            file_count = 0
            
            for filepath, blocks in data.items():
                if not isinstance(blocks, list):
                    continue
                file_count += 1
                for block in blocks:
                    if isinstance(block, dict):
                        grade = block.get("grade", "")
                        complexity = block.get("complexity", 0)
                        name = block.get("name", "")
                        total_complexity += complexity
                        if grade in ("C", "D", "E", "F"):
                            high_complexity.append({
                                "file": filepath,
                                "name": name,
                                "complexity": complexity,
                                "grade": grade,
                            })
            
            result["radon_executed"] = True
            result["radon_high_complexity_count"] = len(high_complexity)
            result["radon_complexity"] = {
                "high_complexity_functions": high_complexity[:20],
                "total_files_analyzed": file_count,
            }
            if file_count > 0:
                result["radon_avg_complexity"] = round(total_complexity / file_count, 2)
            
            # Determine overall grade
            avg = result["radon_avg_complexity"]
            if avg <= 5:
                result["radon_grade"] = "A"
            elif avg <= 10:
                result["radon_grade"] = "B"
            elif avg <= 15:
                result["radon_grade"] = "C"
            elif avg <= 20:
                result["radon_grade"] = "D"
            else:
                result["radon_grade"] = "F"
        except json.JSONDecodeError:
            pass
    
    return result


def _run_mypy(repo_path):
    """Run mypy for type checking."""
    result = {
        "mypy_config_found": False,
        "mypy_team_config": False,
        "mypy_executed": False,
        "mypy_error_count": 0,
        "mypy_errors": [],
        "mypy_warning_count": 0,
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "mypy")
    result["mypy_team_config"] = has_team_cfg
    
    # Check for config
    mypy_cfg = os.path.join(repo_path, "mypy.ini")
    mypy_cfg2 = os.path.join(repo_path, "mypy.cfg")
    pyproject = os.path.join(repo_path, "pyproject.toml")
    
    if os.path.exists(mypy_cfg) or os.path.exists(mypy_cfg2) or has_team_cfg:
        result["mypy_config_found"] = True
    
    # Build command
    cmd = [sys.executable, "-m", "mypy", repo_path, "--ignore-missing-imports", "--no-error-summary"]
    if os.path.exists(mypy_cfg):
        cmd = [sys.executable, "-m", "mypy", "--config-file", mypy_cfg, repo_path, "--no-error-summary"]
    elif os.path.exists(mypy_cfg2):
        cmd = [sys.executable, "-m", "mypy", "--config-file", mypy_cfg2, repo_path, "--no-error-summary"]
    
    rc, stdout, _ = _run_tool(cmd, timeout=60)
    if rc >= 0 and stdout.strip():
        lines = [l for l in stdout.strip().splitlines() if l.strip()]
        errors = [l for l in lines if ": error:" in l]
        warnings = [l for l in lines if ": warning:" in l]
        result["mypy_executed"] = True
        result["mypy_error_count"] = len(errors)
        result["mypy_errors"] = errors[:20]
        result["mypy_warning_count"] = len(warnings)
    
    return result


def _run_pylint(repo_path):
    """Run pylint for code quality."""
    result = {
        "pylint_config_found": False,
        "pylint_team_config": False,
        "pylint_executed": False,
        "pylint_score": None,
        "pylint_error_count": 0,
        "pylint_warning_count": 0,
        "pylint_convention_count": 0,
        "pylint_refactor_count": 0,
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "pylint")
    result["pylint_team_config"] = has_team_cfg
    
    # Check for config
    pylint_cfg = os.path.join(repo_path, ".pylintrc")
    pylint_cfg2 = os.path.join(repo_path, "pylintrc")
    if os.path.exists(pylint_cfg) or os.path.exists(pylint_cfg2) or has_team_cfg:
        result["pylint_config_found"] = True
    
    # Find Python files
    py_files = glob.glob(os.path.join(repo_path, "**", "*.py"), recursive=True)
    py_files = [f for f in py_files if not any(skip in f for skip in ["venv", ".venv", "__pycache__", "tests", "test"])]
    
    if not py_files:
        return result
    
    # Run pylint
    cmd = [
        sys.executable, "-m", "pylint",
        "--output-format=json",
        "--disable=C0114,C0115,C0116,C0103,R0903,R0913,R0902,W0212,W0611,W0612,W0613,W0621,C0301,C0303,C0304,C0305",
        "--max-line-length=120",
        "--jobs=1",
    ] + py_files
    
    rc, stdout, _ = _run_tool(cmd, timeout=120)
    if rc >= 0 and stdout.strip():
        try:
            issues = json.loads(stdout)
            result["pylint_executed"] = True
            for issue in issues:
                cat = issue.get("type", "")
                if cat == "error":
                    result["pylint_error_count"] += 1
                elif cat == "warning":
                    result["pylint_warning_count"] += 1
                elif cat == "convention":
                    result["pylint_convention_count"] += 1
                elif cat == "refactor":
                    result["pylint_refactor_count"] += 1
            
            # Calculate score (10 - (errors * 1 + warnings * 0.5 + conventions * 0.1))
            total_issues = (
                result["pylint_error_count"] * 1.0 +
                result["pylint_warning_count"] * 0.5 +
                result["pylint_convention_count"] * 0.1 +
                result["pylint_refactor_count"] * 0.05
            )
            score = max(0, 10 - total_issues)
            result["pylint_score"] = round(score, 2)
        except json.JSONDecodeError:
            pass
    
    return result


def _run_flake8(repo_path):
    """Run flake8 for style checks."""
    result = {
        "flake8_config_found": False,
        "flake8_team_config": False,
        "flake8_executed": False,
        "flake8_error_count": 0,
        "flake8_errors": [],
        "flake8_error_categories": {},
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "flake8")
    result["flake8_team_config"] = has_team_cfg
    
    # Check for config
    flake8_cfg = os.path.join(repo_path, ".flake8")
    setup_cfg = os.path.join(repo_path, "setup.cfg")
    if os.path.exists(flake8_cfg) or os.path.exists(setup_cfg) or has_team_cfg:
        result["flake8_config_found"] = True
    
    # Run flake8 with default format (flake8 doesn't support JSON)
    cmd = [
        sys.executable, "-m", "flake8",
        "--max-line-length=120",
        "--exclude=.git,.venv,venv,__pycache__,tests,test,build,dist",
        repo_path,
    ]
    
    rc, stdout, _ = _run_tool(cmd, timeout=60)
    if rc >= 0 and stdout.strip():
        result["flake8_executed"] = True
        errors = []
        categories = {}
        
        # Parse default format: path:line:col: code message
        for line in stdout.strip().splitlines():
            match = re.match(r"(.+\.py):(\d+):(\d+): (\w+) (.+)", line)
            if match:
                filepath, line_num, col, code, message = match.groups()
                errors.append({
                    "file": filepath,
                    "line": int(line_num),
                    "code": code,
                    "message": message,
                })
                # Count by category (first letter of code)
                cat = code[0] if code else "unknown"
                categories[cat] = categories.get(cat, 0) + 1
        
        result["flake8_error_count"] = len(errors)
        result["flake8_errors"] = errors[:20]
        result["flake8_error_categories"] = categories
    
    return result


def _run_black(repo_path):
    """Run black for formatting check."""
    result = {
        "black_config_found": False,
        "black_team_config": False,
        "black_executed": False,
        "black_formatted_correctly": False,
        "black_files_to_format": 0,
        "black_files_checked": 0,
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "black")
    result["black_team_config"] = has_team_cfg
    
    # Check for config
    pyproject = os.path.join(repo_path, "pyproject.toml")
    if os.path.exists(pyproject):
        try:
            with open(pyproject, "r", encoding="utf-8") as f:
                if "tool.black" in f.read():
                    result["black_config_found"] = True
                    result["black_team_config"] = True
        except OSError:
            pass
    
    if os.path.exists(os.path.join(DEFAULT_CONFIGS_DIR, "pyproject.toml")):
        result["black_config_found"] = True
    
    # Run black in check mode
    cmd = [
        sys.executable, "-m", "black",
        "--check",
        "--line-length=120",
        "--target-version=py310",
        "--exclude=/(\.git|\.venv|venv|__pycache__|build|dist|tests|test)/",
        repo_path,
    ]
    
    rc, stdout, stderr = _run_tool(cmd, timeout=60)
    result["black_executed"] = True
    
    if rc == 0:
        result["black_formatted_correctly"] = True
    else:
        # Count files that need formatting
        output = stdout + stderr
        files_to_format = re.findall(r"would reformat (.+)", output)
        result["black_files_to_format"] = len(files_to_format)
    
    # Count files checked
    py_files = glob.glob(os.path.join(repo_path, "**", "*.py"), recursive=True)
    py_files = [f for f in py_files if not any(skip in f for skip in ["venv", ".venv", "__pycache__"])]
    result["black_files_checked"] = len(py_files)
    
    return result


def _run_isort(repo_path):
    """Run isort for import sorting check."""
    result = {
        "isort_config_found": False,
        "isort_team_config": False,
        "isort_executed": False,
        "isort_sorted_correctly": False,
        "isort_files_to_sort": 0,
    }
    
    # Check for team config
    has_team_cfg, cfg_path = _detect_team_config(repo_path, "isort")
    result["isort_team_config"] = has_team_cfg
    
    # Check for config
    isort_cfg = os.path.join(repo_path, ".isort.cfg")
    setup_cfg = os.path.join(repo_path, "setup.cfg")
    if os.path.exists(isort_cfg) or os.path.exists(setup_cfg) or has_team_cfg:
        result["isort_config_found"] = True
    
    # Run isort in check mode
    cmd = [
        sys.executable, "-m", "isort",
        "--check-only",
        "--diff",
        "--line-length=120",
        "--profile=black",
        repo_path,
    ]
    
    rc, stdout, stderr = _run_tool(cmd, timeout=60)
    result["isort_executed"] = True
    
    if rc == 0:
        result["isort_sorted_correctly"] = True
    else:
        # Count files that need sorting
        files_to_sort = re.findall(r"(.+\.py)", stdout)
        result["isort_files_to_sort"] = len(set(files_to_sort))
    
    return result


def run_python_audit(repo_path):
    """
    Comprehensive Python static analysis audit.
    Runs radon, mypy, pylint, flake8, black, isort.
    """
    repo_path = resolve_code_root(repo_path)
    
    # Run all tools
    radon_result = _run_radon(repo_path)
    mypy_result = _run_mypy(repo_path)
    pylint_result = _run_pylint(repo_path)
    flake8_result = _run_flake8(repo_path)
    black_result = _run_black(repo_path)
    isort_result = _run_isort(repo_path)
    
    # CI/CD and structure checks
    cicd = _check_cicd_content(repo_path)
    
    result = {
        # Radon
        "radon_config_found": radon_result["radon_config_found"],
        "radon_team_config": radon_result["radon_team_config"],
        "radon_executed": radon_result["radon_executed"],
        "radon_high_complexity_count": radon_result["radon_high_complexity_count"],
        "radon_avg_complexity": radon_result["radon_avg_complexity"],
        "radon_grade": radon_result["radon_grade"],
        "radon_complexity": radon_result["radon_complexity"],
        
        # Mypy
        "static_typing_enabled": mypy_result["mypy_config_found"],
        "mypy_config_found": mypy_result["mypy_config_found"],
        "mypy_team_config": mypy_result["mypy_team_config"],
        "mypy_executed": mypy_result["mypy_executed"],
        "mypy_error_count": mypy_result["mypy_error_count"],
        "mypy_warning_count": mypy_result["mypy_warning_count"],
        "mypy_errors": mypy_result["mypy_errors"],
        
        # Pylint
        "pylint_config_found": pylint_result["pylint_config_found"],
        "pylint_team_config": pylint_result["pylint_team_config"],
        "pylint_executed": pylint_result["pylint_executed"],
        "pylint_score": pylint_result["pylint_score"],
        "pylint_error_count": pylint_result["pylint_error_count"],
        "pylint_warning_count": pylint_result["pylint_warning_count"],
        "pylint_convention_count": pylint_result["pylint_convention_count"],
        
        # Flake8
        "flake8_config_found": flake8_result["flake8_config_found"],
        "flake8_team_config": flake8_result["flake8_team_config"],
        "flake8_executed": flake8_result["flake8_executed"],
        "flake8_error_count": flake8_result["flake8_error_count"],
        "flake8_errors": flake8_result["flake8_errors"],
        
        # Black
        "black_config_found": black_result["black_config_found"],
        "black_team_config": black_result["black_team_config"],
        "black_executed": black_result["black_executed"],
        "black_formatted_correctly": black_result["black_formatted_correctly"],
        "black_files_to_format": black_result["black_files_to_format"],
        
        # Isort
        "isort_config_found": isort_result["isort_config_found"],
        "isort_team_config": isort_result["isort_team_config"],
        "isort_executed": isort_result["isort_executed"],
        "isort_sorted_correctly": isort_result["isort_sorted_correctly"],
        "isort_files_to_sort": isort_result["isort_files_to_sort"],
        
        # CI/CD
        "cicd_real_content": cicd["cicd_real_content"],
        "cicd_files_found": cicd["cicd_files_found"],
        "cicd_stubs": cicd["cicd_stubs"],
        
        # Structure
        "top_level_dir_count": _count_top_level_dirs(repo_path),

        # Pre-commit
        "pre_commit_config_found": os.path.isfile(
            os.path.join(repo_path, ".pre-commit-config.yaml")
        ),
    }

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the python repository")
    args = parser.parse_args()

    audit_results = run_python_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
