# External Context Analysis Prompt

Guides the semantic-analysis step for the External Context domain — read
by whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `08-external-context-trend.json`.

## Version
1.0.0

## Analysis Intent
External Context's score moving is only informative if the reader knows
*why*. This step turns scores + trend + findings into: a short narrative,
chart selection, and fix-plan decisions.

## Inputs
- `08-external-context-scores.json` (from `calculate.py`)
- `08-external-context-trend.json` (from `analyze_trend.py`)
- `08-external-context-validation.json`,
  `08-external-context-det-eval.json`,
  `08-external-context-sem-eval.json` (findings)

## Narrative Guidance
External Context's audit rubric scores: Integration Contract/Constraints/
Dependencies consistency (C1), terminology consistency (C2), and
collection-wide coherence (C3).

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (cross-section consistency) is failing, call out specifically
  which sections contradict — e.g. a dependency exists without a
  corresponding integration contract.
- If terminology inconsistency (C2) keeps recurring across external
  system names, call it out.

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
  "domain": "08-external-context",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "08-external-context",
  "charts": ["domain_scores"],
  "focus_sections": ["integration-contract", "dependencies"],
  "reason": "..."
}
```
