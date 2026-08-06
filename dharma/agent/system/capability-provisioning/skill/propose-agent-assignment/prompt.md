# Propose an agent assignment for a Task

You are given a Task, its derived capabilities, and the registered Agent
Systems. Assign the Task to an agent — or say why it cannot be assigned.

## Input

- `task` — the Task being assigned.
- `capabilities` — the Task's derived capability set (per step: concern +
  skill responsibilities).
- `agent_systems` — the registered Agent Systems, each with its concerns and
  its agents' Skill Bindings.

## Matching

Assignment is per-Task and bottoms out in capabilities:

1. Match each capability's `concern` against the registered Agent Systems'
   concerns.
2. Within the matching systems, match the needed `skill_responsibilities`
   against the agents' Skill Bindings (each binding pairs an agent with a
   skill whose responsibility must cover the need).
3. Assign the Task to exactly one owning agent — the agent whose system and
   bindings cover the Task's capabilities. A Task needing several capabilities
   may be owned by a coordinator-style agent that fans out, but it still has
   one owner.

## Output

- `assignment` — `task`, the owning `agent_role`, its `agent_system`, and the
  `matched_skills`.
- `unassignable_reason` — present only when no registered agent can be bound
  to the Task: name the unresolved capability and the concern or skill
  binding that is missing. An unassignable Task is a gap, never a skipped
  item.

## Rules

- Never invent a registered Agent System or an agent that does not exist in
  the input.
- A concern alone is not an assignment — the agent's Skill Bindings must cover
  the needed skills.
- Name no specific repository or Domain System.
