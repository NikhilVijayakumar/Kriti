# Implications Semantic Audit

This section details the Implications Semantic Audit.

## Version
1.0.0

## Engineering Intent
Ensures Implications honestly acknowledges the system's maturity level rather than overselling deployment readiness or fabricating operational gains.

## Audit Objectives
- Maturity level (mature vs. early-stage) is explicit, and the corresponding template content (deployment/integration/gains for mature; use cases/validation/risks for early-stage) is followed.
- Zero fabricated ROI numbers or unsupported claims of superiority/readiness.

## Expected Quality
- Claims about deployment feasibility or operational gains are concrete and traceable to Results, not aspirational.

## Red Flags
- Fabricated ROI or performance-in-production numbers with no supporting citation or measurement.
- Early-stage system described with mature-system language ("production-ready", "deployed at scale") absent evidence.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | Maturity level is stated honestly and no ROI/operational-gain numbers are fabricated |
| C2 | recommended | 0 or 40 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.75,
  "severity": "error",
  "evidence": { "paragraph_index": 1, "excerpt": "Deployment reduces operational costs by 40%." },
  "message": "Operational cost figure is not traceable to any measurement in Results — unsupported claim."
}
```
