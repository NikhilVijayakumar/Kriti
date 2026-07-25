# State Management Audit

This section details the State Management Audit.

## Version
1.0.0

## Engineering Intent
State Management defines the Context + useState patterns that govern how frontend state is created, shared, and consumed. Good state management ensures predictable data flow, testability, and proper separation between cross-cutting and UI-local state.

## Audit Objectives
- Verify Context is used for cross-cutting state
- Confirm useState is used for UI-local state
- Validate no external state libraries are used
- Check props-down convention is followed
- Ensure state ownership rules are documented

## Expected Quality
- State ownership is clearly defined per component tier
- Context and useState usage has clear criteria
- Props-down convention is enforced consistently

## Red Flags
- External state libraries imported
- Global state used for UI-local concerns
- Props drilled through multiple levels without Context

## Edge Cases
- State shared between unrelated components
- State that needs persistence
- State derived from multiple sources

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | State ownership rules are defined per component tier |
| C2 | mandatory | 0 or 30 | No external state libraries are used in the codebase |
| C3 | recommended | 0 or 30 | Examples demonstrating Context and useState patterns provided |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "example text" },
  "message": "Description of what was found"
}
```
