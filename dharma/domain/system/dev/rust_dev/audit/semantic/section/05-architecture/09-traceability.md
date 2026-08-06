# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability maps architecture decisions and elements back to requirements, forward to implementation, and across architecture sections. It ensures every architectural element has a justified origin and that no requirement is lost between specification and design. Good traceability enables impact analysis and compliance verification.

## Audit Objectives
- Architecture elements are traceable to source requirements
- Cross-references between architecture sections are present
- Architectural decisions link to decision records (ADRs)
- Requirements coverage is complete (no orphaned architecture elements)
- External constraints (regulatory, compliance) are traceable to controls

## Expected Quality
- Each major component or decision references its requirement source
- ADR references use stable numeric or slug IDs (e.g., ADR-042, adr-caching-strategy) — title-only references fail because titles change
- Bidirectional traceability: requirements→architecture and architecture→requirements
- Traceability links are validated (no broken refs, no stale requirement IDs)
- Traceability links are maintained across architecture versions
- Missing traceability is explicitly noted as unresolved

## Red Flags
- Orphaned architecture elements with no requirement source
- Missing ADR references for architectural decisions
- ADR referenced by title only (no stable ID) — title rot breaks traceability silently
- Traceability is one-directional only (req→arch but no arch→req)
- Requirement IDs referenced but not defined or resolvable
- Generic traceability statements ("this satisfies the requirements") without specifics
- Traceability to outdated or superseded requirements

## Edge Cases
- System built without formal requirements (traceability to user stories or epics)
- Third-party or COTS components with external documentation traceability
- Regulatory requirements that cascade across multiple architecture elements
- Architecture evolution where traceability spans multiple requirement versions

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Architecture elements are traceable to source requirements or decisions |
| C2 | mandatory | 0 or 30 | Cross-references between architecture sections are present and resolvable |
| C3 | recommended | 0 or 30 | Decision records (ADR) are referenced with stable numeric or slug IDs (not title-only) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.70,
  "severity": "error",
  "evidence": { "section_id": 40, "paragraph_index": 2, "excerpt": "The reporting component satisfies FR-007 and FR-012." },
  "message": "Traceability to requirements present but no cross-reference to architecture sections or ADRs."
}
```
