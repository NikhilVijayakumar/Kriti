# Section Generation — findings (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `findings` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow Writing Guide §5 results presentation:
- Tables and figures are placed inline at their first mention (not collected at the end)
- Every table/figure must be referenced in text before it appears
- Results must include comparison with baselines/state-of-the-art
- Statistical significance must be stated where applicable
- Avoid interpreting results here — save for discussion

Tables (Tables/01-03):
- Number sequentially: Table I, Table II, etc. (Roman numerals)
- Caption above table, centered
- Include units in column headers
- Minimum font size: 8pt

Figures (Figures/01-03):
- Number sequentially: Fig. 1, Fig. 2, etc.
- Caption below figure
- Minimum resolution: 300 DPI
- Color figures must be readable in grayscale

## Rules
1. Cite evidence — every factual claim must reference a source from the **input documentation only**
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections
5. Flag uncertain claims — if evidence is ambiguous, note it with `[NEEDS VERIFICATION]`

## Output Format
Return a JSON object:
```json
{
  "sections": [{"heading": "Section Title", "text": "Section content..."}],
  "citations_used": ["source1", "source2"],
  "needs_verification": ["claim1"]
}
```
