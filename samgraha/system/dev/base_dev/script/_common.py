"""Shared utilities for base_dev scripts.

Provides: YAML/JSON I/O, fingerprinting, path resolution, CLI arg parsing,
and the check-script output contract used by all 18 audit checks.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOMAIN_NUMS: dict[str, str] = {
    "01": "vision",
    "02": "philosophy",
    "03": "security",
    "04": "feature",
    "05": "architecture",
    "06": "design",
    "07": "engineering",
    "08": "external-context",
    "09": "feature-design",
    "10": "feature-technical",
    "11": "prototype",
    "12": "qa",
    "13": "implementation",
    "14": "build",
    "15": "readme",
    "16": "product-guide",
}

ALL_DOMAINS: list[str] = [
    f"{num}-{name}" for num, name in DOMAIN_NUMS.items()
]

DOMAIN_PREFIX: dict[str, str] = {
    name: num for num, name in DOMAIN_NUMS.items()
}


def resolve_domain(domain: str) -> str:
    """Resolve bare domain name to prefixed form (e.g. 'vision' -> '01-vision').
    If already prefixed, return as-is."""
    if domain in DOMAIN_PREFIX:
        return f"{DOMAIN_PREFIX[domain]}-{domain}"
    return domain

EXCLUDE_DIRS: set[str] = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".opencode", "vendor", "coverage",
    ".next", ".nuxt", "target", ".samgraha",
}


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> Any:
    """Load a YAML file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path: Path, data: Any) -> None:
    """Write data to a YAML file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def load_json(path: Path) -> Any:
    """Load a JSON file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    """Write data to a JSON file with pretty formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        f.write("\n")


def read_text(path: Path) -> str:
    """Read a text file and return its contents."""
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write text content to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Fingerprinting
# ---------------------------------------------------------------------------

def compute_fingerprint(repo_root: Path) -> str:
    """Compute a SHA-256 fingerprint of the repo's git HEAD tree.

    Falls back to a directory hash if not a git repo.
    """
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:16]
    except Exception:
        pass

    # Fallback: hash directory listing
    h = hashlib.sha256()
    for p in sorted(repo_root.rglob("*")):
        if p.is_file() and not any(d in p.parts for d in EXCLUDE_DIRS):
            h.update(str(p.relative_to(repo_root)).encode())
    return h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# Timestamp
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Check script output contract
# ---------------------------------------------------------------------------

def check_result(
    *,
    check: str,
    domain: str,
    category: str,
    status: str,
    metrics: dict[str, Any],
    evidence: list[str],
    repo_fingerprint: str,
) -> dict[str, Any]:
    """Build a check-result dict matching schema.json."""
    return {
        "check": check,
        "domain": domain,
        "category": category,
        "status": status,
        "metrics": metrics,
        "evidence": evidence,
        "executed_at": utc_now_iso(),
        "repo_fingerprint": repo_fingerprint,
    }


def write_check_result(out: Path, result: dict[str, Any], exit_on_error: bool = True) -> None:
    """Write a check result to the output file."""
    write_json(out, result)
    if exit_on_error and result["status"] == "error":
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def check_common_args(parser: argparse.ArgumentParser) -> None:
    """Add the standard --repo-root, --repo-fingerprint, --out arguments."""
    parser.add_argument("--repo-root", required=True, help="Repository root path")
    parser.add_argument("--repo-fingerprint", required=True, help="Repo fingerprint string")
    parser.add_argument("--out", required=True, help="Output JSON file path")


def parse_check_args() -> argparse.Namespace:
    """Parse common check-script arguments."""
    parser = argparse.ArgumentParser()
    check_common_args(parser)
    return parser.parse_args()


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

def walk_source_files(
    root: Path,
    include: str = "*.py",
    exclude_dirs: set[str] | None = None,
) -> list[Path]:
    """Walk a directory tree and return files matching include patterns.

    Args:
        root: Root directory to scan.
        include: Semicolon-separated glob patterns (e.g. "*.py;*.js").
        exclude_dirs: Directory names to skip.
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS

    patterns = [p.strip() for p in include.split(";") if p.strip()]
    results: list[Path] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            for pat in patterns:
                if fpath.match(pat):
                    results.append(fpath)
                    break
    return results


def find_files_by_pattern(root: Path, patterns: list[str]) -> list[Path]:
    """Find files matching any of the given glob patterns (non-recursive first level)."""
    results: list[Path] = []
    for pat in patterns:
        results.extend(root.glob(pat))
    return results


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def extract_section(content: str, heading: str) -> str | None:
    """Extract content under a markdown heading (## level) until next ## or EOF."""
    pattern = rf"(?m)^## {re.escape(heading)}\s*$"
    match = re.search(pattern, content)
    if not match:
        return None

    start = match.end()
    next_heading = re.search(r"(?m)^## ", content[start:])
    end = start + next_heading.start() if next_heading else len(content)
    return content[start:end].strip()


def extract_table_rows(content: str, header_pattern: str) -> list[dict[str, str]]:
    """Extract rows from a markdown table whose header matches the pattern.

    Returns list of dicts keyed by cleaned header names.
    """
    lines = content.split("\n")
    header_idx = None
    for i, line in enumerate(lines):
        if re.search(header_pattern, line):
            header_idx = i
            break

    if header_idx is None:
        return []

    # Parse header columns
    headers = [c.strip() for c in lines[header_idx].split("|") if c.strip()]

    # Skip separator line
    sep_idx = header_idx + 1
    if sep_idx < len(lines) and re.match(r"^\|[\s:-]+", lines[sep_idx]):
        data_start = sep_idx + 1
    else:
        data_start = sep_idx

    rows = []
    for line in lines[data_start:]:
        if not line.strip().startswith("|"):
            break
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) >= len(headers):
            rows.append(dict(zip(headers, cols)))

    return rows


def find_md_files(root: Path, prefix: str = "") -> list[Path]:
    """Find all .md files under root, optionally filtered by filename prefix."""
    results: list[Path] = []
    for p in root.rglob("*.md"):
        if prefix and not p.name.startswith(prefix):
            continue
        results.append(p)
    return sorted(results)


# ---------------------------------------------------------------------------
# Tier loading
# ---------------------------------------------------------------------------

def load_tiers(system_root: Path | None = None) -> dict[str, Any]:
    """Load tiers.yaml from the base_dev system.

    If system_root is provided, loads from plan/core/tiers.yaml under it.
    Otherwise, loads relative to this file's parent (script/ → ../plan/core/).
    """
    if system_root:
        tiers_path = system_root / "plan" / "core" / "tiers.yaml"
    else:
        tiers_path = Path(__file__).parent.parent / "plan" / "core" / "tiers.yaml"
    if tiers_path.exists():
        return load_yaml(tiers_path)
    return {"tiers": []}
