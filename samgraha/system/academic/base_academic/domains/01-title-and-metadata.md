# 01. Title and Metadata

**Domain:** `title-and-metadata`
**Audit Target:** The generated title, author/affiliation block, keyword
list, and venue-formatting metadata for the paper draft.

## Standard Definition

The title and metadata are the paper's first (often only) point of contact
with a reader deciding whether to continue — a title that's vague,
overlong, or keyword-stuffed undercuts everything drafted after it. This
domain also carries whatever mechanical formatting a submission target
imposes (margins, font, page limits) that doesn't belong inside any
content section.

### Expected Evidence (Deterministic)

1. **Title length:** falls within a reasonable range for the target venue
   (a concrete system sets its own bound; flag titles that are a single
   noun phrase with no specificity, or a full sentence).
2. **Keyword list present:** a keyword/index-terms list exists, is neither
   empty nor a copy of the title's own words verbatim.
3. **Author/affiliation block present:** exists, is non-empty, matches
   whatever structural template the concrete system's format expects
   (single-blind, double-blind-anonymized, etc.).
4. **No placeholder text:** no `TODO`, `[Author Name]`, `XXX`, or similar
   unfilled template markers remain.

### Semantic Judgment Criteria

- Does the title specifically name the technique/system/contribution
  rather than describing the general problem area only?
- Do the keywords actually reflect the paper's content, not generic
  field-level terms only?
- Is the title free of unsupported superlatives ("novel," "first,"
  "groundbreaking") that the paper's own contributions section doesn't
  substantiate?
