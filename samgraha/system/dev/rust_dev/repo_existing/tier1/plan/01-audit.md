# Stage 1 - Audit

**Use case:** `repo_existing/tier1`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Existing documentation in the repo, conformance unknown per domain. Audit-first - no generate/migrate stage: run the audit directly against what exists.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified against each document.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| vision |  | `common/tier1/audit/deterministic/document/vision.yaml` | `common/tier1/audit/deterministic/section/vision/*.yaml` | `common/tier1/audit/semantic/document/vision.md` | `common/tier1/audit/semantic/section/vision/*.md` |
| philosophy |  | `common/tier1/audit/deterministic/document/philosophy.yaml` | `common/tier1/audit/deterministic/section/philosophy/*.yaml` | `common/tier1/audit/semantic/document/philosophy.md` | `common/tier1/audit/semantic/section/philosophy/*.md` |

Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report per domain. This stage never fixes anything.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier1 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier1: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the audit files, same procedure is shared.