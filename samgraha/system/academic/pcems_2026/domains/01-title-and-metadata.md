# 01. Title and Metadata

**Domain:** `title-and-metadata`
**Audit Target:** The generated title, author/affiliation block, keyword
list, and venue-formatting metadata for the paper draft.

## Standard Definition

The title and metadata are the paper's first (often only) point of contact
with a reviewer or reader deciding whether to continue. For PCEMS 2026, the
metadata block follows a strict format: title, authors with superscript
institution numbers, affiliations, corresponding-author email, and keywords.
The title must communicate what the paper does, not what the paper is about —
a title that's vague, overlong, or keyword-stuffed undercuts everything
drafted after it. This domain also carries whatever mechanical formatting
the PCEMS template imposes (Arial fonts at prescribed sizes, single-column
layout, Roman-numeral section numbering).

### Expected Evidence (Deterministic)

1. **Title length:** 10–15 words (per `Writing Guide/02-title-and-metadata.md`).
   Flag titles that are a single noun phrase with no specificity, a full
   sentence, or exceed 20 words.
2. **Keyword list present:** 4–6 keywords (per `Writing Guide/02-title-and-
   metadata.md`). Neither empty nor a copy of the title's own words verbatim.
3. **Author/affiliation block present:** exists, is non-empty, matches the
   PCEMS template format (superscript institution numbers linking authors to
   affiliations).
4. **No placeholder text:** no `TODO`, `[Author Name]`, `XXX`, or similar
   unfilled template markers remain.
5. **Font compliance:** title is Arial 14pt bold centered, authors Arial 12pt
   bold centered, affiliations Arial 11pt centered (per `Conference
   Guidelines/03-formatting-guidelines.md`).

### Semantic Judgment Criteria

- Does the title specifically name the technique/system/contribution
  (e.g. "Credit Card Fraud Detection Using Random Forest Classification")
  rather than describing the general problem area only (e.g. "A Study on
  Machine Learning")?
- Do the keywords actually reflect the paper's content — identifying the
  domain, the method, and the application — not generic field-level terms
  only?
- Is the title free of unsupported superlatives ("novel," "first,"
  "groundbreaking") that the paper's own contributions section doesn't
  substantiate?
- Are author names in the correct format (First Last, not initials unless
  field convention) with matching superscript institution numbers?
