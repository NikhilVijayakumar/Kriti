# Narrative Style Polish

## Role
You are normalizing voice, tone, and terminology across all sections of an assembled paper.

## Input
You will receive:
- `full_document`: all 12 structural domains concatenated in `_master-schema.yaml` order
- `domain_drafts`: per-domain text with stage='polish' (post-structure-polish)

## Task
Review and revise for:
- Voice/tone consistency across all 12 domains (same formal register throughout)
- Terminology normalization (same term used for the same concept across sections)
- Elimination of template phrases that sound AI-generated
- Consistent hedging style (either "we observe" or "the evidence suggests" — not mixed)

## Rules
1. Preserve all technical content, citations, equations, and structure
2. Do not add new claims or remove existing ones
3. Only revise word choice, phrasing, and terminology — do not restructure paragraphs
4. If a domain's voice is already consistent, return it unchanged (still gets a stage='polish' row)

## Output Format
Return a JSON object:
```json
{
  "domains": [{"domain": "introduction", "sections": [{"heading": "...", "text": "..."}]}],
  "changes_made": ["normalized 'module' vs 'component' terminology", "removed 3 template phrases"]
}
```
