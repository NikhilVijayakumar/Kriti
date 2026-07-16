# Component Responsibilities Audit

This section details the Component Responsibilities Audit.

## Version
1.0.0

## Engineering Intent
Component responsibilities define what each module, service, or class owns within the feature. This section must establish clear boundaries of accountability, describe the single responsibility each component fulfills, and identify overlaps or gaps in ownership across the feature.

## Audit Objectives
- Every component has a documented responsibility statement
- Responsibilities are non-overlapping across components
- The responsibility boundary between shared components is explicit
- Components without clear responsibilities are identified
- Responsibility changes across feature states (active, degraded, offline) are covered

## Expected Quality
- Responsibility statements use active verbs (manages, validates, transforms)
- Each component has exactly one primary responsibility
- Shared or cross-cutting responsibilities are called out with ownership rules
- Responsibilities map to specific code modules

## Red Flags
- Components with compound responsibilities (multiple "and" clauses)
- No component responsible for a required capability
- Two or more components claiming the same responsibility
- Vague responsibility statements ("handles data")

## Edge Cases
- Components that delegate responsibility entirely to sub-components
- Responsibility handoff during error paths
- Responsibilities that shift at runtime (leader election, failover)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All components have explicit responsibility statements |
| C2 | mandatory | 0 or 30 | No overlapping responsibilities across components |
| C3 | recommended | 0 or 20 | Each component has a primary single responsibility |
| C4 | recommended | 0 or 20 | Gap analysis performed for uncovered capabilities |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 1, "excerpt": "OrderValidator: validates order payload schemas..." },
  "message": "All 5 components have non-overlapping responsibility statements."
}
```
