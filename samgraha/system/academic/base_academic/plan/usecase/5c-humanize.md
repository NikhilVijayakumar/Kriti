# Use-case 5b — Humanize

**Script**: Per-domain triad — `gather-humanize-context` →
`humanize-section` (prompt) → `persist-humanize-pass`

**Inputs**:
- Draft + flagged spans from `academic_plagiarism_findings`
- `templates/generation/humanifier.md`

**Action**: Whole-section rewrite using Pass 1(/2)'s findings as context.
Reserved for sections the cheaper targeted rewrite doesn't fix.

**Completion criteria**:
- One `academic_humanize_passes` row per (domain, iteration) for every
  domain flagged FAIL by plagiarism audit

**Rule**: Triggered only for domains that still FAIL after targeted rewrite.
Loops with plagiarism-audit up to `max_iterations: 5`, falling back to
`human_review`.
