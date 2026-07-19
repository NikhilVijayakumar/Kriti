"""unit-test-coverage — Category A check for domain 12-qa.

Counts source files and checks if each has a corresponding test file.
Reports coverage percentage.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, walk_source_files, EXCLUDE_DIRS


SOURCE_PATTERNS = "*.ts;*.js;*.py;*.go;*.rs;*.java;*.cs"
TEST_PATTERNS = "*.test.*;*.spec.*;*_test.*;test_*.py;tests_*.py"
DEFAULT_THRESHOLD = 80


def run_check(
    repo_root: Path,
    fingerprint: str,
    source_include: str = SOURCE_PATTERNS,
    test_include: str = TEST_PATTERNS,
    threshold: int = DEFAULT_THRESHOLD,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="unit-test-coverage", domain="12-qa", category="A",
            status="error",
            metrics={"source_files": 0, "tested_files": 0, "coverage_percent": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    source_files = walk_source_files(repo_root, source_include)
    test_files = walk_source_files(repo_root, test_include)

    source_count = len(source_files)
    tested_count = 0
    untested: list[str] = []

    for src in source_files:
        src_base = src.stem
        src_dir = src.parent
        has_test = any(
            t.parent == src_dir and src_base in t.stem
            for t in test_files
        )
        if has_test:
            tested_count += 1
        else:
            untested.append(str(src.relative_to(repo_root)))

    if source_count == 0:
        return check_result(
            check="unit-test-coverage", domain="12-qa", category="A",
            status="not_applicable",
            metrics={"source_files": 0, "tested_files": 0, "coverage_percent": 0},
            evidence=[f"No source files found matching patterns: {source_include}"],
            repo_fingerprint=fingerprint,
        )

    pct = round((tested_count / source_count) * 100, 1)
    evidence: list[str] = []

    if pct < threshold:
        evidence.append(f"Coverage {pct}% is below threshold {threshold}%")
        for f in untested[:20]:
            evidence.append(f"  No test: {f}")
        if len(untested) > 20:
            evidence.append(f"  ... and {len(untested) - 20} more untested files")

    status = "pass" if pct >= threshold else "fail"

    return check_result(
        check="unit-test-coverage", domain="12-qa", category="A",
        status=status,
        metrics={"source_files": source_count, "tested_files": tested_count,
                 "coverage_percent": pct},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--source-include", default=SOURCE_PATTERNS)
    parser.add_argument("--test-include", default=TEST_PATTERNS)
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    args = parser.parse_args()

    result = run_check(
        Path(args.repo_root), args.repo_fingerprint,
        args.source_include, args.test_include, args.threshold,
    )
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
