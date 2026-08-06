# Identify agent capability gaps

You are given the assignments and workflows of a provisioning run. Consolidate
every unassigned or uncovered item into a classified gap report with closure
recommendations.

## Input

- `assignments` — task-to-agent assignments, including any with an
  `unassignable_reason`.
- `workflows` — per-task workflows, including any with uncovered steps or
  missing verifiers.

## Classification

Classify each gap by type:

- **concern** — a required capability matches no registered Agent System
  concern.
- **skill** — a concern matches, but no agent of that system binds the needed
  skill.
- **role** — a workflow needs a handoff candidate role that no agent exposes.
- **verifier** — a level has no verifier distinct from its worker.

## Gap entries

```json
{
  "type": "concern",
  "subject": "rust-development",
  "blocked_tasks": 42,
  "recommendation": "register an Agent System with concern 'rust-development'"
}
```

`recommendations[]` collects the closure steps in one list. Recommendations
name what would close the gap (a concern to register, a skill to author, a
binding to add) but do not author or register anything.

## Rules

- Every unassignable assignment and every uncovered workflow must surface as
  a classified gap — nothing is dropped.
- Rank gaps by the volume of Tasks blocked.
- Name no specific repository or Domain System.

## Output

`gaps[]` and `recommendations[]`.
