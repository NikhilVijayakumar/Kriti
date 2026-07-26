# 10. Tables

**Domain:** `tables`
**Audit Target:** The whole document — cross-cutting, new for PCEMS 2026
(no `base_academic` precedent). Tables appear in `findings` (comparison
tables, results tables) and sometimes `methodology` (configuration
parameters), but the craft rules apply document-wide: every table must be
created using Microsoft Word table tools, have a caption above it, clear
header labels, and units in column headers.

## Standard Definition

Tables organize factual information for comparison and analysis. For PCEMS
2026, the mandatory rules from `guide/Tables/01-table-standards.md` are:
tables must be created using Word table tools (not inserted as images),
placed immediately after their first reference, have captions above the
table in Arial bold, header rows with descriptive labels and units, and
consistent decimal places within each column. Six table types are defined
in `guide/Tables/02-table-types.md`: Performance Comparison, Dataset
Description, Configuration/Parameters, Results Across Conditions,
Qualitative Comparison, and Feature Description.

### Expected Evidence (Deterministic)

1. **Every table is created using Word table tools** — not an image of a
   table. Mechanically checkable: tables inserted as images lack the
   structural markup of real Word tables.
2. **Every table has a caption** above it, numbered sequentially (Table I.,
   Table II., etc.).
3. **Every table is referenced in the text** before it appears.
4. **Every table is placed immediately after its first reference** — not
   collected at the end of the manuscript.
5. **Header rows have descriptive labels** with units specified in column
   headers (e.g. "Accuracy (%)", "Time (ms)").
6. **No placeholder text:** no `TODO`, `[Table]`, `XXX`, or similar
   unfilled markers.

### Semantic Judgment Criteria

- Does each table's type match the information being presented (e.g.
  Performance Comparison for method-vs-metric data, Configuration for
  parameter listings)?
- Are decimal places consistent within each column?
- Is the proposed method highlighted (bold or first row) in comparison
  tables?
- Are empty cells handled consistently (use "—" if data is unavailable)?
- Is the table text legible at the final print size (minimum 8pt)?
