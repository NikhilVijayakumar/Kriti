# 08. Gaps

**Domain:** `gaps`
**Audit Target:** The whole document — cross-cutting, same as `novelty`
(§07). Content is appended as a labeled sub-block at the end of
`introduction` (gap identification) — placement defined by
`assemble-final-document.py`'s `CROSS_CUTTING_TARGETS`. For PCEMS 2026, this follows `base_academic/domains/14-gaps.md`
exactly: each gap is severity-tagged, has a stated research impact, and
(where applicable) a remediation direction.

## Standard Definition

Distinct from `conclusion`'s future work: `gaps` is what the *research
area* doesn't yet have an answer for, independent of whether this paper
closes it. `conclusion`'s future work is what *this paper* will do next.
Each gap must be severity-tagged (HIGH/MEDIUM/LOW) and distinguishable from
a limitations entry — the same content shouldn't appear under two different
framings.

### Expected Evidence (Deterministic)

1. **Every gap has a severity tag** (or equivalent structured marker —
   HIGH/MEDIUM/LOW or the concrete system's own scale).
2. **Every gap is distinguishable from a limitations entry** — a
   mechanical check can flag exact-duplicate sentences appearing in both
   domains' output as a structural error (the same content shouldn't be
   generated twice under two different framings).
3. **No placeholder text:** no `TODO`, `XXX`, or similar unfilled markers.

### Semantic Judgment Criteria

- Is each named gap real (would a domain expert recognize it as an open
  problem), or a restatement of this paper's own limitation dressed up as
  a field-wide gap?
- Does the introduction's gap statement actually correspond to one of the
  gaps named here, or do the two disagree about what's unresolved?
- Are severity tags calibrated consistently — is a HIGH-tagged gap
  actually more consequential than a MEDIUM-tagged one, not just labeled
  that way for emphasis?
