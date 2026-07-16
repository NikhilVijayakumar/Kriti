# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Purpose defines the feature's reason for existence and the problem it solves. It must be concise, stakeholder-aligned, and grounded in user or business need. A well-written purpose ensures everyone agrees on why the feature matters before discussing how to build it.

## Audit Objectives
- Purpose states the problem being solved
- Purpose identifies the target users or stakeholders
- Purpose is aligned with business goals
- Purpose is concise (not a requirements list)
- Purpose differentiates from existing solutions

## Expected Quality
- Purpose is 2-5 sentences (not paragraphs)
- User or business need is explicitly named
- Purpose does not prescribe implementation
- Purpose is written in plain language

## Red Flags
- Purpose that reads as a list of features
- Missing problem statement (starts with solution)
- Purpose that is too vague ("improve user experience")
- Purpose that duplicates the project charter

## Edge Cases
- Empty purpose section
- Purpose that conflicts with requirements
- Multiple competing purposes in one section

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Problem statement is clear and specific |
| C2 | mandatory | 0 or 30 | Target users or stakeholders are identified |
| C3 | recommended | 0 or 30 | Purpose is concise and implementation-free |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.97,
  "severity": "error",
  "evidence": { "section_id": 1, "paragraph_index": 0, "excerpt": "Reduce password reset friction for enterprise SSO users." },
  "message": "Purpose clearly states the problem and user need."
}
```
