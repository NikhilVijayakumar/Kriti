# Usecase 3d — Generate Figure Assets

Runs after 3-extract-figures and 3-extract-tables. Fills in `mermaid_source`
and/or `asset_path` for `academic_figure_map` rows that were flagged during
extraction (both columns null).

Two independent paths:
- **Mermaid path** for `architecture_diagram`/`flowchart`/`concept_illustration`
- **Data-chart path** for `comparison_chart`/`graph_plot` with `data_table_map_key`

## Stages

### Mermaid path
1. **gather-flagged** — `gather-map-evidence` script (mode=extract, domain=figures)
2. **generate** — `figure-mermaid.md` prompt → LLM produces `mermaid_source` per flagged row
3. **validate & persist** — `generate-mermaid-figure` deterministic script, validates via `render_mmdc` before writing

### Data-chart path
4. **gather & render** — `generate-data-chart` deterministic script, reads `academic_table_map` rows, renders matplotlib charts, persists `asset_path`

## Inputs
- `academic_figure_map` flagged rows (asset_path IS NULL, mermaid_source IS NULL)
- `academic_table_map` rows (for data-chart path, linked by data_table_map_key)

## Completion
`SELECT COUNT(*) FROM academic_figure_map WHERE paper_id=? AND asset_path IS NULL AND mermaid_source IS NULL` = 0
