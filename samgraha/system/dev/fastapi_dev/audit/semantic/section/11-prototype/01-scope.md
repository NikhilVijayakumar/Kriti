# Scope Audit

This section details the Scope Audit.

## Version
1.0.0

## Engineering Intent
Prototype scope defines the boundary between what is simulated and what is real. Over-scoping inflates cost and delays answers; under-scoping produces misleading results. Scope must explicitly state inclusion and exclusion boundaries relative to the prototype purpose.

## Audit Objectives
- Scope boundaries are explicitly documented
- In-scope and out-of-scope items are enumerated
- Scope aligns with the stated purpose (no scope creep)
- Simulated vs real interfaces are identified
- Scope does not exceed what is needed to answer the purpose question
- Dependencies on external systems or data are scoped

## Expected Quality
- Scope section lists in-scope and out-of-scope as separate lists
- Each scope item references a specific feature, interface, or behavior
- Scope mentions fidelity level (e.g., mocked, stubbed, partial, full)
- Scope explicitly excludes production concerns (auth, scaling, persistence)

## Red Flags
- Scope is empty or says "full implementation"
- Scope contains items unrelated to the stated purpose
- Out-of-scope list is missing
- Scope items use weasel words ("basic", "simple", "core")

## Edge Cases
- Scope expands during development ("while we're at it")
- Prototype depends on a system that does not exist yet
- Scope includes "error handling" without defining which errors

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | In-scope and out-of-scope lists present |
| C2 | mandatory | 0 or 35 | Scope items map to the stated prototype purpose |
| C3 | recommended | 0 or 30 | Fidelity level is defined per scope item |

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
