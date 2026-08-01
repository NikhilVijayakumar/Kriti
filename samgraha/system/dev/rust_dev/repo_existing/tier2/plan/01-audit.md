# Stage 1 - Audit

**Use case:** `repo_existing/tier2`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Input

Existing documentation in the repo, conformance unknown per domain. Audit-first - no generate/migrate stage: run the audit directly against what exists.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against each document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| security | `secret-scan`, `dependency-vuln-scan` | `common/tier2/audit/deterministic/document/security.yaml` | `common/tier2/audit/semantic/document/security.md` |
| feature |  | `common/tier2/audit/deterministic/document/feature.yaml` | `common/tier2/audit/semantic/document/feature.md` |
| architecture | `module-boundary-diff` | `common/tier2/audit/deterministic/document/architecture.yaml` | `common/tier2/audit/semantic/document/architecture.md` |
| engineering | `lint-standards` | `common/tier2/audit/deterministic/document/engineering.yaml` | `common/tier2/audit/semantic/document/engineering.md` |
| external-context | `dependency-reachable` | `common/tier2/audit/deterministic/document/external-context.yaml` | `common/tier2/audit/semantic/document/external-context.md` |

Plus section-level audits for each. Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier2 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier2: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the audit files, same procedure is shared.