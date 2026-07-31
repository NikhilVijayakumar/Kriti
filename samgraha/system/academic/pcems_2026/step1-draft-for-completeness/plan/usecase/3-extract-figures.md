# Usecase 3 — Extract Figures (Extraction Tier)

Runs before 4a-generate-findings. Populates `academic_figure_map` from existing visualization assets and documentation.

## Stages
1. **gather** — `gather-map-evidence` script (mode=extract, domain=figures)
2. **structure** — `extract-figures` prompt → LLM formats asset descriptions into structured JSON entries
3. **persist** — `persist-map-entries` script (domain=figures)

## Inputs
- `docs/paper/Bodha/drafts/visualizations/*.svg` (and .png, .tex)

## Completion
`SELECT COUNT(*) FROM academic_figure_map WHERE paper_id=?` >= 1
