# Implementation Document Audit

This section details the Implementation Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies an Implementation document coheres internally — the Generation Plan and Security Fix Plan (or whichever plan types are present) must not contradict each other, and the implementation collection as a whole must cohere as one consistent as-built record. Section-level quality is owned by `audit/semantic/section/implementation/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Present plan types (Generation, Refactor, Change Request, Enhancement, Security Fix) are mutually consistent — a Security Fix Plan's stated mitigation shouldn't be undone by an Enhancement Plan's optimization
- All Implementation documents in the domain cohere as one system — no orphaned or contradictory implementation plans for the same feature
- Terminology is consistent across all Implementation sections — the same component/mechanism isn't named differently in different plans

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `folder-structure` | `metrics.mismatch_count`, `evidence[]` | Validates whether the repo's folder structure matches the expected layout. If the doc claims "structure is correct" but the script reports mismatches, that's a grounding conflict. The `evidence` array lists the mismatched paths. |
| `dependency-manifest` | `metrics.manifest_exists` | Validates whether a dependency manifest file exists. If the doc claims dependencies are tracked but the script reports no manifest, flag the contradiction. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about implementation structure

## Expected Quality
- A Security Fix Plan's mitigation is respected by any later Refactor or Enhancement Plan touching the same code
- Multiple plans for the same feature/implementation area don't describe contradictory end states
- Component/mechanism names are used identically across all plan types present

## Red Flags
- An Enhancement Plan's optimization would undo a Security Fix Plan's mitigation with no acknowledgment
- Two Implementation documents for the same feature describe contradictory final states
- A Change Request Plan's impact analysis contradicts what a Refactor Plan in the same area claims is safe
- Same component/mechanism named differently across plan documents

## Edge Cases
- Sequential plans where a later one intentionally supersedes an earlier one — acceptable if the supersession is explicit, not read as an unexplained contradiction
- Plans touching genuinely independent parts of the same feature — acceptable if no actual overlap exists, not flagged as inconsistent by proximity alone

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Present plan types are mutually consistent, security mitigations are respected by later plans |
| C2 | mandatory | 0 or 30 | Terminology (components/mechanisms) consistent across all plans and documents |
| C3 | recommended | 0 or 30 | All Implementation documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 51, "paragraph_index": 1, "excerpt": "Security Fix Plan: 'Disable verbose error messages.' Enhancement Plan: 'Add detailed error messages to improve debuggability.'" },
  "message": "Enhancement Plan reintroduces detail that Security Fix Plan explicitly mitigated against."
}
```
