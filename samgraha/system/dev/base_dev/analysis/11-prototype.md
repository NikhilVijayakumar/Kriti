# Prototype Analysis Prompt

Guides the semantic-analysis step for the Prototype domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `11-prototype-trend.json`.

## Version
1.0.0

## Analysis Intent
Prototype's score moving is only informative if the reader knows *why*.
This step turns scores + trend + findings into: a short narrative, chart
selection, and fix-plan decisions.

## Inputs
- `11-prototype-scores.json` (from `calculate.py`)
- `11-prototype-trend.json` (from `analyze_trend.py`)
- `11-prototype-validation.json`, `11-prototype-det-eval.json`,
  `11-prototype-sem-eval.json` (findings)

## Narrative Guidance
Prototype's audit rubric scores: Mock APIs/Data Model consistency (C1),
Scope coverage by Mock APIs (C2), and Traceability accuracy (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (Mock API ↔ Data Model) is failing, call out which entities
  or fields don't match — this is the most actionable finding for a
  prototype.
- If C2 (Scope coverage) is failing, name which in-scope items lack
  mock API coverage.

Two sections minimum: `Summary` and `Key Risks`.

## Visualization Guidance
- `domain_scores` — always include.
- `section_heatmap` — include only if 2+ failing sections.
- `rule_weights_heatmap` — include only if failing rules have
  `weight >= 1.5`.
- `trend_history` — include once `runs_compared >= 3`.

## Fix-Plan Trigger Criteria
- **Always trigger**: mandatory criterion failures (C1, C2).
  C1 failures (Mock API ↔ Data Model mismatch) are especially
  actionable — the fix plan should list the specific entities/fields.
- **Trigger if recurring**: C3 failing for 2+ consecutive runs.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan.

## Output Schema
```json
{
  "domain": "11-prototype",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "11-prototype",
  "charts": ["domain_scores"],
  "focus_sections": ["mock-apis", "data-model"],
  "reason": "..."
}
```
