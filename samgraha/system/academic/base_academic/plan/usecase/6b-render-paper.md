# Use-case 6b — Render Paper

**Script**: `assemble-final-document.py` + `extract-mermaid-images.py` +
`render-docx.py` (planned, not yet built)

**Inputs**:
- `_master-schema.yaml` section order
- Each domain's latest `academic_narratives` row
- `templates/generation/html/_master-schema.html`

**Action**: Concatenate domain drafts per `_master-schema.yaml` order,
rasterize mermaid blocks (hard-fail if `mmdc` unavailable), render through
HTML template, shell to `pandoc` for DOCX, playwright for PDF.

**Completion criteria**:
- One `academic_report_history` row (report_kind='paper') per format
- Every generated file exists, non-zero size
- No unrendered mermaid fences in output

**Rule**: Unchanged mechanics from old usecase 7. Now explicitly the paper
track of the dual-track rendering split.
