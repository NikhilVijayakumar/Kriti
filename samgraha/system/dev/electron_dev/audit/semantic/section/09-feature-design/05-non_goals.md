# Non-Goals Audit

This section details the Non-Goals Audit.

## Version
1.0.0

## Engineering Intent
Non-goals explicitly define what a feature will not do, preventing scope creep and managing stakeholder expectations. They establish boundaries between this feature and adjacent work, clarify intentional omissions, and serve as a contract that keeps design and engineering focused on the feature's core purpose.

## Audit Objectives
- Non-goals are clearly stated and not disguised as missing features
- Each non-goal has a rationale explaining the exclusion
- Non-goals are distinguishable from goals (no ambiguity)
- Non-goals are consistent with product roadmap and scope constraints
- Non-goals reference future phases or related features when applicable

## Expected Quality
- Non-goals are enumerated with identifiers (NG1, NG2)
- Each non-goal includes a one-sentence rationale
- Non-goals do not contradict stated goals
- Non-goals are realistic (not deferred indefinitely)
- Non-goals are at the same granularity as goals

## Red Flags
- Empty non-goals section (implies everything is in scope)
- Non-goals that are actually unfinished goals ("not in v1")
- Non-goals without justification ("out of scope" without reason)
- Non-goals that contradict product priorities
- Non-goals that are trivial or obvious

## Edge Cases
- Feature with no reasonable non-goals (feature is extremely narrow)
- Non-goals that conflict with each other
- Stakeholder expects a non-goal to be delivered (misalignment)
- Non-goal later becomes a goal mid-development

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Non-goals are explicitly listed with identifiers |
| C2 | mandatory | 0 or 30 | Each non-goal includes a rationale |
| C3 | recommended | 0 or 30 | Non-goals do not contradict stated goals |

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
