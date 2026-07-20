# Philosophy Analysis Prompt

Guides the semantic-analysis step for the Philosophy domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `02-philosophy-trend.json`.

## Version
1.0.0

## Analysis Intent
Philosophy's score moving is only informative if the reader knows *why*.
This step turns `02-philosophy-scores.json` + `02-philosophy-trend.json` +
this run's findings into: a short narrative a human can read in 30
seconds, a decision about which charts are worth generating, and a
decision about which findings are worth a DB fix-plan.

## Inputs
- `02-philosophy-scores.json` (from `calculate.py`)
- `02-philosophy-trend.json` (from `analyze_trend.py`)
- `02-philosophy-validation.json`, `02-philosophy-det-eval.json`,
  `02-philosophy-sem-eval.json` (findings)

## Narrative Guidance
Philosophy's audit rubric (`audit/semantic/document/02-philosophy.md`)
scores three things: Principles/Values/Trade-offs consistency (C1),
terminology consistency (C2), and collection-wide coherence (C3).
The narrative should say:
- Is the score trend improving/declining, and by how much, across the
  three trend windows.
- If declining or flat: which of C1/C2/C3 is driving it — name the
  criterion.
- If terminology inconsistency (C2) keeps recurring across runs, call
  that out explicitly.

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
  "domain": "02-philosophy",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "02-philosophy",
  "charts": ["domain_scores"],
  "focus_sections": ["principles", "values"],
  "reason": "..."
}
```
