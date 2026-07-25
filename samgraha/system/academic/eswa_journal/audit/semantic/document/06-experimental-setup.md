# Experimental Setup Semantic Audit

This section details the Experimental Setup Semantic Audit.

## Version
1.0.0

## Engineering Intent
Ensures the reproducibility and baseline rigor ESWA requires before Results can be trusted: a full reproducibility checklist, at least 3 baselines including an ablation, and an explicit statistical significance test.

## Audit Objectives
- Minimum of 3 distinct baselines (1 classical, 2 recent SOTA), plus a separate ablation baseline to prove module necessity.
- Reproducibility Checklist present: hardware, software versions, dataset source/preprocessing, parameter settings and random seed.
- Statistical significance test and p-value threshold explicitly stated.

## Expected Quality
- Baselines and ablation are clearly demarcated, not folded into prose.
- The significance test (e.g., paired t-test, Wilcoxon signed-rank) and threshold (p < 0.05) are named explicitly, not implied.

## Red Flags
- Fewer than 3 baselines, or no ablation baseline.
- Reproducibility Checklist missing one or more of hardware/software/data/seed.
- "Results were statistically significant" with no named test or threshold.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Minimum of 3 baselines (1 classical, 2 recent SOTA) plus a distinct ablation baseline are present |
| C2 | mandatory | 0 or 30 | Reproducibility Checklist covers hardware, software, dataset, and parameter/seed settings |
| C3 | recommended | 0 or 20 | Statistical significance test and p-value threshold are explicitly named |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "paragraph_index": 3, "excerpt": "We compare against Method A and Method B." },
  "message": "Only 2 baselines listed and no ablation baseline — minimum of 3 (including ablation) required."
}
```
