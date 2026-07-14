# Product Guide Document Audit

This section details the Product Guide Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a Product Guide topic coheres internally — Title matches Body, Purpose aligns with Product Context, Public Contract matches what the Body actually describes — and that the guide collection as a whole doesn't contradict itself. Section-level quality is owned by `audit/semantic/section/product-guide/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Title accurately reflects what the Body actually covers
- Purpose (the problem stated) aligns with what Product Context and Body actually address
- Public Contract's documented inputs/outputs/flags match what the Body's instructions actually use
- Terminology is consistent across all Product Guide topics — same concept, same name
- All Product Guide documents cohere as one system — no orphaned or contradictory guides

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `public-contract-diff` | `metrics.mismatches`, `evidence[]` | Validates whether the documented public contract matches the actual implementation. If the doc claims "contract matches code" but the script reports mismatches, that's a grounding conflict. The `evidence` array lists the mismatched inputs/outputs/flags. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about public contract accuracy

## Expected Quality
- A reader could predict the Body's content from the Title alone
- Purpose's stated problem is the one the rest of the topic actually solves
- Every flag/input mentioned in Body instructions appears in Public Contract, and vice versa
- No topic uses a different name for a concept already named elsewhere in the guide collection

## Red Flags
- Title promises something the Body doesn't deliver (or vice versa)
- Purpose states one problem, Body solves a different one
- Public Contract lists a flag never used in Body instructions, or Body uses a flag missing from Public Contract
- Two Product Guide topics use different names for the same concept, confusing cross-references

## Edge Cases
- Topic intentionally covering a narrower slice than its Title implies for scannability — acceptable if Title is still accurate, just narrower in scope, not misleading
- Guide collection spanning multiple product areas with legitimately different vocabularies — acceptable if each area's terminology is internally consistent, cross-area drift is the actual concern

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Title accurately reflects Body content |
| C2 | mandatory | 0 or 35 | Public Contract matches what Body instructions actually use |
| C3 | recommended | 0 or 30 | Terminology consistent across all Product Guide topics |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.81,
  "severity": "error",
  "evidence": { "section_id": 23, "paragraph_index": 2, "excerpt": "Run with `--verbose` to see detailed output." },
  "message": "Body instructions reference a `--verbose` flag not documented in Public Contract."
}
```
