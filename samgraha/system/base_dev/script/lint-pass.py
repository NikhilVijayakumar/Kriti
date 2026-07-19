"""lint-pass — Category A check for domain 13-implementation.

Runs the project's lint command and reports exit code.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


DEFAULT_LINT_COMMAND = "npm run lint"


def run_check(
    repo_root: Path,
    fingerprint: str,
    lint_command: str = DEFAULT_LINT_COMMAND,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="lint-pass", domain="13-implementation", category="A",
            status="error",
            metrics={"lint_exit_code": -1, "error_count": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    start = time.monotonic()
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                lint_command, shell=True, cwd=str(repo_root),
                capture_output=True, text=True, timeout=300,
            )
        else:
            result = subprocess.run(
                ["bash", "-c", lint_command], cwd=str(repo_root),
                capture_output=True, text=True, timeout=300,
            )
        duration = round(time.monotonic() - start, 2)
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        return check_result(
            check="lint-pass", domain="13-implementation", category="A",
            status="error",
            metrics={"lint_exit_code": -1, "error_count": 0},
            evidence=[f"Lint command timed out after 300s: {lint_command}"],
            repo_fingerprint=fingerprint,
        )
    except Exception as e:
        return check_result(
            check="lint-pass", domain="13-implementation", category="A",
            status="error",
            metrics={"lint_exit_code": -1, "error_count": 0},
            evidence=[f"Lint command failed: {e}"],
            repo_fingerprint=fingerprint,
        )

    # Count error patterns in output
    import re
    error_patterns = [r"\d+ error", r"error\[", r"Error:", r"ERROR"]
    error_count = 0
    for pattern in error_patterns:
        error_count += len(re.findall(pattern, result.stdout + result.stderr))

    evidence: list[str] = []
    if exit_code != 0:
        evidence.append(f"Lint failed with exit code {exit_code}")
        stderr_lines = result.stderr.strip().split("\n")[-15:]
        for line in stderr_lines:
            evidence.append(f"  {line}")

    status = "pass" if exit_code == 0 else "fail"

    return check_result(
        check="lint-pass", domain="13-implementation", category="A",
        status=status,
        metrics={"lint_exit_code": exit_code, "error_count": error_count},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--lint-command", default=DEFAULT_LINT_COMMAND)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.lint_command)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
