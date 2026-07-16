# Guiding Principles Audit

This section details the Guiding Principles Audit.

## Version
1.0.0

## Engineering Intent
Guiding principles are the durable design tenets that shape how the product is built. They must be actionable, prioritizable, and falsifiable — not platitudes. Principles resolve ambiguity when user needs or technical constraints conflict.

## Audit Objectives
- Principles are explicit and documented
- Each principle is actionable (can be applied to a design decision)
- Principles are consistent with each other (no inherent contradiction)
- Principles are prioritized or ranked
- When two ranked principles produce opposing decisions, a conflict resolution rule is documented (e.g., "Principle 1 beats Principle 2 when both apply to the same scope")
- Principles are used in design review and decision records
- Principles are stable but revisable with deliberate process, including a documented update mechanism

## Expected Quality
- Each principle is 1-2 sentences with a short rationale
- Principles include examples of what they mean in practice
- Principles can be referenced by name in team discussion
- Principles have a clear owner or review cadence

## Red Flags
- Principles are generic ("keep it simple") with no operational meaning
- Principles contradict each other with no resolution guidance
- Principles exist only in someone's head
- Principles are aspirational but never enforced in reviews
- Principles identical to industry defaults with no product-specific tailoring
- Principles ranked but no tiebreaker rule — ranking is meaningless if two principles apply simultaneously with no guidance on precedence

## Edge Cases
- No guiding principles defined at all
- Principles only cover one dimension (e.g., performance) and ignore others
- Principles that conflict but are both ranked equally

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Guiding principles are documented with rationale |
| C2 | mandatory | 0 or 30 | Each principle is actionable and falsifiable |
| C3 | recommended | 0 or 20 | Conflict resolution rule documented for when two principles oppose |
| C4 | recommended | 0 or 20 | Principles are consistently referenced in decision records |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "..." },
  "message": "..."
}
```
