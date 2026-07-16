# Architectural Constraints Audit

This section details the Architectural Constraints Audit.

## Version
1.0.0

## Engineering Intent
Architectural constraints define non-negotiable properties of the system design. Unlike feature constraints, these apply system-wide and are driven by architectural decisions.

## Audit Objectives
- Constraints are architectural (not implementation or feature-specific)
- Each constraint is justified by a documented decision
- Constraints are specific and falsifiable
- System-wide constraints are consistently applied
- Trade-offs implied by constraints are acknowledged

## Expected Quality
- Constraints reference architectural decisions (ADR links)
- Each constraint states what it prohibits or requires
- Constraints are ordered by impact or scope
- Constraints are written as properties of the architecture, not the implementation

## Red Flags
- Feature-level constraints in architecture section
- Constraints without rationale
- Constraints that contradict each other
- Constraints that are aspirational rather than binding
- Technology-specific constraints without decision record

## Edge Cases
- Empty constraints section (acceptable — may indicate no architectural restrictions)
- Single global constraint that covers all sub-systems
- Constraints that apply only to specific components

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Constraints are architectural, not implementation-specific |
| C2 | mandatory | 0 or 30 | Each constraint has a documented justification |
| C3 | recommended | 0 or 30 | No contradictory constraints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.80,
  "severity": "error",
  "evidence": { "section_id": 35, "paragraph_index": 1, "excerpt": "All services must use PostgreSQL." },
  "message": "Technology constraint without ADR link — architectural decision not documented."
}
```
