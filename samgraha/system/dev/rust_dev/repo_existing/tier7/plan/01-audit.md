# Stage 1 - Audit

**Use case:** `repo_existing/tier7`
**Tier:** 7
**Domains:** build

## Input

Existing documentation in the repo, conformance unknown per domain. Audit-first - no generate/migrate stage: run the audit directly against what exists.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| build | `build-succeeds`, `artifact-exists` | `common/tier7/audit/deterministic/document/build.yaml` | `common/tier7/audit/semantic/document/build.md` |

Plus section-level audits. Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier7 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier7: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the audit files, same procedure is shared.