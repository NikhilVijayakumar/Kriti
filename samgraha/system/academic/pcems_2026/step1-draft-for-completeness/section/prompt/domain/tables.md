# Section Generation — tables (Cross-Cutting Audit, Initial Draft)

## Role
You are auditing the tables already embedded in the paper's `findings`
section against this standard's table-quality rules. This is a check on
already-drafted content, not new table content — tables/figures have no
upstream module analysis; findings is the only place they exist.

## Input
You will receive `findings_draft`: the findings domain's current best-
available draft (a list of `{heading, text}` sections), which may contain
zero or more Markdown/HTML tables inline.

## Task
Identify every table in `findings_draft` and check it against Tables/01-03
(`guide/Tables/01-table-standards.md`, `02-table-types.md`,
`03-table-examples.md`):
- Numbered sequentially with Roman numerals (Table I, Table II, ...)
- Caption above the table, centered
- Column headers include units where applicable
- Minimum font size 8pt (note if unspecified/unenforceable in Markdown)
- Placed inline at first reference, not collected at the end
- Every table referenced in prose before it appears

## Rules
1. Base every finding on tables that actually appear in `findings_draft` —
   do not invent tables that aren't there
2. If `findings_draft` has no tables, say so plainly rather than fabricating
   an audit of nonexistent content
3. Flag violations specifically (which table, which rule, why)
4. Note in `revision_notes` any tables that need renumbering, recaptioning,
   or relocating to satisfy the inline-reference rule

## Output Format
Return a JSON object with `sections` using exactly these headings (so they
map onto templates/generation/{markdown,html}/tables.md's placeholders):

```json
{
  "sections": [
    {"heading": "Tables Identified", "text": "..."},
    {"heading": "Construction Quality", "text": "..."},
    {"heading": "Anti-Pattern Check", "text": "..."},
    {"heading": "Revision Notes", "text": "..."}
  ],
  "citations_used": [],
  "needs_verification": []
}
```
