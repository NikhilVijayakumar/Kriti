# Observability Audit

This section details the Observability Audit.

## Version
1.0.0

## Engineering Intent
At the technical design level, observability must be designed in, not bolted on. This requires specifying the instrumentation library, the metric naming convention, the log schema, the trace propagation mechanism, and the SLO targets that drive alerting. Observability design is a first-class deliverable alongside API and data design.

## Audit Objectives
- Instrumentation library or framework is specified
- Metric names follow a documented naming convention with labels/dimensions
- SLO targets (availability%, latency p99, error budget) are defined
- Log schema is documented (required fields: timestamp, level, correlation_id, service, event)
- Distributed trace propagation format is specified (W3C TraceContext, B3, etc.)
- Alerting rules reference specific SLO thresholds
- Runbook or dashboard link is provided per alert

## Expected Quality
- SLO targets are measurable and linked to user-facing SLAs
- Metric cardinality is bounded (no unbounded label values)
- Logs exclude PII by default; redaction rules are documented
- Trace sampling strategy is defined for high-throughput paths

## Red Flags
- No instrumentation library specified
- Metric names invented ad hoc per developer
- SLO defined in prose without numeric threshold
- Logs contain raw user input without redaction
- No runbook or on-call procedure linked to alerts

## Edge Cases
- Async/event-driven paths where a single user action fans out across services
- Long-running batch jobs where per-operation metrics produce cardinality explosions
- Third-party dependencies with no native instrumentation support

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Instrumentation library and metric naming convention specified |
| C2 | mandatory | 0 or 30 | SLO targets (availability, latency, error budget) defined |
| C3 | recommended | 0 or 20 | Log schema with required fields and PII redaction documented |
| C4 | recommended | 0 or 20 | Trace propagation format specified and runbook linked per alert |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.88,
  "severity": "error",
  "evidence": { "section_id": 3, "paragraph_index": 1, "excerpt": "We will add metrics later." },
  "message": "No instrumentation library or metric naming convention specified."
}
```
