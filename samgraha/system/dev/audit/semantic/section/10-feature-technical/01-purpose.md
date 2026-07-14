# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Purpose defines the rationale, problem statement, and motivation for the feature from a technical perspective. This section must explain what technical problem the feature solves, why existing mechanisms are insufficient, and what engineering value the feature delivers in terms of system qualities.

## Audit Objectives
- The technical problem being solved is clearly stated
- The motivation explains why existing solutions are inadequate
- Engineering value (reduced complexity, improved reliability, etc.) is articulated
- The purpose is distinguishable from business goals
- Success criteria for the feature's technical impact are defined

## Expected Quality
- Purpose is specific to the feature-technical domain, not marketing
- Problem statement includes measurable impact of not solving it
- Technical debt or architectural improvement rationale is included
- Purpose aligns with the system's architectural direction

## Red Flags
- Purpose is identical to business requirements
- Problem statement is vague or generic ("improve user experience")
- No clear engineering value proposition
- Purpose describes the solution rather than the problem
- Purpose contradicts established architectural decisions

## Edge Cases
- Feature with multiple purposes that may conflict
- Purpose that has been obsoleted by other changes
- Retrospective purpose that justifies already-built functionality

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Technical problem and motivation clearly stated |
| C2 | mandatory | 0 or 30 | Engineering value proposition articulated |
| C3 | recommended | 0 or 30 | Success criteria for technical impact defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Current order validation logic is duplicated across 4 services..." },
  "message": "Technical problem, motivation, and engineering value clearly defined."
}
```
