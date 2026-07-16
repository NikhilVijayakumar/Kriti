# Contributing Audit

This section details the Contributing Audit.

## Version
1.0.0

## Engineering Intent
Contributing tells an external contributor how to submit a change that gets accepted — process, review expectations, and quality bar — so a first-time contributor doesn't have to guess or ask.

## Audit Objectives
- Contribution Process describes a concrete step-by-step workflow (fork/branch/PR)
- Code Review states what reviewers check for and how many approvals are needed
- Quality Standards lists concrete expectations, referencing Development setup where relevant

## Expected Quality
- All three required subsections present: Contribution Process, Code Review, Quality Standards
- Process is numbered/sequential, not a vague description
- Quality Standards is specific enough to self-check against before opening a PR

## Red Flags
- No explicit process — just "contributions welcome"
- Code review expectations absent (reader doesn't know what gets a PR merged vs. rejected)
- Quality Standards duplicated verbatim from Development instead of stating contribution-specific expectations

## Edge Cases
- Project not currently accepting external contributions — state that explicitly rather than presenting an inviting but non-functional process
- Contribution process managed entirely via an external CONTRIBUTING.md — a short pointer here is acceptable if that file is linked and covers all three required aspects

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Contribution Process is a concrete, sequential workflow |
| C2 | mandatory | 0 or 30 | Code Review expectations stated (approvals, what's checked) |
| C3 | recommended | 0 or 30 | Quality Standards specific enough to self-check against |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.87,
  "severity": "error",
  "evidence": { "section_id": 13, "paragraph_index": 0, "excerpt": "Contributions welcome! Open a PR." },
  "message": "Contributing has no concrete step-by-step process, review expectations, or quality standards."
}
```
