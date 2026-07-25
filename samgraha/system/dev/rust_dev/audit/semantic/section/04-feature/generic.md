# Generic Section Audit

This section details the Generic Section Audit.

## Version
1.0.0

## Engineering Intent
Generic sections cover content not captured by standard section types. They must still be well-structured, technically substantive, and aligned with project goals. Audit applies broad quality criteria to any unrecognized or custom section.

## Audit Objectives
- Content is technically substantive (not filler)
- Section has a clear heading and purpose
- Content is internally consistent
- Language is precise and unambiguous
- Section does not duplicate content from other sections

## Expected Quality
- Paragraphs are focused on a single topic
- Technical terms are used correctly
- Claims are supported by reasoning or evidence
- Section length is proportional to importance

## Red Flags
- Placeholder text ("TODO", "TBD", "lorem ipsum")
- Content that belongs in another standard section
- Vague or marketing language without substance
- Content that contradicts other parts of the document

## Edge Cases
- Empty generic section
- Very long section with mixed topics
- Section that overlaps with multiple standard types

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Content is technically substantive |
| C2 | mandatory | 0 or 30 | Section purpose is clearly stated |
| C3 | recommended | 0 or 30 | Content does not duplicate other sections |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.88,
  "severity": "error",
  "evidence": { "section_id": 99, "paragraph_index": 2, "excerpt": "The caching strategy uses Redis with TTL of 300s." },
  "message": "Section contains specific technical substance beyond filler."
}
```
