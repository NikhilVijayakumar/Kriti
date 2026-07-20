# Feature Design Analysis Prompt

Guides the semantic-analysis step for the Feature Design domain — read
by whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `09-feature-design-trend.json`.

## Version
1.0.0

## Analysis Intent
Feature Design's score moving is only informative if the reader knows
*why*. This step turns scores + trend + findings into: a short narrative,
chart selection, and fix-plan decisions.

## Inputs
- `09-feature-design-scores.json` (from `calculate.py`)
- `09-feature-design-trend.json` (from `analyze_trend.py`)
- `09-feature-design-validation.json`,
  `09-feature-design-det-eval.json`,
  `09-feature-design-sem-eval.json` (findings)

## Narrative Guidance
Feature Design's audit rubric scores: User Experience/Workflow/States
consistency (C1), terminology consistency (C2), and collection-wide
coherence (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (UX/Workflow/States consistency) is failing, call out
  specifically what contradicts — e.g. a workflow transition references
  a state not defined in the States section.
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
  "domain": "09-feature-design",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "09-feature-design",
  "charts": ["domain_scores"],
  "focus_sections": ["user-experience", "workflow"],
  "reason": "..."
}
```
