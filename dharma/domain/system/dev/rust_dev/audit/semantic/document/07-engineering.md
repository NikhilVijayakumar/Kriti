# Engineering Document Audit

This section details the Engineering Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Engineering Documentation coheres as one set of repo-wide standards — Guiding Principles, Build Standards, Testing Standards, and Code Standards must not contradict each other. Section-level quality is owned by `audit/semantic/section/engineering/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Guiding Principles, Build Standards, Testing Standards, and Code Standards are mutually consistent — a principle implying a priority that another section's concrete rule contradicts is a document-level failure
- All Engineering documents in the domain cohere as one system — no orphaned or contradictory standards
- Terminology is consistent across all Engineering sections — the same tool, gate, or convention isn't named differently in different sections

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `lint-standards` | `metrics.lint_exit_code` | Validates whether the linting standards actually pass. If the doc claims "lint passes" but the script reports a non-zero exit code, that's a grounding conflict. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about engineering standards compliance

## Expected Quality
- Testing Standards' coverage/quality bar is consistent with what Build Standards' CI/CD gates actually enforce
- Code Standards' style rules don't contradict a Guiding Principle (e.g. "explicit over implicit" contradicted by a rule favoring terse magic)
- A tool or convention name (linter, formatter, CI stage) is used identically across sections

## Red Flags
- Testing Standards requires a coverage threshold that Build Standards' pipeline doesn't actually gate on
- Code Standards contradicts a stated Guiding Principle without acknowledgment
- Two Engineering documents specify incompatible build or test tooling for the same concern
- Same tool/gate referred to by different names across sections

## Edge Cases
- Standards actively being migrated (e.g. moving from one test framework to another) — acceptable if the transition is explicitly documented, not silently inconsistent
- Repo-wide standards with a documented, narrow exception for one subsystem — acceptable if the exception is explicit and scoped, not read as a blanket contradiction

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Guiding Principles, Build Standards, Testing Standards, and Code Standards are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology (tools, gates, conventions) consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All Engineering documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 29, "paragraph_index": 0, "excerpt": "Testing Standards: '90% coverage required to merge.' Build Standards: 'CI runs tests but does not block on coverage.'" },
  "message": "Build Standards' pipeline doesn't actually enforce the coverage threshold Testing Standards requires."
}
```
