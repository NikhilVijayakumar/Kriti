# Usecase 3 — Extract Algorithms (Extraction Tier)

Runs before 4a-generate-methodology. Populates `academic_algorithm_map` from mathematical analysis documentation.

## Stages
1. **gather** — `gather-map-evidence` script (mode=extract, domain=algorithms)
2. **structure** — `extract-algorithms` prompt → LLM formats pseudocode/complexity into structured JSON entries
3. **persist** — `persist-map-entries` script (domain=algorithms)

## Inputs
- `docs/paper/Bodha/cross_module/mathematics.md`

## Completion
`SELECT COUNT(*) FROM academic_algorithm_map WHERE paper_id=?` >= 1 (zero is valid if no algorithms are described)
