# Section Generation — findings (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers
- `table_map`: pre-extracted, real table entries from the paper's evaluation documents (map_key, caption, columns_json, rows_json) — every value is verbatim from the source, never invented
- `figure_map`: pre-extracted, real figure entries from the paper's visualization assets (map_key, caption, figure_type, asset_path) — only figures that actually exist

## Task
Write the `findings` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow Writing Guide §5 results presentation:
- Tables and figures are placed inline at their first mention (not collected at the end)
- Every table/figure must be referenced in text before it appears
- When citing a table from `table_map`, reference it by its `map_key` (e.g. "as shown in TBL-1") — the map_key is resolved to the correct display number (Table I, Table II, etc.) at assembly time
- When citing a figure from `figure_map`, reference it by its `map_key` (e.g. "as shown in FIG-1") — same display-number resolution at assembly
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
1. Cite evidence — every factual claim must reference a source from the **input documentation only** using `[evidence: source]` markers (e.g. `[evidence: docs/evaluation.md]`). These are internal grounding markers extracted during the citations pass and stripped before final rendering.
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections
5. Flag uncertain claims — if evidence is ambiguous, note it with `[NEEDS VERIFICATION]`
6. **Never invent numbers, model names, hardware, baselines, or comparisons.**
   Every metric, percentage, model identifier, dataset name, and hardware spec
   in this section must appear verbatim (or as a direct paraphrase) in the
   provided `analysis_docs`/`documentation`. Do not fill gaps with plausible-
   sounding values drawn from general knowledge of what a typical paper in
   this area reports (e.g. "GPT-4", round accuracy percentages, generic
   consumer hardware) — if the evidence doesn't name the model, dataset,
   hardware, or number, do not name one. Where the evidence contains a
   template placeholder (e.g. `[USER: e.g., ...]`) rather than a real value,
   treat that field as **absent** — write `[NEEDS VERIFICATION]`, do not
   substitute the placeholder's example text as if it were real data.

## Output Format
`templates/generation/markdown/findings.md` has exactly three scalar
slots — use these three headings **exactly** (they get snake-cased to the
template's placeholder keys: "Experimental Setup" -> `experimental_setup`,
"Results" -> `results`, "Analysis" -> `analysis`). Any other heading is
silently dropped at assembly time — content under a heading the template
doesn't expect never reaches the paper.

- **Experimental Setup**: hardware/software/models/dataset/baselines used
- **Results**: all tables, each captioned and referenced in the prose that
  precedes it, per the Tables/01-03 rules above — this is where every
  Table I/II/III/... lives, concatenated into one flowing section
- **Analysis**: results interpreted (guide/Examples/04-findings-examples.md
  "Results analyzed, not just presented" — direct comparison statements
  the reader can verify against the tables in Results, not new numbers)

Return a JSON object:
```json
{
  "sections": [
    {"heading": "Experimental Setup", "text": "..."},
    {"heading": "Results", "text": "..."},
    {"heading": "Analysis", "text": "..."}
  ],
  "citations_used": ["source1", "source2"],
  "needs_verification": ["claim1"]
}
```
