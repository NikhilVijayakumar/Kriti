# Section Generation — methodology (Evidence-Grounded, Initial Draft)

## Role
You are generating a paper section from analysis documentation and implementation evidence.

## Input
You will receive:
- `analysis_docs`: the relevant analysis documentation for this domain
- `documentation`: README and source code excerpts
- `upstream_context`: previously completed sections from earlier tiers
- `equation_map`: pre-extracted, real equation entries (map_key, latex, explanation, variables_json) — every formula is verbatim from the source, never invented
- `algorithm_map`: pre-extracted, real algorithm entries (map_key, name, pseudocode, complexity) — only algorithms that exist in the analysis documentation

## Task
Write the `methodology` section of the paper, grounding every claim in the analysis docs or implementation evidence provided.

## Guide Constraints
Follow Writing Guide §4 reproducibility requirements:
- Every algorithm must be named and referenced — cite from `algorithm_map` by `map_key` (e.g. "the Chunk-Parse-Monitor pipeline (ALG-1)"), resolved to display number at assembly time
- Every equation should be cited from `equation_map` by `map_key` (e.g. "the chunking function (EQ-1)"), resolved to display number at assembly time
- Parameters must be listed with values or ranges
- Dataset characteristics must be stated (size, features, train/test split)
- Evaluation metrics must be defined with formulas
- Computational environment must be described

Mathematics formatting (Mathematics/01):
- Use `$inline$` for inline equations, `$$display$$` for display equations
- Number equations sequentially: (1), (2), etc.
- Define all variables on first use

## Rules
1. Cite evidence — every factual claim must reference a source from the **input documentation only** using `[evidence: source]` markers (e.g. `[evidence: docs/architecture.md]`). These are internal grounding markers extracted during the citations pass and stripped before final rendering.
2. Use academic tone — formal language, third person, hedged claims
3. Follow the domain's documentation-standards (from the concrete system)
4. Include proper structure — headings, logical flow, transitions between sections
5. Flag uncertain claims — if evidence is ambiguous, note it with `[NEEDS VERIFICATION]`
6. **Never invent facts not present in the evidence.** Formulas, parameter
   values, algorithm names, and architecture claims must appear (verbatim
   or as direct paraphrase) in the provided `analysis_docs`/`documentation`.
   Do not fill gaps with plausible-sounding values from general knowledge
   of what a typical system in this area uses.

## Output Format
`templates/generation/markdown/methodology.md` has four scalar slots and two
list slots (equation_map/algorithm_map, pre-populated from extraction).
Use these headings **exactly** for the scalar slots (they snake-case to
the template's keys) — a heading the template doesn't expect is silently
dropped at assembly time:

- **Proposed Method**: the core method/algorithm, named and described
- **Architecture**: system architecture/design, including design rationale
  (use plain "Architecture" as the heading — the template's own H2 label is
  "Architecture / Design" but its placeholder key is `architecture`; a "/"
  in your heading would snake-case to a key that doesn't match)
- **Parameters and Settings**: parameter names, values/ranges, and
  justifications as a paragraph (the template renders this as a scalar
  `{{ parameters }}`, not a structured list — write a prose paragraph or
  inline table, don't try to emit a list the persistence pipeline can't
  capture)
- **Implementation Details**: concrete implementation specifics (stack, config, deployment)

The `equation_map` and `algorithm_map` loops (template's
`{{#equation_map}}`/`{{#algorithm_map}}`) are pre-populated from the
extraction tier — each row's `latex` and `explanation` (equations) and
`name`, `complexity`, `pseudocode` (algorithms) render automatically.
Reference them by `map_key` in your prose (e.g. "the chunking function
(EQ-1)"), the display number is resolved at assembly time.

Return a JSON object:
```json
{
  "sections": [
    {"heading": "Proposed Method", "text": "..."},
    {"heading": "Architecture", "text": "..."},
    {"heading": "Implementation Details", "text": "..."}
  ],
  "citations_used": ["source1", "source2"],
  "needs_verification": ["claim1"]
}
```
