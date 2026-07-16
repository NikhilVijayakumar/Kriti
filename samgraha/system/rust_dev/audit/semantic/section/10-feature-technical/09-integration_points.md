# Integration Points Audit

This section details the Integration Points Audit.

## Version
1.0.0

## Engineering Intent
Integration points document every boundary where the feature connects to external systems, other features, shared infrastructure, or platform services. This section must specify the interface contract, protocol, data schema, error contract, and SLA for each integration boundary.

## Audit Objectives
- Every integration point is enumerated with its external system
- The interface contract (API, events, shared DB) is specified
- Protocol and transport details are documented
- Error handling at each integration boundary is defined
- Lifecycle (startup, runtime, teardown) integration behavior is covered

## Expected Quality
- Each integration point has a unique identifier (e.g., IP1, IP2)
- Integration direction (inbound, outbound, bidirectional) is labeled
- Schema or message format is versioned and referenced
- SLA parameters (latency, throughput, availability) are documented per point

## Red Flags
- Missing integration points for features that clearly communicate
- Integration described without protocol or transport
- Error contracts omitted at integration boundaries
- Undocumented assumptions about external system behavior

## Edge Cases
- Integration points used only during deployment or migration
- Integration points that are disabled under feature flags
- Deprecated integration points still referenced in code

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All integration points enumerated with external system |
| C2 | mandatory | 0 or 30 | Interface contract specified per integration point |
| C3 | recommended | 0 or 20 | Error contract documented per boundary |
| C4 | recommended | 0 or 20 | SLA parameters defined for each integration point |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "PaymentGateway (external) via REST over HTTPS..." },
  "message": "All 6 integration points documented with interface contracts."
}
```
