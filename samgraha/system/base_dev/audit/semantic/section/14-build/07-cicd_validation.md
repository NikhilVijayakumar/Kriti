# CI/CD Validation Audit

This section details the CI/CD Validation Audit.

## Version
1.0.0

## Engineering Intent
CI/CD Validation defines the gate sequence a build must pass and what happens when a gate fails. It exists so "the pipeline is green" has a precise, checkable meaning.

## Audit Objectives
- Gate sequence defined (what runs, in what order)
- Failure handling policy stated per gate or overall
- Deployment blockers named explicitly — which gate failures prevent a release

## Expected Quality
- Gates listed in the order they actually execute, not an unordered list
- Failure handling distinguishes "blocks deployment" from "warns but proceeds"
- Deployment blockers map to specific gates, not a vague "all checks must pass"

## Red Flags
- Gate sequence described only as "CI runs tests" with no further detail
- No stated consequence for a gate failure
- Deployment blockers left implicit — reader can't tell which failures actually stop a release

## Edge Cases
- Parallel gate execution — order still matters for blockers even if gates run concurrently; state dependencies explicitly
- Manual approval gates mixed with automated ones — distinguish which gates are human-gated vs. fully automated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Gate sequence defined in execution order |
| C2 | mandatory | 0 or 30 | Failure handling policy stated |
| C3 | recommended | 0 or 30 | Deployment blockers explicitly named per gate |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.81,
  "severity": "error",
  "evidence": { "section_id": 23, "paragraph_index": 0, "excerpt": "CI runs tests and lints the code." },
  "message": "CI/CD Validation lists gates but states no failure handling policy."
}
```
