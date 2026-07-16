# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability maps requirements to implementation artifacts, test cases, and acceptance criteria. It ensures every requirement is addressed and no undocumented behavior exists. Good traceability is bidirectional and exhaustive.

## Audit Objectives
- Every requirement is linked to at least one test case
- Every test case traces back to a requirement
- Trace links are explicit (not implicit)
- No orphaned requirements or test cases
- Traceability covers functional and non-functional requirements

## Expected Quality
- Trace links include direction (forward/backward)
- Links use identifiers (FR1 → TC-FR1)
- Traceability matrix or equivalent exists
- Coverage gaps are documented

## Red Flags
- Requirements with zero trace links
- Test cases attached to no requirement
- Manual traceability without automated verification
- Circular trace links

## Edge Cases
- Empty traceability section
- Many-to-many mappings between requirements and tests
- Cross-document traceability references

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every requirement has at least one trace link |
| C2 | mandatory | 0 or 30 | Every test case traces to a requirement |
| C3 | recommended | 0 or 30 | Traceability is bidirectional and complete |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 12, "paragraph_index": 0, "excerpt": "FR1 → TC-FR1: Login validates credentials." },
  "message": "All 14 requirements have forward trace links."
}
```
