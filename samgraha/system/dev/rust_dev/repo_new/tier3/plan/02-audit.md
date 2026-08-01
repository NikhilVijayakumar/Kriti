# Stage 2 — Audit

**Use case:** `repo_new/tier3`
**Tier:** 3

## Input

Documents produced by stage 1 (`01-create.md`): one document per domain.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

For each domain, run the real audit files unmodified. Produce a report per domain.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| feature-technical | `integration-points-exist` | `common/tier3/audit/deterministic/document/feature-technical.yaml` | `common/tier3/audit/deterministic/section/feature-technical/*.yaml` | `common/tier3/audit/semantic/document/feature-technical.md` | `common/tier3/audit/semantic/section/feature-technical/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier3, repo_existing/tier3, repo_existing_no_doc/tier3) - same audit files, same procedure.