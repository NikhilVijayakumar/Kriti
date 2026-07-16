# Observability Audit

This section details the Observability Audit.

## Version
1.0.0

## Engineering Intent
Architecture-level observability defines the observability infrastructure itself: the telemetry aggregation backend, the service mesh or sidecar pattern for trace collection, the metrics retention policy, and the system-wide correlation ID strategy. It answers how any individual feature's instrumentation reaches operators and what guarantees exist for data freshness, retention, and access.

## Audit Objectives
- Telemetry backend is identified (e.g., Prometheus, Datadog, OpenTelemetry Collector)
- System-wide correlation ID generation and propagation strategy is documented
- Log aggregation pipeline is described (collection, storage, retention period)
- Metrics retention and downsampling policy is stated
- SLO monitoring architecture is described (how SLOs are tracked system-wide)
- On-call and alerting routing is documented

## Expected Quality
- Telemetry backend choice is justified relative to scale and cost constraints
- Correlation IDs are propagated through all async boundaries (queues, events)
- Log and metric access controls are documented (who can query what)
- Retention periods satisfy compliance and incident investigation needs

## Red Flags
- No observability infrastructure described ("we'll use logs")
- Correlation IDs not required at the architecture level
- Log retention shorter than incident investigation window
- Metrics backend does not support the required SLO tracking granularity
- No access control on raw log data containing PII

## Edge Cases
- Multi-region deployments with separate telemetry backends per region
- Air-gapped environments where cloud telemetry backends are unavailable
- High-cardinality event streams where full sampling is cost-prohibitive

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Telemetry backend identified and correlation ID strategy documented |
| C2 | mandatory | 0 or 30 | Log aggregation pipeline with retention policy described |
| C3 | recommended | 0 or 30 | SLO monitoring architecture and on-call routing documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.93,
  "severity": "error",
  "evidence": { "section_id": 7, "paragraph_index": 0, "excerpt": "All services emit to OpenTelemetry Collector; X-Correlation-ID propagated via HTTP header..." },
  "message": "Telemetry backend and correlation ID strategy documented."
}
```
