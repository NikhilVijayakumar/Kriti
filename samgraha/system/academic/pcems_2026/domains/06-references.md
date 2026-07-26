# 06. References

**Domain:** `references`
**Audit Target:** The generated reference list.

## Standard Definition

The References section provides complete bibliographic information for every
source cited in the paper. For PCEMS 2026, analysis of accepted sample
papers shows IEEE numbered style ([1], [2], [3]…) is used in practice despite
the template mentioning APA. Two axes matter: **formatting** (citation style
consistency, font compliance) and **quality/distribution** (recency mix,
source legitimacy). Every in-text citation must resolve to an entry, and
every entry must be cited at least once.

### Expected Evidence (Deterministic)

1. **Citation style internally consistent:** every entry follows the same
   format (numbered, same punctuation, same author formatting), mechanically
   checkable via per-entry pattern match.
2. **Reference count meets range:** 15–30 references (target 20–25; sample
   paper analysis of 11 PCEMS papers shows range 13–47, average 24.2).
   `calculation/generation/references.yaml` enforces min 15, max 30.
3. **Every entry has required fields:** author, year, title, venue — no
   truncated or placeholder entries.
4. **Two-way cross-reference check:** every in-text citation marker resolves
   to an entry in this list, and every entry is cited at least once.
5. **No placeholder text:** no `TODO`, `[Citation]`, `XXX`, or similar
   unfilled markers.
6. **Recency mix:** at least 50% of references from the last 5 years (per
   `Writing Guide/07-references.md`).

### Semantic Judgment Criteria

- Are any entries from blogs, non-peer-reviewed sources, or predatory
  venues?
- Do citations to the same underlying prior work stay consistent across
  the paper (not cited as two different entries due to a name/year
  mismatch)?
- Is the reference count appropriate for the paper's scope (not too few
   for a full research paper, not excessive)?
- Are DOIs included where available?
