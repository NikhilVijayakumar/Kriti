# 04. Findings

**Domain:** `findings`
**Audit Target:** The generated findings section.

## Standard Definition

The Findings section presents the experimental results with strict emphasis
on correct table and media formatting. For PCEMS 2026, this absorbs what
`base_academic` splits into `experimental-setup` + `results` + `discussion`
— the three subsections (Experimental Setup, Results Presentation, Analysis)
all live inside one section. Every table must be created using Microsoft Word
table tools (not inserted as images), every figure must appear immediately
after its first reference, and results must be presented objectively before
interpretation.

### Expected Evidence (Deterministic)

1. **Word count within range:** 600–1,200 words (per `Writing Guide/
   05-findings.md`, target 800–1,000).
2. **Tables present:** at least 1 table (per sample paper analysis: average
   of 2.5). Detectable via `contains_table` or table-reference check.
3. **Figures present:** at least 1 figure (per sample paper analysis:
   average of 2.8). Detectable via `contains_figure` or figure-reference
   check.
4. **Comparison with baselines:** at least 1 comparison table or figure
   (per `Checklists/02-per-domain.md`: "at least 3 baseline methods
   compared", "multiple metrics reported").
5. **No placeholder text:** no `TODO`, `[Table]`, `[Figure]`, `XXX`, or
   similar unfilled markers.
6. **Citation markers present:** at least 1 citation (dataset or baseline
   method reference).

### Semantic Judgment Criteria

- Is the experimental setup described with enough detail for reproduction
  (dataset source, size, features, train/test split, metrics, hardware)?
- Are results presented objectively in the Results subsection, with
  interpretation reserved for the Analysis subsection?
- Does every table have a caption above it, clear header labels, units in
  column headers, and consistent decimal places?
- Does every figure have a caption below it, is placed immediately after
  its first text reference, and is legible in grayscale?
- Are tables created using Word table tools (not images of tables)?
- Is the comparison with existing methods fair and comprehensive (at least
  3 baselines, multiple metrics)?
