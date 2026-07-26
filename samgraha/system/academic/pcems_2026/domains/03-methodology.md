# 03. Methodology

**Domain:** `methodology`
**Audit Target:** The generated methodology section.

## Standard Definition

The Methodology section describes how the proposed solution works. It must
provide sufficient detail for another researcher to understand, evaluate, and
reproduce the approach. For PCEMS 2026, this means a systematic description
pattern: overview → components → process → implementation details. A block
diagram (Figure) illustrating the architecture is expected in 9 of 11 sample
papers. Equations must be numbered, variables defined at first use, and every
formula followed by explanatory prose.

### Expected Evidence (Deterministic)

1. **Word count within range:** 600–1,200 words (per `Writing Guide/
   04-methodology.md`, target 800–1,000).
2. **Diagram present:** at least 1 block diagram or architecture figure
   (per sample paper analysis: 9 of 11 include one). Detectable via
   `contains_mermaid_diagram` or figure-reference check.
3. **Equations present:** at least 1 numbered equation (per sample paper
   analysis: 7 of 11 include at least one). Detectable via
   `contains_equation`.
4. **Implementation details present:** tools, libraries, or frameworks
   mentioned (per sample paper analysis: 8 of 11 specify these).
5. **No placeholder text:** no `TODO`, `[Figure]`, `XXX`, or similar
   unfilled markers.
6. **Citation markers present:** at least 1 citation (methodology references
   prior work or tools).

### Semantic Judgment Criteria

- Is each design/heuristic choice justified (why this threshold, why this
  architecture over an alternative), or asserted without reasoning?
- Does the pseudocode/algorithm actually match what the prose describes,
  or diverge in a way that would make the described approach
  unreproducible?
- Are all variables defined at first use, with consistent notation
  throughout the section?
- If the methodology reuses or extends an existing technique, is the
  extension's novelty specifically identified, not blended
  indistinguishably into the description of the base technique?
- Is the block diagram referenced in the text and placed immediately after
  its first reference?
