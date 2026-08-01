# Stage 2 — Audit

**Use case:** `repo_new/tier2`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Input

Documents produced by stage 1 (`01-create.md`): one document per domain.

## Procedure

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Steps

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

1. **Deterministic document audit:** Run `common/tier2/audit/deterministic/document/{domain}.yaml` against the document.
2. **Deterministic section audit:** Run `common/tier2/audit/deterministic/section/{domain}/*.yaml` against each section.
3. **Semantic document audit:** Run `common/tier2/audit/semantic/document/{domain}.md` against the whole document.
4. **Semantic section audit:** Run `common/tier2/audit/semantic/section/{domain}/*.md` against each section.
5. **Score:** Compute final score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| security | `secret-scan`, `dependency-vuln-scan` | `common/tier2/audit/deterministic/document/security.yaml` | `common/tier2/audit/deterministic/section/security/*.yaml` | `common/tier2/audit/semantic/document/security.md` | `common/tier2/audit/semantic/section/security/*.md` |
| feature |  | `common/tier2/audit/deterministic/document/feature.yaml` | `common/tier2/audit/deterministic/section/feature/*.yaml` | `common/tier2/audit/semantic/document/feature.md` | `common/tier2/audit/semantic/section/feature/*.md` |
| architecture | `module-boundary-diff` | `common/tier2/audit/deterministic/document/architecture.yaml` | `common/tier2/audit/deterministic/section/architecture/*.yaml` | `common/tier2/audit/semantic/document/architecture.md` | `common/tier2/audit/semantic/section/architecture/*.md` |
| engineering | `lint-standards` | `common/tier2/audit/deterministic/document/engineering.yaml` | `common/tier2/audit/deterministic/section/engineering/*.yaml` | `common/tier2/audit/semantic/document/engineering.md` | `common/tier2/audit/semantic/section/engineering/*.md` |
| external-context | `dependency-reachable` | `common/tier2/audit/deterministic/document/external-context.yaml` | `common/tier2/audit/deterministic/section/external-context/*.yaml` | `common/tier2/audit/semantic/document/external-context.md` | `common/tier2/audit/semantic/section/external-context/*.md` |

## Output

A report per domain containing per-rule and per-criterion pass/fail with evidence, category scores, final score, and band assignment.

This stage never fixes anything — that's stage 3's job.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier2, repo_existing/tier2, repo_existing_no_doc/tier2) - same audit files, same procedure.