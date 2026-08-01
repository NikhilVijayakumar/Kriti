# Stage 2 — Audit

**Use case:** `repo_new/tier7`
**Tier:** 7
**Domains:** build

## Input

Document produced by stage 1 (`01-create.md`): `build.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against the generated document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| build | `build-succeeds`, `artifact-exists` | `common/tier7/audit/deterministic/document/build.yaml` | `common/tier7/audit/deterministic/section/build/*.yaml` | `common/tier7/audit/semantic/document/build.md` | `common/tier7/audit/semantic/section/build/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier7, repo_existing/tier7, repo_existing_no_doc/tier7) - same audit files, same procedure.