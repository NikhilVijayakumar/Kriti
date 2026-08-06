# Refactor Plan Audit

This section details the Refactor Plan Audit.

## Version
1.0.0

## Engineering Intent
Refactor Plan documents a restructuring that changes internal design without changing external behavior. It exists so a reviewer can confirm the refactor is behavior-preserving before and after, not just trust the diff.

## Audit Objectives
- Target architecture stated — what the code looks like after the refactor
- Behavior preservation strategy specified (how equivalence is maintained during the change)
- Before/after test verification described — how tests confirm nothing observable changed

## Expected Quality
- Target architecture is concrete (component/module shape), not "cleaner code"
- Behavior preservation strategy addresses the actual risk (e.g. incremental steps, feature flags, parallel run)
- Test verification names the test suite or method used to confirm equivalence, run both before and after

## Red Flags
- "Refactoring for cleaner code" with no target architecture described
- No behavior preservation strategy — refactor treated as low-risk by default
- No before/after verification step — relies on the refactor "looking right"

## Edge Cases
- Refactor that necessarily changes an internal API consumed by other teams — note the compatibility impact even though external user-facing behavior is unchanged
- Large refactor split across multiple PRs — plan should state how equivalence is verified at each increment, not just at the final PR

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Target architecture stated concretely |
| C2 | mandatory | 0 or 35 | Behavior preservation strategy specified |
| C3 | recommended | 0 or 30 | Before/after test verification described |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.83,
  "severity": "error",
  "evidence": { "section_id": 31, "paragraph_index": 0, "excerpt": "Refactoring the module to be cleaner and easier to maintain." },
  "message": "Refactor Plan states no strategy for preserving existing behavior during the change."
}
```
