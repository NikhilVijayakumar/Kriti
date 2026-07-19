"""lint-standards — Category A check for domain 07-engineering.

Probes for lint config files and runs the lint command.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


LINT_CONFIGS = [
    ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml",
    ".pylintrc", ".flake8", "setup.cfg", ".golangci.yml",
    ".rubocop.yml", ".stylelintrc", "biome.json",
]

DEFAULT_LINT_COMMAND = "npm run lint"


def run_check(
    repo_root: Path,
    fingerprint: str,
    lint_command: str = DEFAULT_LINT_COMMAND,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="lint-standards", domain="07-engineering", category="A",
            status="error",
            metrics={"configs_found": 0, "lint_exit_code": -1, "error_count": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Probe for lint configs
    configs_found: list[str] = []
    for config in LINT_CONFIGS:
        if (repo_root / config).exists():
            configs_found.append(config)

    if not configs_found:
        return check_result(
            check="lint-standards", domain="07-engineering", category="A",
            status="not_applicable",
            metrics={"configs_found": 0, "lint_exit_code": 0, "error_count": 0},
            evidence=["No lint configuration files found"],
            repo_fingerprint=fingerprint,
        )

    # Run lint
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
        exit_code = result.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError):
        exit_code = -1

    # Count errors
    output = result.stdout + result.stderr
    error_count = len(re.findall(r"\d+ error|error\[|Error:|ERROR", output))

    evidence: list[str] = [f"Lint configs found: {', '.join(configs_found)}"]
    if exit_code != 0:
        evidence.append(f"Lint failed with exit code {exit_code}")

    status = "pass" if exit_code == 0 else "fail"

    return check_result(
        check="lint-standards", domain="07-engineering", category="A",
        status=status,
        metrics={"configs_found": len(configs_found), "lint_exit_code": exit_code,
                 "error_count": error_count},
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
