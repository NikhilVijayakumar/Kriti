# Stage 2 — Audit

**Use case:** `repo_new/case_2_has_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Input

Documents produced by stage 1 (`01-generation.md`): one document per domain.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against each document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| security | `secret-scan`, `dependency-vuln-scan` | `tier2/audit/deterministic/document/security.yaml` | `tier2/audit/semantic/document/security.md` |
| feature |  | `tier2/audit/deterministic/document/feature.yaml` | `tier2/audit/semantic/document/feature.md` |
| architecture | `module-boundary-diff` | `tier2/audit/deterministic/document/architecture.yaml` | `tier2/audit/semantic/document/architecture.md` |
| engineering | `lint-standards` | `tier2/audit/deterministic/document/engineering.yaml` | `tier2/audit/semantic/document/engineering.md` |
| external-context | `dependency-reachable` | `tier2/audit/deterministic/document/external-context.yaml` | `tier2/audit/semantic/document/external-context.md` |

Plus section-level audits for each. Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
