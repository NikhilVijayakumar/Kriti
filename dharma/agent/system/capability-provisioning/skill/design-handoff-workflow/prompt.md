# Design a Task's workflow

You are given one Task, its assignment, and its epic/usecase context. Emit the
workflow that executes and verifies it.

## Input

- `task` — the Task.
- `assignment` — the owning agent role and its matched skills.
- `epics_context` — the epic and usecase the Task sits in, so the workflow can
  chain with siblings.

## What to emit

`workflow`:

- `task` and `owning_agent` — the assigned role.
- `steps` — the ordered skill invocations the owning agent makes, each
  consuming the previous step's output.
- `handoffs` — the chain between agent turns. Each handoff names a `trigger`
  condition and a `candidate_role`, never a specific agent instance: handoffs
  are resolved by the Handoff Broker against candidate roles.
- `verified_by` — the verification path. Completion is recursive and verified
  at every level by a verifier distinct from the worker: the task's verifier,
  the usecase's verifier, and the epic's verifier. **The verifier is never the
  worker** — if a level's only verifier would be the worker itself, the
  workflow has a gap, not a shortcut.

## Rules

- Name roles, never agent instances, in every handoff.
- Every step must be covered by a skill the owning agent binds; an uncovered
  step is a gap.
- Every level (task, usecase, epic) must have a verifier distinct from its
  worker.
- Name no specific repository or Domain System.

## Output

`workflow` — per the shape above.
