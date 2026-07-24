# Use-case 3 — Mathematics and Diagrams

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module (math + architecture) + cross-module triads —
`gather-module-evidence` → `module-analysis-mathematics` +
`module-analysis-architecture` → `persist-module-analysis` +
`gather-cross-module-evidence` → `cross-module-analysis-mathematics` +
`cross-module-analysis-architecture` + `cross-module-analysis-dependencies` +
`cross-module-analysis-interactions` → `persist-cross-module-analysis`

**Inputs**:
- Module source files, imports, docstrings
- Cross-module evidence (import graph, module summaries)

**Action**: Derive mathematical formalization and mermaid diagrams from
documentation. Per-module math + architecture + cross-module math +
architecture + dependencies + interactions.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind IN ('mathematics','architecture')` >= 1

**Verify script**: `script/verify/uc3_math_diagrams.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Accumulates.
