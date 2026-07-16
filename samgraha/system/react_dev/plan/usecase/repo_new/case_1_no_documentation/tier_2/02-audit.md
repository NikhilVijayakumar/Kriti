# Stage 2 — Audit

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, design, engineering, external-context

## Input

Documents produced by stage 1 (`01-generation.md`): one document per domain.

## Procedure

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Steps

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

1. **Deterministic document audit:** Run `audit/deterministic/document/{domain}.yaml` against the document.
2. **Deterministic section audit:** Run `audit/deterministic/section/{domain}/*.yaml` against each section.
3. **Semantic document audit:** Run `audit/semantic/document/{domain}.md` against the whole document.
4. **Semantic section audit:** Run `audit/semantic/section/{domain}/*.md` against each section.
5. **Score:** Compute final score via `calculation/summary/final_score.yaml` — 4 equal buckets (25% each).

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| security | `secret-scan`, `dependency-vuln-scan` | `audit/deterministic/document/03-security.yaml` | `audit/deterministic/section/03-security/*.yaml` | `audit/semantic/document/03-security.md` | `audit/semantic/section/03-security/*.md` |
| feature |  | `audit/deterministic/document/04-feature.yaml` | `audit/deterministic/section/04-feature/*.yaml` | `audit/semantic/document/04-feature.md` | `audit/semantic/section/04-feature/*.md` |
| architecture | `module-boundary-diff` | `audit/deterministic/document/05-architecture.yaml` | `audit/deterministic/section/05-architecture/*.yaml` | `audit/semantic/document/05-architecture.md` | `audit/semantic/section/05-architecture/*.md` |
| design | `design-tokens-in-implementation` | `audit/deterministic/document/06-design.yaml` | `audit/deterministic/section/06-design/*.yaml` | `audit/semantic/document/06-design.md` | `audit/semantic/section/06-design/*.md` |
| engineering | `lint-standards` | `audit/deterministic/document/07-engineering.yaml` | `audit/deterministic/section/07-engineering/*.yaml` | `audit/semantic/document/07-engineering.md` | `audit/semantic/section/07-engineering/*.md` |
| external-context | `dependency-reachable` | `audit/deterministic/document/08-external-context.yaml` | `audit/deterministic/section/08-external-context/*.yaml` | `audit/semantic/document/08-external-context.md` | `audit/semantic/section/08-external-context/*.md` |

## Output

A report per domain containing per-rule and per-criterion pass/fail with evidence, category scores, final score, and band assignment.

This stage never fixes anything — that's stage 3's job.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documention`:** No difference — same audit files, same procedure.
- **vs. `repo_existing/case_1_no_documentation`:** No difference — same audit files, same procedure.
- **vs. `repo_existing/case_2_has_documention`:** No difference — same audit files, same procedure.
