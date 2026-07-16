# Stage 2 — Audit

**Use case:** `repo_new/case_2_has_documention`
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
| security | `secret-scan`, `dependency-vuln-scan` | `audit/deterministic/document/03-security.yaml` | `audit/semantic/document/03-security.md` |
| feature |  | `audit/deterministic/document/04-feature.yaml` | `audit/semantic/document/04-feature.md` |
| architecture | `module-boundary-diff` | `audit/deterministic/document/05-architecture.yaml` | `audit/semantic/document/05-architecture.md` |
| engineering | `lint-standards` | `audit/deterministic/document/07-engineering.yaml` | `audit/semantic/document/07-engineering.md` |
| external-context | `dependency-reachable` | `audit/deterministic/document/08-external-context.yaml` | `audit/semantic/document/08-external-context.md` |

Plus section-level audits for each. Score via `calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
