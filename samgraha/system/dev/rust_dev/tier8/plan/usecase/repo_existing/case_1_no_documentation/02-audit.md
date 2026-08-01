# Stage 2 — Audit

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Input

Documents produced by stage 1 (`01-generation.md`): `readme.md` and `product-guide.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

For each domain, run the real audit files unmodified against the generated document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| readme |  | `tier8/audit/deterministic/document/readme.yaml` | `tier8/audit/semantic/document/readme.md` |
| product-guide | `public-contract-diff` | `tier8/audit/deterministic/document/product-guide.yaml` | `tier8/audit/semantic/document/product-guide.md` |

Plus section-level audits for each. Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
