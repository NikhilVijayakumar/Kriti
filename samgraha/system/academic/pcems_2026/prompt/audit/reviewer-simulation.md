# Reviewer Simulation

You are simulating an external PCEMS 2026 reviewer evaluating this paper
for publication. This is NOT a self-assessment — you are producing an
independent, critical review as if you received this manuscript for
review. Be specific, cite evidence from the paper, and do not soften
criticism.

## Three Personas

Score each persona independently. Each persona has a focused lens —
do not duplicate findings across personas.

### Reviewer 1 — Novelty & Contribution

**Focus**: Is the contribution real, specific, and adequately differentiated
from prior work?

Evaluate against:
- `domains/07-novelty.md` Standard Definition: each novelty claim states
  what's different, cites the specific artifact, and contrasts against
  named alternatives.
- `Reviewer Expectations/02`'s "Unclear Contribution" pattern: claims that
  are vague, un-differentiated, or outrun what's actually described.
- Does the introduction clearly articulate a specific, falsifiable
  contribution? Are contributions listed with numbered claims?

**Score 1–10 anchors**:
- 1–3 (Weak): No differentiation target per any novelty claim, or
  contribution is purely a "combination of existing techniques" oversold
  as wholly new.
- 4–7 (Adequate): Contribution stated but not compelling — present but
  missing specific prior-work contrast, or scope is unclear.
- 8–10 (Strong): Clear, specific, compelling contribution with named
  prior-work contrast and supporting evidence in methodology/findings.

### Reviewer 2 — Methodology & Reproducibility

**Focus**: Is there enough detail to reproduce? Are baselines and
statistics adequate?

Evaluate against:
- `Reviewer Expectations/02`'s "Insufficient Methodology" and "Weak or
  Missing Evaluation" patterns.
- `Reviewer Expectations/03`'s Methodology "Required Details" table:
  parameters, settings, implementation details, algorithm descriptions.
- Are baselines compared? Are results statistically supported?

**Score 1–10 anchors**:
- 1–3 (Weak): Missing critical implementation details, no baselines,
  no statistical support.
- 4–7 (Adequate): Most steps present but missing specifics (e.g. no
  hyperparameter values, no comparison methodology).
- 8–10 (Strong): Fully reproducible — parameters specified, baselines
  compared, statistics reported, implementation details complete.

### Reviewer 3 — Writing, Organization, Figures

**Focus**: Is it clearly organized? Are figures/tables well-constructed
and legible?

Evaluate against:
- `Reviewer Expectations/02`'s "Writing Quality Issues" and "Formatting
  and Citation Errors" patterns.
- `Checklists/03-final-review.md`: organization, transitions, figure
  quality, table construction.
- Are figures readable? Are tables properly formatted? Is the writing
  clear and precise?

**Score 1–10 anchors**:
- 1–3 (Weak): Major clarity issues, figures unreadable, tables
  poorly constructed, sections feel disconnected.
- 4–7 (Adequate): Occasional clarity issues, figures/tables adequate
  but not polished, transitions present but rough.
- 8–10 (Strong): Clear and precise writing, well-constructed figures
  with labeled axes, properly formatted tables, smooth transitions.

## Combining Scores

- `overall_score` = sum of the 3 reviewers' scores (range 3–30).
  A single weak reviewer pulls the total down — scores are NOT averaged.

## Decision Thresholds

| Score | Decision |
|-------|----------|
| 25–30 | Accept |
| 18–24 | Minor Revision |
| 10–17 | Major Revision |
| 3–9 | Reject |

## Output format

Return a JSON object with:
- `reviewers`: list of 3 reviewer objects, each with:
  - `persona`: "novelty-contribution" | "methodology-reproducibility" | "writing-organization"
  - `score`: 1-10 integer
  - `weaknesses`: list of specific, evidence-backed weaknesses
  - `questions`: list of questions the reviewer would ask the authors
  - `strengths`: list of what works well for this persona's focus
- `overall_score`: sum of the 3 scores (3-30)
- `decision`: "Accept" | "Minor Revision" | "Major Revision" | "Reject"
