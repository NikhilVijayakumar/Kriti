# Build Document Audit

This section details the Build Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies Build Documentation coheres as one policy — Security Checks, Versioning & Naming, and Documentation Quality shouldn't contradict each other, and the collection reads as one packaging/distribution policy. Section-level quality is owned by `audit/semantic/section/build/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Security Checks align with Versioning & Naming — a vulnerability severity threshold that blocks a release shouldn't be contradicted by a versioning rule that allows shipping anyway
- Documentation Quality's gates align with what Security Checks and other gates actually enforce — no gate claimed that isn't real, no real gate left undocumented
- All Build documents in the domain cohere as one system — no orphaned or contradictory build policies
- Terminology consistent across all Build sections — the same gate or artifact type isn't named differently in different sections

## Script Evidence Grounding

When available, the following script outputs provide ground-truth context for this audit. The LLM evaluator should use these as factual anchors rather than relying solely on what the document claims.

| Script | Evidence field | How it grounds the audit |
|--------|---------------|------------------------|
| `build-succeeds` | `metrics.build_exit_code` | Validates whether the build actually passes. If the doc claims "build succeeds" but the script reports a non-zero exit code, that's a grounding conflict. |
| `artifact-exists` | `metrics.artifact_exists` | Validates whether the expected build artifact is produced. If the doc claims an artifact is built but the script reports it doesn't exist, flag the contradiction. |

When script evidence is available, the evaluator should:
1. Compare script-reported metrics against document claims
2. Flag contradictions where script ground-truth differs from doc assertions
3. Use script `evidence` arrays as concrete examples when scoring criteria about build success and artifact delivery

## Expected Quality
- A severity threshold stated in Security Checks is respected by the release/versioning process described elsewhere
- Documentation Quality's list of validated domains matches what's actually gated in CI/CD Validation
- Artifact type names are consistent between Size Checks, Versioning & Naming, and any other section referencing them

## Red Flags
- Security Checks defines a blocking severity threshold that Versioning & Naming's release process doesn't actually respect
- Documentation Quality claims a gate exists that no other section (or CI/CD Validation) actually implements
- Two Build documents describe incompatible versioning schemes for the same artifact type
- An artifact type is named differently across sections (e.g. "bundle" in one, "package" in another, same thing)

## Edge Cases
- Build policy still evolving with a documented transition (e.g. tightening a threshold over several releases) — acceptable if the transition plan is explicit, not read as an unexplained contradiction
- Monorepo with per-package build policies that legitimately differ — acceptable if each package's policy is self-consistent, cross-package drift is the actual concern

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Security Checks and Versioning & Naming are mutually consistent |
| C2 | mandatory | 0 or 30 | Documentation Quality's claimed gates match what's actually enforced |
| C3 | recommended | 0 or 30 | Terminology (artifact/gate names) consistent across all sections and documents |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.8,
  "severity": "error",
  "evidence": { "section_id": 25, "paragraph_index": 0, "excerpt": "Security Checks: 'Critical vulnerabilities block release.' Versioning & Naming: 'Releases proceed on schedule regardless of scan status.'" },
  "message": "Versioning & Naming's release process contradicts Security Checks' stated blocking threshold."
}
```
