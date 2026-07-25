"""mitigation-present-at-boundary — Category B check for domain 03-security.

Reads security docs for declared mitigation types and checks if they
are implemented at code boundaries.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, find_md_files, walk_source_files


# Mitigation types to look for
MITIGATION_TYPES = {
    "sanitization": re.compile(r"sanitiz(?:e|ation|ing)", re.IGNORECASE),
    "escaping": re.compile(r"escap(?:e|ing|ed)", re.IGNORECASE),
    "validation": re.compile(r"validat(?:e|ion|ing)", re.IGNORECASE),
    "authentication": re.compile(r"authenticat(?:e|ion|ing)", re.IGNORECASE),
    "authorization": re.compile(r"authoriz(?:e|ation|ing)", re.IGNORECASE),
    "encryption": re.compile(r"encrypt(?:ion|ed|ing)?", re.IGNORECASE),
    "hashing": re.compile(r"hash(?:ing|ed)?", re.IGNORECASE),
    "rate_limiting": re.compile(r"rate.?limit(?:ing|ed)?", re.IGNORECASE),
    "csrf": re.compile(r"csrf", re.IGNORECASE),
    "xss": re.compile(r"xss", re.IGNORECASE),
}

# Code patterns that implement mitigations
CODE_PATTERNS = {
    "sanitization": re.compile(r"(?:sanitize|escape|clean|strip)[\w(]", re.IGNORECASE),
    "escaping": re.compile(r"(?:escape|encode|htmlEntit)", re.IGNORECASE),
    "validation": re.compile(r"(?:validate|isValid|check|verify|schema\.parse)", re.IGNORECASE),
    "authentication": re.compile(r"(?:authenticate|login|jwt|token|session|passport)", re.IGNORECASE),
    "authorization": re.compile(r"(?:authorize|permission|role|rbac|acl)", re.IGNORECASE),
    "encryption": re.compile(r"(?:encrypt|decrypt|cipher|crypto|aes|rsa)", re.IGNORECASE),
    "hashing": re.compile(r"(?:hash|bcrypt|argon|scrypt|pbkdf|sha256)", re.IGNORECASE),
    "rate_limiting": re.compile(r"(?:rate.?limit|throttl|brute)", re.IGNORECASE),
    "csrf": re.compile(r"(?:csrf|xsrf|csrfToken|csrfProtect)", re.IGNORECASE),
    "xss": re.compile(r"(?:xss|contentSecurityPolicy|sanitizeHtml|domPurify)", re.IGNORECASE),
}


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="mitigation-present-at-boundary", domain="03-security", category="B",
            status="error",
            metrics={"mitigations_declared": 0, "mitigations_implemented": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Extract declared mitigations from security docs
    declared: set[str] = set()
    sec_files = find_md_files(repo_root, prefix="03-security")
    for md_file in sec_files:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in MITIGATION_TYPES.items():
            if pattern.search(content):
                declared.add(name)

    if not declared:
        return check_result(
            check="mitigation-present-at-boundary", domain="03-security", category="B",
            status="not_applicable",
            metrics={"mitigations_declared": 0, "mitigations_implemented": 0},
            evidence=["No security mitigations found in documentation"],
            repo_fingerprint=fingerprint,
        )

    # Check implementation for mitigation patterns
    source_files = walk_source_files(repo_root, "*.py;*.js;*.ts;*.go;*.rs;*.java;*.jsx;*.tsx")
    code_content = ""
    for f in source_files:
        try:
            code_content += f.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            continue

    implemented: set[str] = set()
    for name in declared:
        if name in CODE_PATTERNS and CODE_PATTERNS[name].search(code_content):
            implemented.add(name)

    missing = declared - implemented

    evidence: list[str] = []
    if missing:
        evidence.append(f"{len(missing)} declared mitigations not found in code:")
        for m in sorted(missing):
            evidence.append(f"  {m}")
    else:
        evidence.append(f"All {len(declared)} declared mitigations found in code")

    status = "pass" if not missing else "fail"

    return check_result(
        check="mitigation-present-at-boundary", domain="03-security", category="B",
        status=status,
        metrics={"mitigations_declared": len(declared),
                 "mitigations_implemented": len(implemented)},
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
