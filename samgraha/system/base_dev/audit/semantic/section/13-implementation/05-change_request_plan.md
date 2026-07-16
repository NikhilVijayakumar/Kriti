# Change Request Plan Audit

This section details the Change Request Plan Audit.

## Version
1.0.0

## Engineering Intent
Change Request Plan documents a modification driven by an external request (not a bug, not a refactor) — its impact, how to undo it if wrong, and what tests need updating. It exists so scope creep and untested side effects are caught before merge.

## Audit Objectives
- Impact analysis identifies what else is affected by the change
- Rollback strategy defined — how to undo the change if it causes problems
- Test updates identified — which existing tests need to change, which new ones are needed

## Expected Quality
- Impact analysis names specific components/features, not "should be low risk"
- Rollback strategy is concrete (revert commit, feature flag, config toggle), not "we'll fix forward"
- Test identification distinguishes updated tests from net-new tests

## Red Flags
- No impact analysis — change request implemented without considering side effects
- Rollback strategy absent or vague ("we can always fix it later")
- Test updates not identified, discovered only after the change breaks something

## Edge Cases
- Change request that's purely additive (new optional field/flag) — impact analysis can be brief but should still confirm no interaction with existing behavior
- Time-sensitive change request with compressed review — plan should still cover impact and rollback, even if abbreviated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Impact analysis identifies affected components |
| C2 | mandatory | 0 or 35 | Rollback strategy is concrete |
| C3 | recommended | 0 or 30 | Test updates identified (updated vs. new) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.8,
  "severity": "error",
  "evidence": { "section_id": 32, "paragraph_index": 1, "excerpt": "If something goes wrong we'll fix it later." },
  "message": "Change Request Plan has no concrete rollback strategy."
}
```
