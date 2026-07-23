# 10. Limitations

**Domain:** `limitations`
**Audit Target:** The generated limitations section.

## Standard Definition

An honest account of where the approach doesn't hold: scalability limits,
domain constraints, data dependency, and ethical considerations where
applicable. A concrete system without a dedicated `limitations` domain
(matching the archived `base_academic-proposal.md` §2 finding about
`pcems_2026`, which folds this content into `conclusion` instead) skips
this file entirely rather than leaving it empty — do not force a thin
`limitations` section into a system that structurally routes this content
elsewhere.

**Future-work content belongs here, not in `conclusion`**, for any
concrete system that has this domain — this is the resolution point for
the contradiction the archived proposal flagged (`pcems_2026`'s
`conclusion` domain explicitly requests future work because it has nowhere
else to put it; `eswa_journal`'s `conclusion` domain explicitly forbids it
because `limitations` exists to hold it). This file only applies to
systems in the second category.

### Expected Evidence (Deterministic)

1. **At least one limitation named per category** the concrete system
   requires (scalability, domain constraints, data dependency — ethical
   considerations only where the methodology involves human subjects,
   sensitive data, or dual-use-risk applications).
2. **No new results or claims introduced** — mechanically flaggable if a
   number appears here that doesn't also appear in `results`.

### Semantic Judgment Criteria

- Are the stated limitations genuine (would a critical reviewer actually
  raise them), or token acknowledgments that don't meaningfully constrain
  the paper's claims?
- Is there a limitation the methodology or experimental-setup sections'
  own content implies but this section omits (e.g., a single-dataset
  evaluation with no generalizability limitation stated)?
