# Stage 1 - Audit

**Use case:** `repo_existing/tier6`
**Tier:** 6
**Domains:** qa

## Input

Existing documentation in the repo, conformance unknown per domain. Audit-first - no generate/migrate stage: run the audit directly against what exists.

## Procedure

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

Run the real audit files unmodified.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Semantic doc |
|---|---|---|---|
| qa | `unit-test-coverage` | `common/tier6/audit/deterministic/document/qa.yaml` | `common/tier6/audit/semantic/document/qa.md` |

Plus section-level audits. Score via `common/calculation/summary/final_score.yaml` — 4 equal buckets.

## Output

A report. This stage never fixes anything.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier6 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier6: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the audit files, same procedure is shared.