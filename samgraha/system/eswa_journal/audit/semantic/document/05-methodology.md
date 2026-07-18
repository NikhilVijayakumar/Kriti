# Methodology Semantic Audit

This section details the Methodology Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies Methodology solves only the problem formalized in Problem Definition (no orphaned modules), carries the formal Big-O complexity analysis ESWA requires, and explains algorithmic choices with intuitive reasoning rather than mechanical restatement. This file owns the receiving end of the Problem Definition → Methodology bridge.

## Audit Objectives
- Methodology introduces no module or solution for a problem never mentioned in Problem Definition.
- Formal Big-O time and space complexity analysis is present, with a comparison table (baseline vs. proposed).
- Algorithm/math sentences include a "why" clause explaining the choice for this specific implementation, not just a restatement of the formula.

## Expected Quality
- A standalone Complexity Analysis subsection with a comparison table.
- Every architectural choice is justified against the specific domain problem (e.g., why a CRF layer instead of softmax).

## Red Flags
- A module solves a problem never mentioned in Problem Definition or Introduction.
- Claims of scalability without a mathematical (Big-O) or empirical foundation.
- "The Siamese network reduces dimensionality." (mechanical restatement, no reasoning).

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Methodology attempts to solve only the problem explicitly defined in Problem Definition |
| C2 | mandatory | 0 or 30 | Formal Big-O complexity analysis and a baseline-vs-proposed comparison table are present |
| C3 | recommended | 0 or 20 | Algorithm/math sentences include intuitive "why" reasoning, not mechanical restatement |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "paragraph_index": 5, "excerpt": "We additionally introduce a caching layer to reduce latency." },
  "message": "Caching layer solves a performance concern never raised in Problem Definition — orphaned module."
}
```
