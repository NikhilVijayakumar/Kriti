# Acceptance Criteria Audit

This section details the Acceptance Criteria Audit.

## Version
1.0.0

## Engineering Intent
Acceptance criteria define conditions a feature must satisfy for stakeholder sign-off. They must be pass/fail testable, scoped to a single behavior, and written from the user's perspective. Good criteria eliminate interpretation ambiguity.

## Audit Objectives
- Each criterion is pass/fail testable
- Criteria are written from the user or stakeholder perspective
- Each criterion tests a single behavior
- Criteria are unambiguous
- Criteria map to a specific user story or requirement

## Expected Quality
- Criteria use Given/When/Then or equivalent structured format
- Specific values and conditions are included
- No compound criteria testing multiple behaviors
- Criteria are ordered by priority

## Red Flags
- Criteria that are too vague to write a test for
- Compound criteria joined by "and" or "or"
- Criteria describing implementation rather than behavior
- Criteria that are impossible to automate

## Edge Cases
- Empty acceptance criteria section
- Single criterion covering the entire feature
- Criteria that conflict with each other

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every criterion is pass/fail testable |
| C2 | mandatory | 0 or 30 | Each criterion tests a single behavior |
| C3 | recommended | 0 or 30 | Criteria use structured Given/When/Then format |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.96,
  "severity": "error",
  "evidence": { "section_id": 14, "paragraph_index": 0, "excerpt": "Given user is logged in, When they submit valid data, Then confirmation shown." },
  "message": "All 6 acceptance criteria are pass/fail testable."
}
```
