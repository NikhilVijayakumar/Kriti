# Architecture Document Audit

This section details the Architecture Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Architecture Documentation coheres as one structural model — Component Model, Data Flow, and Communication Paths must describe the same system without contradicting each other, and the collection as a whole must read as one architecture, not several. Section-level quality is owned by `audit/semantic/section/architecture/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Component Model, Data Flow, and Communication Paths are mutually consistent — no component owning data in Data Flow that Component Model doesn't assign to it, no communication path that bypasses a boundary Component Model defines
- All Architecture documents in the domain cohere as one system — no orphaned or contradictory documents describing incompatible structures
- Terminology is consistent across all Architecture sections — a component named in Component Model isn't renamed in Data Flow or Communication Paths

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `module-boundary-diff` | `metrics.boundary_violations`, `evidence[]` | Validates whether the actual module boundaries in the codebase match the declared structure. If the doc claims "boundaries are clean" but the script reports violations, that's a grounding conflict. The `evidence` array lists the violating cross-module imports. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about architectural boundary integrity

## Expected Quality
- Every data ownership claim in Data Flow traces to a component defined in Component Model
- Every communication path in Communication Paths connects components that Component Model actually defines as adjacent/related
- Component names are used identically everywhere they appear across sections and documents

## Red Flags
- Data Flow assigns ownership to a component Component Model never defines
- Communication Paths describes a path between components with no corresponding relationship in Component Model
- Two Architecture documents describe the same component with contradictory responsibilities
- A component is renamed partway through the document set with no migration note

## Edge Cases
- Architecture under active restructuring with a documented transition period — acceptable if both old and new component names are explicitly marked as transitional, not silently inconsistent
- Multi-repository architecture referencing components owned by another repo's documentation — cross-repository references should be explicit, not treated as an internal inconsistency

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Component Model, Data Flow, and Communication Paths are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology (component names) consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All Architecture documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 18, "paragraph_index": 1, "excerpt": "Data Flow: 'Notification Service owns delivery confirmations.' Component Model has no Notification Service." },
  "message": "Data Flow assigns ownership to a component not defined in Component Model."
}
```
