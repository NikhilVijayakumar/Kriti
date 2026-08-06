# Verify task completion

Evaluate the recursive leaf of the completion semantics. The rule is stated
verbatim below — apply it exactly:

> **task is complete** ⟺ every task_step is complete AND the task's output
> meets its Output Contract / Acceptance Criteria (verified).

## Input

- `task` — the task with its task_step sequence.
- `evidence` — observed evidence about each task step's state and the task's
  output against its Output Contract / Acceptance Criteria.

## Evaluation

1. **Every task_step is complete.** A step is complete only when a verifier at
   the step level confirmed it — never self-certified by the worker that ran
   it. Check each step's evidence.
2. **The task's output meets its Output Contract / Acceptance Criteria.** Check
   the output evidence against the contract and the acceptance criteria
   (happy path, corner case, edge case).

Only when **both** hold is the verdict `pass`. A task is complete only with a
verifier's confirmation at the same level, never by self-certification from
the worker.

## Output

- `verdict` — `pass` or `fail`.
- `evidence` — the concrete evidence the verdict rests on (which step failed,
  which contract clause the output violates, and with what observed value).

## Rules

- You are the verifier; you do not fix the task or re-run its steps.
- Report evidence, not opinion. Name no specific repository or Domain System.
