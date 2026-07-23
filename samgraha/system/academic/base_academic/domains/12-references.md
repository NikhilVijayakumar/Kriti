# 12. References

**Domain:** `references`
**Audit Target:** The generated reference list.

## Standard Definition

Two genuinely separate axes, confirmed distinct by the archived
`base_academic-proposal.md` §2 finding: **formatting** (citation style,
font/typography where the venue mandates it) and **quality/distribution**
(recency mix, foundational-classics share, venue-tier bar). A concrete
system may weight these very differently — `pcems_2026`'s bar is
format-only, `eswa_journal`'s is quality/distribution-only with no style
requirement at all. This file audits both axes generically; a concrete
system's own override determines which axis actually gets enforced.

### Expected Evidence (Deterministic)

1. **Citation style is internally consistent** — every entry follows the
   same format (author-year vs numbered, punctuation, italics convention),
   mechanically checkable via a per-entry pattern match.
2. **Reference count meets the concrete system's configured range.**
3. **Every entry has all required fields** (author, year, title, venue) —
   no truncated or placeholder entries.
4. **Every in-text citation marker resolves to an entry in this list, and
   every entry in this list is cited at least once** — a two-way
   cross-reference check against every other domain's text.
5. **Recency/distribution mix meets the concrete system's configured
   percentages**, if it sets any.

### Semantic Judgment Criteria

- Are any entries from blogs, non-peer-reviewed sources, or predatory
  venues? (Detecting "predatory" requires judgment — a known-list check is
  deterministic, an unfamiliar venue's legitimacy is not.)
- Do citations to the same underlying prior work stay consistent across
  the paper (not cited as two different entries due to a name/year
  mismatch)?
