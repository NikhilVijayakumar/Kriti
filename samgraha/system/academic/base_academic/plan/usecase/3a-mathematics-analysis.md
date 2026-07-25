# Use-case 3a — Mathematics Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-mathematics` → `persist-module-analysis` (kind=`mathematics`)
+ `gather-cross-module-evidence` → `cross-module-analysis-mathematics` →
`persist-cross-module-analysis` (kind=`mathematics`)

**Inputs**:
- Module source files, imports, docstrings
- Cross-module evidence (import graph, module summaries)

**Action**: Derive mathematical formalization from documentation. Per-module
math + cross-module math analysis only — architecture/diagrams are in 3b.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind='mathematics'` >= 1

**Verify script**: `script/verify/uc3a_math_analysis.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Independent of 3b —
either can re-run without the other. Accumulates.
