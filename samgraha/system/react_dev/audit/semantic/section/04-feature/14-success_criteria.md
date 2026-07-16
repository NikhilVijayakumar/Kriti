# Success Criteria Audit

This section details the Success Criteria Audit.

## Version
1.0.0

## Engineering Intent
Success criteria define how stakeholders will verify the feature delivers its intended value. They must be measurable, time-bound, and tied to business outcomes.

## Audit Objectives
- Each criterion is measurable (quantified or binary)
- Each criterion is time-bound or version-scoped
- Criteria map to stated requirements
- Criteria are realistic and achievable
- No overlapping or redundant criteria

## Expected Quality
- Criteria include specific thresholds ("< 200ms response time")
- Criteria reference requirement IDs where applicable
- Criteria are written in verifiable language
- Each criterion tests a distinct outcome

## Red Flags
- Vague success language ("users should be happy")
- Criteria that are not verifiable by test or observation
- Criteria that describe implementation output rather than business outcome
- All criteria passed trivially (empty or tautological criteria)

## Edge Cases
- Empty success criteria section
- Only qualitative criteria without quantification
- Criteria that pass by definition (tautologies)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each criterion is measurable |
| C2 | mandatory | 0 or 30 | Criteria map to stated requirements |
| C3 | recommended | 0 or 30 | Criteria include specific thresholds |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "section_id": 25, "paragraph_index": 1, "excerpt": "P95 latency under 200ms for 10K concurrent users." },
  "message": "Criterion is quantified with a specific threshold."
}
```
