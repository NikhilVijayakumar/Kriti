# Audit Proposal (Whole-Run, Pre-Check)

## Role
You are drafting a proposal for what the audit pipeline is about to
check — before any domain's deterministic or semantic audit runs. The
reviewer approves or rejects this proposal; nothing gets audited until
they approve it.

## Input
You will receive (from `gather-proposal-context`, phase=audit):
- `domains`: `[{domain_key, det_rule_count, det_critical_count,
  rubric_criterion_count, rubric_found}]` — every domain that has
  completed generation and is ready to audit, with real counts from the
  same rule/rubric files `deterministic_audit.py` and
  `semantic-audit.md` read. The template renders these in the "What Will
  Be Audited" table; don't restate the numbers in `content_md` — write
  about what they mean for this round's audit scope.
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

## Domain Rubric Grounding
Each domain's audit should reference its specific rubric:
- 6 section domains (title-and-metadata, introduction, methodology,
  findings, conclusion, references) → `audit/semantic/document/{domain}.md`
- 5 cross-cutting domains (novelty, gaps, mathematics, tables, figures) →
  `audit/semantic/document/{domain}.md`

## Rules
1. List every domain in `domains` — a reviewer approving "the audit"
   is approving a specific, enumerated set of checks, not a vague pass
2. Name every model in `models` explicitly — approving a single-model
   round is a different decision from approving a multi-model ensemble
3. If `redraft_of` is present, address `user_comment` directly
4. Don't restate the rubric's full rule text — `rubric_summary` is
   already a summary; one clause per domain is enough
5. The "What Will Be Audited" table is computed from the same rule/rubric
   files the audit scripts read — don't repeat those numbers in
   `content_md`, write about what they mean for this round's audit scope

## Output Format
Return a JSON object:
```json
{
  "summary": "One-paragraph overview of this audit round's scope.",
  "content_md": "Full proposal body, matching templates/proposal/markdown/audit.md's shape.",
  "computed_context": "<pass through the full domains array and models list from Input — persist stores this for template rendering>"
}
```
