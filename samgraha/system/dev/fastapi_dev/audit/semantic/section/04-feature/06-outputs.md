# Outputs Audit

This section details the Outputs Audit.

## Version
1.0.0

## Engineering Intent
Outputs define what the system produces or exposes. They must specify format, destination, frequency, and data structure. Good output specifications enable correct integration testing and consumer contract verification.

## Audit Objectives
- Every output has a defined consumer or destination
- Output format and schema are specified
- Output frequency and timing are documented
- Error output behavior is defined
- Output volume is quantified

## Expected Quality
- Outputs include data schema or field definitions
- Delivery mechanism is specified (API, file, event, UI)
- Success and failure output paths are documented
- Output size estimates are provided

## Red Flags
- Outputs described only as "system returns data"
- Missing schema or format specification
- No distinction between normal and error outputs
- Output assumptions about consumer capabilities

## Edge Cases
- Empty outputs section (system produces no outputs)
- Outputs consumed by multiple downstream systems
- Outputs that trigger external side effects

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every output has a defined consumer and format |
| C2 | mandatory | 0 or 30 | Output schema or structure is specified |
| C3 | recommended | 0 or 30 | Output frequency and volume are quantified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.91,
  "severity": "error",
  "evidence": { "section_id": 9, "paragraph_index": 2, "excerpt": "Export: JSON file written to S3 bucket, schema in appendix A." },
  "message": "Output consumer and format are fully specified."
}
```
