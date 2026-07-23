# 05. Problem Definition

**Domain:** `problem-definition`
**Audit Target:** The generated problem-definition section.

## Standard Definition

A formal statement of the problem this paper solves: inputs, outputs,
constraints, and assumptions, precise enough that a reader could restate
the problem without reference to the rest of the paper. Where the problem
is optimization-, classification-, or regression-shaped, a formal
objective/formulation belongs here, not deferred to the methodology
section.

### Expected Evidence (Deterministic)

1. **Symbol/notation table or inline definitions present** if the section
   uses mathematical notation anywhere — every symbol used must be
   defined at least once before or at first use.
2. **Assumptions explicitly listed**, not left implicit inside prose.
3. **If the problem is formalizable** (optimization/classification/
   regression-shaped, detectable from whether the methodology section
   later reports a loss function or objective), a formal statement
   (equation or precise pseudo-formal description) is present here, not
   only in methodology.

### Semantic Judgment Criteria

- Is the formal definition actually precise, or dressed-up prose with
  symbols added?
- Do the stated assumptions match what the methodology and experimental
  setup sections later rely on, or does the paper silently assume
  something here doesn't hold there?
- Could a reader unfamiliar with this specific system reconstruct the
  problem's scope from this section alone?
