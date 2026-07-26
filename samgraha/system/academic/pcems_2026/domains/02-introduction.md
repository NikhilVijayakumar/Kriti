# 02. Introduction

**Domain:** `introduction`
**Audit Target:** The generated introduction section.

## Standard Definition

The Introduction establishes the context, identifies the gap, and states the
paper's contribution. It follows a funnel pattern: broad context → specific
gap → paper contribution. For PCEMS 2026, this means starting with the
engineering problem (statistics, prevalence, impact), narrowing to what
existing approaches fail to address, and ending with a numbered list of
contributions. The Introduction must not contain methodology details or
results — those belong in their own sections.

### Expected Evidence (Deterministic)

1. **Word count within range:** 400–800 words (per `Writing Guide/
   03-introduction.md`'s length guidelines, target 500–600).
2. **Contributions list present:** a contributions section with at least 2
   listed items (bulleted or numbered), detectable via regex for
   "contributions" or "we propose" or similar patterns.
3. **Citation markers present:** at least 5 in-text citations (per sample
   paper analysis: average of 10, range 5–15).
4. **No placeholder text:** no `TODO`, `[Citation]`, `XXX`, or similar
   unfilled markers.
5. **No methodology or results content:** the Introduction must not describe
   algorithms, equations, or present quantitative results.

### Semantic Judgment Criteria

- Does the problem context start with the engineering problem (not
  dictionary definitions or overly broad statements)?
- Is the gap specific and verifiable — would a reader be able to confirm
  it by reading the cited works — rather than a vague "existing work is
  insufficient"?
- Does the contribution statement directly address the identified gap,
  using explicit numbered contributions?
- Does the Introduction avoid introducing methodology details, results,
  or conclusions that belong in later sections?
