# References Semantic Audit

This section details the References Semantic Audit.

## Version
1.0.0

## Engineering Intent
Enforces the Q1 Reviewer Persona rules for citation quality and completeness — the academic foundation ESWA expects.

## Audit Objectives
- Zero unverified/predatory sources (blogs, non-peer-reviewed URLs, known predatory journals).
- 100% match between in-text citations (especially in Related Work) and the References list — no missing or orphaned entries.

## Expected Quality
- Citations are exclusively from high-impact (Q1/Q2 Scopus, CORE A/A*) venues, meeting the 35-45 reference target and distribution (60-70% recent, 20% foundational, 10-20% architecture/system design, 2-4 ESWA).

## Red Flags
- Links to Medium articles, generic tech blogs, or predatory journals.
- An in-text citation with no matching References entry, or vice versa.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Zero unverified/predatory sources |
| C2 | mandatory | 0 or 50 | 100% match between in-text citations and the References list |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "excerpt": "(Chen et al., 2023) cited in Related Work" },
  "message": "In-text citation 'Chen et al., 2023' has no matching entry in the References section."
}
```
