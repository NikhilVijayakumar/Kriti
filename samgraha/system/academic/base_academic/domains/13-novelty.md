# 13. Novelty

**Domain:** `novelty`
**Audit Target:** The whole document — this is a cross-cutting domain, not
confined to one section (see `templates/generation/document/
_master-schema.yaml`'s `cross_cutting:` list). Its content is woven into
`introduction` (contributions), `methodology` (design novelty), and
`discussion` (comparative positioning) rather than rendered as its own
heading.

## Standard Definition

Every genuine novelty claim needs a specific, falsifiable differentiation
from prior work — not an assertion that the system is "novel." The working
precedent for this domain's evidence shape is
`Bodha/docs/paper/*/cross_module/novelty.md`: each claim states what's
different, cites the specific code/design artifact that embodies the
difference, and explicitly contrasts against named alternatives (not "prior
work" in the abstract).

### Expected Evidence (Deterministic)

1. **Every novelty claim has a differentiation target** — a named
   alternative, technique, or system it's being contrasted against,
   mechanically checkable as "does this sentence contain both a claim verb
   ('propose', 'introduce', 'differs from') and a named comparison."
2. **No unqualified superlatives without an accompanying claim** — "novel,"
   "first," "unprecedented" used without a nearby specific differentiation
   statement is flaggable.

### Semantic Judgment Criteria

- Is each claimed novelty genuinely at the system/method level, or is it a
  novel *combination* of existing techniques being oversold as a wholly new
  technique?
- Does the methodology section's actual described approach support the
  novelty claim, or does the claim outrun what's actually described?
- Is the novelty claim's scope accurate — claimed as a system-level
  innovation when it's actually confined to one module/component, or vice
  versa?
