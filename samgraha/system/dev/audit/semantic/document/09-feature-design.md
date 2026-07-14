# Feature Design Document Audit

This section details the Feature Design Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a Feature Design document coheres internally — User Experience, Workflow, and States must not contradict each other. Section-level quality is owned by `audit/semantic/section/feature-design/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- User Experience, Workflow, and States are mutually consistent — a state transition Workflow describes that States doesn't define, or a UX description that contradicts the actual workflow steps, is a document-level failure
- All Feature Design documents cohere as one system — no two feature designs claiming contradictory UX for the same underlying capability
- Terminology is consistent across all Feature Design sections — the same screen/state/action isn't named differently in different sections

## Expected Quality
- Every state transition in Workflow corresponds to a state defined in States
- User Experience's described interactions match the actual steps in Workflow, not a simplified or different version
- Screen/action/state names are used identically across sections

## Red Flags
- Workflow describes a transition to a state States never defines
- User Experience describes an interaction flow Workflow doesn't actually contain
- Two Feature Design documents give contradictory UX treatment to what should be the same underlying flow
- Same screen or state named differently across sections, confusing Feature Technical Design's realization of it

## Edge Cases
- Feature Design covering multiple variants (e.g. mobile vs. desktop) — acceptable if each variant is internally consistent and the divergence between them is explicit
- Iterative design with a documented "current" vs. "target" state — acceptable if both are clearly labeled, not presented as a single contradictory description

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | User Experience, Workflow, and States are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology (screens/states/actions) consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All Feature Design documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.8,
  "severity": "error",
  "evidence": { "section_id": 37, "paragraph_index": 1, "excerpt": "Workflow: 'transitions to Pending Review state.' States section has no Pending Review state defined." },
  "message": "Workflow describes a transition to a state not defined in States."
}
```
