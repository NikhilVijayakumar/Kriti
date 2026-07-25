"""module-boundary-diff — Category A check for domain 05-architecture.

Scans source files for cross-module imports that violate architecture boundaries.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, walk_source_files, EXCLUDE_DIRS


IMPORT_PATTERNS = [
    re.compile(r"(?:import|from)\s+[\"']([^\"']+)[\"']"),
    re.compile(r"require\s*\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"from\s+[\"']([^\"']+)[\"']"),
]


def run_check(
    repo_root: Path,
    fingerprint: str,
    modules: list[str] | None = None,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="module-boundary-diff", domain="05-architecture", category="A",
            status="error",
            metrics={"modules_checked": 0, "violations": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    if not modules:
        # Auto-detect modules from top-level directories
        modules = []
        for item in repo_root.iterdir():
            if item.is_dir() and item.name not in EXCLUDE_DIRS and not item.name.startswith("."):
                modules.append(item.name)

    violations = 0
    evidence: list[str] = []

    for module_name in modules:
        module_dir = repo_root / module_name
        if not module_dir.is_dir():
            continue

        source_files = walk_source_files(module_dir, "*.py;*.js;*.ts;*.go;*.rs;*.java")

        for src in source_files:
            try:
                content = src.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            for line_no, line in enumerate(content.split("\n"), 1):
                for pattern in IMPORT_PATTERNS:
                    for match in pattern.finditer(line):
                        imported = match.group(1)
                        # Check if import targets another module
                        for other_module in modules:
                            if (other_module != module_name and
                                    (imported.startswith(other_module + "/") or
                                     imported.startswith(other_module + "."))):
                                rel = str(src.relative_to(repo_root))
                                evidence.append(
                                    f"Boundary violation: {rel}:{line_no} "
                                    f"imports from '{other_module}' in module '{module_name}'"
                                )
                                violations += 1
                                break

    status = "pass" if violations == 0 else "fail"

    return check_result(
        check="module-boundary-diff", domain="05-architecture", category="A",
        status=status,
        metrics={"modules_checked": len(modules), "violations": violations},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--modules", nargs="*", default=None)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint, args.modules)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
