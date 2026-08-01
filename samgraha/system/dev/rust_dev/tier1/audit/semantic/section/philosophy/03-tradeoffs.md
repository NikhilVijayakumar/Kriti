# Tradeoffs Audit

This section details the Tradeoffs Audit.

## Version
1.0.0

## Engineering Intent
Tradeoffs document conscious decisions where one quality was sacrificed for another. They must capture the alternatives considered, the rationale for the choice, and the expected cost. Tradeoff records prevent re-litigation and surface accumulated debt.

## Audit Objectives
- Every significant design decision records tradeoffs considered
- Each tradeoff identifies the alternatives and the chosen path
- Tradeoffs include the expected cost or downside
- Tradeoffs are dated and attributed
- Tradeoff records are searchable and cross-referenced
- Accumulated tradeoffs are reviewed for pattern recognition

## Expected Quality
- Tradeoff records follow a template (alternatives, chosen, rationale, cost)
- Costs are specific, not abstract ("2x memory" not "slower")
- Tradeoffs are linked to the relevant decision or PR
- Periodic review identifies whether costs materialized
- Old tradeoffs are revisited when context changes

## Red Flags
- Tradeoffs recorded but never consulted again
- Tradeoffs only describe benefits, never costs
- Tradeoffs missing for decisions with visible quality impact
- Tradeoffs use vague cost language ("slightly more complex")
- No record of who made the call or when

## Edge Cases
- Reversible vs irreversible tradeoffs (cost to undo differs)
- Tradeoffs that become obsolete (context changed)
- Cumulative tradeoffs in same direction creating systemic debt

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Tradeoffs are documented with alternatives and rationale |
| C2 | mandatory | 0 or 35 | Each tradeoff includes explicit cost or downside |
| C3 | recommended | 0 or 30 | Tradeoffs are linked to decisions and reviewed periodically |

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
