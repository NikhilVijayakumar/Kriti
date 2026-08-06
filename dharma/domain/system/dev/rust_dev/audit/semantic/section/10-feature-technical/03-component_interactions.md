# Component Interactions Audit

This section details the Component Interactions Audit.

## Version
1.0.0

## Engineering Intent
Component interactions describe how components invoke, pass data to, and depend on each other within the feature. This section must define call patterns, coupling style, data flow direction, and lifecycle relationships between all participating components.

## Audit Objectives
- Every pairwise interaction between components is documented
- Interaction direction (sync/async, push/pull, event/call) is specified
- Data contracts or interfaces used in each interaction are referenced
- No undocumented or implicit interactions exist
- Component lifecycle dependencies (init order, shutdown sequence) are covered

## Expected Quality
- Each interaction has a unique identifier (e.g., CI1, CI2)
- Interactions distinguish synchronous calls from asynchronous messaging
- Diagrams or textual flow descriptions match the implementation
- Cyclic dependencies are explicitly flagged and justified

## Red Flags
- Missing interaction documentation for clearly coupled components
- Interactions described without direction or protocol
- Hand-written sequence diagrams that contradict actual code paths
- Undocumented circular dependencies

## Edge Cases
- Self-interaction (component talking to itself via internal sub-components)
- Optional or conditional interactions that only occur in specific states
- Interactions that bypass documented layers (e.g., direct DB access from UI)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All component interactions identified and identified |
| C2 | mandatory | 0 or 30 | Each interaction specifies direction and communication type |
| C3 | recommended | 0 or 20 | No undocumented cyclic dependencies |
| C4 | recommended | 0 or 20 | Data contracts or interfaces referenced per interaction |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 1, "excerpt": "Component A invokes Component B via gRPC..." },
  "message": "All 7 component interactions documented with direction and protocol."
}
```
