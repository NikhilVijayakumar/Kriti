# Feature Technical Design Document Audit

This section details the Feature Technical Design Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a Feature Technical Design document coheres internally — Participating Components, Component Interactions, Data Ownership, and Runtime Behavior must describe one consistent realization of the feature, not four independently-written sections. Section-level quality is owned by `audit/semantic/section/feature-technical/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Participating Components, Component Interactions, Data Ownership, and Runtime Behavior are mutually consistent — a component in Component Interactions that Participating Components doesn't list, or a data owner in Data Ownership that Runtime Behavior contradicts, is a document-level failure
- All Feature Technical Design documents cohere as one system — no two documents realizing the same feature with contradictory technical designs
- Terminology is consistent across all sections — the same component/data entity isn't named differently in different sections

## Expected Quality
- Every component referenced in Component Interactions, Data Ownership, or Runtime Behavior appears in Participating Components
- Data Ownership's assignments are consistent with what Runtime Behavior describes each component actually doing
- Component and data entity names are used identically across all sections

## Red Flags
- Component Interactions references a component Participating Components doesn't list
- Data Ownership assigns a data entity to a component Runtime Behavior shows a different component actually managing
- Two Feature Technical Design documents realize the same Feature with contradictory component responsibilities
- Same component/entity named differently across sections

## Edge Cases
- Feature Technical Design realizing a feature across two architectural generations during a migration — acceptable if both are explicitly marked with a transition note, not silently inconsistent
- A component genuinely shared with another feature's Technical Design — acceptable if responsibilities are consistent between both documents, not contradictory

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Participating Components, Component Interactions, Data Ownership, and Runtime Behavior are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology (component/data names) consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All Feature Technical Design documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.86,
  "severity": "error",
  "evidence": { "section_id": 44, "paragraph_index": 0, "excerpt": "Component Interactions: 'Cache Layer forwards to Rate Limiter.' Rate Limiter is not listed in Participating Components." },
  "message": "Component Interactions references a component not listed in Participating Components."
}
```
