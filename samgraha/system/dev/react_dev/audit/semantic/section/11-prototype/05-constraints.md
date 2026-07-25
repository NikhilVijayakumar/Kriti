# Constraints Audit

This section details the Constraints Audit.

## Version
1.0.0

## Engineering Intent
Constraints capture the known limitations, assumptions, and guardrails of a prototype. Every prototype operates under artificial conditions; undisclosed constraints mislead evaluators into overgeneralizing results. Constraints must be surfaced, documented, and traceable to the prototype purpose.

## Audit Objectives
- All known prototype limitations are documented
- Assumptions underlying the simulation are stated
- Constraints are categorized (technical, temporal, data, environmental)
- Each constraint explains how it affects result generalizability
- Constraints are traceable to specific scope or mock decisions
- No undocumented workarounds or hidden assumptions exist

## Expected Quality
- Constraints section lists each limitation with an impact statement
- Assumptions are distinguished from known limitations
- Constraints reference the scope item or mock they originate from
- Constraints include environment-specific notes (OS, browser, hardware)

## Red Flags
- "No constraints" or empty constraints section
- Constraints listed but not linked to any design decision
- Assumptions presented as facts
- Constraints that invalidate the prototype purpose entirely

## Edge Cases
- Constraint only applies in certain environments (e.g., Windows vs Linux)
- Constraint emerges mid-development and is only known to the builder
- Evaluator assumes a constraint is a feature or vice versa

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All known constraints and assumptions are documented |
| C2 | mandatory | 0 or 30 | Each constraint includes an impact on result generalizability |
| C3 | recommended | 0 or 30 | Constraints are traceable to scope items or mock decisions |

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
