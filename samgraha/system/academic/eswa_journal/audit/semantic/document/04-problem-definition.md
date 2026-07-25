# Problem Definition Semantic Audit

This section details the Problem Definition Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies Problem Definition formalizes exactly the gap Related Work's bridge names — no narrower, no broader — and that Methodology later attempts to solve exactly this and nothing else. This file owns the receiving end of the Related Work → Problem Definition bridge and the sending end of the Problem Definition → Methodology bridge.

## Audit Objectives
- The formalized problem matches the gap named in Related Work's Gap-Closing Bridge, not a substitute or expanded scope.
- Mathematical notation and set/decision-function definitions are used consistently, with every variable defined immediately after introduction.
- Zero informal language in the formal exposition.

## Expected Quality
- A reader can trace the formal notation directly back to the plain-language gap statement in Related Work.
- No variable is used before being defined.

## Red Flags
- Problem Definition formalizes a different or broader problem than Related Work's gap.
- Notation used without definition, or defined inconsistently across the section.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | The formalized problem matches exactly the gap named in Related Work's Gap-Closing Bridge |
| C2 | mandatory | 0 or 40 | Mathematical notation is consistent, and every variable is defined immediately after introduction, with zero informal language |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.80,
  "severity": "error",
  "evidence": { "paragraph_index": 1, "excerpt": "We formalize a broader multi-task objective encompassing classification, ranking, and summarization." },
  "message": "Problem Definition formalizes a broader problem than the single gap Related Work identified."
}
```
