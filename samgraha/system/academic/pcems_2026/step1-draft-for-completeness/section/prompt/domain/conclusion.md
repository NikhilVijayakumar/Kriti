# Section Generation — conclusion (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `conclusion` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow Writing Guide §6:
- Restate the contribution in 1–2 sentences (must match introduction)
- Summarize key findings (3–5 bullet points or short paragraph)
- State limitations honestly (1–2 paragraphs)
- Suggest future work (1 paragraph, specific not generic)
- Do NOT introduce new results, new claims, or new evidence

Philosophy (Philosophy/philosophy.md):
- The contribution should remain visible throughout the manuscript and should be reinforced consistently across: Introduction, Methodology, Experimental Evaluation, Results, Conclusion.

## Rules
1. Cite evidence — every factual claim must reference a source from the **input documentation only** using `[evidence: source]` markers (e.g. `[evidence: docs/results.md]`). These are internal grounding markers extracted during the citations pass and stripped before final rendering.
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections
5. Flag uncertain claims — if evidence is ambiguous, note it with `[NEEDS VERIFICATION]`
6. **Never invent facts not present in the evidence.** Do not introduce new
   results, numbers, or claims here (per the Guide Constraints above) — and
   do not invent limitations or future-work directions that aren't
   supportable by the evidence either.

## Output Format
`templates/generation/markdown/conclusion.md` has four scalar slots.
Use these headings **exactly** (they snake-case to the template's keys) —
a heading the template doesn't expect is silently dropped at assembly time:

- **Contribution Summary**: restated contribution, must match introduction
  (use plain "Contribution Summary" — the template's own H2 label is
  "Summary of Contributions" but its placeholder key is
  `contribution_summary`; "Summary of Contributions" would snake-case to a
  key that doesn't match)
- **Impact Statement**: practical/scientific significance (use "Impact
  Statement", not just "Impact" — the placeholder key is `impact_statement`)
- **Limitations**: honest limitations (1-2 paragraphs)
- **Future Work**: suggested future research directions as a paragraph (the
  template renders this as a scalar `{{ future_work }}`, not a structured
  list — write prose, not bulleted items)

Return a JSON object:
```json
{
  "sections": [
    {"heading": "Contribution Summary", "text": "..."},
    {"heading": "Impact Statement", "text": "..."},
    {"heading": "Limitations", "text": "..."}
  ],
  "citations_used": ["source1", "source2"],
  "needs_verification": ["claim1"]
}
```
