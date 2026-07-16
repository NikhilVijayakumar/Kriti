# Vision Statement Audit

This section details the Vision Statement Audit.

## Version
1.0.0

## Engineering Intent
The vision statement is a concise, aspirational description of the future state the product or system enables. It communicates the long-term transformational goal in a memorable and inspiring way, serving as a north star for strategic decisions.

## Audit Objectives
- Vision statement is concise (typically one to three sentences)
- Vision describes a future state, not current functionality
- Vision is aspirational yet grounded in plausible reality
- Vision differentiates from competitor or status-quo approaches
- Vision is stable enough to guide multi-year decisions

## Expected Quality
- Vision statement can be understood by any stakeholder in under 30 seconds
- Vision avoids technical jargon and implementation specifics
- Vision is memorable and can be repeated consistently across teams
- Vision aligns with the purpose and problem context

## Red Flags
- Vision statement longer than three sentences
- Vision reads as a feature list or product specification
- Vision is indistinguishable from a mission statement
- Vision describes what exists today, not the desired future
- Vision uses buzzwords without concrete meaning ("world-class", "best-in-breed")

## Edge Cases
- Vision statement that covers multiple product lines or platforms
- Vision that must balance aspirational goals with regulatory constraints
- Extremely short vision that lacks sufficient directional guidance

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Vision is 1-3 sentences describing a future state |
| C2 | mandatory | 0 or 30 | Vision is free of implementation-specific language |
| C3 | recommended | 0 or 30 | Vision differentiates from current status quo or alternatives |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 1, "paragraph_index": 0, "excerpt": "We envision a platform where every citizen..." },
  "message": "Vision statement is 2 sentences describing a clear future state."
}
```
