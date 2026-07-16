# Component Testing Audit

This section details the Component Testing Audit.

## Version
1.0.0

## Engineering Intent
Component Testing defines the Vitest + Testing Library patterns, mock conventions, and test categories that govern how frontend components are verified. Good component testing ensures reliability, catches regressions, and validates user interactions.

## Audit Objectives
- Verify test files are co-located with components
- Confirm useLanguage is always mocked
- Validate render tests exist
- Check interaction tests exist
- Ensure test categories are documented

## Expected Quality
- Tests are co-located next to their components
- Mocks are consistent across the test suite
- Test categories cover render, interaction, and context

## Red Flags
- Tests not co-located with components
- useLanguage not mocked in tests
- Only render tests without interaction tests
- No context integration tests

## Edge Cases
- Components with complex state machines
- Components that depend on multiple contexts
- Components with animation or transitions

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Test files are co-located with their respective components |
| C2 | mandatory | 0 or 30 | Mocks are consistent and useLanguage is always mocked |
| C3 | recommended | 0 or 30 | Test categories cover render, interaction, and context scenarios |

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
