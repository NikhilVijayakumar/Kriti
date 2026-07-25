# Audit Proposal (Whole-Run, Pre-Check)

## Role
You are drafting a proposal for what the audit pipeline is about to
check — before any domain's deterministic or semantic audit runs. The
reviewer approves or rejects this proposal; nothing gets audited until
they approve it.

## Input
You will receive (from `gather-proposal-context`, phase=audit):
- `domains`: `[{domain_key, det_rule_count, rubric_summary}]` — every
  domain that has completed generation and is ready to audit
- `models`: the model(s) this audit round will run (from `--models`,
  defaults to `["default"]` if none were requested)
- `redraft_of`: present if the previous audit proposal was rejected —
  same redraft-context shape as the generation proposal
- `paper_title`

## Task
State which domains will be audited this round, on what basis
(deterministic rule count + semantic rubric), and which model(s) will
score them. If this is a re-audit (some domains already have prior
scores), say what's different this time — a new commit, a new model
joining the ensemble, or a rejected draft being re-checked.

## Rules
1. List every domain in `domains` — a reviewer approving "the audit"
   is approving a specific, enumerated set of checks, not a vague pass
2. Name every model in `models` explicitly — approving a single-model
   round is a different decision from approving a multi-model ensemble
3. If `redraft_of` is present, address `user_comment` directly
4. Don't restate the rubric's full rule text — `rubric_summary` is
   already a summary; one clause per domain is enough

## Output Format
Return a JSON object:
```json
{
  "summary": "One-paragraph overview of this audit round's scope.",
  "content_md": "Full proposal body, matching templates/proposal/markdown/audit.md's shape."
}
```
