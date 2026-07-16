# Hook Conventions Audit

This section details the Hook Conventions Audit.

## Version
1.0.0

## Engineering Intent
Hook Conventions define the naming, structure, and usage patterns for custom hooks in frontend engineering. Good hook conventions ensure consistency, testability, and proper state ownership across the component tree.

## Audit Objectives
- Verify hook names follow use* convention
- Confirm hooks return typed objects
- Validate no conditional hooks exist
- Check hooks are co-located with consumers
- Ensure hook composition rules are documented

## Expected Quality
- Naming is consistent with use prefix convention
- Return types are explicit and typed
- Composition patterns are clear and actionable

## Red Flags
- Hooks without use prefix
- Hooks returning primitive values directly
- Hooks called conditionally
- Hooks scattered across unrelated directories

## Edge Cases
- Hooks that wrap third-party hooks
- Hooks with optional parameters
- Hooks that manage multiple related state values

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Hook naming and return types are defined with clear conventions |
| C2 | mandatory | 0 or 30 | Composition rules and usage guidelines are present |
| C3 | recommended | 0 or 30 | Examples demonstrating correct hook patterns are provided |

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
