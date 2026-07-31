# Usecase 3 — Extract Tables (Extraction Tier)

Runs before 4a-generate-findings. Populates `academic_table_map` from real evaluation markdown.

## Stages
1. **gather** — `gather-map-evidence` script (mode=extract, domain=tables)
2. **structure** — `extract-tables` prompt → LLM formats raw markdown into structured JSON entries
3. **persist** — `persist-map-entries` script (domain=tables)

## Inputs
- `docs/paper/Bodha/drafts/5. Experimental Evaluation.md`
- `docs/paper/Bodha/drafts/6. Results and Discussion.md`

## Completion
`SELECT COUNT(*) FROM academic_table_map WHERE paper_id=?` >= 1
