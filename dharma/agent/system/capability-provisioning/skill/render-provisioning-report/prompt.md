# Render the execution blueprint

You are given the assembled execution blueprint of a Scenario B run. Render it
as the provisioning report.

## Input

`blueprint` — per-Epic coverage, per-Task assignments, workflows, and the gap
summary.

## Report structure

Render, in order:

1. **Summary** — total Tasks, assigned vs gapped, and the counts by gap type.
2. **Per-Epic sections** — for each Epic: its usecases, and per Task:
   - `assigned_agent` (the owning role)
   - `skills` (the ordered skill invocations)
   - `handoff` (`trigger` + `candidate_role`)
   - `verified_by` (the verifier role — never the assigned agent)
   - the usecase and epic verification roles.
3. **Gap summary** — each gap with its type (`concern`/`skill`/`role`/
   `verifier`), subject, blocked-task count, and recommendation, ranked by
   blocked Tasks.

## Rules

- The verifier line must never equal the assigned agent; if it does, the
  report surfaces it as a verifier gap.
- Preserve the per-level verification path — task, usecase, epic.
- Keep recommendations as recommendations; the report does not author or
  register.
- Name no specific repository or Domain System.

## Output

`report` — the full rendered text.
