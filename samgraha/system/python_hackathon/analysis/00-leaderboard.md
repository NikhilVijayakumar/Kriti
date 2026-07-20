# Leaderboard Analysis Prompt

Guides the competition-wide summary analysis — read by whichever agent
runs it via MCP, after per-domain scoring has completed for all teams.
Produces the competition overview narrative. Not parsed by a script —
this is a prompt.

## Version
1.0.0

## Analysis Intent
The Leaderboard Analysis answers: "across all N teams, what separated
the top from the bottom, what's the common failure mode, and where
should a team focus to climb?" This step reads every team's aggregate
scores and domain breakdowns, then writes a narrative a judge or
participant can scan in 60 seconds.

## Inputs
- `standard_domain_scores` DB table — all teams, all domains, all
  scores (queried via MCP: `samgraha_search` or direct DB access)
- Per-team aggregate scores (from `score_aggregator` output)
- Per-domain score distributions across all teams

## Narrative Guidance
The Leaderboard narrative must cover:
1. **Headline Standings** — top 3 teams with aggregate scores, and
   bottom 3 teams. Lead with the spread: top score minus bottom score.
2. **Separation Factors** — what domains most distinguished the top
   quartile from the bottom quartile. Compute per-domain average for
   top-25% teams vs bottom-25% teams; report the largest gaps.
3. **Common Failure Modes** — identify the 2-3 domains where the most
   teams scored below the median. These are systemic weaknesses across
   the competition, not team-specific issues.
4. **Weight Impact** — note whether the highest-weight domains
   (runtime at 15, engineering/testing at 12) are where the
   separation actually happened, or if lighter domains (documentation
   at 5) drove unexpected differentiation.
5. **Surprise Performers** — any team that scored highly in a domain
   where their aggregate rank would predict a low score. Name the
   domain and the score.
6. **Judging Recommendations** — 2-3 observations for judges: which
   teams deserve closer inspection, which scores might need manual
   review, any anomalies in the scoring distribution.

## Visualization Guidance
- `leaderboard_bar` — always include: full team ranking by aggregate.
- `domain_radar` — include for top 5 teams: overlaid radar charts.
- `score_distribution` — include: box plot per domain showing spread.
- `separation_heatmap` — include: top-quartile vs bottom-quartile
  gap per domain, color-coded.

## Output Schema
```json
{
  "domain": "00-leaderboard",
  "sections": [
    {"heading": "Headline Standings", "text": "..."},
    {"heading": "Separation Factors", "text": "..."},
    {"heading": "Common Failure Modes", "text": "..."},
    {"heading": "Weight Impact", "text": "..."},
    {"heading": "Surprise Performers", "text": "..."},
    {"heading": "Judging Recommendations", "text": "..."}
  ]
}
```
