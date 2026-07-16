# Scalability Testing Audit

This section details the Scalability Testing Audit.

## Version
1.0.0

## Engineering Intent
Scalability Testing characterizes how the system behaves as load grows well beyond current levels — where it breaks and how it degrades. Unlike Load Testing (does it meet targets at known profiles), Scalability Testing explores the growth curve itself.

## Audit Objectives
- Growth scenarios defined as multiples of current load (2x, 5x, 10x)
- Breaking points identified — where the system stops scaling linearly or fails outright
- Scaling behavior characterized (linear, sub-linear, cliff) rather than just pass/fail at one point

## Expected Quality
- Growth scenarios are concrete multiples tied to a stated baseline
- Breaking point is a specific number/threshold, not "eventually it breaks"
- Scaling behavior description explains the shape of degradation, useful for capacity planning

## Red Flags
- No growth scenarios — scalability discussed only qualitatively
- Breaking point never identified — testing stops before finding the actual limit
- Scaling behavior reduced to pass/fail with no characterization of the curve

## Edge Cases
- Horizontally scalable systems where the bottleneck is a shared resource (database, queue) — the breaking point analysis should identify that shared resource, not just report an aggregate number
- Cost-prohibitive to test at extreme multiples — acceptable to extrapolate from lower multiples if the extrapolation method is stated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Growth scenarios defined as concrete multiples of baseline |
| C2 | mandatory | 0 or 35 | Breaking points identified with specific thresholds |
| C3 | recommended | 0 or 30 | Scaling behavior characterized (linear/sub-linear/cliff) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.81,
  "severity": "error",
  "evidence": { "section_id": 44, "paragraph_index": 0, "excerpt": "The system should scale reasonably well as usage grows." },
  "message": "Scalability Testing identifies no breaking point or threshold."
}
```
