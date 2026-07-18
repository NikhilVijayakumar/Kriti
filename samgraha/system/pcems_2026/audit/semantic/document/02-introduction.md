# Introduction Semantic Audit

This section details the Introduction Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies the Introduction's typography matches spec and that the gap it identifies is exactly what Methodology later resolves. This file owns the sending end of the Introduction → Methodology bridge.

## Audit Objectives
- Section heading is Heading 1 (Arial, 12pt bold); body text is Arial 11pt, single column.
- The broader problem space, the specific gap, and the objectives/contributions are each stated, and the gap is specific enough for Methodology to resolve directly.
- Zero informal language or predictable AI transition-word fingerprints.

## Expected Quality
- A reader can name the exact gap Methodology must close after reading only the Introduction.

## Red Flags
- Heading/body font or size deviates from spec.
- Gap stated too vaguely to verify against Methodology.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Heading and body typography match spec (Heading 1 Arial 12pt bold, body Arial 11pt, single column) |
| C2 | mandatory | 0 or 30 | Problem space, specific gap, and objectives/contributions are stated, and the gap is specific enough for Methodology to resolve |
| C3 | recommended | 0 or 20 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "excerpt": "Section heading styled as Heading 2, 11pt" },
  "message": "Introduction heading must be Heading 1, Arial 12pt bold — found Heading 2, 11pt."
}
```
