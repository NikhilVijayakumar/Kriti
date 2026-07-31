# Usecase 3 — Extract Equations (Extraction Tier)

Runs before 4a-generate-methodology. Populates `academic_equation_map` from mathematical analysis documentation.

## Stages
1. **gather** — `gather-map-evidence` script (mode=extract, domain=equations)
2. **structure** — `extract-equations` prompt → LLM formats LaTeX + variable definitions into structured JSON entries
3. **persist** — `persist-map-entries` script (domain=equations)

## Inputs
- `docs/paper/Bodha/cross_module/mathematics.md`

## Completion
`SELECT COUNT(*) FROM academic_equation_map WHERE paper_id=?` >= 1
