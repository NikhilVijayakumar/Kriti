# Verify usecase completion

Evaluate the completion semantics one level up. The rule is stated verbatim
below — apply it exactly:

> **usecase is complete** ⟺ all its tasks are complete AND verified AND the
> usecase itself is fully verified (its user-facing capability is actually
> delivered — a check above the sum of its tasks)

## Input

- `usecase` — the usecase being evaluated.
- `task_verdicts` — the verifier verdicts for each of the usecase's tasks.

## Evaluation

1. **All tasks complete AND verified.** Every task verdict must be `pass`,
   produced by a task-level verifier — never self-certified by the workers.
2. **The usecase itself is fully verified.** The usecase's user-facing
   capability is actually delivered. This is a check *above the sum of its
   tasks*: the tasks may all pass and the usecase still fail if the capability
   they were supposed to deliver is not present end to end.

Only when **both** hold is the verdict `pass`. The usecase verifier is not the
usecase's worker; completion is never self-certified.

## Output

- `verdict` — `pass` or `fail`.
- `evidence` — which task verdict failed (if any) or what capability check
  failed above the tasks, with the observed state.

## Rules

- Verify; do not fix or re-run the usecase's work.
- Report evidence, not opinion. Name no specific repository or Domain System.
