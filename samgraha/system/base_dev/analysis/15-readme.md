# README Analysis Prompt

Guides the semantic-analysis step for the README domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `15-readme-trend.json`.

## Version
1.0.0

## Analysis Intent
README's score moving is only informative if the reader knows *why*.
This step turns scores + trend + findings into: a short narrative, chart
selection, and fix-plan decisions.

## Inputs
- `15-readme-scores.json` (from `calculate.py`)
- `15-readme-trend.json` (from `analyze_trend.py`)
- `15-readme-validation.json`, `15-readme-det-eval.json`,
  `15-readme-sem-eval.json` (findings)

## Narrative Guidance
README's audit rubric scores: Usage examples/Build-Installation
consistency (C1), Development/Contributing workflow consistency (C2),
and terminology consistency (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (Usage ↔ Build/Install) is failing, call out specifically
  which commands or flags don't match — this is the most actionable
  finding for a README.
- If C2 (Dev/Contributing workflow) is failing, name which workflow
  steps contradict.
- If terminology inconsistency (C3) keeps recurring, call it out.

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
  "domain": "15-readme",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "15-readme",
  "charts": ["domain_scores"],
  "focus_sections": ["usage", "build-installation"],
  "reason": "..."
}
```
