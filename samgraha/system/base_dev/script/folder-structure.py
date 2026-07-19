"""folder-structure — Category A check for domain 13-implementation.

Compares expected directory structure against actual repo structure.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, EXCLUDE_DIRS


def run_check(
    repo_root: Path,
    fingerprint: str,
    expected_structure: list[str] | None = None,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="folder-structure", domain="13-implementation", category="A",
            status="error",
            metrics={"expected_count": 0, "actual_count": 0, "mismatch_count": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Collect actual directories
    actual_dirs: set[str] = set()
    for dirpath, dirnames, _ in repo_root.walk():
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        rel = dirpath.relative_to(repo_root)
        if str(rel) != ".":
            actual_dirs.add(str(rel).replace("\\", "/"))

    if expected_structure is None:
        # If no expected structure provided, just report what exists
        return check_result(
            check="folder-structure", domain="13-implementation", category="A",
            status="not_applicable",
            metrics={"expected_count": 0, "actual_count": len(actual_dirs),
                     "mismatch_count": 0},
            evidence=["No expected structure defined — use --expected-structure or structure.yaml"],
            repo_fingerprint=fingerprint,
        )

    expected_set = set(expected_structure)

    missing = expected_set - actual_dirs
    unexpected = actual_dirs - expected_set

    evidence: list[str] = []
    for d in sorted(missing):
        evidence.append(f"Missing directory: {d}")
    for d in sorted(unexpected):
        evidence.append(f"Unexpected directory: {d}")

    mismatch_count = len(missing) + len(unexpected)
    status = "pass" if mismatch_count == 0 else "fail"

    return check_result(
        check="folder-structure", domain="13-implementation", category="A",
        status=status,
        metrics={"expected_count": len(expected_set), "actual_count": len(actual_dirs),
                 "mismatch_count": mismatch_count},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--expected-structure", nargs="*", default=None)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.expected_structure)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
