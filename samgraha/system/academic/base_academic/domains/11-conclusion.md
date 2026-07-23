# 11. Conclusion

**Domain:** `conclusion`
**Audit Target:** The generated conclusion section.

## Standard Definition

A concise close: restate the contribution, reinforce the empirical
validation, note practical impact. No new claims, no new citations, no new
data. Whether future work belongs here is **not** settled at the
base_academic level — see `limitations` (§10) for why: it depends on
whether the concrete system has a dedicated `limitations` domain to route
that content to instead. A concrete system's own `conclusion` rubric
overrides this file to state its own position explicitly; this file does
not pick a default.

### Expected Evidence (Deterministic)

1. **No citations appear in this section** — conclusions synthesize, they
   don't introduce new supporting evidence; a citation marker here is
   mechanically flaggable.
2. **No numeric result appears here that isn't already in `results`** —
   cross-reference check, same pattern as `discussion`'s and
   `limitations`' checks.
3. **Length is proportionate** — a conclusion longer than the introduction
   is a structural smell, mechanically comparable by word count.

### Semantic Judgment Criteria

- Does the restated contribution match what the introduction originally
  promised, or has scope drifted across the paper?
- Is the practical-impact statement specific to this work, or a generic
  closing sentence that could apply to any paper in the field?
- (System-specific, resolved by the concrete system's override, not
  audited generically here): does future-work content appear in the
  place the concrete system's own policy requires — inside `conclusion` if
  no `limitations` domain exists, or absent from `conclusion` if one does?
