"""generate_calc_yamls.py — create 62 calculation YAML files:
  12  calculation/aggregation/domain/{domain}.yaml
   1  calculation/semantic/full-part-blend.yaml
   1  calculation/semantic/rerun-policy.yaml
  12  calculation/semantic/ensemble/{domain}.yaml          (section-full)
  36  calculation/semantic/ensemble/{domain}-{part_kind}.yaml (section-part)
"""
import os
from pathlib import Path

DOMAINS = [
    "title-and-metadata", "abstract", "introduction", "related-work",
    "problem-definition", "methodology", "experimental-setup", "results",
    "discussion", "limitations", "conclusion", "references",
]
PART_KINDS = ["citations", "enrichment", "budget-fit"]

ROOT = Path(__file__).resolve().parents[2]


def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def domain_id(d):
    return d.replace("-", "_")


def aggregation_domain(d):
    did = domain_id(d)
    return (
        f"id: aggregation_{did}\n"
        f"calculation: weighted_merge\n"
        f"scope: domain\n"
        f"inputs:\n"
        f"  deterministic: calculation/deterministic/{d}.yaml\n"
        f"  semantic: calculation/semantic/full-part-blend.yaml\n"
        f"weights:\n"
        f"  deterministic: 0.50\n"
        f"  semantic: 0.50\n"
        f"formula: |\n"
        f"  final_score = (deterministic.score * weights.deterministic) + (semantic.score * weights.semantic)\n"
        f"note: >\n"
        f"  Per-domain 50/50 deterministic/semantic blend, matching\n"
        f"  calculation/summary/final_score.yaml's per-domain half.\n"
    )


def full_part_blend():
    return (
        "id: semantic_full_part_blend\n"
        "calculation: weighted_merge\n"
        "inputs:\n"
        "  full: academic_semantic_runs WHERE scope='section-full'\n"
        "  citations: academic_semantic_runs WHERE scope='section-part' AND part_kind='citations'\n"
        "  enrichment: academic_semantic_runs WHERE scope='section-part' AND part_kind='enrichment'\n"
        "  budget_fit: academic_semantic_runs WHERE scope='section-part' AND part_kind='budget-fit'\n"
        "weights:\n"
        "  full: 0.70\n"
        "  citations: 0.10\n"
        "  enrichment: 0.10\n"
        "  budget_fit: 0.10\n"
        "formula: |\n"
        "  score = full.score * 0.70 + citations.score * 0.10 + enrichment.score * 0.10 + budget_fit.score * 0.10\n"
        "note: >\n"
        "  Part-level scores are missing until their usecases run (references\n"
        "  domain has no part scores at all — collation only, no citations/\n"
        "  enrichment/budget-fit stages of its own). Missing parts redistribute\n"
        "  their weight to full rather than treating a missing part as 0.\n"
    )


def rerun_policy():
    return (
        "id: semantic_rerun_policy\n"
        "calculation: cache_key\n"
        "key_fields: [commit_sha, model]\n"
        "rule: >\n"
        "  A semantic run is reusable (skip re-scoring) iff an existing row\n"
        "  matches on both commit_sha and model for the same\n"
        "  (paper, domain, scope, part_kind). Any mismatch requires a new run.\n"
    )


def ensemble_full(d):
    did = domain_id(d)
    return (
        f"id: semantic_ensemble_{did}\n"
        f"calculation: reliability_aware_ensemble\n"
        f"scope: section-full\n"
        f"inputs:\n"
        f"  from: academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE domain_key='{d}') AND scope='section-full'\n"
        f"  fields: [model, overall_score, reasoning]\n"
        f"formula: |\n"
        f"  mean_score = mean(scores)\n"
        f"  stdev_score = stdev(scores)\n"
        f'  agreement = "High" if stdev_score <= 5 else "Medium" if stdev_score <= 15 else "Low"\n'
        f"  final_score = mean_score\n"
        f"outputs:\n"
        f"  - score\n"
        f"  - agreement\n"
        f"  - stdev\n"
        f"note: >\n"
        f"  Single-model rounds (stdev undefined / n=1) report agreement=N/A.\n"
    )


def ensemble_part(d, pk):
    did = domain_id(d)
    return (
        f"id: semantic_ensemble_{did}_{pk.replace('-', '_')}\n"
        f"calculation: reliability_aware_ensemble\n"
        f"scope: section-part\n"
        f"inputs:\n"
        f"  from: academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE domain_key='{d}') AND scope='section-part' AND part_kind='{pk}'\n"
        f"  fields: [model, overall_score, reasoning]\n"
        f"formula: |\n"
        f"  mean_score = mean(scores)\n"
        f"  stdev_score = stdev(scores)\n"
        f'  agreement = "High" if stdev_score <= 5 else "Medium" if stdev_score <= 15 else "Low"\n'
        f"  final_score = mean_score\n"
        f"outputs:\n"
        f"  - score\n"
        f"  - agreement\n"
        f"  - stdev\n"
        f"note: >\n"
        f"  Part-level ensemble: single-model rounds report agreement=N/A.\n"
    )


def main():
    base = ROOT / "calculation"
    count = 0

    print("=== aggregation/domain/ ===")
    for d in DOMAINS:
        write_file(base / "aggregation" / "domain" / f"{d}.yaml", aggregation_domain(d))
        count += 1

    print("=== semantic/full-part-blend.yaml ===")
    write_file(base / "semantic" / "full-part-blend.yaml", full_part_blend())
    count += 1

    print("=== semantic/rerun-policy.yaml ===")
    write_file(base / "semantic" / "rerun-policy.yaml", rerun_policy())
    count += 1

    print("=== semantic/ensemble/ (section-full) ===")
    for d in DOMAINS:
        write_file(base / "semantic" / "ensemble" / f"{d}.yaml", ensemble_full(d))
        count += 1

    print("=== semantic/ensemble/ (section-part) ===")
    for d in DOMAINS:
        for pk in PART_KINDS:
            write_file(base / "semantic" / "ensemble" / f"{d}-{pk}.yaml", ensemble_part(d, pk))
            count += 1

    print(f"\nTotal: {count} files generated")


if __name__ == "__main__":
    main()
