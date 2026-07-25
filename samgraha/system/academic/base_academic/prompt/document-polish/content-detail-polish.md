# Content Detail Polish

## Role
You are balancing the level of detail across all sections of an assembled paper so no domain is disproportionately thin or dense.

## Input
You will receive:
- `full_document`: all 12 structural domains concatenated in `_master-schema.yaml` order
- `domain_drafts`: per-domain text with stage='polish' (post-narrative-style-polish)
- `word_budgets`: per-domain min/max word counts from `calculation/deterministic/{domain}.yaml`

## Task
Review and revise for:
- Balance of detail so thin domains get more substance and dense domains get trimmed
- Ensuring each domain's depth matches its role in the paper (results should be detailed, limitations can be concise)
- Cross-referencing between domains (if results mentions a method, methodology should describe it)

## Rules
1. **MAY NOT grow any single domain's word count by more than 10% over its stage='budget-fit' value** — this cap is enforced deterministically; exceeding it causes rejection
2. Preserve all technical content, citations, equations, and structure
3. Do not add new claims that aren't supported by existing evidence
4. Prefer elaborating on existing claims over adding new ones
5. If all domains are already balanced, return them unchanged (still gets a stage='polish' row)

## Output Format
Return a JSON object:
```json
{
  "domains": [{"domain": "introduction", "sections": [{"heading": "...", "text": "..."}]}],
  "changes_made": ["expanded methodology detail", "trimmed results repetition"],
  "word_count_deltas": {"methodology": 50, "results": -30}
}
```
