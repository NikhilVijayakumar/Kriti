# Map a Task to its required capabilities

You are given one Task and its task-step sequence. Derive the capability set
each step requires so the assignment planner can match it against registered
Agent Systems.

## Input

- `task` — the Task, including its input/output contract.
- `task_steps` — the ordered task-step sequence.

## What to derive

For every step, produce a capability entry:

```json
{
  "step": "s1",
  "concern": "the concern that would execute this step",
  "skill_responsibilities": ["the skill responsibilities the step needs"]
}
```

- `concern` comes from the step's required capability, interpreted as the
  concern an Agent System registers in the registry.
- `skill_responsibilities` are the concrete skill responsibilities the step's
  work calls for, derived from the contract and the step description.

## Rules

- Derive capabilities per step, not per Task — a multi-step Task may need
  several capabilities and several concerns.
- If a step's required capability is empty or unresolvable, emit the entry
  with an empty `concern` and note it — an unmappable step is a flag, not a
  silent pass.
- Assignment is per-Task and bottoms out in capabilities; your output is what
  makes that matching possible.
- Name no specific repository or Domain System.

## Output

`capabilities` — one entry per step.
