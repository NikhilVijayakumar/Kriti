```toml
[system]
id = "capability-provisioning"
concern = "capability-provisioning"
is_privileged_request = false
scenarios = ["provision-agent-capability"]
```

# capability-provisioning — Agent System

Analyses a Domain System as an artifact to provision agent capability. Given a Domain
System listing, it identifies every agent and skill required to execute its
Epics/Usecases/Tasks, assigns each Task to one or another agent, defines each
agent's workflow and the handoff chains between agents, and reports gaps in
the registered Agent System set. It reads Domain Systems; it never writes to one.

## Scenarios

- **Scenario B — provision the agent capability.** Given the same Domain
  System listing, identify every agent and skill required to execute its
  Epics/Usecases/Tasks, assign each Task to one or another agent, define each
  agent's workflow and the handoff chains between agents, and report gaps in
  the registered Agent System set.

## Scenario B pipeline

Scenario B produces an **execution blueprint** — for every Epic, its Usecases,
and every Usecase's Tasks: the assigned agent, the skills that agent binds, the
workflow/handoff chain, and the verification path certifying each level
complete. The pipeline is a strict chain:

```
capability-analyser ─map-task-to-capability─▶ capabilities per task
  ─▶ assignment-planner ─propose-agent-assignment─▶ assignments (task → agent)
    ─▶ workflow-designer ─design-handoff-workflow + verify-{task,usecase,epic}─▶ workflows
      ─▶ gap-analyser ─identify-agent-gaps─▶ gaps + recommendations
orchestrator ─render-provisioning-report─▶ execution blueprint
```

The model the blueprint must satisfy:

- **Assignment is per-Task and bottoms out in capabilities.** Every Task (and
  each task_step) declares a required capability. The planner matches each
  capability against the concerns of registered Agent Systems and, within the
  matching systems, against agents whose Skill Bindings cover the needed
  skills. Every Task ends up assigned or gapped — never skipped.
- **Workflow is a chain of agent turns linked by handoff conditions.** Each
  handoff names a trigger and a candidate role, resolved by the Handoff Broker;
  it never names a specific agent instance.
- **Completion is recursive and verified at every level.** The blueprint
  carries, per level, *who verifies* — the verifier is never the worker. Where
  a level has no worker-and-verifier pair, the blueprint has a gap.

Scenario B consumes Scenario A's output: A's `gaps[]` (unresolved
`required_capability`, empty Task contracts, 0-Task usecases) is B's starting
input. A verifies the Domain System declaration; B reasons about who could
execute it.

## Completion / verification semantics

Both scenarios run on one recursive semantics, evaluated from the leaves up. A
level is complete only when a verifier at that level confirms it — never by
self-certification from the worker:

- **task is complete** ⟺ every task_step is complete AND the task's output
  meets its Output Contract / Acceptance Criteria (verified).
- **usecase is complete** ⟺ all its tasks are complete AND verified AND the
  usecase itself is fully verified (its user-facing capability is actually
  delivered — a check above the sum of its tasks).
- **epic is complete** ⟺ all its usecases (and their tasks) are complete AND
  verified AND the epic itself is verified (its domain-wide objective is
  actually satisfied).

Consequences this system treats as constraints:

1. Verification is a distinct act at every level, done by distinct agents. The
   agent that performs a task's steps does not certify that task complete; a
   verifier agent does. The usecase verifier is not the usecase's worker; the
   epic verifier is not the epic's worker.
2. A level cannot claim completion while a lower level is open. An epic is not
   partially complete because its usecases are done — it is either complete
   (all usecases complete and verified, epic verified) or not.
3. Assignment is per-Task and bottoms out in capabilities. Every Task is
   assigned to one or another agent; an unassignable Task is a gap, not a
   skipped item.
4. Handoffs are structural. A workflow is a chain of agent turns linked by
   handoff conditions resolved against `handoff_candidate_role`, never a
   worker's own choice of successor.

## Skills policy

Every skill in this Agent System is analysis-only. The system produces
reports, assignments, and gap lists; no skill is effect-capable and none
mutates the Domain System or an Agent System it analyses. No agent or skill
names a specific repository or Domain System.
