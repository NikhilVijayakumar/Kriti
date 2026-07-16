# Observability Audit

This section details the Observability Audit.

## Version
1.0.0

## Engineering Intent
A feature must be observable in production. Observability means operators can determine current health, diagnose failures, and track business outcomes without modifying code. This requires structured logging, metrics emission with defined SLIs, and distributed trace instrumentation.

## Audit Objectives
- Metrics emitted by the feature are enumerated (SLIs: request rate, error rate, latency percentiles)
- Logging strategy is defined (log levels, structured fields, correlation ID propagation)
- Alerting thresholds are specified for error rate and latency SLIs
- Trace instrumentation spans are named and documented
- Dashboard or monitoring view requirements are referenced

## Expected Quality
- SLI definitions reference the feature's performance targets
- Log events cover feature entry, exit, and all failure paths
- Correlation IDs propagated from inbound request to all downstream calls
- Alert thresholds distinguish page-worthy incidents from noise

## Red Flags
- No metrics defined (feature is a black box in production)
- Log statements use unstructured strings without fields
- No correlation ID on outbound calls
- Alert missing for the feature's primary failure mode
- Metrics defined but no alerting thresholds stated

## Edge Cases
- Features with no user-facing surface (batch jobs, background workers)
- Features that proxy third-party services (observability at boundary vs inside)
- High-frequency features where per-request logging is cost-prohibitive

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | SLIs (rate, error, latency) enumerated and linked to performance targets |
| C2 | mandatory | 0 or 30 | Logging strategy defined with structured fields and correlation ID |
| C3 | recommended | 0 or 30 | Alert thresholds specified for primary failure modes |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.92,
  "severity": "error",
  "evidence": { "section_id": 5, "paragraph_index": 0, "excerpt": "Metrics: feature_request_total, feature_error_rate, feature_latency_p99..." },
  "message": "SLIs defined and cross-referenced to p99 latency target of 200ms."
}
```
