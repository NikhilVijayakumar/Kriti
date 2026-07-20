import subprocess
import json
import argparse
import os
import glob


def _run_tool(cmd, timeout=60):
    """Run a tool command, return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return -1, "", "tool not available"


def run_python_audit(repo_path):
    """
    Checks for Python static analysis configurations (Radon, Bandit, Mypy)
    and executes radon/mypy if installed. Bandit is owned by audit_security.py.
    """
    result = {
        "static_typing_enabled": False,
        "radon_config_found": False,
        "bandit_config_found": False,
        # New: actual tool execution results
        "radon_executed": False,
        "radon_complexity": None,  # dict of function -> complexity
        "radon_high_complexity_count": 0,
        "mypy_executed": False,
        "mypy_error_count": 0,
        "mypy_errors": [],
    }

    # 1. Check Configurations
    pyproject_path = os.path.join(repo_path, "pyproject.toml")
    radon_cfg = os.path.join(repo_path, "radon.cfg")
    bandit_cfg = os.path.join(repo_path, ".bandit")

    if os.path.exists(radon_cfg):
        result["radon_config_found"] = True

    if os.path.exists(bandit_cfg):
        result["bandit_config_found"] = True

    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "tool.mypy" in content or "tool.pyright" in content:
                result["static_typing_enabled"] = True
            if "tool.radon" in content:
                result["radon_config_found"] = True
            if "tool.bandit" in content:
                result["bandit_config_found"] = True
        except OSError:
            pass

    # 2. Run radon for cyclomatic complexity
    rc, stdout, _ = _run_tool(
        ["python", "-m", "radon", "cc", repo_path, "-j", "--no-assert"],
        timeout=60,
    )
    if rc == 0 and stdout.strip():
        try:
            data = json.loads(stdout)
            # data is a dict of filepath -> list of blocks
            high_complexity = []
            for filepath, blocks in data.items():
                if not isinstance(blocks, list):
                    continue
                for block in blocks:
                    if isinstance(block, dict):
                        grade = block.get("grade", "")
                        complexity = block.get("complexity", 0)
                        name = block.get("name", "")
                        # Grade A/B = low complexity, C+ = concerning
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
                "high_complexity_functions": high_complexity[:20],  # cap at 20
                "total_files_analyzed": len(data),
            }
        except json.JSONDecodeError:
            pass

    # 3. Run mypy for type checking
    mypy_cfg = os.path.join(repo_path, "mypy.ini")
    cmd = ["python", "-m", "mypy", repo_path, "--ignore-missing-imports", "--no-error-summary"]
    if os.path.exists(mypy_cfg):
        cmd = ["python", "-m", "mypy", "--config-file", mypy_cfg, repo_path, "--no-error-summary"]
    elif os.path.exists(pyproject_path):
        # If pyproject has [tool.mypy], mypy picks it up automatically
        cmd = ["python", "-m", "mypy", repo_path, "--ignore-missing-imports", "--no-error-summary"]

    rc, stdout, _ = _run_tool(cmd, timeout=60)
    if rc >= 0 and stdout.strip():
        lines = [l for l in stdout.strip().splitlines() if l.strip()]
        errors = [l for l in lines if ": error:" in l]
        result["mypy_executed"] = True
        result["mypy_error_count"] = len(errors)
        result["mypy_errors"] = errors[:20]  # cap at 20

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the python repository")
    args = parser.parse_args()

    audit_results = run_python_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
