import json
import argparse
import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root


def run_documentation_audit(repo_path):
    """
    Checks for documentation artifacts: README presence, structure, and link validity.
    External links are treated as unverifiable (offline-only standard).
    """
    repo_path = resolve_code_root(repo_path)
    result = {
        "readme_present": False,
        "readme_has_installation_section": False,
        "readme_has_setup_section": False,
        "readme_has_usage_section": False,
        "readme_length_chars": 0,
        "local_links_valid": True,
        "local_links_broken": [],
        "external_links_count": 0,
        "docs_directory_present": False,
    }

    # Check for README variants
    readme_path = None
    for name in ("README.md", "README.rst", "README.txt", "README", "readme.md"):
        candidate = os.path.join(repo_path, name)
        if os.path.isfile(candidate):
            readme_path = candidate
            break

    if not readme_path:
        return result

    result["readme_present"] = True

    try:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return result

    result["readme_length_chars"] = len(content)

    # Check for common section headings (case-insensitive)
    content_lower = content.lower()
    for section in ("installation", "setup", "install"):
        if re.search(rf"^#+\s*{section}", content_lower, re.MULTILINE):
            if section == "installation":
                result["readme_has_installation_section"] = True
            else:
                result["readme_has_setup_section"] = True

    for section in ("usage", "getting started", "quick start"):
        if re.search(rf"^#+\s*{section}", content_lower, re.MULTILINE):
            result["readme_has_usage_section"] = True
            break

    # Extract and validate links
    link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")
    links = link_pattern.findall(content)

    for link in links:
        if link.startswith(("http://", "https://", "mailto:")):
            result["external_links_count"] += 1
            continue

        # Local link — resolve relative to repo root
        # Strip anchor (#section)
        clean_link = link.split("#")[0]
        if not clean_link:
            continue
        target = os.path.join(repo_path, clean_link)
        if not os.path.exists(target):
            result["local_links_valid"] = False
            result["local_links_broken"].append(link)

    # Check for docs/ directory
    docs_dir = os.path.join(repo_path, "docs")
    if os.path.isdir(docs_dir):
        result["docs_directory_present"] = True

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the repository")
    args = parser.parse_args()

    audit_results = run_documentation_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
