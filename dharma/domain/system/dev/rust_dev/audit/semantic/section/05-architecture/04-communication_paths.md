# Communication Paths Audit

This section details the Communication Paths Audit.

## Version
1.0.0

## Engineering Intent
Communication paths define how components interact: protocols, message formats, invocation patterns, and network topology. Each path should specify directionality, protocol, synchronization model, and quality-of-service characteristics. Complete documentation enables integration testing and failure mode analysis.

## Audit Objectives
- All inter-component communication paths are documented
- Each path specifies protocol, direction, and synchronization model
- Message formats or schemas are referenced
- Network topology and connectivity requirements are described
- Quality-of-service guarantees (latency, throughput, reliability) are stated
- Error handling and retry strategies are defined per path

## Expected Quality
- Paths are mapped to specific component interfaces
- Protocol versions are specified where relevant
- Synchronous and asynchronous paths are clearly distinguished
- Timeouts, retries, and circuit-breaker settings are documented
- Communication patterns (request-reply, publish-subscribe, etc.) are identified

## Red Flags
- Missing communication paths between documented components
- Protocol or API version not specified
- Synchronization model ambiguous (sync vs. async unclear)
- Network dependencies assumed but not stated
- No error handling or retry strategy
- Communication paths described using implementation code (not architecture)

## Edge Cases
- Self-contained components with no external communication
- Bidirectional communication over a single path (duplex)
- Third-party communication paths with versioning concerns
- Polyglot protocols — different paths using different transport layers

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All inter-component communication paths are identified with protocol and direction |
| C2 | mandatory | 0 or 30 | Synchronization model and quality-of-service are defined per path |
| C3 | recommended | 0 or 30 | Error handling and retry strategies are documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 25, "paragraph_index": 1, "excerpt": "The Auth Service calls User Service over REST." },
  "message": "Protocol specified (REST) but no direction, timeout, or retry strategy documented."
}
```
