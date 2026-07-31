# 09. Mathematics

**Domain:** `mathematics`
**Audit Target:** The whole document — cross-cutting, same as `novelty`
(§07) and `gaps` (§08). Content is appended as a labeled sub-block at the
end of `methodology` (derivations, complexity, equations) — placement
defined by `assemble-final-document.py`'s `CROSS_CUTTING_TARGETS`.
Audited here as its own domain because mathematical rigor is a distinct
failure mode from either section's structural completeness.

## Standard Definition

Every formula, equation, or algorithm appearing anywhere in the document
must be (a) correctly notated, (b) explained — not left to stand alone —
and (c) accompanied by a stated complexity/scalability characterization
where it describes a computational procedure. For PCEMS 2026, this follows
`base_academic/domains/15-mathematics.md` with PCEMS-specific notation
rules layered on top (per `guide/Mathematics/01-equation-formatting.md`
and `02-notation-conventions.md`: equations numbered sequentially, all
variables defined at first use, consistent notation throughout).

### Extraction Source

Equations and algorithms are extracted from `docs/paper/Bodha/cross_module/mathematics.md` into `academic_equation_map` and `academic_algorithm_map` before methodology generation — the generation prompt receives structured map entries (latex, pseudocode, complexity, variable definitions) rather than raw markdown, so it can cite them by stable `map_key` (EQ-1, ALG-1) without re-extracting or inventing formulas.

### Expected Evidence (Deterministic)

1. **Every symbol used in an equation is defined** before or at first use
   — cross-checkable against a symbol-definition list.
2. **Every equation is followed by explanatory prose** — an equation block
   with no adjacent sentence referencing it is flaggable.
3. **Complexity notation present** (Big-O or equivalent) for every
   described algorithmic procedure — mechanically detectable as "does an
   algorithm/pseudocode block exist with no accompanying complexity
   statement anywhere in the section."
4. **No placeholder text:** no `TODO`, `XXX`, or similar unfilled markers.

### Semantic Judgment Criteria

- Is the "why this formulation" reasoning genuine — does it justify this
  specific approach over an alternative — or is it a mechanical restatement
  of what the formula computes?
- Is the stated complexity bound actually correct given the described
  algorithm, or does the algorithm as described imply a different bound
  than the one claimed?
- Are statistical claims (significance tests, confidence intervals)
  mathematically sound — correct test choice for the data shape, not just
  present?
- Is notation consistent throughout the paper (same variable name for the
  same concept, no ambiguous symbols)?
