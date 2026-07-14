# Philosophy Document Audit

This section details the Philosophy Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Philosophy Documentation coheres as one system of values, principles, and trade-offs — not three independently-written sections that happen to share a file. Section-level quality (is each principle stated well) is owned by `audit/semantic/section/philosophy/`; this file owns whether Principles, Values, and Trade-offs are mutually consistent and collection-wide terminology holds.

## Audit Objectives
- Principles, Values, and Trade-offs don't contradict each other (a principle that implies a priority the Trade-offs section reverses is a document-level failure)
- All Philosophy documents in the domain cohere as one system — no orphaned document contradicting another
- Terminology is consistent across all Philosophy sections — the same value/principle isn't named differently in different sections

## Expected Quality
- Every Trade-off traces back to a Value it prioritizes and one it deliberately sacrifices
- Principles are consistent with the priorities implied by Values and Trade-offs, not orthogonal or contradictory
- A term introduced in Values (e.g. "Reliability") is referenced by the same name in Principles/Trade-offs, not a near-synonym

## Red Flags
- A Principle states a decision rule that a Trade-off entry directly contradicts
- Values list priorities that Trade-offs never actually trades against (unused values)
- Multiple Philosophy documents in the repo state incompatible core values with no reconciliation
- Same underlying value referred to by different names across sections (drift)

## Edge Cases
- Deliberately evolving philosophy (a value being phased out) — acceptable if the transition is stated explicitly, not read as an unexplained contradiction
- Repo with a single Philosophy document (no cross-document collection to check) — collection coherence criterion is vacuously satisfied, not a failure

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Principles, Values, and Trade-offs are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology is consistent across all sections |
| C3 | recommended | 0 or 30 | All Philosophy documents in the domain cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.83,
  "severity": "error",
  "evidence": { "section_id": 12, "paragraph_index": 1, "excerpt": "Principle: 'Ship fast, iterate later.' Trade-off: 'We prioritize correctness over speed, always.'" },
  "message": "Principles section states a speed-first decision rule that the Trade-offs section directly contradicts."
}
```
