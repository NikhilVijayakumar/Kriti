# Load Testing Audit

This section details the Load Testing Audit.

## Version
1.0.0

## Engineering Intent
Load Testing verifies the system behaves acceptably under expected and peak traffic. It exists so performance targets are validated against a defined load profile, not assumed from production experience after the fact.

## Audit Objectives
- Load profiles defined (expected, peak, stress) with concrete numbers
- Performance targets stated per profile (latency, throughput)
- Acceptable degradation thresholds specified — how much slower is still acceptable under peak/stress

## Expected Quality
- Load profiles use real numbers (requests/sec, concurrent users), not "normal load" and "high load"
- Performance targets are measurable and tied to a specific profile
- Degradation thresholds distinguish "acceptable slowdown" from "failure"

## Red Flags
- Load profiles described qualitatively with no numbers
- Performance targets stated without saying under which load profile they apply
- No degradation threshold — pass/fail is all-or-nothing with no graceful boundary

## Edge Cases
- Bursty traffic patterns (not steady-state) — load profile should describe burst shape, not just average rate
- Third-party rate limits that cap achievable load in testing — note the ceiling and how it's worked around

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Load profiles defined with concrete numbers |
| C2 | mandatory | 0 or 30 | Performance targets stated per profile |
| C3 | recommended | 0 or 30 | Acceptable degradation thresholds specified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.86,
  "severity": "error",
  "evidence": { "section_id": 43, "paragraph_index": 0, "excerpt": "We test under normal and high load conditions." },
  "message": "Load Testing gives no concrete numbers for expected/peak/stress profiles."
}
```
