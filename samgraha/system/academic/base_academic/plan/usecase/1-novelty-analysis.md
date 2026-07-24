# Use-case 1 — Novelty Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-novelty` (prompt) → `persist-module-analysis` +
`gather-cross-module-evidence` → `cross-module-analysis-novelty` (prompt) →
`persist-cross-module-analysis`

**Inputs**:
- Module source files, imports, docstrings
- Cross-module evidence (import graph, module summaries)

**Action**: Identify what's novel in the codebase, sourced from actual
documentation. Per-module novelty + cross-module novelty.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind='novelty'` >= 1

**Verify script**: `script/verify/uc1_novelty.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Accumulates —
re-running adds new analyses, never overwrites.
