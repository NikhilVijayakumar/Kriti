# Engineering Analysis Prompt

Guides the semantic-analysis step for the Engineering domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `07-engineering-trend.json`.

## Version
1.0.0

## Analysis Intent
Engineering's score moving is only informative if the reader knows *why*.
This step turns scores + trend + findings into: a short narrative, chart
selection, and fix-plan decisions.

## Inputs
- `07-engineering-scores.json` (from `calculate.py`)
- `07-engineering-trend.json` (from `analyze_trend.py`)
- `07-engineering-validation.json`, `07-engineering-det-eval.json`,
  `07-engineering-sem-eval.json` (findings)

## Narrative Guidance
Engineering's audit rubric scores: Guiding Principles/Build Standards/
Testing Standards/Code Standards consistency (C1), terminology
consistency (C2), and collection-wide coherence (C3). Script evidence
from `lint-standards` grounds factual claims about actual lint
compliance.

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (standards consistency) is failing, call out which standards
  contradict — e.g. build standards require a tool that testing
  standards don't reference.
- If `lint-standards` script found actual violations, name them —
  these are grounded facts, not heuristic estimates.

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
  "domain": "07-engineering",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "07-engineering",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["build-standards", "testing-standards"],
  "reason": "..."
}
```
