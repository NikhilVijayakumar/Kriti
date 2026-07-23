# 15. Mathematics

**Domain:** `mathematics`
**Audit Target:** The whole document — cross-cutting, same as `novelty`
(§13) and `gaps` (§14). Content lives primarily in `problem-definition`
(formal statement) and `methodology` (derivations, complexity), audited
here as its own domain because mathematical rigor is a distinct failure
mode from either section's structural completeness.

## Standard Definition

Every formula, equation, or algorithm appearing anywhere in the document
must be (a) correctly notated, (b) explained — not left to stand alone —
and (c) accompanied by a stated complexity/scalability characterization
where it describes a computational procedure. The working precedent for
depth is `Bodha/docs/paper/*/{modules,cross_module}/mathematics.md` —
formal notation ($\LaTeX$), a stated "why this formulation" rationale, and
explicit complexity bounds are all present per formula, not just the
formula itself.

### Expected Evidence (Deterministic)

1. **Every symbol used in an equation is defined** before or at first use
   — cross-checkable against a symbol-definition list, same mechanism as
   `problem-definition`'s notation-table check.
2. **Every equation is followed by explanatory prose** — an equation block
   with no adjacent sentence referencing it is flaggable.
3. **Complexity notation present** (Big-O or equivalent) for every
   described algorithmic procedure — mechanically detectable as "does an
   algorithm/pseudocode block exist with no accompanying complexity
   statement anywhere in the section."

### Semantic Judgment Criteria

- Is the "why this formulation" reasoning genuine — does it justify this
  specific approach over an alternative — or is it a mechanical restatement
  of what the formula computes (the exact "mechanical vs. intuitive"
  distinction `ai-evaluation-prompt.md`'s Pass 1 forensic audit already
  checks for at the sentence level)?
- Is the stated complexity bound actually correct given the described
  algorithm, or does the algorithm as described imply a different bound
  than the one claimed?
- Are statistical claims (significance tests, confidence intervals)
  mathematically sound — correct test choice for the data shape, not just
  present?
