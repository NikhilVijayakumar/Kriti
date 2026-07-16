# Architectural Constraints Audit

This section details the Architectural Constraints Audit.

## Version
1.0.0

## Engineering Intent
Architectural constraints define the non-negotiable design rules and patterns the feature must adhere to. This section must document required architectural styles, forbidden patterns, layer isolation rules, dependency direction rules, and compliance with enterprise architecture standards.

## Audit Objectives
- Every architectural constraint is explicitly stated
- Forbidden or disallowed patterns are enumerated
- Layer or tier isolation rules are defined
- Dependency direction (which layers can import which) is specified
- Compliance with enterprise architecture principles is verifiable

## Expected Quality
- Constraints reference specific architectural decisions (ADRs)
- Each constraint is falsifiable (can check if violated)
- Constraints are justified with rationale
- Consequences of violating each constraint are documented

## Red Flags
- Constraints that are subjective or unverifiable ("clean architecture")
- Missing dependency direction rules between layers
- Constraints that contradict each other
- Constraints that are aspirational rather than enforced

## Edge Cases
- Constraints that apply only to specific deployment modes
- Temporary exceptions or waivers to architectural constraints
- Constraints inherited from parent systems that no longer apply

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All architectural constraints enumerated |
| C2 | mandatory | 0 or 30 | Dependency direction rules specified |
| C3 | recommended | 0 or 20 | Layer isolation rules defined |
| C4 | recommended | 0 or 20 | Each constraint linked to an ADR or rationale |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "All DB access must go through the repository layer..." },
  "message": "All 7 architectural constraints documented with ADR references."
}
```
