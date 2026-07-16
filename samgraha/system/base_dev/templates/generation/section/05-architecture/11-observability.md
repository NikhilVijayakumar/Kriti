# Observability — Generation Template

> **Domain:** architecture
> **Section:** observability
> **Source:** `audit/semantic/section/05-architecture/11-observability.md`
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Observability section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / testing_standards | Observability must be consistent with Engineering's testing standards |

## Template

```markdown
## Observability

### Telemetry Backend
[Identified backend — e.g. OpenTelemetry Collector, Prometheus, Datadog — with justification relative to scale and cost]

### Correlation ID Strategy
[How correlation IDs are generated, propagated through async boundaries (queues, events), and used for request tracing]

### Log Aggregation Pipeline
[Collection, storage, retention period, access controls]

### Metrics Retention
[Retention and downsampling policy, SLO monitoring architecture]

### On-Call and Alerting
[Alert routing, on-call escalation, SLO breach notification]
```

## Examples

**Correct:**
> **Telemetry Backend**
> - Backend: OpenTelemetry Collector → ClickHouse for traces, Prometheus for metrics
> - Justification: ClickHouse handles high-cardinality trace data at scale; Prometheus chosen for SLO recording rules and cost-effectiveness at current metric volume
>
> **Correlation ID Strategy**
> - Generated: UUID v4 at system entry point (Ingestion Service)
> - Propagated: X-Correlation-ID header across HTTP; embedded in event envelope for async paths
> - Scope: All requests carry correlation ID; spans emitted per component hop
>
> **Log Aggregation Pipeline**
> - Collection: Fluentd sidecar per component
> - Storage: ClickHouse, 90-day hot retention, 1-year cold (S3)
> - Access: Read-only for all engineers; PII fields redacted at collection time
>
> **Metrics Retention**
> - Raw metrics: 30 days
> - Downsampled (5m): 90 days
> - SLO burn rate alerts: 1% and 10% thresholds, 5m and 1h windows

**Incorrect:**
> We use logs and metrics. Correlation IDs are nice to have. Retention is handled by the platform team.
> *Why wrong: lacks specific infrastructure, retention periods, access controls, and correlation strategy — the audit expects architectural observability decisions, not vague aspirations.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** operator
- **Do:** Identify the telemetry backend with justification; document correlation ID generation and propagation across all async boundaries; define log retention and access controls; specify SLO monitoring architecture
- **Don't:** Name tools without justification; leave correlation ID propagation implicit; omit retention periods; conflate architecture-level observability with feature-level instrumentation

**Minimum content:** Telemetry backend, correlation ID strategy
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Component Model, Communication, Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
