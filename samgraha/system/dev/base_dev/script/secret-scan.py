"""secret-scan — Category A check for domain 03-security.

Scans source files for potential secrets using regex patterns.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, walk_source_files


SECRET_PATTERNS = [
    ("AWS Key", r"AKIA[0-9A-Z]{16}"),
    ("Private Key", r"-----BEGIN.*PRIVATE KEY-----"),
    ("Password Assignment", r"(?i)password\s*[:=]\s*[\"'][^\"']+[\"']"),
    ("API Key Assignment", r"(?i)api[_-]?key\s*[:=]\s*[\"'][^\"']+[\"']"),
    ("Token Assignment", r"(?i)token\s*[:=]\s*[\"'][^\"']+[\"']"),
    ("Secret Assignment", r"(?i)secret\s*[:=]\s*[\"'][^\"']+[\"']"),
]

DEFAULT_SCAN_INCLUDE = "*.ts;*.js;*.py;*.go;*.java;*.cs;*.env;*.yml;*.yaml;*.json;*.toml;*.xml;*.config;*.cfg;*.ini;*.properties"


def run_check(
    repo_root: Path,
    fingerprint: str,
    scan_include: str = DEFAULT_SCAN_INCLUDE,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="secret-scan", domain="03-security", category="A",
            status="error",
            metrics={"secrets_found": 0, "files_scanned": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    files = walk_source_files(repo_root, scan_include)
    files_scanned = 0
    secrets_found = 0
    findings: list[str] = []

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if not content:
            continue

        files_scanned += 1
        for name, pattern in SECRET_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                rel = str(fpath.relative_to(repo_root))
                findings.append(f"{name} in {rel}")
                secrets_found += len(matches)

    evidence: list[str] = []
    if secrets_found == 0:
        evidence.append(f"No secrets found in {files_scanned} files")
    else:
        evidence.append(f"Found {secrets_found} potential secrets in {files_scanned} files")
        for f in findings[:20]:
            evidence.append(f"  {f}")

    status = "pass" if secrets_found == 0 else "fail"

    return check_result(
        check="secret-scan", domain="03-security", category="A",
        status=status,
        metrics={"secrets_found": secrets_found, "files_scanned": files_scanned},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--scan-include", default=DEFAULT_SCAN_INCLUDE)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.scan_include)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
