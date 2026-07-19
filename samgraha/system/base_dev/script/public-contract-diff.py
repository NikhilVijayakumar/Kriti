"""public-contract-diff — Category A check for domain 16-product-guide.

Extracts declared API endpoints from docs and actual routes from code,
then diffs them for mismatches.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, find_md_files, walk_source_files


# Patterns for extracting endpoints from docs
DOC_ENDPOINT_PATTERNS = [
    re.compile(r"(?:GET|POST|PUT|PATCH|DELETE)\s+(/[^\s\)`]+)", re.IGNORECASE),
    re.compile(r"`(?:GET|POST|PUT|PATCH|DELETE)\s+([^\s\)`]+)`", re.IGNORECASE),
]

# Patterns for extracting routes from code
CODE_ROUTE_PATTERNS = [
    # Express
    re.compile(r"(?:app|router)\.(get|post|put|patch|delete)\s*\(\s*[\"']([^\"']+)[\"']"),
    # Flask
    re.compile(r"@(?:app|bp)\.route\s*\(\s*[\"']([^\"']+)[\"']"),
    # Go
    re.compile(r'(?:HandleFunc|Handle)\s*\(\s*"([^"]+)"'),
    # FastAPI
    re.compile(r"@(?:app|router)\.(get|post|put|patch|delete)\s*\(\s*[\"']([^\"']+)[\"']"),
]


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="public-contract-diff", domain="16-product-guide", category="A",
            status="error",
            metrics={"doc_endpoints": 0, "code_routes": 0, "mismatches": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Extract endpoints from docs
    doc_endpoints: set[str] = set()
    md_files = find_md_files(repo_root)
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        for pattern in DOC_ENDPOINT_PATTERNS:
            for match in pattern.finditer(content):
                endpoint = match.group(1).rstrip(".,;:)")
                doc_endpoints.add(endpoint)

    # Extract routes from code
    code_routes: set[str] = set()
    source_files = walk_source_files(repo_root, "*.py;*.js;*.ts;*.go;*.java")
    for src in source_files:
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pattern in CODE_ROUTE_PATTERNS:
            for match in pattern.finditer(content):
                groups = match.groups()
                # Different patterns return different group counts
                if len(groups) == 2:
                    route = groups[1] if groups[0].lower() in ("get", "post", "put", "patch", "delete") else groups[0]
                else:
                    route = groups[0]
                code_routes.add(route)

    # Diff
    documented_not_in_code = doc_endpoints - code_routes
    code_not_documented = code_routes - doc_endpoints

    evidence: list[str] = []
    if documented_not_in_code:
        evidence.append(f"Documented but not in code ({len(documented_not_in_code)}):")
        for ep in sorted(documented_not_in_code):
            evidence.append(f"  {ep}")
    if code_not_documented:
        evidence.append(f"In code but not documented ({len(code_not_documented)}):")
        for route in sorted(code_not_documented):
            evidence.append(f"  {route}")

    if not evidence:
        evidence.append(f"All {len(doc_endpoints)} documented endpoints match code routes")

    mismatches = len(documented_not_in_code) + len(code_not_documented)
    status = "pass" if mismatches == 0 else "fail"

    return check_result(
        check="public-contract-diff", domain="16-product-guide", category="A",
        status=status,
        metrics={"doc_endpoints": len(doc_endpoints), "code_routes": len(code_routes),
                 "mismatches": mismatches},
        evidence=evidence, repo_fingerprint=fingerprint,
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
