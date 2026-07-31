# Section Generation — gaps (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers

## Task
Write the `gaps` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Writing Guide gap-analysis framing:
- State the specific gap in existing work that this paper addresses
- Ground the gap claim in cited literature — do not assert a gap without evidence
- Connect the gap to the paper's contribution (the gap is what the contribution fills)

Reviewer Expectations/03:
- "Missing key works" scores Weak (1) for Literature coverage; "Comprehensive and current" scores Strong (3).
- The gap must be real and documented, not manufactured.

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
