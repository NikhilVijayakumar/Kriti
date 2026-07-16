# Failure Handling Audit

This section details the Failure Handling Audit.

## Version
1.0.0

## Engineering Intent
Failure handling documents how the feature detects, responds to, and recovers from errors, exceptions, and degraded states. This section must describe error detection mechanisms, fallback strategies, retry policies, circuit breakers, and data consistency guarantees during failure scenarios.

## Audit Objectives
- All known failure modes are enumerated
- Detection mechanism is defined per failure mode
- Retry policy (count, interval, backoff) is specified
- Fallback behavior or degradation path is documented
- Data consistency guarantees during failures are stated
- Recovery procedure (auto vs manual) is defined

## Expected Quality
- Failure modes are categorized (transient, permanent, security)
- Each failure mode has a severity level
- Retry policies include jitter and max duration
- Error paths have test coverage referenced
- Downstream system failure propagation is mapped

## Red Flags
- Catch-all "retry forever" without max attempts or backoff
- No distinction between recoverable and unrecoverable errors
- Silent failures without logging or metrics
- Undocumented cascading failure risks

## Edge Cases
- Partial failure (some sub-operations succeed, others fail)
- Failure during a rollback of a previous failure
- System clock skew affecting retry interval calculations

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All failure modes enumerated with detection mechanism |
| C2 | mandatory | 0 or 30 | Retry policy defined per failure mode |
| C3 | recommended | 0 or 20 | Fallback or degradation behavior documented |
| C4 | recommended | 0 or 20 | Data consistency guarantees stated for failure scenarios |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 2, "excerpt": "DB timeout: retry 3x with exponential backoff (100ms base)..." },
  "message": "All 8 failure modes enumerated with retry policies."
}
```
