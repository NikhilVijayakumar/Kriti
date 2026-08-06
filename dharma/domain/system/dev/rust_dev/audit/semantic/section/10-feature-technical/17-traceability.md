# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability documents the links between feature requirements, design decisions, implementation artifacts, and verification artifacts. This section must provide bidirectional trace from requirements to code, code to tests, and design decisions to their rationale, enabling impact analysis and completeness verification.

## Audit Objectives
- Every requirement is traceable to its implementation component(s)
- Every implementation component is traceable to at least one requirement
- Design decisions are linked to their ADRs or rationale documents
- Tests are mapped to the requirements or specifications they verify
- Trace links are bidirectional (requirements to code and code to requirements)
- Gaps or untraced elements are documented

## Expected Quality
- Traceability matrix or equivalent structure is present
- Links use stable identifiers that survive refactoring
- Coverage gaps are explicitly called out, not hidden
- Traceability is machine-readable for automated verification
- Cross-references between related trace items are maintained

## Red Flags
- Requirements or components present in code but absent from traceability
- Unidirectional traces that can't be navigated in reverse
- Stale or broken trace links
- Traceability that only covers happy path requirements
- Missing traceability for cross-cutting concerns

## Edge Cases
- Traceability for deprecated but still deployed features
- Verifying traceability for generated code or configurations
- Requirements that can't be cleanly traced to a single component

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Bidirectional trace between requirements and components |
| C2 | mandatory | 0 or 30 | All tests mapped to requirements or specifications |
| C3 | recommended | 0 or 20 | Design decisions linked to ADR documents |
| C4 | recommended | 0 or 20 | Gaps and untraced elements explicitly documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "FR1 -> OrderValidator.validate() -> OrderValidationTests/TC1..." },
  "message": "Bidirectional traceability established for all 12 requirements across 8 components."
}
```
