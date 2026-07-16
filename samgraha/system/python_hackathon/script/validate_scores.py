#!/usr/bin/env python3
"""
Scoring pipeline validator for the Python Hackathon Audit Standard.
Validates weight totals, score bounds, and normalization invariants.
"""

import sys
import yaml
from pathlib import Path


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_weights(weights_path):
    """Validate weight sum == 100 and all weights are positive."""
    data = load_yaml(weights_path)
    domains = data.get('domains', {})
    total = sum(d['weight'] for d in domains.values())
    errors = []

    if total != 100:
        errors.append(f"Weight sum is {total}, expected 100")

    for name, domain in domains.items():
        if domain['weight'] <= 0:
            errors.append(f"Domain '{name}' has non-positive weight: {domain['weight']}")

    return errors


def validate_scores(scores, weights_path):
    """Validate all score bounds and invariants."""
    data = load_yaml(weights_path)
    domains = data.get('domains', {})
    errors = []

    for domain_name, domain_scores in scores.items():
        det = domain_scores.get('deterministic', 0)
        sem = domain_scores.get('semantic_mean', 0)
        raw = domain_scores.get('raw_domain_score', 0)
        z_adj = domain_scores.get('zscore_adjustment', 0)
        adj = domain_scores.get('adjusted_score', 0)

        if not (0 <= det <= 100):
            errors.append(f"{domain_name}: deterministic score {det} out of [0,100]")
        if not (0 <= sem <= 100):
            errors.append(f"{domain_name}: semantic mean {sem} out of [0,100]")
        if not (0 <= raw <= 100):
            errors.append(f"{domain_name}: raw domain score {raw} out of [0,100]")
        if not (-10 <= z_adj <= 10):
            errors.append(f"{domain_name}: z-score adjustment {z_adj} out of ±10")
        if not (0 <= adj <= 115):
            errors.append(f"{domain_name}: adjusted score {adj} out of [0,115]")

    return errors


def validate_final_score(final_score):
    """Validate final normalized score bounds."""
    errors = []
    if not (0 <= final_score <= 20):
        errors.append(f"Final score {final_score} out of [0,20]")
    return errors


def main():
    base = Path(__file__).parent.parent
    weights_path = base / 'calculation' / 'weights.yaml'
    validation_path = base / 'calculation' / 'validation' / 'scoring_validation.yaml'

    print("=== Python Hackathon Scoring Validator ===\n")

    # Validate weights
    print("Checking weights.yaml...")
    weight_errors = validate_weights(weights_path)
    if weight_errors:
        for e in weight_errors:
            print(f"  FAIL: {e}")
    else:
        print("  PASS: weights sum to 100, all positive")

    # Validate validation config exists
    print("\nChecking scoring_validation.yaml...")
    if validation_path.exists():
        vdata = load_yaml(validation_path)
        check_count = len(vdata.get('checks', []))
        print(f"  PASS: {check_count} validation checks defined")
    else:
        print(f"  WARN: {validation_path} not found")

    if weight_errors:
        print(f"\nValidation FAILED with {len(weight_errors)} error(s)")
        sys.exit(1)
    else:
        print("\nValidation PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
