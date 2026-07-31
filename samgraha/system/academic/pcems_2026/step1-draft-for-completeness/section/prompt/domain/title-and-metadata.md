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
1. Cite evidence — every factual claim must reference a source from the **input documentation only** using `[evidence: source]` markers (e.g. `[evidence: docs/overview.md]`). In-repo grounding markers are extracted during the citations pass and stripped before final rendering. External literature citations are handled separately in the citations usecase.
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections (diagram/equation/table weaving is handled separately in the enrichment usecase)
5. Flag uncertain claims — if evidence is ambiguous, note it with `[NEEDS VERIFICATION]`
6. **Never invent facts not present in the evidence.** Do not invent an
   author name, affiliation, or corresponding-author email that isn't
   named in the evidence — write `[NEEDS VERIFICATION]` for that field
   instead of a plausible-sounding placeholder.

## Output Format
`templates/generation/markdown/title-and-metadata.md` has three scalar
slots and three list slots (authors, affiliations, keywords). Use these
headings **exactly** for the scalar slots (they snake-case to the
template's keys) — a heading the template doesn't expect is silently
dropped at assembly time:

- **Title**: the paper title (snake-cases to `title`, fills the `# {{ title }}` page header)
- **Corresponding Author Email**: only if named in evidence, else `[NEEDS VERIFICATION]`
- **Abstract**: structured Purpose/Method/Results/Conclusion, 2400-4800 characters

The `authors`, `affiliations`, and `keywords` lists (template's
`{{#authors}}`/`{{#affiliations}}`/`{{#keywords}}` loops) are **not
populated by this step** — the persistence pipeline only stores flat
`{heading, text}` sections, not structured lists, as of this prompt's
current version. Do not fabricate placeholder authors/affiliations to fill
these — leave them for a later pass once that gap is closed.

Return a JSON object:
```json
{
  "sections": [
    {"heading": "Title", "text": "..."},
    {"heading": "Corresponding Author Email", "text": "..."},
    {"heading": "Abstract", "text": "..."}
  ],
  "citations_used": ["source1", "source2"],
  "needs_verification": ["claim1"]
}
```
