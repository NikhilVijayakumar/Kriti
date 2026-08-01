# Stage 2 — Audit

**Use case:** `repo_new/tier6`
**Tier:** 6
**Domains:** qa

## Input

Document produced by stage 1 (`01-create.md`): `qa.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against the generated document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| qa | `unit-test-coverage` | `common/tier6/audit/deterministic/document/qa.yaml` | `common/tier6/audit/deterministic/section/qa/*.yaml` | `common/tier6/audit/semantic/document/qa.md` | `common/tier6/audit/semantic/section/qa/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier6, repo_existing/tier6, repo_existing_no_doc/tier6) - same audit files, same procedure.