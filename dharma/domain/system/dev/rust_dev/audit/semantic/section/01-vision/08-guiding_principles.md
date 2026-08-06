# Guiding Principles Audit

This section details the Guiding Principles Audit.

## Version
1.0.0

## Engineering Intent
Guiding principles are actionable rules that translate the vision and philosophy into concrete decision-making criteria. They govern trade-offs, prioritization, and design choices throughout the project lifecycle. Each principle must be prescriptive enough to resolve real disputes.

## Audit Objectives
- Each principle is prescriptive (do this, not that)
- Principles are distinct and non-overlapping
- Principles are ordered or weighted to resolve conflicts
- Principles trace back to the vision, pillars, or philosophy
- Principles are testable (a decision can be evaluated against them)

## Expected Quality
- Principles are written as imperatives with clear direction
- Each principle includes a rationale statement
- Principles are limited to a focused set (typically 5-10)
- Principles address expected trade-off scenarios
- Principles are consistent across the document ecosystem

## Red Flags
- Principles that are vague or non-actionable ("be good")
- Principles that contradict each other without guidance
- Principles that describe aspirations rather than decision rules
- Principles that duplicate pillar or philosophy content
- Principles that are too many to remember or apply consistently

## Edge Cases
- Principles that apply differently across product lifecycle phases
- Principles that conflict with organizational policies or regulations
- Principles that require interpretation for novel situations

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each principle is prescriptive with clear decision-making direction |
| C2 | mandatory | 0 or 30 | Principles are distinct, limited in number, and include rationale |
| C3 | recommended | 0 or 30 | Principles address expected trade-off scenarios with ordering |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 6, "paragraph_index": 2, "excerpt": "Principle 4: Default to open — all non-sensitive data must be machine-readable..." },
  "message": "Each principle is prescriptive and provides clear decision direction."
}
```
