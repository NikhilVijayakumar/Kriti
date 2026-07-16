# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability maps each external dependency and integration point back to its authoritative source — vendor documentation, SLA contracts, API specs, or configuration registries. It ensures every external-context claim is verifiable against an upstream source and that changes to external systems are trackable to internal impact assessments.

## Audit Objectives
- Every external dependency links to its authoritative source
- Integration contract references are bidirectional (internal→external, external→internal)
- Changes in external systems are traceable to internal impact notes
- Source documents are version-pinned or snapshot-referenced
- Traceability matrix covers all external-context documents
- Missing or dead links are identified

## Expected Quality
- Links are stable (permanent URLs, DOIs, or committed snapshots)
- Each traceability entry includes timestamp of last verification
- Forward traces (requirement → source) and backward traces (source → requirement) exist
- Traceability is maintained across dependency version upgrades

## Red Flags
- Dead or redirected links to external sources
- Missing traceability for critical dependencies
- External source document is internal-only (no shared reference)
- Traceability list is empty when dependencies exist
- Links point to uncontrolled documents (wiki pages, team drive files)

## Edge Cases
- External source document no longer exists (404)
- Traceability to an external system that has multiple conflicting sources
- Source document update that invalidates internal assumptions
- Circular traceability (A depends on B depends on A)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Every dependency has link to authoritative source |
| C2 | mandatory | 0 or 30 | Integration contracts have bidirectional traceability |
| C3 | mandatory | 0 or 20 | External changes logged with internal impact notes |
| C4 | recommended | 0 or 20 | Traceability verification date present on each entry |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Stripe Orders API → https://docs.stripe.com/api/orders" },
  "message": "All 3 external dependencies traceable to authoritative sources."
}
```
