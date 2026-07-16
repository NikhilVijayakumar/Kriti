# Runtime Constraints Audit

This section details the Runtime Constraints Audit.

## Version
1.0.0

## Engineering Intent
Runtime constraints specify measurable resource limits and environmental bounds the feature must operate within. This section must document memory limits, CPU quotas, disk IPS, network bandwidth, concurrent user capacity, request rate limits, and any other runtime resource budgets.

## Audit Objectives
- All resource constraints are enumerated with numeric thresholds
- Measurement units are specified (MB, QPS, ms p99)
- Constraints differentiate between normal and burst mode
- Hard limits vs soft advisory limits are distinguished
- Monitoring or alerting thresholds reference these constraints

## Expected Quality
- Constraints are realistic and based on load testing or capacity planning
- Constraints are versioned and have a review date
- Constraint violations have documented consequences
- Scaling behavior near limits is described

## Red Flags
- Constraints stated without numeric values ("low memory footprint")
- Hard limits that contradict infrastructure capabilities
- Constraints that are impossible to verify or measure
- No distinction between dev, staging, and production constraints

## Edge Cases
- Constraints that differ by deployment environment
- Constraints that change based on feature flag state
- Zero-value constraints (no limit specified)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All runtime constraints enumerated with numeric thresholds |
| C2 | mandatory | 0 or 30 | Measurement units specified per constraint |
| C3 | recommended | 0 or 20 | Normal vs burst mode constraints distinguished |
| C4 | recommended | 0 or 20 | Hard and soft limits clearly differentiated |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 1, "excerpt": "Max heap: 512 MB, Max RPS: 1000, p99 latency: 200ms..." },
  "message": "All 6 runtime constraints have numeric thresholds with units."
}
```
