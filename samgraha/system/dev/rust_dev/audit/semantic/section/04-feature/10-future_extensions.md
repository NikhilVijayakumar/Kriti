# Future Extensions Audit

This section details the Future Extensions Audit.

## Version
1.0.0

## Engineering Intent
Future extensions document planned or possible enhancements beyond the current scope. They must be clearly marked as out-of-scope for the current delivery, prioritized, and linked to trigger conditions. Good extension notes prevent scope creep while preserving architectural foresight.

## Audit Objectives
- Extensions are clearly marked as out of current scope
- Each extension has a trigger or rationale
- Extensions are distinct (not repackaged requirements)
- Architectural impact of each extension is considered
- Extensions are prioritized or sequenced

## Expected Quality
- Extensions are described in 1-2 sentences each
- Trigger conditions are specified ("when MAU > 100K")
- Extensions reference affected components
- No extension duplicates a current requirement

## Red Flags
- Extensions disguised as current requirements
- No clear boundary between scope and future work
- Extensions without any trigger or condition
- Too many extensions suggesting scope underspecification

## Edge Cases
- Empty future extensions section (acceptable)
- Extensions that change core architecture assumptions
- Extensions that invalidate current design decisions

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Extensions are clearly marked as out of scope |
| C2 | recommended | 0 or 30 | Each extension has a trigger condition |
| C3 | recommended | 0 or 30 | Architectural impact is noted |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.94,
  "severity": "error",
  "evidence": { "section_id": 30, "paragraph_index": 0, "excerpt": "[FUTURE] Real-time sync — deferred until WebSocket infra is available." },
  "message": "Extension is explicitly flagged as out of current scope."
}
```
