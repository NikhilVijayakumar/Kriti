# Vision Analysis Prompt

Guides the semantic-analysis step for the Vision domain — read by
whichever agent runs it via MCP, on-demand, after `analyze_trend.py`
(deterministic, scripted) has produced `01-vision-trend.json`. Not
parsed by a script — this is a prompt, not a rule file like
`audit/semantic/document/01-vision.md`. That file scores a document;
this one writes the human-facing narrative and picks what to fix and
visualize, given the score's history.

## Version
1.0.0

## Analysis Intent
Vision's score moving is only informative if the reader knows *why*.
This step turns `01-vision-scores.json` + `01-vision-trend.json` +
this run's findings into: a short narrative a human can read in 30
seconds, a decision about which charts are worth generating, and a
decision about which findings are worth a DB fix-plan (not all of
them are).

## Inputs
Read directly — no bundler script, these are already at known paths
in the domain's output directory:
- `01-vision-scores.json` (from `calculate.py`)
- `01-vision-trend.json` (from `analyze_trend.py` — `vs_last_run`,
  `vs_last_3_runs`, `vs_baseline`)
- `01-vision-validation.json`, `01-vision-det-eval.json`,
  `01-vision-sem-eval.json` (findings — same sources
  `analyze.py`'s `analyze_findings()` already reads, for consistency)

## Narrative Guidance
Vision's audit rubric (`audit/semantic/document/01-vision.md`) scores
three things: Problem/Solution/Vision-Statement coherence, zero
technology references, and cross-document terminology consistency.
The narrative should say, in plain language:
- Is the score trend improving/declining, and by how much, across the
  three trend windows — lead with this, it's what a human scans for
  first.
- If declining or flat: which of the three rubric criteria (C1/C2/C3)
  is driving it — name the criterion, not just "semantic score is low."
- If a technology reference (C2) keeps recurring across runs
  (compare this run's findings against the trend direction) — call
  that out explicitly, it's a mandatory criterion and a pattern, not
  a one-off.

Two sections minimum: `Summary` (trend + headline number) and
`Key Risks` (what's failing and why) — see the shared
`{domain}-narrative.json` schema in the analysis proposal, §5.

## Visualization Guidance
From the chart catalog (proposal §6):
- `domain_scores` — always include, it's the anchor chart.
- `section_heatmap` — include only if `01-vision-det-eval.json` or
  `01-vision-sem-eval.json` shows 2+ failing sections this run; a
  heatmap with one red cell isn't worth a chart.
- `rule_weights_heatmap` — include only if this run's failing rules
  have `weight >= 1.5` (i.e. the failures are the ones that actually
  move the score) — skip for low-weight/cosmetic rule failures.
- `trend_history` (once built per proposal §6) — include once
  `01-vision-trend.json` has `runs_compared >= 3`; meaningless before
  that.

## Fix-Plan Trigger Criteria
Not every finding deserves a DB fix plan — that's this step's actual
judgment call, per the proposal's correction that `audit_fix_plan`
generates the plan content server-side, so the only decision here is
*whether to ask for one*:
- **Always trigger**: mandatory criterion failures (C1, C2) — these
  block the tier gate and a fix plan should exist for a human to act
  on.
- **Trigger if recurring**: a recommended criterion (C3) failing for
  2+ consecutive runs (check `vs_last_run`/`vs_last_3_runs` direction
  in `01-vision-trend.json` plus whether the same finding id appears
  again this run) — a one-off C3 dip usually self-corrects on the next
  content-fill pass, don't spam a fix plan for it.
- **Never trigger**: `info`-severity findings, or findings already
  covered by an open fix plan (check via `audit_fix_plan_get` before
  calling `audit_fix_plan` again for the same finding id).

## Output Schema
Same shape as every other domain — see analysis proposal §5:

```json
{
  "domain": "01-vision",
  "sections": [
    {"heading": "Summary", "text": "..."},
    {"heading": "Key Risks", "text": "..."}
  ]
}
```

```json
{
  "domain": "01-vision",
  "charts": ["domain_scores"],
  "focus_sections": ["problem", "solution"],
  "reason": "..."
}
```

Fix-plan calls: `audit_fix_plan(finding, domain="01-vision", report_id=<01-vision-trend.json's run timestamp>, report_type="documentation-tier-analysis", target_path=<vision doc path>)` — one call per triggered finding, made directly by the agent running this step (it already has MCP access as the thing invoking this rubric).
