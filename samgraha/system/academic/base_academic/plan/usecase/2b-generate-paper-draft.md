# Use-case 2b — Generate Paper Draft

**Script**: Per-domain pre/semantic/post triad —
`gather-domain-evidence` (mode=`generate`) → `generate-section` (prompt) →
`persist-section-draft`

**Inputs**:
- `academic_module_analysis` / `academic_cross_module_analysis` (usecase 1's
  output) as evidence source
- `templates/generation/document/{domain}.md` per-domain skeleton +
  `_master-schema.yaml` for section order

**Action**: Generates every structural domain, citing analysis-doc content
as evidence for quantitative claims. `persist-section-draft` writes with
`stage='generate'`, marked `validated=true` where evidence backs the
claim.

**Completion criteria**:
- One `academic_narratives` row (stage=`generate`) per structural domain
- Every claim traceable to `academic_module_analysis`/
  `academic_cross_module_analysis` content, not asserted with no evidence
  pointer

**Verify script**: `verify_usecase_2b_generate_paper_draft.py --standard base_academic --paper-id <id>`
- Reports `N/12` structural domains drafted
- Exits 0 only if `12/12`

**Rule**: Runs for `IMPL_WITH_ANALYSIS` classification directly, or as the
fallthrough after usecase 1 completes for `IMPL_NO_ANALYSIS`. Never runs
before usecase 1 has produced analysis docs for an `IMPL_NO_ANALYSIS` repo
— `classify-repo` enforces this ordering, not this usecase.
