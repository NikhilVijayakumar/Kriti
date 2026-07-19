"""dependency-manifest — Category A check for domain 13-implementation.

Probes for dependency manifest files and parses dependency counts.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


MANIFEST_PROBES = [
    "package.json", "requirements.txt", "Pipfile", "pyproject.toml",
    "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "Gemfile",
    "composer.json",
]


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="dependency-manifest", domain="13-implementation", category="A",
            status="error",
            metrics={"manifests_found": 0, "total_dependencies": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    found: list[str] = []
    dep_count = 0
    evidence: list[str] = []

    for manifest in MANIFEST_PROBES:
        path = repo_root / manifest
        if path.exists():
            found.append(manifest)

            # Parse dependency counts for common formats
            try:
                if manifest == "package.json":
                    data = json.loads(path.read_text(encoding="utf-8"))
                    deps = len(data.get("dependencies", {}))
                    dev_deps = len(data.get("devDependencies", {}))
                    dep_count += deps + dev_deps
                    evidence.append(f"package.json: {deps} deps, {dev_deps} devDeps")

                elif manifest == "requirements.txt":
                    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
                             if l.strip() and not l.startswith("#") and not l.startswith("-")]
                    dep_count += len(lines)
                    evidence.append(f"requirements.txt: {len(lines)} dependencies")

                elif manifest == "pyproject.toml":
                    content = path.read_text(encoding="utf-8")
                    dep_matches = re.findall(r'"([^"]+)"', content)
                    dep_count += len(dep_matches)
                    evidence.append(f"pyproject.toml: {len(dep_matches)} dependencies")

                elif manifest == "go.mod":
                    content = path.read_text(encoding="utf-8")
                    dep_count += content.count("\n\t")
                    evidence.append(f"go.mod: dependencies parsed")

                elif manifest == "Cargo.toml":
                    content = path.read_text(encoding="utf-8")
                    dep_count += content.count("\n")
                    evidence.append(f"Cargo.toml: dependencies parsed")

            except Exception as e:
                evidence.append(f"Error parsing {manifest}: {e}")

    if not found:
        status = "not_applicable"
        evidence = ["No dependency manifest files found"]
    else:
        status = "pass"

    return check_result(
        check="dependency-manifest", domain="13-implementation", category="A",
        status=status,
        metrics={"manifests_found": len(found), "total_dependencies": dep_count},
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
