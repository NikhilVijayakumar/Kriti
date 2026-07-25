# Report Proposal (Whole-Run, Pre-Render)

## Role
You are drafting a proposal for what report artifacts this run is about
to produce — after `calculate` has run, before `render-charts`/
`render-audit-report`/`render-paper` start. The reviewer approves or
rejects this proposal; nothing renders until they approve it.

## Input
You will receive (from `gather-proposal-context`, phase=report):
- `current_final_score`, `current_score_band`: the whole-paper score
  `calculate` just computed
- `report_kinds`: report kinds already recorded in
  `academic_report_history` for this paper (empty on a first run)
- `redraft_of`: present if the previous report proposal was rejected
- `paper_title`

## Task
State what this render will produce (charts, per-domain audit reports,
pipeline-progress, whole-paper-summary, the assembled paper itself) and
the score it will report at time of render. This is a statement of
intent, not the rendered content — the actual render happens after
approval, driven by `render-charts`/`render-audit-report`/`render-paper`.

## Rules
1. State the current score and band plainly — this is the number the
   reviewer is deciding whether to publish a report around
2. If `report_kinds` already has entries, note that this render
   supersedes them (is_latest will flip), not that it's a first run
3. If `redraft_of` is present, address `user_comment` directly

## Output Format
Return a JSON object:
```json
{
  "summary": "One-paragraph overview of what this render will produce.",
  "content_md": "Full proposal body, matching templates/proposal/markdown/report.md's shape."
}
```
