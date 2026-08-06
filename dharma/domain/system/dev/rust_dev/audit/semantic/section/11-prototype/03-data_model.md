# Data Model Audit

This section details the Data Model Audit.

## Version
1.0.0

## Engineering Intent
A prototype's data model is a simplified representation of real domain entities and their relationships. The model must be sufficient to exercise the prototype scenario without introducing unrealistic constraints or omitted fields that would invalidate simulation results.

## Audit Objectives
- Core entities and their relationships are defined
- Data model is minimal — only fields needed for the prototype purpose exist
- Field types and constraints are documented
- Sample data or fixtures are available
- Model does not accidentally introduce production data or PII
- Data lifecycle (create, read, update, delete) is scoped to prototype needs

## Expected Quality
- Entity-relationship diagram or structured schema is present
- Each entity field has a type, example value, and nullability
- Model documentation distinguishes prototype-required vs nice-to-have fields
- Seed data covers normal, boundary, and minimal cases

## Red Flags
- Data model is a copy of the full production schema
- Fields present but never used by any prototype scenario
- PII or secrets present in sample data
- No seed data or fixtures
- Model is too abstract to produce meaningful simulation output

## Edge Cases
- Model designed around a single happy-path scenario only
- Dates, times, or currencies use inconsistent formats
- Model assumes real-time data availability (e.g., live market prices in a prototype)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Core entities and relationships are documented |
| C2 | mandatory | 0 or 30 | No PII, secrets, or production data in the model |
| C3 | recommended | 0 or 30 | Seed or fixture data covers at least 2 scenarios |

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
