# 14. Gaps

**Domain:** `gaps`
**Audit Target:** The whole document — cross-cutting, same as `novelty`
(§13). Content is woven into `limitations` (research/scope gaps),
`discussion` (threats to validity), and informs what `related-work`'s
closing bridge names as unresolved.

## Standard Definition

Distinct from `limitations` (§10): `limitations` is what the *current
work* doesn't handle; `gaps` is what the *research area* doesn't yet
have an answer for, independent of whether this paper closes it. The
working precedent is `Bodha/docs/paper/*/cross_module/gaps.md` — each gap
is severity-tagged, has a stated research impact, and (where applicable) a
remediation direction, not just "more work needed here."

### Expected Evidence (Deterministic)

1. **Every gap has a severity tag** (or equivalent structured marker —
   HIGH/MEDIUM/LOW or the concrete system's own scale).
2. **Every gap is distinguishable from a `limitations` entry** — a
   mechanical check can flag exact-duplicate sentences appearing in both
   domains' output as a structural error (the same content shouldn't be
   generated twice under two different framings).

### Semantic Judgment Criteria

- Is each named gap real (would a domain expert recognize it as an open
  problem), or a restatement of this paper's own limitation dressed up as
  a field-wide gap?
- Does `related-work`'s closing bridge sentence actually correspond to one
  of the gaps named here, or do the two disagree about what's unresolved?
- Are severity tags calibrated consistently — is a HIGH-tagged gap
  actually more consequential than a MEDIUM-tagged one, not just labeled
  that way for emphasis?
