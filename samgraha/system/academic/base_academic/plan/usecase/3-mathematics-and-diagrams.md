# Use-case 3 — Mathematics and Diagrams

**Script**: Per-module triads — `gather-module-evidence` →
`module-analysis-mathematics` + `module-analysis-architecture` (two
semantic prompts per module) → `persist-module-analysis`, then
cross-module: `architecture` + `dependencies` + `interactions`.

**Inputs**:
- Repo documentation as primary evidence
- `templates/generation/analysis/{module,cross_module}/{mathematics,architecture,dependencies,interactions}.md`
- `prompt/common/mermaid-diagram-standards.md` conventions

**Action**: Derive mathematical formalization (LaTeX) and mermaid diagrams
(classDiagram for module architecture, flowchart TD + classDef tiers for
cross-module dependencies/interactions). All sourced from documentation.

**Completion criteria**:
- One `academic_module_analysis` row per (module, mathematics) and (module, architecture)
- Three `academic_cross_module_analysis` rows: architecture, dependencies, interactions

**Rule**: Merges old usecase 1's mathematics kind + old usecase 3's figures kind.
Single place where `prompt/common/mermaid-diagram-standards.md` conventions apply.
