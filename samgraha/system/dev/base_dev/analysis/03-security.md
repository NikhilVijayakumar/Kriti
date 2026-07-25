# Security Analysis Prompt

Guides the semantic-analysis step for the Security domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
has produced `03-security-trend.json`.

## Version
1.0.0

## Analysis Intent
Security's score moving is only informative if the reader knows *why*.
This step turns `03-security-scores.json` + `03-security-trend.json` +
this run's findings into: a short narrative, chart selection, and
fix-plan decisions.

## Inputs
- `03-security-scores.json` (from `calculate.py`)
- `03-security-trend.json` (from `analyze_trend.py`)
- `03-security-validation.json`, `03-security-det-eval.json`,
  `03-security-sem-eval.json` (findings)

## Narrative Guidance
Security's audit rubric scores: Threat Model/Data Classification/
Security Principles consistency (C1), every Data Classification tier
having corresponding protections (C2), and terminology consistency
(C3). Script evidence from `secret-scan`, `dependency-vuln-scan`,
`mitigation-present-at-boundary` grounds factual claims.

The narrative should say:
- Is the score trend improving/declining, and by how much.
- If declining or flat: which of C1/C2/C3 is driving it.
- If C1 (cross-section consistency) is failing, call out specifically
  which sections contradict each other.
- If script evidence (secrets, vulns, boundary mitigations) shows
  findings, name them — these are grounded facts, not heuristic
  estimates.

Two sections minimum: `Summary` and `Key Risks`.

## Visualization Guidance
- `domain_scores` — always include.
- `section_heatmap` — include only if 2+ failing sections.
- `rule_weights_heatmap` — include only if failing rules have
  `weight >= 1.5`.
- `trend_history` — include once `runs_compared >= 3`.

## Fix-Plan Trigger Criteria
- **Always trigger**: mandatory criterion failures (C1, C2).
  Security C1/C2 failures are high-signal — a threat model
  inconsistency is a real gap, not a cosmetic issue.
- **Trigger if recurring**: C3 failing for 2+ consecutive runs.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan.

## Output Schema
```json
{
  "domain": "03-security",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "03-security",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["threat-model", "data-classification"],
  "reason": "..."
}
```
