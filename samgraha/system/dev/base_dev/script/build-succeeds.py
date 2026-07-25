"""build-succeeds — Category A check for domain 14-build.

Runs the project's build command and reports exit code and duration.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


DEFAULT_BUILD_COMMAND = "npm run build"


def run_check(
    repo_root: Path,
    fingerprint: str,
    build_command: str = DEFAULT_BUILD_COMMAND,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="build-succeeds", domain="14-build", category="A",
            status="error",
            metrics={"build_exit_code": -1, "build_duration_seconds": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    start = time.monotonic()
    try:
        # Detect shell based on platform
        if sys.platform == "win32":
            result = subprocess.run(
                build_command, shell=True, cwd=str(repo_root),
                capture_output=True, text=True, timeout=600,
            )
        else:
            result = subprocess.run(
                ["bash", "-c", build_command], cwd=str(repo_root),
                capture_output=True, text=True, timeout=600,
            )
        duration = round(time.monotonic() - start, 2)
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        duration = 600
        exit_code = -1
        return check_result(
            check="build-succeeds", domain="14-build", category="A",
            status="error",
            metrics={"build_exit_code": exit_code, "build_duration_seconds": duration},
            evidence=[f"Build command timed out after 600s: {build_command}"],
            repo_fingerprint=fingerprint,
        )
    except Exception as e:
        duration = round(time.monotonic() - start, 2)
        return check_result(
            check="build-succeeds", domain="14-build", category="A",
            status="error",
            metrics={"build_exit_code": -1, "build_duration_seconds": duration},
            evidence=[f"Build command failed: {e}"],
            repo_fingerprint=fingerprint,
        )

    evidence: list[str] = []
    if exit_code != 0:
        evidence.append(f"Build failed with exit code {exit_code}")
        stderr_lines = result.stderr.strip().split("\n")[-15:]
        for line in stderr_lines:
            evidence.append(f"  {line}")

    status = "pass" if exit_code == 0 else "fail"

    return check_result(
        check="build-succeeds", domain="14-build", category="A",
        status=status,
        metrics={"build_exit_code": exit_code, "build_duration_seconds": duration},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--build-command", default=DEFAULT_BUILD_COMMAND)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.build_command)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
