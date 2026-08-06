# Mock APIs Audit

This section details the Mock APIs Audit.

## Version
1.0.0

## Engineering Intent
Prototypes often depend on external services that do not exist or are impractical to call during simulation. Mock APIs must faithfully represent the real interface contract without implementing production logic. Mismatched mocks produce false confidence or false negatives.

## Audit Objectives
- Every external dependency has a defined mock or stub
- Mock returns plausible data shapes matching real API contracts
- Mock latency and error behavior are configurable or documented
- Mock does not leak production credentials or endpoints
- Mock is independently runnable without external network
- Mock data is deterministic or seeded for reproducibility

## Expected Quality
- Mock API surface matches the real API endpoints, methods, and status codes
- Response schemas are defined (even if simplified)
- Error scenarios are represented (timeout, 4xx, 5xx)
- Mock startup is idempotent and requires no manual setup

## Red Flags
- Mock calls real production endpoints silently
- Mock returns static data that never varies
- No error paths in mock responses
- Mock credentials hardcoded in source
- Mock logic duplicates real business rules

## Edge Cases
- Mock for an API that does not have a published contract yet
- Mock used for both prototype and production code (no separation)
- Mock returns success for every call, masking real failure modes

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every external dependency has a mock or stub |
| C2 | mandatory | 0 or 30 | Mock responses match real API schema (or documented deviation) |
| C3 | recommended | 0 or 30 | Mock includes at least one error scenario |

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
