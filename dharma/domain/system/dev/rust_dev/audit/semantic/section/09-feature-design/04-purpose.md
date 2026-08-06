# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Purpose defines the core rationale for a feature: what problem it solves and why it exists. A clear purpose ensures alignment across stakeholders and prevents scope creep by anchoring all decisions to the feature's intended value.

## Audit Objectives
- Feature purpose is explicitly stated and unambiguous
- Purpose aligns with product strategy and user needs
- Purpose is distinguishable from implementation or solution details
- Value proposition is quantified or qualifiable
- Purpose is consistent across related documents

## Expected Quality
- Purpose is stated in a single concise paragraph
- Purpose references a specific user need or pain point
- Success criteria can be derived from purpose
- Purpose does not prescribe UI layout or technology

## Red Flags
- Purpose describes "how" instead of "why"
- Purpose is generic (e.g., "improve user experience")
- Purpose contradicts existing feature or product goals
- Multiple conflicting purposes listed

## Edge Cases
- Purpose that overlaps with another feature (boundary ambiguity)
- Purpose that is purely internal/technical with no user-facing benefit
- Feature without a stated purpose

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Purpose is explicitly stated and unambiguous |
| C2 | mandatory | 0 or 30 | Purpose aligns with product strategy and user needs |
| C3 | recommended | 0 or 30 | Purpose is distinguishable from implementation details |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "..." },
  "message": "..."
}
```
