# Use-case 2 — Gap Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-gaps` (prompt) → `persist-module-analysis` +
`gather-cross-module-evidence` → `cross-module-analysis-gaps` (prompt) →
`persist-cross-module-analysis`

**Inputs**:
- Module source files, imports, docstrings
- Cross-module evidence (import graph, module summaries)

**Action**: Identify gaps in the codebase, sourced from actual documentation.
Per-module gaps + cross-module gaps.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind='gaps'` >= 1

**Verify script**: `script/verify/uc2_gaps.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Accumulates.
