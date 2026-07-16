# Component Patterns Audit

This section details the Component Patterns Audit.

## Version
1.0.0

## Engineering Intent
Component Patterns define the composition strategies (compound components, render props, HOC) that govern how frontend components share behavior and UI. Good pattern selection ensures readability, reusability, and appropriate abstraction levels.

## Audit Objectives
- Verify pattern selection criteria are documented
- Confirm composition vs inheritance guidance exists
- Validate render prop usage is appropriate
- Check HOC patterns are justified
- Ensure anti-patterns are listed

## Expected Quality
- Pattern selection has clear criteria
- Examples show correct and incorrect usage
- Anti-patterns are explicitly called out

## Red Flags
- All components use same pattern regardless of need
- HOCs used when composition would suffice
- No guidance on when to use each pattern

## Edge Cases
- Components that need multiple patterns
- Patterns that conflict with TypeScript generics
- Patterns that affect testing strategies

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Pattern selection criteria are defined with clear decision logic |
| C2 | mandatory | 0 or 30 | Anti-patterns are listed with explanations |
| C3 | recommended | 0 or 30 | Examples demonstrating correct and incorrect patterns provided |

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
