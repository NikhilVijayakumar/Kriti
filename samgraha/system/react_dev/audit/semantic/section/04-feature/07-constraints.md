# Constraints Audit

This section details the Constraints Audit.

## Version
1.0.0

## Engineering Intent
Constraints define boundaries the implementation must operate within. They must be specific, justified, and non-negotiable.

## Audit Objectives
- Each constraint is specific and measurable
- Each constraint has a clear justification
- Constraints are truly constraints (not requirements)
- Constraints are not contradictory
- Constraints are implementation-independent at the feature level

## Expected Quality
- Every constraint has a unique identifier
- Constraints are quantified where possible
- Each constraint includes rationale
- Constraints are verifiable

## Red Flags
- Constraints that are actually requirements ("the system shall...")
- Constraints without justification ("because we said so")
- Vague constraints ("must be scalable")
- Contradictory constraints

## Edge Cases
- Empty constraints section (acceptable if no constraints)
- Single constraint vs comprehensive list
- Constraints that conflict with each other

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each constraint is specific and measurable |
| C2 | mandatory | 0 or 30 | Each constraint has a clear justification |
| C3 | recommended | 0 or 30 | No contradictory constraints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 20, "paragraph_index": 2, "excerpt": "The system must be scalable." },
  "message": "Constraint is not quantified — 'scalable' is not measurable."
}
```
