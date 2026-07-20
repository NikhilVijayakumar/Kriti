# Architecture Analysis Prompt

Guides the semantic-analysis step for the Architecture domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `05-architecture-trend.json`.

## Version
1.0.0

## Analysis Intent
Architecture's score moving is only informative if the reader knows *why*.
This step turns scores + trend + findings into: a short narrative, chart
selection, and fix-plan decisions.

## Inputs
- `05-architecture-scores.json` (from `calculate.py`)
- `05-architecture-trend.json` (from `analyze_trend.py`)
- `05-architecture-validation.json`, `05-architecture-det-eval.json`,
  `05-architecture-sem-eval.json` (findings)

## Narrative Guidance
Architecture's audit rubric scores: Component Model/Data Flow/
Communication Paths consistency (C1), terminology consistency (C2),
and collection-wide coherence (C3). Script evidence from
`module-boundary-diff` grounds factual claims about actual module
boundaries vs declared architecture.

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (structural consistency) is failing, call out which sections
  contradict — e.g. a data flow references a component not in the
  component model.
- If `module-boundary-diff` script found mismatches between declared
  and actual boundaries, name them — these are grounded facts.

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
  "domain": "05-architecture",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "05-architecture",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["component-model", "data-flow"],
  "reason": "..."
}
```
