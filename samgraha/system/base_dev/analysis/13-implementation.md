# Implementation Analysis Prompt

Guides the semantic-analysis step for the Implementation domain — read
by whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `13-implementation-trend.json`.

## Version
1.0.0

## Analysis Intent
Implementation's score moving is only informative if the reader knows
*why*. This step turns scores + trend + findings into: a short narrative,
chart selection, and fix-plan decisions.

## Inputs
- `13-implementation-scores.json` (from `calculate.py`)
- `13-implementation-trend.json` (from `analyze_trend.py`)
- `13-implementation-validation.json`,
  `13-implementation-det-eval.json`,
  `13-implementation-sem-eval.json` (findings)

## Narrative Guidance
Implementation's audit rubric scores: plan type consistency — security
mitigations not undone by later plans (C1), terminology consistency (C2),
and collection-wide coherence (C3). Script evidence from
`folder-structure` and `dependency-manifest` grounds factual claims.

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (plan type consistency) is failing, call out specifically
  which later plan undoes a security mitigation — this is the most
  critical finding for an implementation document.
- If `folder-structure` or `dependency-manifest` scripts found
  mismatches, name them — these are grounded facts.

Two sections minimum: `Summary` and `Key Risks`.

## Visualization Guidance
- `domain_scores` — always include.
- `section_heatmap` — include only if 2+ failing sections.
- `rule_weights_heatmap` — include only if failing rules have
  `weight >= 1.5`.
- `trend_history` — include once `runs_compared >= 3`.

## Fix-Plan Trigger Criteria
- **Always trigger**: mandatory criterion failures (C1, C2).
  C1 failures (security mitigation undoing) are critical — the fix
  plan should identify which plan conflicts with which security fix.
- **Trigger if recurring**: C3 failing for 2+ consecutive runs.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan.

## Output Schema
```json
{
  "domain": "13-implementation",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "13-implementation",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["plan-consistency", "security-mitigations"],
  "reason": "..."
}
```
