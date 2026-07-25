# Methodology Semantic Audit

This section details the Methodology Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies Methodology's typography matches spec, that it solves only the problem Introduction posed, carries formal complexity analysis where scalability is claimed, and explains algorithmic choices with reasoning rather than mechanical restatement. This file owns the receiving end of the Introduction → Methodology bridge.

## Audit Objectives
- Section heading is Heading 1 (Arial, 12pt bold); subsections are Heading 2 (Arial 12pt) or Heading 3 (Arial 12pt italics); body text is Arial 11pt.
- Methodology introduces no module or solution for a problem never mentioned in Introduction.
- Formal Big-O time/space complexity analysis is present wherever scalability is claimed.
- Algorithm/equation explanations include a "why" clause, not mechanical restatement of the formula.

## Expected Quality
- Every architectural choice is justified against the specific problem stated in Introduction.

## Red Flags
- Heading/subsection/body font or size deviates from spec.
- A module solves a problem never mentioned in Introduction.
- Scalability claimed with no Big-O or empirical foundation.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Heading, subsection, and body typography match spec |
| C2 | mandatory | 0 or 35 | Methodology solves only the problem stated in Introduction, and formal Big-O complexity analysis backs any scalability claim |
| C3 | recommended | 0 or 30 | Algorithm/equation explanations include intuitive "why" reasoning, not mechanical restatement |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "excerpt": "Our approach scales efficiently to large datasets." },
  "message": "Scalability claimed with no Big-O or empirical (latency/memory) foundation."
}
```
