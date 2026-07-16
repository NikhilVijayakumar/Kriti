# Purpose Audit

Rubric for auditing the **purpose** section of build documentation.

## Engineering Intent

Build purpose and scope definition.

## Red Flags

- Section is missing or empty
- Content is generic rather than specific to this project
- Claims are not backed by evidence or examples
- Section contradicts information in other sections

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Section exists with substantive content specific to this project |
| C2 | mandatory | 0 or 30 | Content is internally consistent and does not contradict other sections |
| C3 | recommended | 0 or 30 | Content includes concrete examples, evidence, or project-specific detail |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "section": "purpose",
  "score": 0-100,
  "criteria": [
    {
      "id": "C1",
      "passed": true/false,
      "score": 0-40,
      "evidence": "string"
    }
  ],
  "findings": ["string"]
}
```
