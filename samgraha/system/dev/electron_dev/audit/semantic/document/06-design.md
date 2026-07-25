# Design Document Audit

This section details the Design Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Design Documentation coheres as one reusable design system — Design Principles, UX Principles, and Accessibility must not contradict each other, and the collection reads as one design language, not several competing ones. Section-level quality is owned by `audit/semantic/section/design/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Design Principles, UX Principles, and Accessibility are mutually consistent — an interaction principle that conflicts with an accessibility requirement is a document-level failure
- All Design documents in the domain cohere as one system — no orphaned or contradictory design guidance
- Terminology is consistent across all Design sections — the same pattern or principle isn't named differently in different sections

## Expected Quality
- Every UX Principle is compatible with the Accessibility requirements stated elsewhere — no principle that would break keyboard navigation or screen-reader support
- Design Principles' stated priorities are reflected consistently in UX Principles' specific guidance
- A named pattern (e.g. "progressive disclosure") means the same thing everywhere it's referenced

## Red Flags
- A UX Principle recommends an interaction pattern Accessibility explicitly prohibits
- Two Design documents propose contradictory visual or interaction guidance for the same pattern
- Design Principles state a priority that UX Principles' concrete guidance never actually reflects
- Same design concept given different names across sections, creating ambiguity for Feature Design authors

## Edge Cases
- Design system in transition (old pattern being deprecated) — acceptable if both old and new are explicitly marked with migration guidance, not silently contradictory
- Platform-specific design variations (web vs. mobile) — acceptable if each platform's guidance is internally consistent and the divergence is explicit, not accidental

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Design Principles, UX Principles, and Accessibility are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All Design documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.83,
  "severity": "error",
  "evidence": { "section_id": 27, "paragraph_index": 1, "excerpt": "UX Principles: 'Use hover-only reveal for secondary actions.' Accessibility: 'All interactive affordances must be keyboard-reachable, not hover-dependent.'" },
  "message": "UX Principles recommends a hover-only pattern that Accessibility's requirements explicitly prohibit."
}
```
