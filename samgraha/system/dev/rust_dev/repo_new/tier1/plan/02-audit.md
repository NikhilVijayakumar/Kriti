# Stage 2 — Audit

**Use case:** `repo_new/tier1`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Documents produced by stage 1 (`01-create.md`): `vision.md` and `philosophy.md`.

## Procedure

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Steps

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `common/script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

1. **Deterministic document audit:** Run `common/tier1/audit/deterministic/document/{domain}.yaml` against the document. Produces per-rule pass/fail with evidence.

2. **Deterministic section audit:** Run `common/tier1/audit/deterministic/section/{domain}/*.yaml` against each section of the document. Produces per-section, per-rule pass/fail with evidence.

3. **Semantic document audit:** Run `common/tier1/audit/semantic/document/{domain}.md` against the whole document. Produces per-criterion pass/fail with confidence and evidence.

4. **Semantic section audit:** Run `common/tier1/audit/semantic/section/{domain}/*.md` against each section. Produces per-section, per-criterion pass/fail with confidence and evidence.

5. **Score:** Compute final score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (deterministic_whole 25%, deterministic_section 25%, semantic_whole 25%, semantic_section 25%), weighted sum formula.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| vision |  | `common/tier1/audit/deterministic/document/vision.yaml` | `common/tier1/audit/deterministic/section/vision/*.yaml` | `common/tier1/audit/semantic/document/vision.md` | `common/tier1/audit/semantic/section/vision/*.md` |
| philosophy |  | `common/tier1/audit/deterministic/document/philosophy.yaml` | `common/tier1/audit/deterministic/section/philosophy/*.yaml` | `common/tier1/audit/semantic/document/philosophy.md` | `common/tier1/audit/semantic/section/philosophy/*.md` |

## Output

A report per domain containing:
- Per-rule and per-criterion pass/fail with evidence
- Category scores (deterministic document, deterministic section, semantic document, semantic section)
- Final score (0–100) computed via `common/calculation/summary/final_score.yaml`
- Band assignment via `common/calculation/summary/score_bands.yaml`

This stage never fixes anything — that's stage 3's job, reading this stage's output.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier1, repo_existing/tier1, repo_existing_no_doc/tier1) - same audit files, same procedure.