# Section Generation — figures (Cross-Cutting Audit, Initial Draft)

## Role
You are auditing the figures already embedded in the paper's `findings`
section against this standard's figure-quality rules. This is a check on
already-drafted content, not new figure content — tables/figures have no
upstream module analysis; findings is the only place they exist.

## Input
You will receive `findings_draft`: the findings domain's current best-
available draft (a list of `{heading, text}` sections), which may reference
zero or more figures inline (image embeds, diagram descriptions).

## Task
Identify every figure in `findings_draft` and check it against Figures/01-03
(`guide/Figures/01-figure-standards.md`, `02-figure-types.md`,
`03-figure-examples.md`):
- Numbered sequentially (Fig. 1, Fig. 2, ...)
- Caption below the figure
- Minimum resolution 300 DPI (note if unverifiable from text alone)
- Color figures must remain readable in grayscale
- Placed inline at first reference, not collected at the end
- Every figure referenced in prose before it appears

## Rules
1. Base every finding on figures that actually appear in `findings_draft` —
   do not invent figures that aren't there
2. If `findings_draft` has no figures, say so plainly rather than
   fabricating an audit of nonexistent content
3. Flag violations specifically (which figure, which rule, why)
4. Note in `revision_notes` any figures needing renumbering, recaptioning,
   relocating, or a grayscale-legibility fix

## Output Format
Return a JSON object with `sections` using exactly these headings (so they
map onto templates/generation/{markdown,html}/figures.md's placeholders):

```json
{
  "sections": [
    {"heading": "Figures Identified", "text": "..."},
    {"heading": "Construction Quality", "text": "..."},
    {"heading": "Grayscale Legibility", "text": "..."},
    {"heading": "Anti-Pattern Check", "text": "..."},
    {"heading": "Revision Notes", "text": "..."}
  ],
  "citations_used": [],
  "needs_verification": []
}
```
