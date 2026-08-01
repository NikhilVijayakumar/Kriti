# Stage 2 — Audit

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Documents produced by stage 1 (`01-generation.md`): `vision.md` and `philosophy.md`.

## Procedure

For each domain, run the real audit files unmodified against the generated document. Produce a report per domain.

### Per-Domain Audit Steps

0. **Run applicable scripts:** for domains with scripts (Scripts column below), run each per its manifest's `depends_on` order, reusing a cached result where `script/policy.yaml`'s policy allows, else executing fresh. Capture JSON per check-name.

1. **Deterministic document audit:** Run `tier1/audit/deterministic/document/{domain}.yaml` against the document. Produces per-rule pass/fail with evidence.

2. **Deterministic section audit:** Run `tier1/audit/deterministic/section/{domain}/*.yaml` against each section of the document. Produces per-section, per-rule pass/fail with evidence.

3. **Semantic document audit:** Run `tier1/audit/semantic/document/{domain}.md` against the whole document. Produces per-criterion pass/fail with confidence and evidence.

4. **Semantic section audit:** Run `tier1/audit/semantic/section/{domain}/*.md` against each section. Produces per-section, per-criterion pass/fail with confidence and evidence.

5. **Score:** Compute final score via `common/calculation/summary/final_score.yaml` — 4 equal buckets (deterministic_whole 25%, deterministic_section 25%, semantic_whole 25%, semantic_section 25%), weighted sum formula.

### Per-Domain Audit Files

| Domain | Scripts (check-name) | Deterministic doc | Deterministic section | Semantic doc | Semantic section |
|---|---|---|---|---|---|
| vision |  | `tier1/audit/deterministic/document/vision.yaml` | `tier1/audit/deterministic/section/vision/*.yaml` | `tier1/audit/semantic/document/vision.md` | `tier1/audit/semantic/section/vision/*.md` |
| philosophy |  | `tier1/audit/deterministic/document/philosophy.yaml` | `tier1/audit/deterministic/section/philosophy/*.yaml` | `tier1/audit/semantic/document/philosophy.md` | `tier1/audit/semantic/section/philosophy/*.md` |

## Output

A report per domain containing:
- Per-rule and per-criterion pass/fail with evidence
- Category scores (deterministic document, deterministic section, semantic document, semantic section)
- Final score (0–100) computed via `common/calculation/summary/final_score.yaml`
- Band assignment via `common/calculation/summary/score_bands.yaml`

This stage never fixes anything — that's stage 3's job, reading this stage's output.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documentation`:** No difference — same audit files, same procedure.
- **vs. `repo_existing/case_1_no_documentation`:** No difference — same audit files, same procedure.
- **vs. `repo_existing/case_2_has_documentation`:** No difference — same audit files, same procedure.
