"""validate.py — Invokes the 18 check scripts and aggregates results.

Reads script/mapping.yaml for check→domain mappings, discovers check scripts
by name, runs each one, and collects results into a findings array.

Usage:
  python validate.py --system-root <path> --repo-root <path> --out <path>
  python validate.py --system-root <path> --repo-root <path> --out <path> --domain <domain>
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from _common import (
    load_yaml, write_json, compute_fingerprint, utc_now_iso, ALL_DOMAINS,
)


# ---------------------------------------------------------------------------
# Check discovery
# ---------------------------------------------------------------------------

SCRIPT_EXTENSIONS = [".py", ".ps1", ".sh"]

CHECK_SEARCH_DIRS = [
    Path("script"),  # Relative to system root
]


def discover_check_script(system_root: Path, check_name: str) -> Path | None:
    """Find a check script by name, preferring .py over .ps1/.sh."""
    for search_dir in CHECK_SEARCH_DIRS:
        base = system_root / search_dir
        for ext in SCRIPT_EXTENSIONS:
            candidate = base / f"{check_name}{ext}"
            if candidate.exists():
                return candidate

        # Also check domain-specific subdirectories
        for domain_dir in base.iterdir():
            if domain_dir.is_dir():
                for ext in SCRIPT_EXTENSIONS:
                    candidate = domain_dir / f"{check_name}{ext}"
                    if candidate.exists():
                        return candidate

    return None


def get_check_timeout(system_root: Path, check_name: str) -> int:
    """Read timeout from the check's manifest file."""
    schema_dir = system_root / "script" / "schema"
    for manifest in schema_dir.rglob(f"{check_name}.manifest.yaml"):
        data = load_yaml(manifest)
        return data.get("timeout_seconds", 300)
    return 300


# ---------------------------------------------------------------------------
# Script execution
# ---------------------------------------------------------------------------

def run_check(
    script_path: Path,
    repo_root: Path,
    docs_root: Path | None,
    fingerprint: str,
    timeout: int,
) -> dict[str, Any] | None:
    """Run a single check script and return its JSON output."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp:
        out_path = Path(tmp.name)

    try:
        # Build command based on script type
        if script_path.suffix == ".py":
            cmd = [
                sys.executable, str(script_path),
                "--repo-root", str(repo_root),
                "--repo-fingerprint", fingerprint,
                "--out", str(out_path),
            ]
            if docs_root:
                cmd.extend(["--docs-root", str(docs_root)])
        elif script_path.suffix == ".ps1":
            cmd = [
                "powershell", "-ExecutionPolicy", "Bypass",
                "-File", str(script_path),
                "-RepoRoot", str(repo_root),
                "-RepoFingerprint", fingerprint,
                "-Out", str(out_path),
            ]
            if docs_root:
                cmd.extend(["-DocsRoot", str(docs_root)])
        elif script_path.suffix == ".sh":
            cmd = [
                "bash", str(script_path),
                "--repo-root", str(repo_root),
                "--repo-fingerprint", fingerprint,
                "--out", str(out_path),
            ]
            if docs_root:
                cmd.extend(["--docs-root", str(docs_root)])
        else:
            return None

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if out_path.exists():
            from _common import load_json
            return load_json(out_path)
        else:
            return {
                "check": script_path.stem,
                "domain": "_unknown",
                "category": "A",
                "status": "error",
                "metrics": {},
                "evidence": [f"Script produced no output. stderr: {result.stderr[:500]}"],
                "executed_at": utc_now_iso(),
                "repo_fingerprint": fingerprint,
            }

    except subprocess.TimeoutExpired:
        return {
            "check": script_path.stem,
            "domain": "_unknown",
            "category": "A",
            "status": "error",
            "metrics": {},
            "evidence": [f"Script timed out after {timeout}s"],
            "executed_at": utc_now_iso(),
            "repo_fingerprint": fingerprint,
        }
    except Exception as e:
        return {
            "check": script_path.stem,
            "domain": "_unknown",
            "category": "A",
            "status": "error",
            "metrics": {},
            "evidence": [f"Script execution error: {e}"],
            "executed_at": utc_now_iso(),
            "repo_fingerprint": fingerprint,
        }
    finally:
        out_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Main validation
# ---------------------------------------------------------------------------

def validate(
    system_root: Path,
    repo_root: Path,
    docs_root: Path | None = None,
    target_domain: str | None = None,
) -> dict[str, Any]:
    """Run all applicable checks and return aggregated results."""
    mapping = load_yaml(system_root / "script" / "mapping.yaml")
    fingerprint = compute_fingerprint(repo_root)

    findings: list[dict[str, Any]] = []
    checks_run = 0
    checks_skipped = 0
    checks_error = 0

    for entry in mapping.get("mappings", []):
        check_name = entry["check"]
        check_domain = entry["domain"]
        category = entry.get("category", "A")

        # Filter by target domain if specified
        if target_domain:
            if check_domain != "_generic" and check_domain != target_domain:
                checks_skipped += 1
                continue

        # Discover script
        script = discover_check_script(system_root, check_name)
        if script is None:
            findings.append({
                "check": check_name,
                "domain": check_domain,
                "category": category,
                "status": "error",
                "metrics": {},
                "evidence": [f"No script found for check '{check_name}'"],
                "executed_at": utc_now_iso(),
                "repo_fingerprint": fingerprint,
            })
            checks_error += 1
            continue

        # Get timeout
        timeout = get_check_timeout(system_root, check_name)

        # Run check
        result = run_check(script, repo_root, docs_root, fingerprint, timeout)
        if result:
            findings.append(result)
            checks_run += 1
            if result["status"] == "error":
                checks_error += 1
        else:
            checks_error += 1

    # Compute summary
    passed = sum(1 for f in findings if f["status"] == "pass")
    failed = sum(1 for f in findings if f["status"] == "fail")
    not_applicable = sum(1 for f in findings if f["status"] == "not_applicable")

    return {
        "validated_at": utc_now_iso(),
        "repo_fingerprint": fingerprint,
        "summary": {
            "checks_run": checks_run,
            "checks_skipped": checks_skipped,
            "checks_error": checks_error,
            "passed": passed,
            "failed": failed,
            "not_applicable": not_applicable,
            "total_findings": len(findings),
        },
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run audit check scripts")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--repo-root", required=True, help="Repository root to audit")
    parser.add_argument("--docs-root", help="Documentation root (for generic checks)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--domain", help="Run checks for a specific domain only")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    repo_root = Path(args.repo_root)

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)
    if not repo_root.is_dir():
        print(f"Error: repo-root not found: {repo_root}", file=sys.stderr)
        sys.exit(1)

    result = validate(
        system_root,
        repo_root,
        Path(args.docs_root) if args.docs_root else None,
        args.domain,
    )

    write_json(Path(args.out), result)

    # Print summary
    s = result["summary"]
    print(f"Validation complete: {s['passed']} passed, {s['failed']} failed, "
          f"{s['not_applicable']} N/A, {s['checks_error']} errors "
          f"({s['checks_run']} run, {s['checks_skipped']} skipped)")


if __name__ == "__main__":
    main()
