# Stage 2 — Audit

**Use case:** `repo_existing/case_2_has_documention`
**Tier:** 5
**Domains:** implementation

## Input

Document produced by stage 1 (`01-generation.md`).

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| implementation | `folder-structure`, `dependency-manifest`, `lint-pass` | `audit/deterministic/document/13-implementation.yaml` | `audit/semantic/document/13-implementation.md` |

Plus section-level audits. Score via `calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference — same audit files, same procedure.
