# Feature Technical Analysis Prompt

Guides the semantic-analysis step for the Feature Technical domain — read
by whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `10-feature-technical-trend.json`.

## Version
1.0.0

## Analysis Intent
Feature Technical's score moving is only informative if the reader knows
*why*. This step turns scores + trend + findings into: a short narrative,
chart selection, and fix-plan decisions.

## Inputs
- `10-feature-technical-scores.json` (from `calculate.py`)
- `10-feature-technical-trend.json` (from `analyze_trend.py`)
- `10-feature-technical-validation.json`,
  `10-feature-technical-det-eval.json`,
  `10-feature-technical-sem-eval.json` (findings)

## Narrative Guidance
Feature Technical's audit rubric scores: Participating Components/
Component Interactions/Data Ownership/Runtime Behavior consistency (C1),
terminology consistency (C2), and collection-wide coherence (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (technical consistency) is failing, call out specifically what
  contradicts — e.g. a component interaction references a data owner
  that doesn't match the Data Ownership section.
- If terminology inconsistency (C2) keeps recurring, call it out.

Two sections minimum: `Summary` and `Key Risks`.

## Visualization Guidance
- `domain_scores` — always include.
- `section_heatmap` — include only if 2+ failing sections.
- `rule_weights_heatmap` — include only if failing rules have
  `weight >= 1.5`.
- `trend_history` — include once `runs_compared >= 3`.

## Fix-Plan Trigger Criteria
- **Always trigger**: mandatory criterion failures (C1, C2).
- **Trigger if recurring**: C3 failing for 2+ consecutive runs.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan.

## Output Schema
```json
{
  "domain": "10-feature-technical",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "10-feature-technical",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["component-interactions", "data-ownership"],
  "reason": "..."
}
```
