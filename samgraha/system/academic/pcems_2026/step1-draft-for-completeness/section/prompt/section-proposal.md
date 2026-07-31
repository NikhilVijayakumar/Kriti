You are drafting a "section proposal" — a focused plan for generating
the {{target_domain}} section of an academic paper.

## Paper title
{{paper_title}}

## Target domain
{{target_domain}}

## Section context
{{#domain_context}}
{{domain_context}}
{{/domain_context}}

## Available map entries
{{#map_entries}}
- {{map_key}}: {{type}} (target: {{target_section}})
{{/map_entries}}
{{^map_entries}}
No map entries available for this domain.
{{/map_entries}}

## Existing draft (if any)
{{#existing_draft}}
{{existing_draft}}
{{/existing_draft}}
{{^existing_draft}}
No existing draft.
{{/existing_draft}}

## Instructions

1. Assess the current state: does the domain have enough source evidence
   to generate a complete section?
2. Identify specific source materials to use (file paths).
3. Note any gaps or missing evidence.
4. Estimate word count and structure.

Write your proposal as a plain-text Markdown document with sections:
**Assessment**, **Source Materials**, **Gaps**, **Plan**.

End with a one-line summary prefixed with `SUMMARY:`.
