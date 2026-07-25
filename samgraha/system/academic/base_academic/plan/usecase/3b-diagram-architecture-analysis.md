# Use-case 3b — Diagram & Architecture Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-architecture` → `persist-module-analysis` (kind=`architecture`)
+ `gather-cross-module-evidence` → `cross-module-analysis-architecture` +
`cross-module-analysis-dependencies` + `cross-module-analysis-interactions` →
`persist-cross-module-analysis` (3 kinds)

**Inputs**:
- Module source files, imports, docstrings
- Cross-module evidence (import graph, module summaries)

**Action**: Derive mermaid diagrams and architecture analysis from documentation.
Per-module architecture + cross-module architecture + dependencies + interactions
— mathematics formalization is in 3a.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind IN ('architecture','dependencies','interactions')` >= 1

**Verify script**: `script/verify/uc3b_diagram_architecture.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Independent of 3a.
Accumulates.
