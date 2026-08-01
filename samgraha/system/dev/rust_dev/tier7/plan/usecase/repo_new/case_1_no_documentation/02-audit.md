# Stage 2 — Audit

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 7
**Domains:** build

## Input

Document produced by stage 1 (`01-generation.md`): `build.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against the generated document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| build | `build-succeeds`, `artifact-exists` | `tier7/audit/deterministic/document/build.yaml` | `tier7/audit/deterministic/section/build/*.yaml` | `tier7/audit/semantic/document/build.md` | `tier7/audit/semantic/section/build/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
