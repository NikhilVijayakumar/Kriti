# Design Principles Audit

This section details the Design Principles Audit.

## Version
1.0.0

## Engineering Intent
Design principles are the foundational rules guiding visual and interaction decisions. They ensure consistency, coherence, and a unified product identity across all surfaces.

## Audit Objectives
- Design principles are explicitly defined and documented
- Principles are consistently applied across all UI components
- No contradictory or overlapping principles exist
- Principles are referenced in design reviews and decisions
- Principles support both brand identity and usability goals

## Expected Quality
- 3–7 core design principles exist and are distinct
- Each principle has a clear definition and rationale
- Component implementations can be mapped to at least one principle
- Principles are used as decision-making criteria

## Red Flags
- More than 10 principles (too many to operationalize)
- Principles that are vague or unactionable
- Principles that conflict with each other
- Principles defined but never referenced in design artifacts

## Edge Cases
- Principles that apply differently across platforms (web vs mobile)
- Principles inherited from parent design systems
- Principles that evolve over time without deprecation notice

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Design principles are documented and distinct |
| C2 | mandatory | 0 or 30 | Principles consistently applied across components |
| C3 | recommended | 0 or 30 | Principles used as decision-making criteria in reviews |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "We follow clarity, consistency, and feedback as core design principles..." },
  "message": "All 5 design principles clearly defined with no overlaps."
}
```
