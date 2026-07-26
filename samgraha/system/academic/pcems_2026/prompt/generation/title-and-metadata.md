# Section Generation — title-and-metadata (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `title-and-metadata` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow PCEMS 2026 template structure for the title block:
- Paper title (concise, specific, ≤15 words preferred)
- Author names and affiliations
- Corresponding author email
- Abstract (2400–4800 characters, structured: Purpose / Method / Results / Conclusion)
- Keywords (4–6, relevant to the paper's domain)

Order: Title → Authors → Affiliations → Corresponding Author → Abstract → Keywords.

## Rules
1. Cite evidence — every factual claim must reference a source from the **input documentation only** (in-repo grounding markers; external literature citations are handled separately in the citations usecase)
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections (diagram/equation/table weaving is handled separately in the enrichment usecase)
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
