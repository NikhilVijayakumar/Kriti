# Generic Audit

This section details the Generic Audit.

## Version
1.0.0

## Engineering Intent
The generic section type serves as a fallback for feature-technical content that does not map to any specialized section type. It must still contain coherent technical information, be internally consistent, and not duplicate content from other sections. The generic type captures miscellaneous but relevant technical detail.

## Audit Objectives
- Content is relevant to the feature-technical domain
- Information does not duplicate content from other named sections
- Claims made in the generic section are verifiable
- Terminology is consistent with the rest of the document
- The section has a clear topical scope (not a grab bag)

## Expected Quality
- The section has a clear sub-topic heading
- All statements are specific and falsifiable
- No placeholder, TODO, or stub content
- Cross-references to other sections are correct

## Red Flags
- Section contains implementation code without explanation
- Content belongs in a specialized section type
- Vague or non-technical language
- Section is empty or contains only placeholder text

## Edge Cases
- Document with only a generic section and no specialized sections
- Generic section that spans multiple unrelated topics
- Content that straddles two specialized section types

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Content is relevant to the feature-technical domain |
| C2 | mandatory | 0 or 30 | No duplication with other named sections |
| C3 | recommended | 0 or 30 | All claims are verifiable and specific |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "This section covers miscellaneous deployment topology notes..." },
  "message": "Content is relevant and does not duplicate other sections."
}
```
