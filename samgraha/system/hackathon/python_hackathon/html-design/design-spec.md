# Design Spec — python_hackathon HTML Report System

## What this is

A scoring/audit report system for a Python hackathon competition. Each
competing team's repository gets audited across 10 technical domains
(infrastructure, engineering, testing, documentation, security, mlops,
runtime, team-workflow, data-quality, ai-explanations), each domain
scored 0-100 via a deterministic rule-checker (60%) + semantic LLM
judgment averaged across multiple models (40%), then adjusted with a
per-domain z-score bonus/penalty (rewarding standout performance
relative to the field), aggregated into one weighted score out of 100,
then rescaled to a final /20 leaderboard score.

This is **not** a marketing site or consumer product — it's a
precision instrument for judges and competitors to read exact numbers,
which rule passed/failed and why, and where a team stands relative to
everyone else. Read like a CI dashboard or an academic scoring rubric,
not like a landing page.

## Audience & distribution (confirmed)

- **Teams**: each team gets their own complete report (all 10 domains'
  breakdown, their own scores/bonuses/penalties) — this becomes a
  single per-team PDF (multi-page HTML → PDF merge).
- **Judges/organizers**: receive every team's report separately (the
  same per-team artifact, once per team) — not a special aggregated
  organizer view beyond the leaderboard.
- **Leaderboard**: one shared page/report, visible to everyone —
  final rankings + all 10 domains' scores per team + the relative
  scoring stats (global mean/stdev per domain, z-scores, bonuses).

## Page architecture (confirmed: standalone page per template)

Per team, one HTML page per (domain × audit-kind) — 10 domains ×
{deterministic, semantic, summary} = 30 pages — plus one
team-final-summary page (31 pages/team), all merged into one PDF per
team via a deck-style multi-page → PDF pipeline. Plus one shared
global-leaderboard page (not duplicated per team).

**This round's representative pages** (per the "show 2 pages before
batching 31" rule for large decks): one domain-level deep-dive page
(`{domain}-summary`, the richest single-domain template — combines
deterministic score, semantic score, z-score/bonus, and narrative) and
the `global-leaderboard` page (the cross-team comparison view). These
two stress-test the two fundamentally different data shapes in this
system: "one team, one domain, in depth" vs. "all teams, all domains,
compressed."

## Exact data contract — every field must be represented

Pulled directly from the existing markdown templates
(`templates/reports/domain/01-infrastructure-summary.md` and
`templates/reports/global-leaderboard.md`) — these are binding, not
suggestions. The HTML is a second rendering of the same data, richer
presentation, but **nothing here may be silently dropped**.

### `{domain}-summary` page fields
- `repo_name`, `evaluation_date`
- `scores.deterministic`, `scores.semantic`, `scores.raw_merge` (the
  0.60/0.40 weighted merge)
- `global_stats.mean`, `global_stats.stdev` (this domain, across all
  teams)
- `team_stats.z_score`, `team_stats.relative_bonus` (this team's
  standing vs. the field)
- `scores.final_domain_score` (the number that actually counts toward
  the leaderboard)
- **Additional, beyond markdown** (this is what earns the HTML over
  the .md): a chart showing this team's score against the field
  distribution for this domain, and the agent-written narrative
  (`standard_narratives` — 2+ sections: "Summary", "Key Risks" or
  similar, full text, not the one-paragraph markdown gets)

### `global-leaderboard` page fields
- `report_date`, `total_teams`
- Ranked table: `rank`, `repo_name`/team name, `final_score`/20, and
  all 10 domains' individual scores per team (Infra/Eng/Test/Doc/
  Sec/MLOps/Run/T-W/D-Q/AI-Expl — abbreviated column headers, full
  names on hover/legend)
- `global_stats.{domain}.{mean, stdev}` for all 10 domains
- **Additional, beyond markdown**: rank-change/distribution
  visualization (score spread per domain — where does this team sit
  in the pack), and the competition-wide agent narrative.

## Sample data (Placeholder > bad implementation)

No hackathon has run yet — no real scores exist. Use clearly-labeled,
internally-consistent **realistic sample numbers** (e.g. a team
scoring 71.5 in infrastructure with a +3.2 z-score bonus, a leaderboard
of 6-8 sample teams with a real score spread) — not Lorem Ipsum, not
zeros. Realistic enough that a judge looking at it understands exactly
what the real thing will show.

## Tone / visual temperature

Precision, not excitement. Technical credibility over polish-for-its-
-own-sake. Numbers must be scannable and comparable at a glance — this
is closer to a stock terminal or a CI results page than a product
page. Whatever visual direction, tabular numerals for all scores,
strict alignment, no decorative elements that don't carry information
(§5 "data slop" ban applies directly — no icons/gradients that aren't
load-bearing).

## Constraints

- Pure HTML/CSS, no build step (single-file per page, later merged
  into a deck for PDF export).
- No brand/logo to match — confirmed, from-scratch internal tool.
- Charts: pure CSS/SVG for this demo round (matplotlib PNGs will
  replace them in the real system, but the layout must reserve space
  and treat them identically regardless of source).
