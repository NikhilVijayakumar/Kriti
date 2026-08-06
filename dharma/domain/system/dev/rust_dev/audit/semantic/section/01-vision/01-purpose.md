# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
The purpose section defines why the vision document exists and what it intends to accomplish. It establishes the scope, context, and motivation for the vision, orienting readers to the document's role in the project lifecycle.

## Audit Objectives
- Purpose is clearly stated and distinct from problem statement
- Scope boundaries are explicit (what is in-scope and out-of-scope)
- The intended audience for the vision document is identified
- Purpose aligns with broader organizational or program goals
- No conflation of purpose with solution approach

## Expected Quality
- Purpose is articulated in one or two concise paragraphs
- Scope boundaries prevent scope creep
- Document purpose is differentiated from product purpose
- Language is accessible to both technical and non-technical readers

## Red Flags
- Purpose section merely repeats the document title
- Scope boundaries are absent or ambiguous
- Purpose is written as a mission statement for the product (not the doc)
- Multiple conflicting purpose statements within the section

## Edge Cases
- Vision document that serves multiple purposes (e.g., strategy + roadmap)
- Extremely brief purpose that omits necessary scope context
- Purpose section that overlaps heavily with adjacent sections

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Purpose distinguishes document intent from product mission |
| C2 | mandatory | 0 or 30 | Scope boundaries explicitly stated (in-scope and out-of-scope) |
| C3 | recommended | 0 or 30 | Purpose aligned with program-level objectives |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "This vision document defines the strategic direction..." },
  "message": "Purpose clearly distinguishes document intent from product mission."
}
```
