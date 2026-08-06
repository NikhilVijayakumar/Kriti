# Verify epic completion

Evaluate the completion semantics at the top level. The rule is stated
verbatim below — apply it exactly:

> **epic is complete** ⟺ all its usecases (and their tasks) are complete AND
> verified AND the epic itself is verified (its domain-wide objective is
> actually satisfied)

## Input

- `epic` — the epic being evaluated, including its objective.
- `usecase_verdicts` — the verifier verdicts for each of the epic's usecases.

## Evaluation

1. **All usecases (and their tasks) complete AND verified.** Every usecase
   verdict must be `pass`, produced by a usecase-level verifier that itself
   required task-level verification — never self-certified.
2. **The epic itself is verified.** The epic's domain-wide objective is
   actually satisfied. This is a check *above the sum of its usecases*: the
   usecases may all pass and the epic still fail if the objective they were
   supposed to achieve is not satisfied across the domain.

Only when **both** hold is the verdict `pass`. An epic is not partially
complete because its usecases are done — it is either complete or not. The
epic verifier is not the epic's worker; completion is never self-certified.

## Output

- `verdict` — `pass` or `fail`.
- `evidence` — which usecase verdict failed (if any) or what objective check
  failed above the usecases, with the observed state.

## Rules

- Verify; do not fix or re-run the epic's work.
- Report evidence, not opinion. Name no specific repository or Domain System.
