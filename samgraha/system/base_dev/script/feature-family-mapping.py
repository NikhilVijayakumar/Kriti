"""feature-family-mapping — Category C generic check.

Validates that every Feature has a matching Feature-Design and Feature-Technical,
and vice versa — no orphans.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


def run_check(docs_root: Path, fingerprint: str) -> dict:
    if not docs_root.is_dir():
        return check_result(
            check="feature-family-mapping", domain="_generic", category="C",
            status="error",
            metrics={"features": 0, "feature_designs": 0, "feature_technicals": 0,
                     "orphans": 0},
            evidence=[f"docs-root not found: {docs_root}"],
            repo_fingerprint=fingerprint,
        )

    features: set[str] = set()
    feature_designs: set[str] = set()
    feature_technicals: set[str] = set()
    evidence: list[str] = []

    for md_file in docs_root.glob("*.md"):
        name = md_file.stem
        # Extract family name: "04-feature-auth" → "auth"
        if re.match(r"^04-feature-", name):
            family = name[len("04-feature-"):]
            features.add(family)
        elif re.match(r"^09-feature-design-", name):
            family = name[len("09-feature-design-"):]
            feature_designs.add(family)
        elif re.match(r"^10-feature-technical-", name):
            family = name[len("10-feature-technical-"):]
            feature_technicals.add(family)

    orphans = 0

    # Features without design or technical
    for f in features:
        if f not in feature_designs:
            evidence.append(f"Feature '{f}' has no matching feature-design document")
            orphans += 1
        if f not in feature_technicals:
            evidence.append(f"Feature '{f}' has no matching feature-technical document")
            orphans += 1

    # Designs/technicals without feature
    for fd in feature_designs:
        if fd not in features:
            evidence.append(f"Feature-design '{fd}' has no matching feature document")
            orphans += 1

    for ft in feature_technicals:
        if ft not in features:
            evidence.append(f"Feature-technical '{ft}' has no matching feature document")
            orphans += 1

    total = len(features) + len(feature_designs) + len(feature_technicals)
    if total == 0:
        status = "not_applicable"
        evidence = ["No feature-family documents found in docs-root"]
    elif orphans > 0:
        status = "fail"
    else:
        status = "pass"

    return check_result(
        check="feature-family-mapping", domain="_generic", category="C",
        status=status,
        metrics={"features": len(features), "feature_designs": len(feature_designs),
                 "feature_technicals": len(feature_technicals), "orphans": orphans},
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
