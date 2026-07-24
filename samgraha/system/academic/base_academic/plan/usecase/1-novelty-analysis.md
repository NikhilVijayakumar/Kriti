# Use-case 1 — Novelty Analysis

**Script**: Per-module triad — `gather-module-evidence` →
`module-analysis-novelty` (prompt) → `persist-module-analysis`, then
cross-module rollup with `gather-cross-module-evidence` →
`cross-module-analysis-novelty` → `persist-cross-module-analysis`

**Inputs**:
- Repo documentation (README, docs/, docstrings) as primary evidence
- Module source code as corroborating evidence (never invented)
- `templates/generation/analysis/{module,cross_module}/novelty.md`

**Action**: Identify what's novel in each module and across modules, citing
documentation passages. `[NEEDS AUTHOR INPUT]` where docs don't support a
claim that source code alone would suggest.

**Completion criteria**:
- One `academic_module_analysis` row per (module, novelty) — `module_count` rows
- One `academic_cross_module_analysis` row for novelty

**Rule**: Runs after classify-repo confirms HAS_DOCS. Part of the analysis
phase (usecases 1-3), before paper assembly.
