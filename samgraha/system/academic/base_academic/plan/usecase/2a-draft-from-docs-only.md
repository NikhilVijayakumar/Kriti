# Use-case 2a — Draft From Docs Only

**Script**: Per-domain pre/semantic/post triad —
`gather-domain-evidence` (mode=`draft`) → `generate-section-docs-only`
(prompt) → `persist-section-draft`

**Inputs**:
- Author-supplied documentation only — no implementation to pull
  quantitative evidence from
- `templates/generation/document/{domain}.md` per-domain skeleton +
  `_master-schema.yaml` for section order

**Action**: Drafts every domain in `_master-schema.yaml`'s `sections:`
list from documentation alone. Every claim needing implementation proof
gets flagged `[NEEDS AUTHOR INPUT]` (same convention
`templates/generation/humanifier.md` already established) rather than
invented. `persist-section-draft` writes with `stage='generate'` and marks
the row unvalidated.

**Completion criteria**:
- One `academic_narratives` row (stage=`generate`) per structural domain
  in `_master-schema.yaml`
- Every row's evidence is traceable to documentation only — no
  implementation-sourced claim without a matching `[NEEDS AUTHOR INPUT]`
  flag where evidence is thin

**Verify script**: `verify_usecase_2a_draft_from_docs_only.py --standard base_academic --paper-id <id>`
- Reports `N/12` structural domains drafted
- Exits 0 only if `12/12`, regardless of how many `[NEEDS AUTHOR INPUT]`
  flags exist within them (that's expected, not a failure)

**Rule**: Only runs for `DOCS_ONLY` classification. Output stays
unvalidated indefinitely unless the repo later gains an implementation and
gets reclassified — no automatic promotion path exists (open question,
`base_academic-usecase-proposal.md` §7).
