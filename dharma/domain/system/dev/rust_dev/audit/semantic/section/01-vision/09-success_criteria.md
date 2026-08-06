# Success Criteria Audit

This section details the Success Criteria Audit.

## Version
1.0.0

## Engineering Intent
The success criteria section defines measurable outcomes that determine whether the vision has been achieved. These criteria bridge the aspirational vision statement to concrete, verifiable results. They should span multiple dimensions (user, business, technical, operational) and be time-bound where applicable.

## Audit Objectives
- Success criteria are specific and measurable, not vague aspirations
- Criteria cover multiple dimensions (user, business, technical)
- Each criterion has a clear target or threshold
- Criteria are traceable back to the vision statement and pillars
- Criteria are realistic and achievable within the vision horizon

## Expected Quality
- Success criteria use quantitative metrics where possible
- Qualitative criteria include clear evaluation rubrics
- Criteria distinguish between leading indicators and lagging outcomes
- Each criterion includes a timeframe or milestone reference
- Criteria are limited to the most impactful measures (avoid metric bloat)
- Criteria across dimensions are prioritized: when user, business, and technical criteria conflict, the document states which dimension takes precedence and why
- Leading indicators are specified so early success (or failure) is detectable before lagging outcomes are measurable

## Red Flags
- Criteria that are untestable ("users will love the system")
- Criteria that measure outputs instead of outcomes ("deploy 5 features")
- Criteria that are aspirational without measurable thresholds
- Criteria that cover only one dimension (e.g., technical only)
- Criteria that are impossible to verify within the vision timeline
- Multi-dimensional criteria with no conflict resolution — if user satisfaction and technical debt reduction point in opposite directions, the document is silent on which wins

## Edge Cases
- Success criteria that apply differently across phased delivery
- Criteria that require external factors beyond the project's control
- Qualitative criteria in domains where measurement is inherently subjective

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Criteria are specific, measurable, and include clear targets |
| C2 | mandatory | 0 or 30 | Criteria span multiple dimensions (user, business, technical) |
| C3 | recommended | 0 or 30 | Criteria include timeframes, distinguish leading vs lagging, and state dimension priority for conflict resolution |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 8, "paragraph_index": 1, "excerpt": "Success metric: reduce form processing time from 4 hours to under 30 minutes..." },
  "message": "Success criteria are specific, measurable, and span user and operational dimensions."
}
```
