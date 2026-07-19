"""traceability-refs-exist — Category C generic check.

Checks that every downstream document referenced in a domain's Traceability
section actually exists in --docs-root.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import (
    check_result, write_check_result, utc_now_iso, compute_fingerprint, DOMAIN_NUMS,
)


def run_check(docs_root: Path, fingerprint: str) -> dict:
    if not docs_root.is_dir():
        return check_result(
            check="traceability-refs-exist", domain="_generic", category="C",
            status="error", metrics={"domains_checked": 0, "refs_found": 0,
                                      "refs_valid": 0, "refs_missing": 0},
            evidence=[f"docs-root not found: {docs_root}"],
            repo_fingerprint=fingerprint,
        )

    domains_checked = 0
    refs_found = 0
    refs_valid = 0
    refs_missing = 0
    evidence: list[str] = []

    for md_file in docs_root.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"(?m)^## Traceability", content):
            continue

        domains_checked += 1
        docname = md_file.stem

        # Extract Traceability section
        in_trace = False
        trace_lines: list[str] = []
        for line in content.split("\n"):
            if re.match(r"(?m)^## ", line) and in_trace:
                break
            if re.match(r"(?m)^## Traceability", line):
                in_trace = True
                continue
            if in_trace:
                trace_lines.append(line)

        trace_content = "\n".join(trace_lines)

        # Find Consuming Standards table
        in_table = False
        for line in trace_content.split("\n"):
            if re.match(r"^\|[\s]*Standard[\s]*\|", line):
                in_table = True
                continue
            if in_table:
                if re.match(r"^\|[\s]*-+", line):
                    continue
                if not line.strip().startswith("|"):
                    break

                cols = [c.strip() for c in line.split("|") if c.strip()]
                standard = cols[0] if cols else ""
                if not standard:
                    continue

                refs_found += 1

                num_match = re.search(r"\((\d{2})\)", standard)
                if not num_match:
                    evidence.append(f"{docname}: Cannot resolve domain number from standard '{standard}'")
                    refs_missing += 1
                    continue

                domain_num = num_match.group(1)
                domain_name = DOMAIN_NUMS.get(domain_num, "unknown")

                matches = list(docs_root.glob(f"{domain_num}-{domain_name}*"))
                if matches:
                    refs_valid += 1
                else:
                    refs_missing += 1
                    evidence.append(
                        f"{docname}: Referenced standard '{standard}' "
                        f"(domain {domain_num}-{domain_name}) has no matching document"
                    )

    if domains_checked == 0:
        status = "not_applicable"
        evidence = ["No domains with Traceability sections found in docs-root"]
    elif refs_missing > 0:
        status = "fail"
    else:
        status = "pass"

    return check_result(
        check="traceability-refs-exist", domain="_generic", category="C",
        status=status,
        metrics={"domains_checked": domains_checked, "refs_found": refs_found,
                 "refs_valid": refs_valid, "refs_missing": refs_missing},
        evidence=evidence, repo_fingerprint=fingerprint,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--docs-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result = run_check(Path(args.docs_root), args.repo_fingerprint)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
