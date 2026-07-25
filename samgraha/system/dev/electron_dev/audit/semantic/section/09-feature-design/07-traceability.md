# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability ensures every design decision, requirement, and state can be linked back to the feature's purpose and forward to implementation artifacts. It creates a navigable chain from user need → specification → design → code → test, enabling impact analysis, coverage validation, and regression prevention.

## Audit Objectives
- Every design element is traceable to a stated requirement or purpose
- Requirements have forward references to their design implementation
- Design artifacts link to test cases or acceptance criteria
- Cross-references between related design decisions are documented
- Orphaned or untraceable elements are identified
- Traceability is bidirectional (parent→child and child→parent)

## Expected Quality
- Each design component has a unique ID referenced in requirements
- Traceability matrix or map is present (explicit or implicit)
- No design element exists without a justifying requirement
- Every user-facing state maps to at least one acceptance criterion
- Traceability survives document reorganization (stable anchors)

## Red Flags
- No cross-references between design and requirements
- Design elements present without corresponding requirement ID
- Changes in one document cannot be assessed for impact on others
- Traceability is linear only (cannot go from test → requirement)
- Traceability section references outdated or deleted requirements

## Edge Cases
- Design element serves multiple requirements (N:M mapping)
- Requirement with no corresponding design element (gap)
- Third-party or inherited components with partial traceability
- Traceability across different document formats or tools

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Design elements traceable to requirements |
| C2 | mandatory | 0 or 35 | Bidirectional traceability exists (req↔design↔test) |
| C3 | recommended | 0 or 30 | No orphaned design elements without requirement |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "..." },
  "message": "..."
}
```
