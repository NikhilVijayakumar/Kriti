# Assign Target Sections

Step 0 extracted these assets (tables, figures, equations, algorithms,
citations) without deciding which manuscript section each belongs in —
that decision is drafting, not extraction, and it's your job now.

## Input

- `unassigned`: assets grouped by kind (`table`, `figure`, `equation`,
  `algorithm`, `citation`), each with its content (`caption`/`citation`
  text) and `source_evidence`.
- `structural_domains`: the paper's real 6 sections —
  `title-and-metadata`, `introduction`, `methodology`, `findings`,
  `conclusion`, `references`.
- `reference_guidance`: which sections an analysis kind's findings
  *typically* land in. This is guidance, not a rule — use the asset's
  actual content to decide, not a mechanical lookup.

## Task

For every asset in `unassigned`, assign exactly one `target_section`
(or `domain_id`'s equivalent section key, for citations) from
`structural_domains`. Base the decision on what the asset actually
shows — a comparison chart belongs wherever comparisons are discussed,
not wherever "figures" generically points.

## Rules

1. Every asset must get exactly one assignment — no assets left
   unassigned, no asset assigned to more than one section.
2. Only use section keys from `structural_domains` — never invent a
   section name.
3. If an asset's evidence doesn't clearly support any one section,
   pick the closest fit and flag it in `needs_verification` rather than
   guessing silently.

## Output (JSON)

```json
{
  "assignments": [
    {"kind": "table", "id": 12, "target_section": "findings"},
    {"kind": "citation", "id": 4, "target_section": "introduction"}
  ],
  "needs_verification": ["table:12 — ambiguous between findings and methodology"]
}
```
