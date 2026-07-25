# States Audit

This section details the States Audit.

## Version
1.0.0

## Engineering Intent
States audit covers every visual and interactive state a UI component or screen can exhibit. Exhaustive state enumeration prevents runtime surprises by ensuring designers and developers agree on what the user sees during loading, empty, error, success, disabled, and edge conditions.

## Audit Objectives
- All component states (default, hover, active, focus, disabled, loading, error, empty, success) are defined
- State transitions are documented (what action triggers which state)
- Empty states provide guidance, not dead ends
- Error states display actionable message and recovery path
- Loading states show meaningful progress indication
- States are consistent across similar components

## Expected Quality
- Every interactive element has at least default, hover, focus, disabled, error states
- Empty state includes illustration or message plus call to action
- Loading state appears within 200ms and shows progress if >1s
- Error state is inline near the relevant element (not just a toast)
- State definitions exist for both light and dark mode

## Red Flags
- States described only for happy path
- Missing disabled state for form elements
- Error state is a generic alert with no recovery guidance
- State transitions are undefined (user must guess what happens next)
- Loading state is a blank spinner with no context

## Edge Cases
- Component used inside a container that also has states (nested state conflict)
- Rapid state transitions (loading → error → success in <500ms)
- Offline state when feature requires connectivity
- Multi-select or bulk action states (partial selection, mixed states)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All core states (default/loading/empty/error/success) defined |
| C2 | mandatory | 0 or 30 | State transitions and trigger actions documented |
| C3 | recommended | 0 or 20 | Empty and error states provide recovery guidance |
| C4 | recommended | 0 or 20 | States defined for light and dark mode |

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
