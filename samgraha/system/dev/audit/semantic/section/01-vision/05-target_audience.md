# Target Audience Audit

This section details the Target Audience Audit.

## Version
1.0.0

## Engineering Intent
The target audience section identifies and describes the primary and secondary audiences for whom the vision is created. It defines who will use, benefit from, or be affected by the envisioned system, including their characteristics, needs, and context of use.

## Audit Objectives
- Primary and secondary audiences are clearly distinguished
- Each audience segment includes relevant characteristics
- Audience needs or pain points are linked to the problem statement
- Audience segmentation is meaningful (not arbitrary demographics)
- Coverage is complete for all stakeholders implied by the vision

## Expected Quality
- Audience descriptions include context, goals, and constraints
- Segments are mutually exclusive where possible
- Each audience has a clear stake in the vision outcomes
- Language is empathetic and user-centered
- Audience size or reach is estimated where relevant

## Red Flags
- Audiences defined by technology role only ("developers", "admins")
- Audience section is a generic persona template without substance
- Key stakeholders implied by the problem are missing from audiences
- Audiences listed but not described or differentiated
- Confusion between target audience (vision readers) and target users (product users)

## Edge Cases
- Audiences with competing or conflicting needs that must be balanced
- Audiences that differ across deployment contexts (region, scale, sector)
- Indirect stakeholders who are affected but not direct users

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Primary and secondary audiences clearly distinguished with characteristics |
| C2 | mandatory | 0 or 30 | All stakeholders implied by the problem are covered |
| C3 | recommended | 0 or 30 | Audience needs and pain points explicitly linked to problem statement |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 7, "paragraph_index": 0, "excerpt": "Primary audience: field inspectors in rural districts with limited connectivity..." },
  "message": "Primary and secondary audiences distinguished with context and characteristics."
}
```
