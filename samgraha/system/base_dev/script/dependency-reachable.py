"""dependency-reachable — Category A check for domain 08-external-context.

Scans docs for HTTP/HTTPS URLs and checks if they are reachable.
"""

import argparse
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, find_md_files


URL_PATTERN = re.compile(r"https?://[^\s\"'<>\)\]]+")


def run_check(
    repo_root: Path,
    fingerprint: str,
    timeout: int = 10,
) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="dependency-reachable", domain="08-external-context", category="A",
            status="error",
            metrics={"urls_found": 0, "urls_reachable": 0, "urls_unreachable": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Scan docs for URLs
    urls: set[str] = set()
    md_files = find_md_files(repo_root)
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        for match in URL_PATTERN.finditer(content):
            url = match.group(0).rstrip(".,;:)")
            if url.startswith("http"):
                urls.add(url)

    if not urls:
        return check_result(
            check="dependency-reachable", domain="08-external-context", category="A",
            status="not_applicable",
            metrics={"urls_found": 0, "urls_reachable": 0, "urls_unreachable": 0},
            evidence=["No HTTP/HTTPS URLs found in documentation"],
            repo_fingerprint=fingerprint,
        )

    # Check reachability
    unreachable: list[str] = []
    reachable_count = 0

    def check_url(url: str) -> tuple[str, bool]:
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", "samgraha-audit/1.0")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, resp.status < 400
        except (urllib.error.URLError, urllib.error.HTTPError, Exception):
            return url, False

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, is_reachable = future.result()
            if is_reachable:
                reachable_count += 1
            else:
                unreachable.append(url)

    evidence: list[str] = []
    if unreachable:
        evidence.append(f"{len(unreachable)} URLs unreachable:")
        for u in unreachable[:20]:
            evidence.append(f"  {u}")
    else:
        evidence.append(f"All {len(urls)} URLs reachable")

    status = "pass" if not unreachable else "fail"

    return check_result(
        check="dependency-reachable", domain="08-external-context", category="A",
        status=status,
        metrics={"urls_found": len(urls), "urls_reachable": reachable_count,
                 "urls_unreachable": len(unreachable)},
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
