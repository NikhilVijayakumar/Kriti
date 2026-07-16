# Values Audit

This section details the Values Audit.

## Version
1.0.0

## Engineering Intent
Values define what the product team prioritizes when tradeoffs arise — simplicity over features, reliability over speed, accessibility over novelty. Values must be ranked or weighted so they produce consistent decisions across the team.

## Audit Objectives
- Values are documented with clear definitions
- Values are ranked or grouped by priority
- Values are used to resolve feature or design conflicts
- Values are reflected in product behavior, not just documentation
- Values are communicated to new team members
- Values have a review mechanism to detect drift

## Expected Quality
- Each value has a name, definition, and concrete example
- Rank/priority is unambiguous (ordinal or tiered)
- Values are tested against past decisions for consistency
- Values are visible in onboarding materials and design templates

## Red Flags
- Values list is a copy-paste from a template or another product
- Values are all equally important (no ranking, no conflict resolution)
- Values contradict observed behavior in the product
- Values change every quarter
- Values are aspirational but never invoked in discussions

## Edge Cases
- Values implied by code or design patterns but never written
- Single value that dominates all decisions (no balance)
- Values that are internally contradictory (e.g., "privacy" and "full transparency")

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Values are documented and ranked by priority |
| C2 | mandatory | 0 or 30 | Each value has a concrete definition and example |
| C3 | recommended | 0 or 30 | Values demonstrably influence product decisions |

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
