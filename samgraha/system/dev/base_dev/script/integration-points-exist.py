"""integration-points-exist — Category B check for domain 10-feature-technical.

Reads feature-technical docs for integration points and checks if they exist in code.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, find_md_files, walk_source_files


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="integration-points-exist", domain="10-feature-technical", category="B",
            status="error",
            metrics={"integration_points": 0, "found_in_code": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Extract integration points from feature-technical docs
    integration_points: set[str] = set()
    ft_files = find_md_files(repo_root, prefix="10-feature-technical")
    for md_file in ft_files:
        content = md_file.read_text(encoding="utf-8", errors="ignore")

        # Look for code blocks (import/require statements)
        code_block_pattern = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)
        for block_match in code_block_pattern.finditer(content):
            block = block_match.group(1)
            # Extract import sources
            import_pattern = re.compile(r"(?:import|from|require)\s+[\"']([^\"']+)[\"']")
            for m in import_pattern.finditer(block):
                integration_points.add(m.group(1))

        # Look for prose integration keywords
        keyword_pattern = re.compile(
            r"(?:integrates?|connects? to|calls?|imports? from|uses?)\s+[\"']?([A-Za-z_][\w./-]+)",
            re.IGNORECASE,
        )
        for m in keyword_pattern.finditer(content):
            integration_points.add(m.group(1))

    if not integration_points:
        return check_result(
            check="integration-points-exist", domain="10-feature-technical", category="B",
            status="not_applicable",
            metrics={"integration_points": 0, "found_in_code": 0},
            evidence=["No integration points found in feature-technical documentation"],
            repo_fingerprint=fingerprint,
        )

    # Load all code content
    source_files = walk_source_files(repo_root, "*.py;*.js;*.ts;*.go;*.rs;*.java;*.jsx;*.tsx")
    code_content = ""
    for f in source_files:
        try:
            code_content += f.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            continue

    # Check each integration point
    found_in_code: set[str] = set()
    for point in integration_points:
        # Simple substring check
        if point in code_content:
            found_in_code.add(point)

    missing = integration_points - found_in_code

    evidence: list[str] = []
    if missing:
        evidence.append(f"{len(missing)} integration points not found in code:")
        for p in sorted(missing)[:20]:
            evidence.append(f"  {p}")
    else:
        evidence.append(f"All {len(integration_points)} integration points found in code")

    status = "pass" if not missing else "fail"

    return check_result(
        check="integration-points-exist", domain="10-feature-technical", category="B",
        status=status,
        metrics={"integration_points": len(integration_points),
                 "found_in_code": len(found_in_code)},
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
