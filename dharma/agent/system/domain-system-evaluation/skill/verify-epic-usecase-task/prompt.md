# Verify an Epic's subtree

You are given one Epic with its full usecase/task/task-step subtree. Check the
hierarchy structure and produce a verdict, findings, and gaps.

## Checks

1. **Parent chain** — every usecase resolves to this epic; every task resolves
   to its usecase; every task step resolves to its task. No orphaned rows, no
   naming collisions within a scope.
2. **At least one Task per Usecase** — a usecase with zero tasks is an
   *invalid* state, not an empty one. Report it as a finding.
3. **Contract completeness** — every task carries an input contract and an
   output contract.
4. **Task-step completeness** — every task has a task-step sequence, and every
   task step carries a `required_capability`.
5. **Capability resolution** — every `required_capability` value resolves to a
   registered Agent System concern. An unresolved value is a **gap**, not a
   defect.

## Finding shape

```json
{
  "id": "EUT-TASK-001",
  "condition": "every usecase has at least one task",
  "message": "usecase 'draft-vision' has 0 tasks",
  "severity": "error",
  "weight": 1.0,
  "mandatory": true,
  "evidence": "usecase 'draft-vision' tasks == []",
  "kind": "defect"
}
```

## Gaps

`gaps[]` collects everything Scenario B must resolve: unresolved
`required_capability` concerns, tasks without contracts, and usecases without
tasks. Each gap entry names the unresolved item and its location in the tree.
This is the hand-off to the provisioning scenario.

## Rules

- Check the declaration, never the quality of produced work.
- Do not assign or fix; report with evidence.
- Do not name a specific repository or Domain System.
