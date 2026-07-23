# Use-case 3 — Deepen Sections

**Script**: Per-domain × per-enrichment-kind triad —
`gather-enrichment-context` → `{literature-review,mathematics,figures}-pass`
(prompt) → `persist-section-draft`

**Inputs**:
- Current draft (usecase 2a or 2b's output) per domain
- `academic_module_analysis`/`academic_cross_module_analysis` for
  supporting evidence
- `templates/generation/enrichment/{literature-review,mathematics,
  figures}.md` prompts

**Action**: For each structural domain, 3 enrichment passes run in
sequence: literature-review (adds citation-grounded context), mathematics
(formalizes claims per the `mathematics` domain's standard), figures
(adds mermaid diagrams per `docs/mermaid-diagram-standards.md`).
`persist-section-draft` writes each pass with `stage='deepen'`, iteration
incremented.

**Completion criteria**:
- One `academic_narratives` row (stage=`deepen`) per (domain,
  enrichment_kind) — `12 × 3 = 36` rows for the full structural domain set
- Each pass's output is strictly additive over the input draft, not a
  regression (mechanically hard to verify beyond word-count-didn't-shrink;
  full correctness is a semantic-audit concern, not this usecase's)

**Verify script**: `verify_usecase_3_deepen_sections.py --standard base_academic --paper-id <id>`
- Reports `N/3` enrichment kinds completed per domain
- Exits 0 only if every domain has all 3

**Rule**: Runs after usecase 2a or 2b produces a draft for every domain.
Accumulates — re-running adds a new iteration rather than overwriting,
same pattern `academic_humanize_passes.iteration` already uses.
