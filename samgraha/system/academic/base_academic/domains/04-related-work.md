# 04. Related Work

**Domain:** `related-work`
**Audit Target:** The generated related-work section.

## Standard Definition

Related work positions this paper against prior approaches, grouped into a
structured taxonomy — not a chronological or alphabetical list of papers
with one sentence each. It ends with an explicit narrative bridge into why
none of the surveyed approaches solve this paper's problem, which is what
actually motivates the work rather than restating the introduction's gap.

### Expected Evidence (Deterministic)

1. **Taxonomy structure present:** prior work is grouped under named
   categories (subheadings or clearly labeled clusters), not one flat
   list.
2. **Citation coverage:** a minimum citation count and recency mix exists
   (exact numbers are venue-specific, set by the concrete system —
   this domain checks that *some* threshold is enforced, not what it is).
3. **Every citation used in this section appears in the references list**
   — a direct cross-reference check against the `references` domain's
   output, fully mechanical.
4. **Closing bridge sentence present:** the section ends with an explicit
   "none of the above address X" (or equivalent) statement, locatable by
   its position (last paragraph) and content (contrast language).

### Semantic Judgment Criteria

- Are the taxonomy categories genuinely distinct, or just relabeled
  synonyms of each other?
- Does the closing gap statement match the introduction's stated gap, or
  contradict/diverge from it?
- Are sources credible — no blog posts, no non-peer-reviewed URLs, no
  citations to predatory or low-credibility venues (the concrete system's
  quality bar sets the exact venue-tier requirement; this criterion flags
  obvious violations regardless of tier).
