# Stage 2 — Audit

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Input

Documents produced by stage 1 (`01-generation.md`): one document per domain.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| security | `secret-scan`, `dependency-vuln-scan` | `tier2/audit/deterministic/document/security.yaml` | `tier2/audit/deterministic/section/security/*.yaml` | `tier2/audit/semantic/document/security.md` | `tier2/audit/semantic/section/security/*.md` |
| feature |  | `tier2/audit/deterministic/document/feature.yaml` | `tier2/audit/deterministic/section/feature/*.yaml` | `tier2/audit/semantic/document/feature.md` | `tier2/audit/semantic/section/feature/*.md` |
| architecture | `module-boundary-diff` | `tier2/audit/deterministic/document/architecture.yaml` | `tier2/audit/deterministic/section/architecture/*.yaml` | `tier2/audit/semantic/document/architecture.md` | `tier2/audit/semantic/section/architecture/*.md` |
| engineering | `lint-standards` | `tier2/audit/deterministic/document/engineering.yaml` | `tier2/audit/deterministic/section/engineering/*.yaml` | `tier2/audit/semantic/document/engineering.md` | `tier2/audit/semantic/section/engineering/*.md` |
| external-context | `dependency-reachable` | `tier2/audit/deterministic/document/external-context.yaml` | `tier2/audit/deterministic/section/external-context/*.yaml` | `tier2/audit/semantic/document/external-context.md` | `tier2/audit/semantic/section/external-context/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
