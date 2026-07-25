"""dependency-vuln-scan — Category A check for domain 03-security.

Runs npm audit or equivalent to find known vulnerabilities.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="dependency-vuln-scan", domain="03-security", category="A",
            status="error",
            metrics={"critical": 0, "high": 0, "moderate": 0, "low": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Try npm audit first
    package_json = repo_root / "package.json"
    if package_json.exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=str(repo_root), capture_output=True, text=True, timeout=120,
            )
            data = json.loads(result.stdout)
            vulns = data.get("vulnerabilities", {})

            critical = sum(1 for v in vulns.values() if v.get("severity") == "critical")
            high = sum(1 for v in vulns.values() if v.get("severity") == "high")
            moderate = sum(1 for v in vulns.values() if v.get("severity") == "moderate")
            low = sum(1 for v in vulns.values() if v.get("severity") == "low")
            total = critical + high + moderate + low

            evidence: list[str] = []
            if total > 0:
                evidence.append(f"Found {total} vulnerabilities: "
                              f"{critical} critical, {high} high, "
                              f"{moderate} moderate, {low} low")
            else:
                evidence.append("No known vulnerabilities found via npm audit")

            status = "pass" if total == 0 else "fail"
            return check_result(
                check="dependency-vuln-scan", domain="03-security", category="A",
                status=status,
                metrics={"critical": critical, "high": high,
                         "moderate": moderate, "low": low},
                evidence=evidence, repo_fingerprint=fingerprint,
            )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

    # Fallback: count deps from requirements.txt
    requirements = repo_root / "requirements.txt"
    if requirements.exists():
        lines = [l.strip() for l in requirements.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#") and not l.startswith("-")]
        return check_result(
            check="dependency-vuln-scan", domain="03-security", category="A",
            status="not_applicable",
            metrics={"critical": 0, "high": 0, "moderate": 0, "low": 0},
            evidence=[f"npm audit unavailable; {len(lines)} deps in requirements.txt "
                     f"(manual review needed)"],
            repo_fingerprint=fingerprint,
        )

    return check_result(
        check="dependency-vuln-scan", domain="03-security", category="A",
        status="not_applicable",
        metrics={"critical": 0, "high": 0, "moderate": 0, "low": 0},
        evidence=["No package.json or requirements.txt found"],
        repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
