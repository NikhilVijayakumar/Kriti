# 02. Abstract

**Domain:** `abstract`
**Audit Target:** The generated abstract section.

## Standard Definition

The abstract is a structured, self-contained summary — a reader who reads
nothing else should still understand the problem, the approach, the
headline result, and why it matters. It is not a teaser for the
introduction; every quantitative claim it makes must be traceable to a
number that also appears in the results section.

### Expected Evidence (Deterministic)

1. **Word count** falls within the concrete system's configured range
   (word-count bound is venue-specific — this domain only checks that a
   bound exists and is respected, not what the bound is).
2. **Single paragraph, no citations, no undefined acronyms** — abstracts
   conventionally carry none of these; flag any that slip in.
3. **Structural coverage:** the abstract's text touches, in some order,
   each of: problem statement, approach/method name, at least one
   quantitative result, and a closing significance/impact statement. A
   deterministic check can grep for the *presence* of a number and an
   approach-name mention; it cannot judge whether the coverage is any
   good — that's semantic.

### Semantic Judgment Criteria

- Does the stated problem match what the introduction later develops, or
  is the abstract describing a different (broader/narrower) problem?
- Is the headline number in the abstract the same number reported in
  results, not a rounded-up or cherry-picked variant?
- Is the significance statement specific to this paper's contribution, or
  a generic claim that could be pasted into any paper in the field?
