# Security Document Audit

This section details the Security Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Security Documentation coheres as one threat model — Threat Model, Data Classification, and Security Principles must not contradict each other. Section-level quality is owned by `audit/semantic/section/security/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Threat Model, Data Classification, and Security Principles are mutually consistent — a Security Principle contradicted by how Threat Model actually treats a threat, or a Data Classification tier with no corresponding protections in Security Principles, is a document-level failure
- All Security documents in the domain cohere as one system — no orphaned or contradictory security posture across documents
- Terminology is consistent across all Security sections — the same asset or threat category isn't named differently in different sections

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `secret-scan` | `metrics.secrets_found`, `evidence[]` | Validates whether the repository actually has hardcoded secrets. If the doc claims "no secrets in code" but the script found 3, that's a grounding conflict. The `evidence` array names the files and secret types. |
| `dependency-vuln-scan` | `metrics.vulnerabilities_found`, `evidence[]` | Validates whether dependencies have known vulnerabilities. If the doc claims "all dependencies patched" but the script found CVEs, flag the contradiction. |
| `mitigation-present-at-boundary` | `metrics.mitigations_missing`, `evidence[]` | Cross-domain check: validates whether security mitigations declared in this doc actually appear in the implementation code. If the doc says "inputs are sanitized" but the script found no sanitization at the claimed boundary, that's a grounding gap. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about security posture

## Expected Quality
- Every data classification tier (e.g. "confidential") has corresponding protections named in Security Principles
- Threat Model's mitigations don't contradict a stated Security Principle
- Asset and threat category names are used identically across sections

## Red Flags
- A Data Classification tier with no corresponding protection requirement anywhere in Security Principles
- Threat Model's accepted risk for a threat contradicts a Security Principle that claims that class of risk is never accepted
- Two Security documents classify the same asset at different sensitivity tiers with no reconciliation
- Same asset/threat category named differently across sections, undermining Compliance's obligation-to-control traceability

## Edge Cases
- Security posture with an explicitly accepted, time-boxed risk exception — acceptable if documented as such, not silently contradicting stated principles
- Multi-tenant system with per-tenant classification differences — acceptable if each tenant's classification is internally consistent and the variance is explicit

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Threat Model, Data Classification, and Security Principles are mutually consistent |
| C2 | mandatory | 0 or 30 | Every Data Classification tier has corresponding protections in Security Principles |
| C3 | recommended | 0 or 30 | Terminology (assets, threat categories) consistent across all documents |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 9, "paragraph_index": 0, "excerpt": "Data Classification: 'Restricted tier includes payment data.' Security Principles has no protection requirement mentioning Restricted tier." },
  "message": "Restricted data classification tier has no corresponding protection stated in Security Principles."
}
```
