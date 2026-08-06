# Non-Goals Audit

This section details the Non-Goals Audit.

## Version
1.0.0

## Engineering Intent
Non-goals explicitly state what the feature will NOT address. They prevent scope creep and set stakeholder expectations. Good non-goals are specific, justified, and distinct from the feature's goals.

## Audit Objectives
- Each non-goal is specific and testable as out-of-scope
- Non-goals are justified (why excluded)
- Non-goals are distinct from goals (not inverted goals)
- Non-goals are bounded to current delivery
- No overlap between non-goals and future extensions

## Expected Quality
- Non-goals are written with explicit negation ("will not")
- Rationale for exclusion is stated
- Each non-goal is a single statement
- Non-goals reference related goals where applicable

## Red Flags
- Non-goals that are secretly goals ("we will not deliver... unless...")
- Non-goals without any justification
- Non-goals that duplicate future extensions
- Non-goals that contradict stated requirements

## Edge Cases
- Empty non-goals section (acceptable)
- Non-goals that stakeholders might assume are in scope
- Non-goals that change architectural boundaries

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each non-goal is specific and explicitly excluded |
| C2 | mandatory | 0 or 30 | Exclusion rationale is provided |
| C3 | recommended | 0 or 30 | Non-goals are distinct from future extensions |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.93,
  "severity": "error",
  "evidence": { "section_id": 10, "paragraph_index": 0, "excerpt": "Multi-language support will not be included in v1.0." },
  "message": "Non-goal is specific, negated, and scoped to current delivery."
}
```
