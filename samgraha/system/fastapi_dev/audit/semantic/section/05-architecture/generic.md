# Generic Architecture Audit

This section details the Generic Architecture Audit.

## Version
1.0.0

## Engineering Intent
The generic architecture section captures high-level architectural context that does not fit into a specialized section. It should describe architecture-relevant decisions, rationale, and system-level properties that inform the overall design.

## Audit Objectives
- Content is relevant to architecture (not implementation or project management)
- Technical assertions are justified
- The section does not duplicate content from other typed sections
- Architecture decisions are traceable to requirements
- Content is internally consistent

## Expected Quality
- Statements are specific and falsifiable
- Architecture rationale is clearly separated from implementation details
- Claims are supported by evidence or reasoning
- Terminology is consistent with other architecture sections

## Red Flags
- Vague or non-falsifiable statements
- Off-topic content (deployment steps, team process, feature specs)
- Duplication of content in typed sections (component-model, constraints, etc.)
- Implementation-specific details that belong in design docs

## Edge Cases
- Empty generic section (acceptable — content may live in typed sections)
- Generic section used as catch-all for unmatched content
- Hybrid paragraphs mixing architecture and implementation concerns

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Content is architecture-relevant, not implementation-specific |
| C2 | mandatory | 0 or 30 | Claims and assertions are justified by evidence or reasoning |
| C3 | recommended | 0 or 30 | No duplication of content from other architecture section types |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "section_id": 10, "paragraph_index": 0, "excerpt": "The system follows a microservices architecture with event-driven communication." },
  "message": "Architecture-relevant statement with no implementation detail."
}
```
