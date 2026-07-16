# Inputs Audit

This section details the Inputs Audit.

## Version
1.0.0

## Engineering Intent
Inputs define the data and triggers the system receives. They must specify source, format, frequency, volume, and validation rules. Good input specifications enable correct boundary testing and data flow verification.

## Audit Objectives
- Every input has a defined source
- Input format and schema are specified
- Validation rules are documented
- Input frequency and volume are quantified
- Error handling for malformed inputs is defined

## Expected Quality
- Inputs include data type and format constraints
- Boundary values are documented ("min 1, max 1000")
- Source system or actor is identified
- Null/empty/missing input behavior is specified

## Red Flags
- Inputs described only as "user provides data"
- Missing validation rules
- No specification of optional vs required inputs
- Input volume assumptions without justification

## Edge Cases
- Empty inputs section (document accepts no inputs)
- Streaming vs batch input sources
- Inputs from external untrusted systems

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every input has a defined source and format |
| C2 | mandatory | 0 or 30 | Validation rules are specified |
| C3 | recommended | 0 or 30 | Input frequency and volume are quantified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.92,
  "severity": "error",
  "evidence": { "section_id": 8, "paragraph_index": 1, "excerpt": "User upload: CSV file, max 10MB, UTF-8 encoded." },
  "message": "Input source and format are fully specified."
}
```
