# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability connects prototype artifacts — purpose, scope, mocks, data model, constraints — into a coherent chain. Every design decision should be traceable back to the prototype purpose and forward to the code or configuration that implements it. Broken traceability means broken auditability.

## Audit Objectives
- Every prototype artifact references its parent purpose or scope item
- Each mock and data model entity traces to a defined scope element
- Constraints trace to the specific scope, mock, or data model decision they constrain
- No orphaned code, mocks, or data that lack a trace to purpose
- Traceability is documented (matrix, annotations, or cross-references)
- Changes to purpose or scope produce observable traces downstream

## Expected Quality
- A traceability matrix or equivalent exists mapping artifacts to purpose
- Each file or module header references the scope item it implements
- Constraint documentation cites specific mock or model elements
- Trace paths are acyclic and terminate at the purpose statement

## Red Flags
- Files or mocks with no reference to any scope or purpose item
- Purpose changes without corresponding updates to scope or mocks
- Artifacts that are untraceable by design (e.g., "utility" code)
- Traceability documented but never verified against actual code

## Edge Cases
- Scope references a feature that maps to multiple mock implementations
- Purpose is updated mid-prototype but scope trace was never re-run
- Shared mock used by multiple scope items but constraint applies to only one usage path

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every artifact traces to a purpose or scope item |
| C2 | mandatory | 0 or 30 | No orphaned code, mocks, or data without a trace |
| C3 | recommended | 0 or 30 | Traceability matrix or equivalent is documented |

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
