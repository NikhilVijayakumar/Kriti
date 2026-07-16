# End-to-End Testing Audit

This section details the End-to-End Testing Audit.

## Version
1.0.0

## Engineering Intent
End-to-End Testing verifies critical user journeys work through the full system, from the user's perspective. It exists to catch integration failures that unit and integration tests, scoped to individual components, can't see.

## Audit Objectives
- Critical user journeys are named specifically, not "test the app"
- Expected outcomes stated per journey
- Acceptance criteria defined — what counts as the journey passing
- Maps to Feature-Technical(10)'s documented runtime behavior rather than inventing untracked ones

## Expected Quality
- Journeys named as user-facing flows (e.g. "sign up → verify email → first login"), not internal function calls
- Each journey has a stated expected outcome, not just "it works"
- Acceptance criteria are checkable by an automated assertion, not subjective judgment

## Red Flags
- "We test the main flows" with no journeys actually named
- Journeys that test implementation details instead of user-observable outcomes
- No mapping to Feature-Technical's runtime behavior — E2E scope invented independently of the documented behavior

## Edge Cases
- Multi-role journeys (admin + end user interacting) — state both roles' expected outcomes, not just one
- Journeys with external dependencies (payment processor, email delivery) — note how those are handled in test (mocked, sandboxed, or live)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Critical user journeys named specifically |
| C2 | mandatory | 0 or 35 | Expected outcomes and acceptance criteria stated per journey |
| C3 | recommended | 0 or 30 | Workflows map to Feature-Technical(10)'s documented runtime behavior |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.84,
  "severity": "error",
  "evidence": { "section_id": 41, "paragraph_index": 0, "excerpt": "We run E2E tests on the main user flows." },
  "message": "End-to-End Testing doesn't name any specific critical user journey."
}
```
