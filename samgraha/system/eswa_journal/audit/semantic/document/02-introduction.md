# Introduction Semantic Audit

This section details the Introduction Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies the Introduction sets up a Technical Gap that Related Work must later close, and that the Contributions list is concrete rather than a restatement of the abstract in list form. This file owns the Introduction end of the Introduction → Related Work narrative bridge; `03-related-work.md` owns the receiving end.

## Audit Objectives
- Technical Gap & Limitations and Proposed Solution Overview align without contradiction — the Solution must actually close the stated Gap.
- Contributions is a bulleted/numbered list that explicitly signals "novel", "statistically validated", and "complexity" as required by the standard.
- Zero informal language or predictable AI transition-word fingerprints.

## Expected Quality
- The Technical Gap named here is specific enough that a reader could recognize it being closed in Related Work's Gap-Closing Bridge.
- Claims of importance are anchored to specifics, not hollow assertions.

## Red Flags
- Proposed Solution Overview addresses a different problem than the one in Technical Gap.
- Contributions list is prose, not a bulleted/numbered list, or omits novelty/validation/complexity language.
- Informal adjectives or clustered AI transition words.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | Technical Gap and Proposed Solution Overview align without contradiction, and Contributions is a list stating novelty, statistical validation, and complexity analysis |
| C2 | mandatory | 0 or 25 | Zero informal language and low density of predictable AI transition words |
| C3 | recommended | 0 or 15 | Claims of domain importance are grounded in specifics, not hollow assertions |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "paragraph_index": 2, "excerpt": "Technical Gap: 'existing taggers ignore long-range dependencies.' Proposed Solution: 'we present a lightweight annotation UI.'" },
  "message": "Proposed Solution Overview does not address the Technical Gap stated earlier in the Introduction."
}
```
