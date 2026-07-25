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
| security | `secret-scan`, `dependency-vuln-scan` | `audit/deterministic/document/03-security.yaml` | `audit/deterministic/section/03-security/*.yaml` | `audit/semantic/document/03-security.md` | `audit/semantic/section/03-security/*.md` |
| feature |  | `audit/deterministic/document/04-feature.yaml` | `audit/deterministic/section/04-feature/*.yaml` | `audit/semantic/document/04-feature.md` | `audit/semantic/section/04-feature/*.md` |
| architecture | `module-boundary-diff` | `audit/deterministic/document/05-architecture.yaml` | `audit/deterministic/section/05-architecture/*.yaml` | `audit/semantic/document/05-architecture.md` | `audit/semantic/section/05-architecture/*.md` |
| engineering | `lint-standards` | `audit/deterministic/document/07-engineering.yaml` | `audit/deterministic/section/07-engineering/*.yaml` | `audit/semantic/document/07-engineering.md` | `audit/semantic/section/07-engineering/*.md` |
| external-context | `dependency-reachable` | `audit/deterministic/document/08-external-context.yaml` | `audit/deterministic/section/08-external-context/*.yaml` | `audit/semantic/document/08-external-context.md` | `audit/semantic/section/08-external-context/*.md` |

Score via `calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
