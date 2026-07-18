# Conclusion Semantic Audit

This section details the Conclusion Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies Conclusion is a concise reinforcement of what Results already validated — no new claims, citations, or future work — and ties back directly to the gap Introduction named. This file owns the receiving end of the Results → Conclusion bridge.

## Audit Objectives
- Every claim in Conclusion is a restatement or direct reinforcement of something already established in Results — no new claims, citations, or future-work items (those belong in Limitations).
- Conclusion explicitly ties back to the gap stated in Introduction.
- Zero informal language or predictable AI transition-word fingerprints.

## Expected Quality
- Concise (1-2 paragraphs), reinforcing empirical validation and applied relevance.

## Red Flags
- A claim, citation, or future-work item appears in Conclusion with no counterpart in Results.
- No explicit connection back to Introduction's stated gap.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | Every claim restates or reinforces something already validated in Results, with no new claims/citations/future-work, and ties back to Introduction's gap |
| C2 | recommended | 0 or 40 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "paragraph_index": 1, "excerpt": "Future work will explore extending this to multilingual settings." },
  "message": "New future-work claim introduced in Conclusion — belongs in Limitations, not Conclusion."
}
```
