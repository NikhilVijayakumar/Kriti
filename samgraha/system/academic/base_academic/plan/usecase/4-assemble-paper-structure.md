# Use-case 4 — Assemble Paper Structure

**Script**: Per-domain triad — `gather-domain-evidence` →
`generate-section` (prompt) → `persist-section-draft`, plus
conditional 4th step for `literature-review` on cite_context domains.

**Inputs**:
- `academic_module_analysis` / `academic_cross_module_analysis` from uses 1-3
- `templates/generation/document/{domain}.md` + `_master-schema.yaml`
- `_master-schema.yaml`'s `cite_context:` list (default: related-work,
  introduction, discussion)

**Action**: Generate every structural domain, citing documentation as
primary evidence. Gaps become `future-scope` content, not dropped.
Claims backed by implementation evidence get `validated=true`.

Conditional literature-review pass adds external citation context for
domains listed in `cite_context:`.

**Completion criteria**:
- One `academic_narratives` row (stage=`generate`) per structural domain
- Conditional literature-review step completed for cite_context domains

**Rule**: Unifies old usecases 2a and 2b — one usecase under the 2-state gate.
