# Smoke Testing Audit

This section details the Smoke Testing Audit.

## Version
1.0.0

## Engineering Intent
Smoke Testing is a fast, minimal check that the core system is functioning after a deploy — not full verification, just "is it alive and basically working." It exists to catch catastrophic deploy failures immediately.

## Audit Objectives
- Core function scope defined — what "basically working" actually checks
- Pass/fail criteria stated explicitly
- Execution timing specified (post-deploy, pre-traffic-shift, etc.) with a maximum duration threshold

## Expected Quality
- Scope is deliberately narrow — a handful of critical checks, not a full regression pass
- Pass/fail is binary and automatable, not subjective
- Duration threshold is short (seconds to low minutes) — a long smoke test defeats its purpose

## Red Flags
- Smoke test scope overlaps heavily with the full test suite (defeats the "fast check" purpose)
- No duration threshold — smoke test could silently take as long as full regression
- Pass/fail criteria left ambiguous ("looks okay")

## Edge Cases
- Multi-region deploys — smoke test scope should state whether it runs per-region or against one representative region
- Feature-flagged deploys — smoke test should cover the flag's default state, noted explicitly

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Core function scope defined narrowly and explicitly |
| C2 | mandatory | 0 or 30 | Pass/fail criteria stated explicitly |
| C3 | recommended | 0 or 30 | Execution timing and maximum duration threshold specified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C3",
  "passed": false,
  "confidence": 0.79,
  "severity": "warning",
  "evidence": { "section_id": 42, "paragraph_index": 0, "excerpt": "Smoke tests run after every deploy." },
  "message": "Smoke Testing states when it runs but gives no maximum duration threshold."
}
```
