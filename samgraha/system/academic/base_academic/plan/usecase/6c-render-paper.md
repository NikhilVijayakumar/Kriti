# Use-case 6c — Render Paper

**Depends on**: `document-semantic-audit` (PASS) — `assemble-final-document.py`'s
first action calls `usecase_status()` for each upstream and hard-fails,
listing which domains/audits are still outstanding, rather than
concatenating a partial document silently.

**Script**: `assemble-final-document.py` + `extract-mermaid-images.py` +
`render-docx.py` (planned, not yet built)

**Inputs**:
- `_master-schema.yaml` section order
- Each domain's latest `academic_narratives` row
- `templates/generation/html/_master-schema.html`

**Action**: Concatenate domain drafts per `_master-schema.yaml` order,
rasterize mermaid blocks (hard-fail if `mmdc` unavailable), render through
HTML template, shell to `pandoc` for DOCX, playwright for PDF.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_report_history WHERE paper_id=? AND report_kind='paper'` >= 1
- Every generated file exists, non-zero size
- No unrendered mermaid fences in output

**Verify script**: `script/verify/uc6c_render_paper.py --paper-id <id>`

**Rule**: Runs after document-semantic-audit PASS. Gates on all upstream
usecases completing.
