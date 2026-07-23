# Use-case 7 — Render

**Status: NOT YET IMPLEMENTED.** No `render`, `assemble-final-document`,
`extract-mermaid-images`, or `render-docx` scripts exist. This document
specifies the intended shape
(`base_academic-data-pipeline-proposal.md` §6.3-§6.6, §7), not a built
usecase — `run_full_workflow.py`'s Phase 8 loop already calls
`steps_of(steps, "render")`, finds an empty list, and silently no-ops,
same as usecase 6.

**Script (planned)**: `assemble-final-document.py` (deterministic),
calling `extract-mermaid-images.py` and `render-docx.py` in sequence.

**Inputs (planned)**:
- `_master-schema.yaml`'s `sections:` list for document order
- Each domain's latest `academic_narratives` row (`stage='humanize'` if it
  exists, else `deepen`, else `generate` — the most-processed version)
- `templates/generation/document/html/_master-schema.html`
- `academic_visualizations` for mermaid-diagram reuse (skip re-render if a
  matching `content_hash` already exists)

**Action (planned)**:
1. Concatenate sections per `_master-schema.yaml`'s order.
2. `extract-mermaid-images.py`: scan for ` ```mermaid ` blocks, render via
   `mmdc` (hard-fail if unavailable — see §6.4's dependency note, no
   silent skip), record in `academic_visualizations`.
3. Render through `_master-schema.html` (chevron, matching
   `python_hackathon`'s templating choice).
4. `render-docx.py`: shell out to `pandoc` for the `.docx` variant.
5. `playwright`-based HTML→PDF, matching
   `python_hackathon/script/usecase-7-pdf/export_team_pdfs.py`'s already-
   proven approach.
6. Write `docs/paper/{system}/final/{system}-{paper|journal}.{md,html,pdf,docx}`
   and record the run in `academic_report_history`, flipping the prior
   `is_latest=1` row for this (paper, format) to `0` first.

**Completion criteria (planned)**:
- One `academic_report_history` row per format (`markdown`/`html`/`pdf`/
  `docx`) per run, exactly one `is_latest=1` per (paper, format)
- Every generated file exists on disk, non-zero size
- No unrendered ` ```mermaid ` fence text survives into the HTML/PDF/DOCX
  output (would indicate `extract-mermaid-images.py` failed silently
  instead of hard-failing, per §6.4)

**Verify script (planned)**: `verify_usecase_7_render.py --standard base_academic --paper-id <id>`

**Rule**: Run once per desired snapshot; harmless to re-run — regenerates
entirely from DB-stored data, no re-audit or re-generation needed (matches
"report can be easily regenerated at any time as long as data is in db").
