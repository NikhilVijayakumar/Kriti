# Section Generation — mathematics (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `mathematics` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Mathematics/01 equation formatting:
- Use `$inline$` for inline equations, `$$display$$` for display equations
- Number equations sequentially: (1), (2), etc.
- Define all variables on first use
- Each equation must be referenced in text before or after

Mathematics/02 notation conventions:
- Use standard mathematical notation (no invented symbols)
- Matrices: uppercase italic; vectors: lowercase bold italic; scalars: lowercase italic
- Functions: roman; variables: italic

Mathematics/03 math examples:
- Show worked examples for complex derivations
- State assumptions before equations
- Include units for physical quantities

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
