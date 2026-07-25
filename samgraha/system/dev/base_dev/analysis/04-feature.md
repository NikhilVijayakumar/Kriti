# Feature Analysis Prompt

Guides the semantic-analysis step for the Feature domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `04-feature-trend.json`.

## Version
1.0.0

## Analysis Intent
Feature's score moving is only informative if the reader knows *why*.
This step turns `04-feature-scores.json` + `04-feature-trend.json` +
this run's findings into: a short narrative, chart selection, and
fix-plan decisions.

## Inputs
- `04-feature-scores.json` (from `calculate.py`)
- `04-feature-trend.json` (from `analyze_trend.py`)
- `04-feature-validation.json`, `04-feature-det-eval.json`,
  `04-feature-sem-eval.json` (findings)

## Narrative Guidance
Feature's audit rubric scores: Functional Requirements/Acceptance
Criteria/Business Rules consistency (C1), every FR having a
corresponding AC (C2), and terminology consistency (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C2 (FR-to-AC coverage) is failing, name which functional
  requirements lack acceptance criteria — this is the most actionable
  finding for a feature document.
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
  C2 failures (missing ACs) are especially actionable — the fix plan
  should list which FRs need ACs written.
- **Trigger if recurring**: C3 failing for 2+ consecutive runs.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan.

## Output Schema
```json
{
  "domain": "04-feature",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "04-feature",
  "charts": ["domain_scores"],
  "focus_sections": ["functional-requirements", "acceptance-criteria"],
  "reason": "..."
}
```
