# Feature Specification Audit

This section details the Feature Specification Audit.

## Version
1.0.0

## Engineering Intent
The feature specification defines the technical boundaries, inputs, outputs, and behavioral contract of the entire feature. This section must describe what the feature does at its boundary, its observable behavior, preconditions and postconditions, invariants, and the scope of what is included versus explicitly excluded.

## Audit Objectives
- Feature scope is clearly stated with inclusion and exclusion criteria
- Preconditions and postconditions are defined
- Inputs and outputs are specified with types and formats
- Feature-level invariants are documented
- Behavioral contract leaves no ambiguity about what the feature guarantees

## Expected Quality
- Specification is complete enough to derive acceptance tests
- Boundary conditions are explicitly listed
- Feature interactions (what this feature does NOT handle) are stated
- Specification is written declaratively, not prescriptively

## Red Flags
- Specification describes implementation rather than behavior
- Preconditions or postconditions are missing
- Input/output formats are undefined
- Feature scope is circular or self-referential
- Contradictory statements about what the feature does

## Edge Cases
- Feature that behaves differently based on deployment context
- Legacy behavior that the spec describes but should deprecate
- Feature that is part of a larger feature hierarchy

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Feature scope with inclusion and exclusion criteria |
| C2 | mandatory | 0 or 30 | Preconditions and postconditions defined |
| C3 | recommended | 0 or 20 | Input and output specifications with types |
| C4 | recommended | 0 or 20 | Feature-level invariants documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Feature: Order Cancellation. Inputs: orderId (UUID), reason (string)..." },
  "message": "Feature specification complete with preconditions, postconditions, and invariants."
}
```
