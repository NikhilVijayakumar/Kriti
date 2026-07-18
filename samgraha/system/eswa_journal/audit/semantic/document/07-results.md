# Results Semantic Audit

This section details the Results Semantic Audit.

## Version
1.0.0

## Engineering Intent
Ensures Results proves empirical superiority with anchored numbers rather than hollow claims, and explicitly addresses Sensitivity/Robustness and Threats to Validity as ESWA requires.

## Audit Objectives
- Every performance claim is accompanied by a specific empirical anchor (e.g., +8.4% F1), never a bare descriptor like "high accuracy" or "significant improvement".
- Zero unsupported claims of superiority over baselines.
- Dedicated Sensitivity/Robustness subsection and Threats to Validity subsection (internal, external, construct, dataset bias) are both present.

## Expected Quality
- Explanations connect back to specific result tables, not just restated numbers.
- Threats to Validity names all four categories explicitly.

## Red Flags
- "The model achieved high accuracy." (no metric).
- Superiority claimed without a corresponding baseline comparison in the tables.
- Threats to Validity omits one or more of internal/external/construct/dataset-bias.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | Every performance claim is accompanied by a specific empirical anchor, referencing the result tables |
| C2 | mandatory | 0 or 25 | Sensitivity/Robustness and Threats to Validity (all four categories) subsections are both present |
| C3 | recommended | 0 or 15 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "paragraph_index": 4, "excerpt": "The model achieved high accuracy and significant improvement." },
  "message": "Hollow technical claim detected. Replace with the specific F1/precision/recall figures from the result tables."
}
```
