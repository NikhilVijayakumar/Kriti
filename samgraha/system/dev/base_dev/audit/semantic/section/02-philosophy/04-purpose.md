# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Purpose articulates the core reason the product exists. It must be grounded in user need, durable across strategy shifts, and distinct from implementation goals. Every feature decision should trace back to purpose.

## Audit Objectives
- Purpose statement is clear and concise
- Purpose is distinct from business goals or technical strategy
- Purpose remains stable across product iterations
- Purpose is documented and visible to all stakeholders
- Purpose aligns with documented user needs
- Purpose can be used to reject out-of-scope requests

## Expected Quality
- Purpose is stated in a single sentence or short paragraph
- Purpose avoids technical or implementation language
- Purpose differentiates the product from competitors
- Purpose is referenced in decision-making artifacts

## Red Flags
- Purpose that reads like a marketing slogan
- Purpose that changes with every release
- Purpose omitted or buried in unrelated documents
- Purpose indistinguishable from feature list

## Edge Cases
- Multiple competing purpose statements in different docs
- Purpose so broad it fails to constrain decisions
- Purpose so narrow it blocks valuable evolution

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Purpose is documented in a single coherent statement |
| C2 | mandatory | 0 or 30 | Purpose is distinct from business goals and implementation |
| C3 | recommended | 0 or 30 | Purpose is referenced in feature or roadmap decisions |

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
