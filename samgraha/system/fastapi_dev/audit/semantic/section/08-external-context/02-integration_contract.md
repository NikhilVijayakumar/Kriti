# Integration Contract Audit

This section details the Integration Contract Audit.

## Version
1.0.0

## Engineering Intent
Integration contracts define the formal interface between the system and external dependencies: API endpoints, data schemas, protocol versions, authentication mechanisms, and expected behaviors. They serve as the source of truth for integration correctness.

## Audit Objectives
- Every external dependency has a documented integration contract
- Contract specifies request/response schemas or equivalent protocol definition
- Authentication and authorization method is documented
- API version or protocol version is pinned
- Rate limits, throttling, and retry policies are specified
- Error handling and fallback behavior is defined

## Expected Quality
- Contracts are versioned and referenceable
- Schema definitions use consistent formats (OpenAPI, Protobuf, etc.)
- All fields have defined types and constraints
- Timeout and circuit-breaker parameters are documented
- Contract changes are tracked with changelogs

## Red Flags
- No integration contract for a critical external dependency
- Contract references API version "latest" (unpinned)
- Missing error response schemas or status code documentation
- Authentication credentials or secrets leaked in contract examples
- Contract documents behavior that differs from actual implementation

## Edge Cases
- Contract version mismatch between document and deployed dependency
- Deprecated endpoints still listed in active contract
- Optional vs required fields ambiguity in schema
- Contract with zero defined failure modes

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 25 | Contract exists for every external dependency |
| C2 | mandatory | 0 or 25 | API version or protocol version is pinned |
| C3 | mandatory | 0 or 25 | Request/response schemas documented |
| C4 | recommended | 0 or 25 | Rate limits, retry, and error handling defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "POST /api/v2/orders (Stripe Orders API)" },
  "message": "Contract documented for all 4 external dependencies."
}
```
