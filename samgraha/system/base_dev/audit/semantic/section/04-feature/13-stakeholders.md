# Stakeholders Audit

This section details the Stakeholders Audit.

## Version
1.0.0

## Engineering Intent
Stakeholders identify individuals or groups with interest in the feature's outcome. They must specify role, responsibility, and engagement model. Good stakeholder documentation ensures the right people are consulted at each decision point.

## Audit Objectives
- Every stakeholder has a clearly defined role
- Responsibility per stakeholder is specified
- Engagement frequency or trigger is documented
- Decision authority is assigned
- Stakeholder communication channels are identified

## Expected Quality
- Stakeholders are categorized by role type
- Contact or escalation path is documented
- Stakeholder influence on scope decisions is noted
- RACI or equivalent model is used

## Red Flags
- Stakeholders listed without roles or responsibilities
- Missing key stakeholders (QA, security, ops)
- Stakeholder list that is identical for every feature
- No escalation path for blocked decisions

## Edge Cases
- Empty stakeholders section
- Single stakeholder acting in multiple roles
- External stakeholders with contractual constraints

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every stakeholder has a defined role and responsibility |
| C2 | mandatory | 0 or 30 | Decision authority is assigned |
| C3 | recommended | 0 or 30 | Engagement model or frequency is documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.92,
  "severity": "error",
  "evidence": { "section_id": 3, "paragraph_index": 0, "excerpt": "Product Owner: Jane Doe — approves scope changes." },
  "message": "Each stakeholder has a named role and stated responsibility."
}
```
