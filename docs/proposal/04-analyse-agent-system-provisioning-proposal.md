# analyse — Agent System Provisioning (Proposal 04 of 3: Scenario B)

## 0. Status

**Draft.** Part 3 of the 3-part `analyse` Agent System series. Part 1
(`02-analyse-agent-system-overview-proposal.md`) pins the system's two
scenarios, its recursive completion/verification semantics, its content-root
layout, and its `dharma-agent.toml` (including the series' source convention:
`schema/mcp/*.sql` and `docs/proposal/*` references resolve to
`/home/dell/PycharmProjects/dharma/`). Part 2 (`03-analyse-domain-system-
verification-proposal.md`) designs Scenario A (verify a Domain System). This
part designs **Scenario B — identify the agent capability needed to execute a
Domain System's work**: the agents and skills that map every Task to a required
capability, assign every Task to one or another agent, define each agent's
workflow and the handoff chains between agents, apply the recursive
completion/verification semantics at every level, and report gaps in the
registered Agent System set. Design-only; nothing under
`dharma/agent/system/analyse/` is authored yet.

## 1. What Scenario B is for

Given a Domain System — a declared set of Epics, Usecases, Tasks, and
Task-Steps — Scenario B answers: *what agents and skills are required to
complete this Domain System's work, who does each Task, in what order, handing
off to whom, and how is each level verified complete?* It produces an
**execution blueprint**: for every Epic, its Usecases, and every Usecase's
Tasks, the assigned agent, the skills that agent will bind, the
workflow/handoff chain, and the verification path that will certify each level
complete. Anything the blueprint cannot assign — a Task whose required
capability no registered Agent System's concern satisfies, a workflow step no
agent's Skill Bindings cover, a Usecase no combination of agents can deliver —
is a **gap**. Gap identification is the point of the whole scenario (Part 1
§1): the analyse Agent System exists partly to tell its owner *where the Agent
System set is missing capability for a domain*.

Scenario B consumes Scenario A's output: A's `gaps[]` (unresolved
`required_capability`, empty Task contracts, 0-Task usecases) is B's starting
input. A verifies the Domain System *declaration*; B reasons about *who could
execute it*.

## 2. The model Scenario B runs on

**Assignment is per-Task and bottoms out in capabilities.** Each Task (and each
`task_step`) declares a required capability. The capability-analyser maps the
Task's contract and steps to the capability or capabilities they need; the
assignment-planner matches each capability against the concerns of registered
Agent Systems (`agent_system_registry.concern`) and, within the matching
systems, against agents whose Skill Bindings cover the needed skills
(`agent_skill_binding` × `skill.responsibility`). "Assign everything to one or
another agent" (Part 1 §1) means: every Task in the Domain System ends up
assigned, including Tasks the planner can only assign to an orchestrator-like
coordinator agent that fans out to others. A Task that no agent can be bound to
is reported as a gap, never silently skipped.

**Workflow is a chain of agent turns linked by handoff conditions.** For each
assigned Task the workflow-designer emits: the owning agent, the ordered skills
it invokes, the verification step that certifies the Task complete (the
Completion-Validator role, per `docs/proposal/07`), and — when the Task needs a
capability a different agent holds — a handoff condition naming the candidate
role. Handoffs are resolved by the Handoff Broker against
`handoff_candidate_role`; the workflow names the *role*, never a specific agent
instance (`docs/proposal/01` handoff policy, `docs/proposal/07`).

**Completion is recursive and verified at every level** (Part 1 §3), restated
here as the model the blueprint must satisfy:

```
task     complete ⟺ every task_step complete  AND  output meets Output Contract
                    / Acceptance Criteria  (verified)
usecase  complete ⟺ all its tasks complete AND verified  AND  the usecase itself
                    fully verified
epic     complete ⟺ all its usecases (and their tasks) complete AND verified
                    AND  the epic itself verified
```

The blueprint therefore carries, per level, *who verifies* — the verifier is
never the worker (Part 2 §3). Where a level has no worker-and-verifier pair,
the blueprint has a gap.

## 3. Agents (Scenario B)

Four Scenario-B-specific agents plus the shared orchestrator execute Scenario B.
Same `agent/*.yaml` discipline as Part 2 §3: repository-independent, ≤8 goals,
backstory per goal, handoff fields, analysis-only skill bindings.

| Agent | Role (one sentence) | Handoff trigger → candidate | Key goals (≤8, abridged) |
|---|---|---|---|
| `orchestrator` | Coordinates a Scenario B run: takes the Domain System (and Scenario A's `gaps[]`), drives the analyser→planner→designer→gap-analyser chain, and produces the execution blueprint. | When a Task's capability needs a deeper read of an Agent System → `capability-analyser`; when the blueprint is assembled → report render. | Sequence the B pipeline; merge per-epic blueprints; ensure every Task is assigned or gapped; emit the blueprint with coverage/gap summary. |
| `capability-analyser` | Maps every Task's contract and `task_step`s to the concrete capabilities (concern + skill responsibilities) it requires. | When a mapping needs a registered-agent lookup → `assignment-planner`; on an unmappable Task → `gap-analyser`. | Parse a Task's input/output contract and step sequence; derive required capability per step; flag unmappable tasks. |
| `assignment-planner` | Assigns every Task to an agent: matches required capability → registered Agent System concern → agent whose Skill Bindings cover it. | When no agent binds the needed skill → `gap-analyser`; when the Task needs multi-agent sequence → `workflow-designer`. | Resolve capability→Agent System; match agent Skill Bindings; assign each Task to exactly one owning agent; record unassignable Tasks as gaps. |
| `workflow-designer` | For each assigned Task, emits the workflow: ordered skill invocations, per-step handoff conditions (by role), and the verification path certifying task/usecase/epic completion. | On an uncovered workflow step → `gap-analyser`; on a level whose verifier is missing → `gap-analyser`. | Emit per-Task workflows; chain handoffs into Epic-level sequences; pair every level with its verifier per Part 1 §3. |
| `gap-analyser` | Consolidates every unassigned/uncovered item into a gap report: missing Agent System concerns, missing skills, missing handoff roles, missing verifiers. | None (terminal of the B pipeline) → report to orchestrator. | Classify gaps (concern/skill/role/verifier); recommend new agents/skills to close them; rank by the volume of Tasks blocked. |

## 4. Skills (Scenario B)

Same bundle discipline as Part 2 §4 (`skill.yaml` + `prompt.md` + `examples/`,
optional `script.py`, single responsibility, `is_analysis_only: true`,
invocation contract). Scenario B reuses Part 2's three verification skills and
adds five:

| Skill | Responsibility (one sentence) | Invocation input → output | Path |
|---|---|---|---|
| `map-task-to-capability` | Derive the capability set (concern + skill responsibilities) a Task's contract and steps require. | `{task, task_steps[]}` → `{capabilities[]}` | Prompt |
| `propose-agent-assignment` | Assign a Task to an agent by matching its capabilities to registered Agent System concerns and that system's agents' Skill Bindings. | `{task, capabilities[], agent_systems[]}` → `{assignment, unassignable_reason?}` | Prompt + script |
| `design-handoff-workflow` | Emit a Task's workflow: ordered skill invocations, handoff conditions by role, and the verification path per Part 1 §3. | `{task, assignment, epics_context}` → `{workflow}` | Prompt |
| `identify-agent-gaps` | Consolidate unassigned/uncovered items into classified gaps with closure recommendations. | `{assignments, workflows}` → `{gaps[], recommendations[]}` | Prompt + script |
| `render-provisioning-report` | Render the execution blueprint: per-Epic coverage, per-Task assignment/workflow/verification, and the gap summary. | `{blueprint}` → `{report}` | Prompt + template |
| `verify-task-completion` / `verify-usecase-completion` / `verify-epic-completion` | (Reused from Part 2 §4 — the recursive completion semantics, verbatim.) | `{level, evidence}` → `{verdict, evidence}` | Prompt |

Agent→Skill bindings (allowlist, `schema/mcp/19-agent_skill_binding.sql`):

- `orchestrator` → `map-task-to-capability`, `render-provisioning-report`,
  `verify-epic-completion`
- `capability-analyser` → `map-task-to-capability`
- `assignment-planner` → `map-task-to-capability`, `propose-agent-assignment`
- `workflow-designer` → `propose-agent-assignment`, `design-handoff-workflow`,
  `verify-task-completion`, `verify-usecase-completion`, `verify-epic-completion`
- `gap-analyser` → `identify-agent-gaps`

## 5. Workflow (Scenario B)

```
orchestrator ─(Domain System + Scenario A gaps[])──▶
  capability-analyser ─map-task-to-capability──▶ capabilities per task
    ─▶ assignment-planner ─propose-agent-assignment──▶ assignments (task → agent)
      ─▶ workflow-designer ─design-handoff-workflow + verify-{task,usecase,epic}──▶ workflows
        ─▶ gap-analyser ─identify-agent-gaps──▶ gaps + recommendations
orchestrator ─render-provisioning-report──▶ execution blueprint (per-epic
  coverage, per-task assignment/workflow/verification, gap summary)
```

The blueprint's per-level rows look like (shape, not rust_dev output):

```
epic: <epic>
  usecase: <usecase>
    task: <task>
      assigned_agent: <role>
      skills: [<skill>…]
      handoff: {trigger: <condition>, candidate_role: <role>}
      verified_by: <verifier role>        # never the assigned agent
  usecase_verification: <verifier role>
epic_verification: <verifier role>
gaps: [{type: concern|skill|role|verifier, subject: …, blocked_tasks: N, recommendation: …}]
```

## 6. Acceptance criteria (Scenario B)

1. Content-root files per Part 1 §4 exist: `agent/{orchestrator,
   capability-analyser, assignment-planner, workflow-designer, gap-analyser}.yaml`
   and `skill/{map-task-to-capability, propose-agent-assignment,
   design-handoff-workflow, identify-agent-gaps, render-provisioning-report}/`
   bundles (plus Part 2's verification skills reused).
2. Agent/skill discipline identical to Part 2 §6 items 2-3 (goals/backstory/
   handoff fields; single responsibility, analysis-only, prompt + ≥1 example,
   invocation contract).
3. `map-task-to-capability`/`propose-agent-assignment`/`design-handoff-workflow`/
   `identify-agent-gaps` state the §2 model (per-Task assignment, capability
   resolution, role-based handoff, verifier-never-worker) as their
   responsibilities; the three verify-`{task,usecase,epic}` skills are shared
   with Part 2 and state Part 1 §3 verbatim.
4. Running Scenario B against `dharma/domain/system/dev/rust_dev/` assigns or
   gaps **every** one of the 82 usecases' Tasks, and — because that Domain
   System has 0 Tasks today and no `rust-development` Agent System registered —
   reports the known state as a classified gap set (Task-contract gaps,
   `required_capability` concern gaps), not as assignments of nothing.
5. Verification of the above programmatically against the live filesystem.

## 7. Open questions (Scenario B)

- **Orchestrator as both scenarios' coordinator.** Part 2 §3 and this part both
  define `orchestrator`. Whether it is one agent with two goal sets scoped by
  scenario, or two roles, is open — the series assumes one agent (one
  `agent.yaml`) whose goals cover both, and that A/B runs differ by invocation
  input, not by agent.
- **Where registered Agent Systems come from at run time.** The planner matches
  against "registered Agent Systems". Whether that read is `get_agent_system_info`
  per system, a `list_agent_systems` snapshot, or the consumer repo's synced
  `agent-summary.md` (proposal 11) is unverified against the execution model —
  default is the registry reads named in `docs/proposal/14`.
- **Gap-closure scope.** `gap-analyser` recommends new agents/skills; whether
  the recommendation is itself proposal-ready content (agent.yaml/skill.yaml
  drafts the Agent-Management Agent System could author) or just a gap list is
  open — the series assumes recommendations only.
- **Effect-capable future.** Scenario B currently assigns work it never runs
  (analysis-only). Whether a later concern of this Agent System (or a sibling)
  will *execute* blueprints is out of scope but flagged so the blueprint shape
  doesn't preclude it.

## 8. Non-Goals (Scenario B)

- Does not execute the Domain System's Tasks or run any of the assigned
  workflows — it designs and reports them.
- Does not register any Agent System, including `rust-development` (Part 1 §5,
  proposal 00 §7).
- Does not author new agents/skills to close the gaps it finds; it recommends.
- Does not modify the Domain System or any Agent System it analyses.
- Does not call any MCP tool live.

## 9. Traceability (Scenario B)

- Model sources: Part 1 §3 (recursion), Part 2 §4 (verification skills),
  `docs/proposal/01` (handoff policy, goals), `02` (Epic/Usecase/Task),
  `03` (skill single-responsibility), `04` (open registry, concern resolution),
  `07` (proposal gate, Handoff Broker, Completion Validator),
  `11` (agent summary / filtered agent copy), `14` (registry read tools),
  `schema/mcp/{01,12,13,14,19,08,09,10,11}.sql`.
- Input: Scenario A's report/gaps (Part 2); the Domain System being analysed
  (first target `dharma/domain/system/dev/rust_dev/`, commit `d8b029f`); the
  Task-contract gap state whose resolution is designed by this repo's
  `docs/proposal/01-rust_dev-task-contract-acceptance-criteria-proposal.md`
  (whose §7 carries the still-open `rust-development` Agent System
  registration gap this scenario's `gap-analyser` would flag).
- Feeds: authoring + `mcp__dharma__register_agent_system` execution once the
  three parts are finalized.
