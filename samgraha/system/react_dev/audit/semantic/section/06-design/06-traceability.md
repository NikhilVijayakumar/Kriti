# Design Traceability Audit

This section details the Design Traceability Audit.

## Version
1.0.0

## Engineering Intent
Design traceability ensures every design decision, component, and visual element can be linked back to a requirement, principle, or user need. It prevents orphaned designs and enables impact analysis when upstream requirements change.

## Audit Objectives
- Every design component is traceable to a requirement or user story
- Design decisions are linked to their rationale
- Bidirectional traceability exists between design artifacts and requirements
- Changes to requirements trigger design impact assessment
- Orphaned or unused design components are identified

## Expected Quality
- Each UI component references its originating requirement ID
- Design change log records rationale and affected requirements
- Traceability matrix covers screens, components, and states
- Impact analysis is documented for all requirement changes

## Red Flags
- Design components with no traceable requirement
- Requirements with no corresponding design artifact
- Missing traceability for error states and edge case screens
- Design changes made without updating traceability records

## Edge Cases
- Shared components used across multiple features with different requirements
- Deprecated components still referenced in traceability documents
- Third-party components with no internal requirement mapping

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All design components traceable to requirements |
| C2 | mandatory | 0 or 30 | Bidirectional traceability matrix exists |
| C3 | recommended | 0 or 30 | Design change log records rationale and affected requirements |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Button component maps to FR-12 (submit action). Error state maps to FR-12.3..." },
  "message": "All 47 design components traceable to requirements with bidirectional mapping."
}
```
