"""artifact-exists — Category A check for domain 14-build.

Tests whether the build artifact path exists and reports its size.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


DEFAULT_ARTIFACT_PATH = "dist"


def run_check(
    repo_root: Path,
    fingerprint: str,
    artifact_path: str = DEFAULT_ARTIFACT_PATH,
) -> dict:
    target = repo_root / artifact_path

    if not target.exists():
        return check_result(
            check="artifact-exists", domain="14-build", category="A",
            status="fail",
            metrics={"exists": False, "is_directory": False, "file_count": 0,
                     "total_size_bytes": 0},
            evidence=[f"Artifact path does not exist: {artifact_path}"],
            repo_fingerprint=fingerprint,
        )

    is_dir = target.is_dir()
    if is_dir:
        files = list(target.rglob("*"))
        file_count = sum(1 for f in files if f.is_file())
        total_size = sum(f.stat().st_size for f in files if f.is_file())
    else:
        file_count = 1
        total_size = target.stat().st_size

    evidence = [f"Artifact found: {artifact_path} ({file_count} files, {total_size} bytes)"]

    return check_result(
        check="artifact-exists", domain="14-build", category="A",
        status="pass",
        metrics={"exists": True, "is_directory": is_dir, "file_count": file_count,
                 "total_size_bytes": total_size},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--artifact-path", default=DEFAULT_ARTIFACT_PATH)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.artifact_path)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
