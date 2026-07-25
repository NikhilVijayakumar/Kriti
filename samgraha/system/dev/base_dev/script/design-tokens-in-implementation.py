"""design-tokens-in-implementation — Category B check for domain 06-design.

Reads design docs for design tokens (hex colors, px/rem values, font-families)
and checks if they appear in style/code files.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result, find_md_files, walk_source_files


# Token extraction patterns
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_VALUE = re.compile(r"\b\d+(?:\.\d+)?px\b")
REM_VALUE = re.compile(r"\b\d+(?:\.\d+)?rem\b")
FONT_FAMILY = re.compile(r"(?:font-family|font)\s*:\s*[\"']?([^\"';\n]+)", re.IGNORECASE)


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="design-tokens-in-implementation", domain="06-design", category="B",
            status="error",
            metrics={"tokens_found": 0, "tokens_implemented": 0},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Extract tokens from design docs
    design_tokens: set[str] = set()
    design_files = find_md_files(repo_root, prefix="06-design")
    for md_file in design_files:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        for pattern in [HEX_COLOR, PX_VALUE, REM_VALUE, FONT_FAMILY]:
            for match in pattern.finditer(content):
                design_tokens.add(match.group(0).strip())

    if not design_tokens:
        return check_result(
            check="design-tokens-in-implementation", domain="06-design", category="B",
            status="not_applicable",
            metrics={"tokens_found": 0, "tokens_implemented": 0},
            evidence=["No design tokens found in design documentation"],
            repo_fingerprint=fingerprint,
        )

    # Check implementation files for token usage
    impl_files = walk_source_files(
        repo_root, "*.css;*.scss;*.less;*.styled;*.js;*.ts;*.jsx;*.tsx"
    )
    impl_content = ""
    for f in impl_files:
        try:
            impl_content += f.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            continue

    implemented: set[str] = set()
    for token in design_tokens:
        # Normalize for comparison
        token_lower = token.lower()
        if token_lower in impl_content.lower():
            implemented.add(token)

    not_implemented = design_tokens - implemented

    evidence: list[str] = []
    if not_implemented:
        evidence.append(f"{len(not_implemented)} design tokens not found in implementation:")
        for t in sorted(not_implemented)[:20]:
            evidence.append(f"  {t}")
    else:
        evidence.append(f"All {len(design_tokens)} design tokens found in implementation")

    tokens_missing = len(not_implemented)
    status = "pass" if tokens_missing == 0 else "fail"

    return check_result(
        check="design-tokens-in-implementation", domain="06-design", category="B",
        status=status,
        metrics={"tokens_found": len(design_tokens),
                 "tokens_implemented": len(implemented)},
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
