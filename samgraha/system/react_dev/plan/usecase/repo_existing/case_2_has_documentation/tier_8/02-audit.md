# Stage 2 — Audit

**Use case:** `repo_existing/case_2_has_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Input

Documents produced by stage 1 (`01-generation.md`).

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against each document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| readme |  | `audit/deterministic/document/15-readme.yaml` | `audit/semantic/document/15-readme.md` |
| product-guide | `public-contract-diff` | `audit/deterministic/document/16-product-guide.yaml` | `audit/semantic/document/16-product-guide.md` |

Plus section-level audits for each. Score via `calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
