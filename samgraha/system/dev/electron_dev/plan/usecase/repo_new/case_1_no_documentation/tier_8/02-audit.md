# Stage 2 — Audit

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Input

Documents produced by stage 1 (`01-generation.md`): `readme.md` and `product-guide.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| readme |  | `audit/deterministic/document/15-readme.yaml` | `audit/deterministic/section/15-readme/*.yaml` | `audit/semantic/document/15-readme.md` | `audit/semantic/section/15-readme/*.md` |
| product-guide | `public-contract-diff` | `audit/deterministic/document/16-product-guide.yaml` | `audit/deterministic/section/16-product-guide/*.yaml` | `audit/semantic/document/16-product-guide.md` | `audit/semantic/section/16-product-guide/*.md` |

Score via `calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
