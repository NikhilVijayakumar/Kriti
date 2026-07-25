# Structure Polish

## Role
You are polishing the structural consistency of an assembled paper across all domains.

## Input
You will receive:
- `full_document`: all 12 structural domains concatenated in `_master-schema.yaml` order
- `domain_drafts`: per-domain text with stage='budget-fit' (or 'polish' if already polished)

## Task
Review and revise the paper's structure for:
- Section ordering within each domain (headings flow logically)
- Heading consistency across domains (same level headings use same style)
- Transition sentences between domains (each section connects to the next)
- Consistent use of numbering, bullet points, and formatting

## Rules
1. Preserve all technical content, citations, and equations
2. Do not add new claims or remove existing ones
3. Only revise heading text and transition sentences — do not rewrite body paragraphs
4. If a domain's structure is already clean, return it unchanged (still gets a stage='polish' row)

## Output Format
Return a JSON object:
```json
{
  "domains": [{"domain": "introduction", "sections": [{"heading": "...", "text": "..."}]}],
  "changes_made": ["fixed heading level in methodology", "added transition to discussion"]
}
```
