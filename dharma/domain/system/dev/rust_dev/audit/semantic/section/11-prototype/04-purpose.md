# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
A prototype must have a clearly stated purpose that defines what question it answers or what risk it mitigates. Without an explicit purpose, a prototype cannot be evaluated for fitness. The purpose drives simulation fidelity, scope, and termination criteria.

## Audit Objectives
- Prototype purpose is explicitly stated and documented
- Purpose identifies a specific question, risk, or decision to inform
- Purpose is scoped to a single objective (not a catch-all)
- Purpose distinguishes prototype from production intent
- Intended audience or stakeholder is identified
- Success criteria for the prototype are explicitly stated: what answer to the question counts as success, and what counts as failure — "falsifiable question" alone is insufficient if the answer thresholds are not defined

## Expected Quality
- Purpose is stated in one or two sentences
- Purpose references a concrete decision or unknown
- Purpose clarifies what is NOT being prototyped
- Stakeholder agreement on purpose is documented

## Red Flags
- "Build a prototype of X" without explaining why
- Purpose conflates exploration, validation, and demonstration
- No mention of what happens after the prototype is evaluated
- Purpose reads like a product requirement

## Edge Cases
- Prototype serves multiple implicit purposes (e.g., both technical feasibility and user research)
- Purpose is only known to one stakeholder
- Prototype built to "see if it works" without defining "works" — this is the most common failure mode; C2 must reject it unless a numeric or behavioral threshold is given

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Purpose explicitly stated in the prototype entry point or README |
| C2 | mandatory | 0 or 30 | Purpose references a falsifiable question with explicit success and failure thresholds |
| C3 | recommended | 0 or 30 | Stakeholder or audience is identified |

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
