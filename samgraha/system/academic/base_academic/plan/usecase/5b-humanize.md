# Use-case 5b — Humanize

**Script**: Per-domain triad — `gather-humanize-context` →
`humanize-section` (prompt — `templates/generation/humanifier.md`, Pass 3)
→ `persist-humanize-pass`

**Inputs**:
- Draft + this run's flagged spans from `academic_plagiarism_findings`
  (usecase 5a's output)
- `templates/generation/humanifier.md` — 3-layer rewrite: structural
  rhythm, technical-DNA injection, voice restoration

**Action**: Whole-section rewrite using Pass 1(/2)'s findings as context —
more expensive than usecase 5a's targeted rewrite, reserved for sections
the cheaper pass doesn't fix. `persist-humanize-pass` writes change
summary + `[NEEDS AUTHOR INPUT]` risk flags to `academic_humanize_passes`,
iteration incremented per re-run.

**Completion criteria**:
- One `academic_humanize_passes` row per (domain, iteration) for every
  domain usecase 5a flagged FAIL
- Re-running 5a on the humanized output shows improvement (fewer/no
  High-Critical flags) — not mechanically guaranteed, tracked via
  iteration history

**Verify script**: `verify_usecase_5b_humanize.py --standard base_academic --paper-id <id>`
- Reports iteration count per domain that required humanizing
- Exits 0 if every FAIL-flagged domain from the latest 5a run has >= 1
  humanize pass

**Rule**: Triggered only for domains usecase 5a flags FAIL. Loops with 5a
(re-audit after humanize) up to `max_iterations: 5` per
`plan/core/loop.yaml`'s existing fix-loop cap, falling back to
`human_review` if still failing after 5 iterations.
