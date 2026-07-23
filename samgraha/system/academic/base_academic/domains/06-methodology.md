# 06. Methodology

**Domain:** `methodology`
**Audit Target:** The generated methodology section.

## Standard Definition

The core-innovation section: a step-by-step, reproducible account of the
proposed approach, grounded mathematically/statistically where applicable,
with its computational complexity characterized and its design choices
justified rather than merely stated. This is the section reviewers scrutinize
hardest for rigor — depth requirements here are the single biggest lever a
concrete system has for distinguishing a conference-paper bar from a
Q1-journal bar (see the archived `base_academic-proposal.md` §2 finding:
`pcems_2026`'s methodology bar and `eswa_journal`'s are genuinely,
deliberately different depths, not a shared baseline this domain file
overrides).

### Expected Evidence (Deterministic)

1. **Pseudocode or algorithm block present** for the core procedure.
2. **A diagram exists** (architecture, flowchart, or pipeline — see
   `docs/mermaid-diagram-standards.md`) illustrating the approach's
   structure, not just prose describing it.
3. **Complexity analysis present:** at minimum, a stated time complexity
   (Big-O or equivalent); space complexity and scalability discussion are
   concrete-system-configurable requirements on top of this floor.
4. **Every formula/equation is followed by prose**, not left to stand
   alone with no explanation of what it computes or why.

### Semantic Judgment Criteria

- Is each design/heuristic choice justified (why this threshold, why this
  architecture over an alternative), or asserted without reasoning?
- Does the pseudocode/algorithm actually match what the prose describes,
  or diverge in a way that would make the described approach
  unreproducible?
- If the methodology reuses or extends an existing technique, is the
  extension's novelty specifically identified (feeds `novelty`, §14), not
  blended indistinguishably into the description of the base technique?
