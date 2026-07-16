# Feature Document Audit

This section details the Feature Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a Feature document coheres internally — Functional Requirements, Acceptance Criteria, and Business Rules must not contradict each other, and the feature collection as a whole must be internally consistent. Section-level quality is owned by `audit/semantic/section/feature/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Functional Requirements, Acceptance Criteria, and Business Rules are mutually consistent — an Acceptance Criterion that contradicts a Business Rule, or a Functional Requirement with no corresponding Acceptance Criterion, is a document-level failure
- All Feature documents in the domain cohere as one system — no two features claiming ownership of the same capability with contradictory behavior
- Terminology is consistent across all Feature sections — the same entity or concept isn't named differently in different sections

## Expected Quality
- Every Functional Requirement has at least one Acceptance Criterion that verifies it
- Business Rules are respected by Acceptance Criteria — no criterion that would pass while violating a stated rule
- Entity/concept names are used identically across Functional Requirements, Acceptance Criteria, and Business Rules

## Red Flags
- A Functional Requirement with no corresponding Acceptance Criterion — unverifiable requirement
- An Acceptance Criterion that would pass even though it violates a stated Business Rule
- Two Feature documents claim the same capability with contradictory behavior
- Same entity named differently across sections (e.g. "order" vs. "purchase" for the same concept)

## Edge Cases
- Feature intentionally deferring some Acceptance Criteria to a follow-up (Future Extensions) — acceptable if explicitly noted as deferred, not silently unverifiable
- Overlapping features by design (e.g. a capability intentionally available through two different Feature docs for different audiences) — acceptable if the overlap is explicit and behavior is consistent between them

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Functional Requirements, Acceptance Criteria, and Business Rules are mutually consistent |
| C2 | mandatory | 0 or 30 | Every Functional Requirement has a corresponding Acceptance Criterion |
| C3 | recommended | 0 or 30 | Terminology consistent across all Feature documents |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.84,
  "severity": "error",
  "evidence": { "section_id": 15, "paragraph_index": 0, "excerpt": "FR-3: 'The system shall support bulk export.' No Acceptance Criterion references bulk export." },
  "message": "Functional Requirement FR-3 has no corresponding Acceptance Criterion to verify it."
}
```
