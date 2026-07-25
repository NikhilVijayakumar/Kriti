import yaml
import sys
from pathlib import Path


WEIGHTS_FILE = "calculation/weights.yaml"
DOMAIN_DIRS = [
    "audit/deterministic/document",
    "audit/semantic/document",
    "calculation/aggregation/domain",
    "calculation/deterministic/document",
    "calculation/semantic/ensemble",
]


def load_weights(base: Path) -> list[str]:
    weights_path = base / WEIGHTS_FILE
    if not weights_path.exists():
        print(f"Weights file not found: {weights_path}")
        sys.exit(1)
    with open(weights_path, "r") as f:
        data = yaml.safe_load(f)
    return list(data.get("domains", {}).keys())


def find_domain_file(directory: Path, domain: str) -> bool:
    for file in directory.iterdir():
        if file.suffix == ".yaml" and file.stem.endswith(f"-{domain}"):
            return True
    return False


def validate_yaml_syntax(base: Path) -> list[str]:
    errors = []
    for yaml_file in base.rglob("*.yaml"):
        try:
            with open(yaml_file, "r") as f:
                yaml.safe_load(f)
        except Exception as e:
            errors.append(f"{yaml_file.relative_to(base)}: {e}")
    return errors


def cross_reference(domains: list[str], base: Path) -> dict[str, list[str]]:
    missing = {d: [] for d in domains}
    for domain in domains:
        for dir_name in DOMAIN_DIRS:
            directory = base / dir_name
            if directory.exists() and not find_domain_file(directory, domain):
                missing[domain].append(dir_name)
    return {d: dirs for d, dirs in missing.items() if dirs}


def print_summary(
    domains: list[str],
    yaml_errors: list[str],
    missing_refs: dict[str, list[str]],
    base: Path,
) -> None:
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Standard root: {base}")
    print(f"Domains defined in weights.yaml: {len(domains)}")
    print(f"  {', '.join(domains)}")
    print()

    yaml_ok = len(yaml_errors) == 0
    refs_ok = len(missing_refs) == 0

    if yaml_ok:
        print("YAML Syntax: OK (all files parse successfully)")
    else:
        print(f"YAML Syntax: FAILED ({len(yaml_errors)} errors)")
        for err in yaml_errors:
            print(f"  - {err}")
    print()

    if refs_ok:
        print("Cross-References: OK (all domains have files in every expected directory)")
    else:
        total_missing = sum(len(v) for v in missing_refs.values())
        print(f"Cross-References: FAILED ({total_missing} missing file(s))")
        for domain, dirs in missing_refs.items():
            for d in dirs:
                print(f"  - {domain}: missing in {d}")
    print()

    if yaml_ok and refs_ok:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")
    print("=" * 60)


def main() -> None:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

    print(f"Verifying standard in: {base}\n")

    domains = load_weights(base)
    print(f"Loaded {len(domains)} domains from {WEIGHTS_FILE}")

    print("\nChecking YAML syntax...")
    yaml_errors = validate_yaml_syntax(base)

    print("Checking cross-references...")
    missing_refs = cross_reference(domains, base)

    print_summary(domains, yaml_errors, missing_refs, base)

    if yaml_errors or missing_refs:
        sys.exit(1)


if __name__ == "__main__":
    main()
