# Component Model Audit

This section details the Component Model Audit.

## Version
1.0.0

## Engineering Intent
The component model identifies the major structural elements of the system. Each component must have a clear responsibility, defined interfaces, and known dependencies.

## Audit Objectives
- All system components are identified
- Each component has a defined responsibility
- Component boundaries are clear (no overlapping responsibilities)
- Interfaces between components are documented
- External dependencies are identified

## Expected Quality
- Component names follow project conventions
- Each component has a single responsibility
- Dependencies between components are explicitly stated
- Component-responsibility mapping is unambiguous

## Red Flags
- Missing components (gaps in architecture coverage)
- Components with undefined responsibilities
- Overlapping responsibilities between components
- Circular dependencies
- Implementation-specific technology in component descriptions

## Edge Cases
- Single-component system
- Systems with no external dependencies
- Components that are pure infrastructure (no business logic)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All system components identified |
| C2 | mandatory | 0 or 30 | Each component has a clear responsibility |
| C3 | recommended | 0 or 20 | Interfaces between components documented |
| C4 | recommended | 0 or 20 | No overlapping component responsibilities |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.92,
  "severity": "error",
  "evidence": { "section_id": 30, "paragraph_index": 2, "excerpt": "Component: AuthService" },
  "message": "All 6 components identified with distinct responsibilities."
}
```
