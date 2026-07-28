# 11. Figures

**Domain:** `figures`
**Audit Target:** The whole document — cross-cutting, new for PCEMS 2026
(no `base_academic` precedent). Figures appear in `findings` (performance
charts, results visualizations) and `methodology` (block diagrams,
architecture figures), but the craft rules apply document-wide. Content is
appended as a labeled sub-block at the end of `findings` — placement
defined by `assemble-final-document.py`'s `CROSS_CUTTING_TARGETS`.

## Standard Definition

Figures communicate technical information that cannot be explained more
effectively using text alone. For PCEMS 2026, the mandatory rules from
`guide/Figures/01-figure-standards.md` are: figures must appear immediately
after their first reference (not collected at the end), have captions below
the figure in Arial, be legible when printed in grayscale (reviewers may
print in black and white), and meet minimum resolution (300 DPI for
photographs, 600 DPI for line art). Seven figure types are defined in
`guide/Figures/02-figure-types.md`: Block Diagram, Performance Bar Chart,
Line Graph, Confusion Matrix Heatmap, Flowchart, ROC/PR Curve, and Box
Plot.

### Expected Evidence (Deterministic)

1. **Every figure is referenced in the text** before it appears.
2. **Every figure is placed immediately after its first reference** — not
   collected at the end of the manuscript.
3. **Every figure has a caption** below it, numbered sequentially
   (Fig. 1., Fig. 2., etc.).
4. **All axes are labeled** with units in parentheses where applicable.
5. **Figures are legible in grayscale** — no reliance solely on color to
   convey meaning.
6. **No placeholder text:** no `TODO`, `[Figure]`, `XXX`, or similar
   unfilled markers.

### Semantic Judgment Criteria

- Does each figure's type match the information being communicated (e.g.
  Block Diagram for architecture, Bar Chart for categorical comparison,
  Line Graph for trends)?
- Are distinct data series distinguishable in grayscale (different line
  styles, patterns, or markers)?
- Do figures communicate information not better conveyed by text (no
  decorative images)?
- Is figure numbering sequential throughout the paper?
- Are error bars or confidence intervals included when standard deviation
  data is available?
