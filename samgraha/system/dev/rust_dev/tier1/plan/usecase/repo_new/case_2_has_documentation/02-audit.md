# Stage 2 — Audit

**Use case:** `repo_new/case_2_has_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Documents produced by stage 1 (`01-generation.md`): `vision.md` and `philosophy.md` — either migrated from existing docs or generated from scratch.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

For each domain, run the real audit files unmodified against the document. Produce a report per domain.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| vision |  | `tier1/audit/deterministic/document/vision.yaml` | `tier1/audit/deterministic/section/vision/*.yaml` | `tier1/audit/semantic/document/vision.md` | `tier1/audit/semantic/section/vision/*.md` |
| philosophy |  | `tier1/audit/deterministic/document/philosophy.yaml` | `tier1/audit/deterministic/section/philosophy/*.yaml` | `tier1/audit/semantic/document/philosophy.md` | `tier1/audit/semantic/section/philosophy/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure across all use cases.
