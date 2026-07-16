# Constraints Audit

This section details the Constraints Audit.

## Version
1.0.0

## Engineering Intent
Constraints capture the limitations, requirements, and boundaries imposed by external systems on the design and operation of the internal system. These include performance bounds, data volume limits, compliance requirements, and operational restrictions originating outside the system boundary.

## Audit Objectives
- All external-imposed constraints are enumerated
- Constraints are testable (measurable limits)
- Constraint source is attributed to the specific external dependency
- Impact of each constraint on system design is described
- No undocumented assumptions that mask constraints
- Constraint violations have defined consequences

## Expected Quality
- Each constraint has a numeric or binary measurable threshold
- Constraints distinguish hard limits from soft recommendations
- Time-bound constraints include expiration or review dates
- Constraint interactions (combined effect) are noted

## Red Flags
- Constraint described as assumption rather than documented limit
- Measurable threshold missing ("must be fast" instead of "<200ms P95")
- Source of constraint is unverifiable
- Constraint contradicted by integration contract parameters
- Constraint section is empty when external dependencies exist

## Edge Cases
- Constraint that conflicts with another constraint from a different dependency
- Constraint that becomes irrelevant after dependency upgrade
- Soft constraint with no hard enforcement mechanism
- Circular constraint dependencies between external systems

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Constraints enumerated per external dependency |
| C2 | mandatory | 0 or 30 | Each constraint has measurable threshold |
| C3 | mandatory | 0 or 20 | Constraint source attributed |
| C4 | recommended | 0 or 20 | Design impact described for each constraint |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Stripe API rate limit: 100 req/s per account." },
  "message": "All 6 external constraints enumerated with measurable thresholds."
}
```
