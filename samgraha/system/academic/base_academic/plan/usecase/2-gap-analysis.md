# Use-case 2 — Gap Analysis

**Script**: Per-module triad — `gather-module-evidence` →
`module-analysis-gaps` (prompt) → `persist-module-analysis`, then
cross-module rollup.

**Inputs**: Same as novelty-analysis, with `.../gaps.md` templates.

**Action**: Identify gaps — things the documentation implies should exist
but doesn't cover, or areas where the approach has known limitations.
Each finding becomes a future-scope item in usecase 4, not dropped.

**Completion criteria**:
- One `academic_module_analysis` row per (module, gaps)
- One `academic_cross_module_analysis` row for gaps

**Rule**: Required upstream for assemble-paper-structure's `future-scope` domain.
