# Section Generation — introduction (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `introduction` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow Writing Guide §2 structure:
1. Broad context (2–3 sentences establishing the problem domain)
2. Specific problem statement (gap the paper addresses)
3. Literature gap (what existing work misses)
4. Proposed approach (one-paragraph summary of the contribution)
5. Paper organization (optional, brief)

Reviewer expectations (Reviewer Expectations/03):
- Contribution must be stated explicitly in the first 2 paragraphs
- Avoid vague claims ("This paper presents a new method") — state the specific contribution with numbers
- Abstract must match introduction's claims exactly

AI-Generated Language Flags (Writing Guide/01):
- Avoid: delve, landscape, tapestry, crucial, paramount
- Avoid hedging: "it should be noted that," "it is worth mentioning"
- Avoid: "In the realm of," "In the landscape of"

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
