# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
The traceability section establishes how the vision connects to downstream artifacts — requirements, design decisions, implementation plans, and verification activities. It ensures that every element of the vision can be traced forward to concrete outcomes and that no orphaned or untraced vision elements exist.

## Audit Objectives
- Every vision element maps to at least one downstream artifact type
- Traceability links are bidirectional (forward to implementation, backward to vision)
- Traceability matrix or mapping method is clearly defined
- Gaps in traceability are identified and documented
- Traceability is maintained across document versions and revisions

## Expected Quality
- Traceability uses a consistent identifier scheme across documents
- Traceability coverage is complete (no vision element is orphaned)
- Traceability links include rationale for the connection
- The method for maintaining traceability over time is documented
- Tools or processes for traceability management are specified

## Red Flags
- No traceability links defined between vision and downstream artifacts
- Traceability is only forward (vision to requirements) without backward linkage
- Traceability identifiers are inconsistent or missing
- Orphaned vision elements with no corresponding downstream artifacts
- Traceability section is placeholder or "to be determined" without substance

## Edge Cases
- Vision elements that span multiple downstream documents or repositories
- Traceability across different versions or baselines of the vision document
- Traceability for elements that are intentionally deferred or deprioritized

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every vision element maps to at least one downstream artifact type |
| C2 | mandatory | 0 or 30 | Traceability uses consistent identifiers and is bidirectional |
| C3 | recommended | 0 or 30 | Traceability maintenance process and tools are documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 9, "paragraph_index": 0, "excerpt": "Vision Element VE-3 (Pillar: Data Integration) maps to Requirements REQ-12 through REQ-18..." },
  "message": "All 7 vision elements map to downstream artifacts with bidirectional identifiers."
}
```
