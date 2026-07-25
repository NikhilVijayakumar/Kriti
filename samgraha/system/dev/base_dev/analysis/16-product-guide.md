# Product Guide Analysis Prompt

Guides the semantic-analysis step for the Product Guide domain — read
by whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `16-product-guide-trend.json`.

## Version
1.0.0

## Analysis Intent
Product Guide's score moving is only informative if the reader knows
*why*. This step turns scores + trend + findings into: a short narrative,
chart selection, and fix-plan decisions.

## Inputs
- `16-product-guide-scores.json` (from `calculate.py`)
- `16-product-guide-trend.json` (from `analyze_trend.py`)
- `16-product-guide-validation.json`,
  `16-product-guide-det-eval.json`,
  `16-product-guide-sem-eval.json` (findings)

## Narrative Guidance
Product Guide's audit rubric scores: Title/Body accuracy (C1), Public
Contract/Body consistency (C2), and terminology consistency (C3). Script
evidence from `public-contract-diff` grounds factual claims.

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (Title ↔ Body) is failing, name which topic's title doesn't
  match its body content.
- If C2 (Public Contract ↔ Body) is failing, name which contract
  elements don't match what the body instructions actually use.
- If `public-contract-diff` script found mismatches, name them —
  these are grounded facts.

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
  "domain": "16-product-guide",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "16-product-guide",
  "charts": ["domain_scores"],
  "focus_sections": ["title-body", "public-contract"],
  "reason": "..."
}
```
