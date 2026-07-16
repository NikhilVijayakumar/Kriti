# Constraints Audit

This section details the Constraints Audit.

## Version
1.0.0

## Engineering Intent
Constraints document the deliberate boundaries and limitations that engineering decisions must respect. Good constraint documentation distinguishes between hard constraints that cannot be violated and soft constraints that should be preserved when practical.

## Audit Objectives
- Verify all constraints have clear rationale explaining why they exist
- Check that constraints are categorized as hard or soft
- Ensure constraints reference their origin (architecture, external factors, team decisions)
- Validate that constraint expiry or review conditions are documented
- Confirm implications of violating each constraint are stated

## Expected Quality
- Each constraint has a unique identifier for traceability
- Rationale prevents future teams from unknowingly violating intent
- Constraint scope is precisely defined
- Interactions between constraints are noted when relevant

## Red Flags
- Constraints stated without any justification or context
- Hard vs soft distinction is absent
- No guidance on what to do when constraints conflict

## Edge Cases
- Conflicting constraints where satisfying both is impossible
- Constraints that become obsolete over time
- Environmental constraints (cloud provider, regulatory) that change externally

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each constraint includes rationale and origin |
| C2 | mandatory | 0 or 30 | Hard vs soft constraints are clearly distinguished |
| C3 | recommended | 0 or 30 | Constraint expiry or review cadence is specified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Must use PostgreSQL 15+ per engineering decision ADR-2024-003" },
  "message": "Constraint has clear rationale and origin reference"
}
```
