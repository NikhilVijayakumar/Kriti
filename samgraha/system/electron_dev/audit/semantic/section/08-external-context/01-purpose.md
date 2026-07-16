# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
External context documents describe how the system depends on, integrates with, and is constrained by external systems, APIs, services, and data sources. They must clearly define why each external dependency exists and what role it plays.

## Audit Objectives
- Purpose of each external dependency is explicitly stated
- Business justification is present for every external integration
- Scope boundaries are defined (what is external vs internal)
- No orphan references to undocumented external systems
- Purpose statements are consistent with architecture decisions
- External context documents link to authoritative source definitions

## Expected Quality
- Each external dependency has a clear purpose statement
- Purpose distinguishes between required and optional dependencies
- Rationale explains why the external system was chosen
- Purpose aligns with documented functional and non-functional requirements

## Red Flags
- Purpose section is missing or empty
- Purpose describes implementation details rather than intent
- Contradictory purposes across multiple external-context documents
- External dependency exists in code but has no purpose document

## Edge Cases
- Zero external dependencies (purpose section with "none")
- Single dependency with multiple purposes
- Dependency used across multiple system boundaries

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Purpose stated for every external dependency |
| C2 | mandatory | 0 or 35 | Business justification documented |
| C3 | recommended | 0 or 30 | Scope boundaries clearly defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Purpose: Payment gateway Stripe for checkout processing." },
  "message": "All 3 external dependencies have explicit purpose statements."
}
```
