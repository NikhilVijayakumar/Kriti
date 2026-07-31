# Fit to Budget (Word Count Adjustment)

## Role
You are adjusting a paper section's word count to fit within its configured min/max range.

## Input
You will receive:
- `current_draft`: the section text (post-enrichment)
- `word_count`: current word count
- `budget_min`: minimum word count
- `budget_max`: maximum word count
- `citations`: list of citations that must be preserved

## Task
Adjust the section to fit within the word budget while preserving all technical content, citations, and structural integrity.

## Rules
1. **If over budget**: compress sentence-by-sentence (preferred) rather than cutting whole paragraphs — cutting paragraphs risks losing claims that fail deterministic audit for missing content
2. **If under budget**: expand by elaborating on existing claims with more detail, not by adding new claims
3. Preserve every citation — citations are never removed during budget fitting
4. Preserve the heading structure
5. Maintain academic tone throughout

## Output Format
Return a JSON object:
```json
{
  "sections": [{"heading": "Section Title", "text": "Adjusted content..."}],
  "adjustment_summary": "Summary of what was trimmed or expanded",
  "final_word_count": 450
}
```
