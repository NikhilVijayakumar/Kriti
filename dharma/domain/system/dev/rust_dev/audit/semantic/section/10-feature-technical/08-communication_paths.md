# Communication Paths Audit

This section details the Communication Paths Audit.

## Version
1.0.0

## Engineering Intent
Communication paths describe the data flow topology across the feature, including message routing, channel selection, serialization format, and delivery guarantees. This section must document each distinct path data travels from source to sink, including intermediary transforms and queuing.

## Audit Objectives
- Every distinct data flow path is documented from source to sink
- Message format and serialization are specified per path
- Delivery guarantees (at-most-once, at-least-once, exactly-once) are defined
- Routing logic and addressing scheme are described
- Backpressure handling is documented for each path

## Expected Quality
- Paths are visualized or described with clear start and end points
- Each path has a latency budget allocated
- Synchronous vs asynchronous paths are distinguished
- Data transformation points along the path are called out
- Dead letters or poison message handling is documented

## Red Flags
- Missing paths for data that clearly moves between components
- Undefined delivery guarantees for critical data flows
- No backpressure or flow control mechanism described
- Synchronous paths used where async is standard for the domain

## Edge Cases
- Paths that change at runtime (re-routing, dynamic discovery)
- Unidirectional paths that become bidirectional under error conditions
- Data paths that bypass the documented communication layer

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All communication paths enumerated source-to-sink |
| C2 | mandatory | 0 or 30 | Delivery guarantees defined per path |
| C3 | recommended | 0 or 20 | Backpressure or flow control documented |
| C4 | recommended | 0 or 20 | Serialization format specified per path |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 3, "excerpt": "OrderCreated event: Producer -> Kafka topic event.orders -> Consumer..." },
  "message": "All 5 communication paths documented with delivery guarantees."
}
```
