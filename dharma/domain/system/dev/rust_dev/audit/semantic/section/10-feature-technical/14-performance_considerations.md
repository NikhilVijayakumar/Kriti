# Performance Considerations Audit

This section details the Performance Considerations Audit.

## Version
1.0.0

## Engineering Intent
Performance considerations document the non-functional performance requirements and expected behavior of the feature under various load conditions. This section must specify latency targets (p50, p95, p99), throughput capacity, concurrency limits, resource utilization profiles, and performance degradation characteristics.

## Audit Objectives
- Latency targets are specified with percentile levels
- Throughput capacity (transactions per second) is defined
- Concurrency limits for simultaneous users or requests are stated
- Resource utilization profile (CPU, memory, IO) per transaction is documented
- Performance degradation behavior under load is described
- Caching strategy and cache invalidation are covered

## Expected Quality
- Performance targets are realistic and based on user research or SLAs
- Targets distinguish between average and peak load
- Cold-start vs warm performance characteristics are documented
- Performance test criteria are referenced
- Bottlenecks and known performance risks are called out

## Red Flags
- Performance targets stated without percentiles ("under 200ms")
- No distinction between normal and peak load
- Missing resource utilization estimates
- Caching strategy described without invalidation rules
- "Optimize later" without defining what good enough means now

## Edge Cases
- Performance characteristics when dependent services are degraded
- Thundering herd scenarios for cache expiration
- Resource contention with co-located features

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Latency targets with percentile levels specified |
| C2 | mandatory | 0 or 30 | Throughput and concurrency limits defined |
| C3 | recommended | 0 or 20 | Resource utilization profile per transaction |
| C4 | recommended | 0 or 20 | Caching strategy with invalidation documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 1, "excerpt": "p99 latency: 500ms, throughput: 5000 TPS, max concurrent: 200..." },
  "message": "Performance targets specified with percentiles and throughput figures."
}
```
