# Stage 2 — Audit

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 4
**Domains:** prototype

## Input

Document produced by stage 1 (`01-generation.md`): `prototype.md`.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against the generated document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| prototype | `mock-api-runs` | `audit/deterministic/document/11-prototype.yaml` | `audit/deterministic/section/11-prototype/*.yaml` | `audit/semantic/document/11-prototype.md` | `audit/semantic/section/11-prototype/*.md` |

Score via `calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
