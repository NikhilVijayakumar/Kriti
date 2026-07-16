# Vision Document Audit

This section details the Vision Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Vision Documentation coheres as one aspirational statement — Problem, Solution, and Vision Statement must align without contradiction, and the document must remain technology-independent as a whole, not just section by section. Section-level quality is owned by `audit/semantic/section/vision/`; this file owns cross-section consistency and the document-wide technology-independence guarantee.

## Audit Objectives
- Problem, Solution, and Vision Statement align without contradiction — the Solution must actually address the Problem, and the Vision Statement must be the aspirational extension of that Solution, not a disconnected claim
- No section in the document contains implementation technology references, checked across the whole document, not just within individual sections (a technology reference split across two sentences in different sections is still a violation)
- All Vision documents in the domain cohere as one coherent vision — no orphaned or contradictory vision statements
- Terminology is consistent across all Vision sections — the same value/goal isn't named differently in different sections

## Expected Quality
- Solution's approach is traceable back to the specific pain described in Problem
- Vision Statement's aspirational future state is a plausible extension of what Solution actually does, not an unrelated ambition
- Zero technology, framework, or implementation references anywhere in the document
- Named goals/values in Platform Pillars are consistent with what Vision Statement and Success Criteria describe

## Red Flags
- Solution addresses a different problem than the one Problem describes
- Vision Statement makes aspirational claims with no connection to Solution's actual approach
- A technology reference appears anywhere in the document (even in an example or aside)
- Multiple Vision documents for the same product describe incompatible long-term directions

## Edge Cases
- Vision document evolving across a major pivot — acceptable if the old vision is explicitly archived/superseded, not left contradicting the current one
- Product with genuinely multiple vision documents for distinct sub-products — acceptable if each is internally consistent and their relationship (independent vs. nested) is stated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Problem, Solution, and Vision Statement align without contradiction |
| C2 | mandatory | 0 or 35 | No technology/implementation references anywhere in the document |
| C3 | recommended | 0 or 30 | Terminology consistent and all Vision documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 3, "paragraph_index": 0, "excerpt": "Problem: 'Teams lose hours reconciling spreadsheets.' Solution: 'Our GraphQL API lets developers build custom integrations.'" },
  "message": "Solution describes a developer-facing API instead of addressing the reconciliation pain stated in Problem."
}
```
