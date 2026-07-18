# Conclusion Semantic Audit

This section details the Conclusion Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies Conclusion's typography matches spec and that its claims are grounded in what Findings actually validated, not overstated. This file owns the receiving end of the Findings → Conclusion bridge.

## Audit Objectives
- Section heading is Heading 1 (Arial, 12pt bold); body text is Arial 11pt.
- Claims of contribution/superiority are grounded in what Findings demonstrated — no unsupported claims.

## Expected Quality
- Every summarized contribution has a traceable counterpart in Findings.

## Red Flags
- Heading/body font or size deviates from spec.
- A claim of superiority with no corresponding result in Findings.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Heading and body typography match spec |
| C2 | mandatory | 0 or 30 | Claims of contribution/superiority are grounded in what Findings actually validated |
| C3 | recommended | 0 or 20 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.80,
  "severity": "error",
  "evidence": { "excerpt": "Our method is the best-performing approach in the field." },
  "message": "Superiority claim has no corresponding baseline comparison in Findings."
}
```
