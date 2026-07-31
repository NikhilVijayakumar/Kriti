You are drafting a "map proposal" for **mathematics/equation entries** — a structured plan for extracting mathematics/equation entries from the paper's source materials.

## Paper title
{{paper_title}}

## Map kind
mathematics

## Module registry
{{#module_registry}}
- **{{module_name}}** (role: {{role}}, interest_weight: {{interest_weight}}) — {{module_path}}
{{/module_registry}}
{{^module_registry}}
No modules registered.
{{/module_registry}}

## Candidate source files
{{#candidate_files}}
- {{.}}
{{/candidate_files}}
{{^candidate_files}}
No source files found matching mathematics-related content.
{{/candidate_files}}

## File snippets
{{#file_snippets}}
### {{path}}
{{content}}
{{/file_snippets}}

## Reasoning chain (follow in order)
1. Review the module registry — understand which modules are declared, their roles, and their interest weights.
2. For each module, identify which candidate source files belong to it (by path prefix).
3. Per module, identify which files contain extractable mathematics/equation entries and estimate how many per file — weight the primary module's findings as the main narrative, dependent modules as supporting/comparative context.
4. Flag ambiguous or borderline entries that need human judgment.
5. Propose extraction order (one module at a time, primary first, then dependents).

Write your proposal as Markdown with sections: **Source Files**, **Estimated Entries**, **Ambiguities**, **Extraction Order**.

End with `SUMMARY:` one-liner.
