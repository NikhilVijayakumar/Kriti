# analyse — Agent System Proposal (Proposal 02 of 3: Overview & Design)

## 0. Status

**Draft.** Design-only — no agents, no skills, no content under
`dharma/agent/system/analyse/` yet, nothing registered against Dharma's MCP.
This is the first proposal in a 3-part series for a single new Agent System,
`analyse`, which Kriti will provide to Dharma's MCP the same way it provides
the `rust-dev-domain` Domain System (proposal 00, archived; content committed
at `dharma/domain/system/dev/rust_dev/`). Part 2 (`03-analyse-domain-system-
verification-proposal.md`) designs the Domain-System-verification scenario's
agents and skills; Part 3 (`04-analyse-agent-system-provisioning-proposal.md`)
designs the agent-system-identification scenario's agents, skills, and
assignment/handoff workflow. This part pins what the Agent System *is* — its
two scenarios and the recursive completion/verification semantics both
scenarios run on — plus its content-root layout and `dharma-agent.toml`.

## 1. What prompted this

Owner's ask (paraphrased): create an Agent System at
`Kriti/dharma/agent/system/analyse` that can analyse a given Domain System and
(1) verify it, and (2) identify the agents and skills required to complete the
Domain System's work — the workflow of agents performing each task, the
handoffs between agents, and assignment "from epic to usecase to task",
assigning everything to one or another agent. Each agent must know what it
needs to do and how to proceed, complete, and verify a task. A task is complete
once all of its steps are complete and it is verified; a usecase is complete
once all its tasks are complete and the usecase itself is fully verified; an
epic is complete once all its usecases and tasks are complete, verified, and the
epic itself is verified. The system should identify the agents needed to manage
all of this, assign work to the relevant agents, get the work done, verify it,
and define the skills needed. In this way the analyse Agent System identifies
gaps in the agent capability available for a domain. A second, closely-related
set of agents checks and validates the Domain System itself — each and every
domain, each and every epic, usecase, task, and everything inside the Domain
System (section maps, section profiles), since a Domain System is itself a
collection of agents and tasks.

## 2. What exists today (traced against live files)

**Source convention.** Unless this series says otherwise, every `schema/mcp/*.sql`
and `docs/proposal/*` reference resolves to the Dharma source project at
`/home/dell/PycharmProjects/dharma/` — not to this repo, whose `docs/proposal/`
holds only the rust_dev/analyse proposal series. `dharma/domain/system/dev/
rust_dev/` and proposal 00 references resolve in this repo.

**Dharma's Agent System model** (read directly from `dharma`, not assumed):

- `schema/mcp/01-agent_system_registry.sql`: one row per Agent System (`name`
  UNIQUE, `concern` UNIQUE, `description`, `is_privileged`). `concern` is the
  foreign-key target of `task_step.required_capability` (`schema/mcp/11-task_step.sql`)
  — so the concern string an Agent System registers is what a Domain System's
  Tasks name when they need it.
- `schema/mcp/12-agent.sql`: one Agent System's agents. `agent.name` is unique
  **per Agent System**, not globally. Fields: `role`, `handoff_trigger_condition`,
  `handoff_candidate_role` (free text, fuzzy-matched at handoff time), plus the
  `agent.yaml` capture. `schema/mcp/13-agent_goal.sql` holds the numbered goals
  (`CHECK (goal_order BETWEEN 1 AND 8)` — the eight-goal cap from
  `docs/proposal/01-agent-model.md`).
- `schema/mcp/14-skill.sql`: `name` (unique per Agent System), `responsibility`,
  `is_analysis_only` (checked by the Proposal Loop before any effect, per
  `docs/proposal/07-proposal-execution-protocol.md`), `invocation_input_json`/
  `invocation_output_json` (JSON Schema). Assets live in 15-18: `skill_prompt`
  (mandatory `.md`), `skill_script` (optional `.py`), `skill_example` (mandatory
  ≥1), `skill_template` (optional). `schema/mcp/19-agent_skill_binding.sql` is
  the Agent→Skill allowlist. Per `docs/proposal/03-skill-model.md`: a Skill has
  exactly one responsibility, must not reference a specific Task or repository
  domain by name, and every Skill is reachable through a mandatory Prompt path.
- `config.example/dharma-agent.toml`: an Agent System provider declares itself
  at its own repository root via `[agent_system]` (`name`, `concern`,
  `description`, `is_privileged_request`) + `[agent_system.content]`
  (`root_dir = "${DHARMA_AGENT_CONTENT_DIR}"`) + `[agent_system.mcp]`
  (`mcp_dir = "${DHARMA_MCP_DIR}"`) + `[repository.ignore]`.
- `docs/proposal/04-agent-system-registry.md`: Agent Systems are an **open
  registry** — any concern, not a fixed taxonomy. The default/bootstrap Agent
  System is the privileged one invoked first at repo registration; the
  Agent-Management Agent System is the privileged writer. This proposal's
  `analyse` Agent System is a concern-specific, non-privileged entry.
- `docs/proposal/07-proposal-execution-protocol.md`: every Task passes a
  mandatory Propose → Review → Approve gate (Proposal Loop, analysis-only
  Skills) before the Execution Loop (handoff chain, Completion Validator).
  Handoffs go through the Handoff Broker, which resolves a target Agent by
  role/policy — an Agent cannot self-assign its successor.
- `config.example/dharma-agent.toml` names `rust-development` as the worked
  example concern. **Not registered anywhere yet** — `dharma list_agent_systems`
  shows none (confirmed live, this session's earlier registry listing).
  `task_step.required_capability` is therefore an open gap for the rust_dev
  Domain System (proposal 00 §7), which this series does **not** close — the
  analyse Agent System is a *cross-cutting* concern, not the `rust-development`
  one rust_dev's task_steps will eventually name.

**Kriti's side** (traced live):

- `dharma/domain/system/dev/rust_dev/` exists and is committed (`d8b029f`):
  13 `domain/map/*-map.yaml`, 136 `domain/profile/<domain>/<section>.yaml`,
  `task.yaml` with 4 Epics (`repo-new` 13, `repo-existing` 14,
  `document-maintenance` 52, `cross-domain` 3 = 82 usecases, 0 tasks), no
  shared profile-default, `SYSTEM.md` carried over unmodified. This is the
  first concrete artifact the `analyse` Agent System will analyse.
- `dharma/agent/system/analyse/` **exists but is empty** — no content yet
  (`agent/`, `skill/`, `SYSTEM.md`, `dharma-agent.toml` all still to be
  authored). The path is the proposed content root for this proposal.
- Kriti's root has no `dharma-agent.toml`. It has `dharma-domain.toml`
  (proposal 00's deliverable, committed) — an Agent System provider config
  would sit beside it at the same root.

## 3. The core model: two scenarios, one recursive completion/verification semantics

The `analyse` Agent System serves one concern — **analysis** — with two
scenarios that are the same kind of work pointed at two different subjects:

**Scenario A — verify the Domain System.** Check and validate a Domain System
as an artifact: each and every domain, its Section Map, each Section Profile,
each Epic, each Usecase, each Task (and `task_step`), and the system as a
whole. A Domain System is itself a collection of Epics/Usecases/Tasks and
section content, so "verify the domain system" is a bounded, enumerable job —
nothing open-ended about it. Output is a per-domain verification report that
says what passed, what failed, and with what evidence. (Designed in Part 2.)

**Scenario B — provision the agent capability to do the Domain System's
work.** Given a Domain System, identify every agent and skill required to
execute its Epics/Usecases/Tasks, assign each Task to one or another agent,
define each agent's workflow (what it does, how it proceeds, how it completes
and verifies), define the handoff chains between agents, and report gaps in
the registered Agent System set — concerns no agent satisfies, skills no agent
binds, usecases no workflow covers. (Designed in Part 3.)

Both scenarios run on the same recursive completion/verification semantics,
which is the spine of the whole Agent System. It is recursive from the leaves
up, so "complete" is always *defined by a verifier at the same level*, never
by self-certification from the worker:

```
task is complete     ⟺ every task_step is complete  AND  the task's output meets
                       its Output Contract / Acceptance Criteria  (verified)
usecase is complete  ⟺ all its tasks are complete AND verified  AND  the usecase
                       itself is fully verified (its user-facing capability is
                       actually delivered — a check above the sum of its tasks)
epic is complete     ⟺ all its usecases (and their tasks) are complete AND
                       verified  AND  the epic itself is verified (its
                       domain-wide objective is actually satisfied)
```

Consequences the rest of this series treats as constraints:

1. **Verification is a distinct act at every level, and distinct agents do
   it.** The agent that performs a task's steps does not certify that task
   complete; a verifier agent does. The usecase verifier is not the usecase's
   worker; the epic verifier is not the epic's worker. This mirrors
   `docs/proposal/07`'s Completion Validator ("structurally independent of every
   executing Agent") and proposal 00's audit-style evidence rule: every verdict
   carries evidence.
2. **A level cannot claim completion while a lower level is open.** An epic is
   not partially complete because its usecases are done — it is either complete
   (all usecases complete and verified, epic verified) or not.
3. **Assignment is per-Task and bottoms out in capabilities.** The planner
   assigns every Task in the Domain System — "everything to one or another
   agent" — by matching the Task's (and its `task_step`'s) required capability
   against the concerns of registered Agent Systems and the Skill Bindings of
   registered agents. An unassignable Task is a *gap*, not a skipped item.
4. **Handoffs are structural.** A workflow is a chain of agent turns linked by
   handoff conditions, resolved by the Handoff Broker against
   `handoff_candidate_role` — never a worker's own choice of successor
   (proposal 07). Part 3's workflow designer emits these chains.

## 4. Proposed content-root layout

`dharma/agent/system/analyse/`, mirroring how proposal 00 laid out the Domain
System content root and how `config.example/dharma-agent.toml` expects an agent
content root to be walked (capture flow → `content_asset`, schema 02):

```
dharma/agent/system/analyse/
├── agent/
│   ├── orchestrator.yaml            # Scenario A+B coordinator: manages the whole
│   │                                #   analyse run, assigns/verifies at every level
│   ├── domain-system-verifier.yaml  # Scenario A: system-level verification
│   ├── domain-verifier.yaml         # Scenario A: per-domain verification
│   ├── section-verifier.yaml        # Scenario A: Section Map + Section Profile checks
│   ├── hierarchy-verifier.yaml      # Scenario A: Epic/Usecase/Task/Task-Step checks
│   ├── capability-analyser.yaml     # Scenario B: Task → required capability mapping
│   ├── assignment-planner.yaml      # Scenario B: assign every Task to an agent
│   ├── workflow-designer.yaml       # Scenario B: agent workflows + handoff chains
│   └── gap-analyser.yaml            # Scenario B: missing agents/skills/workflows
├── skill/
│   ├── analyse-domain-system/       # Scenario A entry: enumerate + parse a Domain System
│   │   ├── skill.yaml               #   responsibility, invocation contract, is_analysis_only
│   │   ├── prompt.md                #   mandatory semantic path
│   │   └── examples/…               #   mandatory ≥1 worked example
│   ├── verify-section-map/ …        # Scenario A skills (Part 2 pins each)
│   ├── verify-section-profile/ …
│   ├── verify-epic-usecase-task/ …
│   ├── verify-task-completion/ …    # the recursive completion semantics, one skill per level
│   ├── verify-usecase-completion/ …
│   ├── verify-epic-completion/ …
│   ├── map-task-to-capability/ …    # Scenario B skills (Part 3 pins each)
│   ├── propose-agent-assignment/ …
│   ├── design-handoff-workflow/ …
│   └── identify-agent-gaps/ …
└── SYSTEM.md                        # analyse-system declaration (mirrors rust_dev convention)
```

Rules carried from the Dharma model, applied to every file in that tree:

- `agent/*.yaml` shape per `docs/proposal/08` §Agents: `role`, numbered `goal`
  list (≤ 8), `backstory`, plus `handoff_trigger_condition` and
  `handoff_candidate_role`. No agent names a specific repository or Domain
  System (`docs/proposal/01` hard constraint — repository-independence).
- `skill/<name>/` is a bundle: `skill.yaml` (single responsibility, mandatory
  Prompt path, optional Script, mandatory ≥1 Example, optional Template,
  `is_analysis_only`, `invocation_input_json`/`invocation_output_json`),
  `prompt.md`, optional `script.py`, `examples/`. No skill names a specific Task
  or repository domain (`docs/proposal/03` hard constraint).
- Both the verifier agents (Scenario A) and the provisioning agents
  (Scenario B) bind **analysis-only** skills — none of this Agent System does
  effect-capable work. It produces reports, assignments, and gap lists; it
  never mutates the Domain System or an Agent System it analyses.

## 5. `dharma-agent.toml` (new file, Kriti repo root)

Same shape as `config.example/dharma-agent.toml`, with the analyse values and
the domain-exclusion-style convenience keys proposal 00 added to its toml for
the same reason (testing a subset of the 13 domains during Kriti's own dev):

```toml
[agent_system]
name = "analyse"
concern = "analysis"
description = "Agents and skills that analyse a Domain System: verify it end to end (each domain, section map/profile, epic/usecase/task) and identify the agent/skill capability needed to execute its work, with per-level assignment, workflow, and gap reporting."
is_privileged_request = false

[agent_system.content]
root_dir = "${DHARMA_AGENT_CONTENT_DIR}"
# Optional dev/test scoping of the analysed domain set, mirroring
# dharma-domain.toml's `domains`/`domain_exclusion` (proposal 00 §6).
domains = []
domain_exclusion = []

[agent_system.mcp]
mcp_dir = "${DHARMA_MCP_DIR}"

[repository.ignore]
patterns = [
    "**/node_modules/**",
    "**/.git/**",
    "**/target/**",
]
```

`concern = "analysis"` is a deliberate choice: it must be UNIQUE in
`agent_system_registry` and is what `task_step.required_capability` would name
if a Domain System's task_step needed this Agent System. It is **not**
`rust-development` — that concern, which rust_dev's future Tasks will name, is a
separate, still-unregistered Agent System (proposal 00 §7) and is a non-goal
here.

## 6. Acceptance criteria (stated so the series is verifiable at a glance)

1. 1 `dharma-agent.toml` at Kriti root with `name = "analyse"`,
   `concern = "analysis"`, `is_privileged_request = false`,
   `root_dir = "${DHARMA_AGENT_CONTENT_DIR}"` (§5).
2. A populated content root at `dharma/agent/system/analyse/`: ≥ 9 `agent/*.yaml`
   (orchestrator + the Scenario A and Scenario B agents above), one `skill/`
   bundle per skill, every agent's Skill Bindings resolvable to a bundle that
   exists in that tree, every skill bundle carrying a `prompt.md` and ≥1
   `examples/` entry, and a `SYSTEM.md`.
3. Every agent carries `role`, ≤ 8 numbered `goal`s, a `backstory` entry per
   goal, and the two handoff fields; every skill declares exactly one
   `responsibility`, an invocation contract, and `is_analysis_only: true`
   (Part 2/Part 3 name the full lists).
4. The recursive completion semantics of §3 are stated in the system's own
   content — one verify-`{task,usecase,epic}`-completion skill each — and are
   used by both scenarios' workflows.
5. No agent or skill references a specific repository or Domain System by name
   (repository-independence); no skill is effect-capable.
6. Verification of the series' claims against the live filesystem, in the same
   style proposal 00's verification ran: counts, names, and reference-resolves
   checked programmatically, not eyeballed.

## 7. Open questions (named, not silently resolved)

- **`dharma-agent.toml` `domains`/`domain_exclusion` keys.** Proposal 00 added
  these beyond the pinned example for a provider-facing reason; the analyse
  Agent System is a *consumer* of domain content it analyses, not a domain
  provider, so the keys' semantics here are "which domains the analyse run
  considers", which is arguably run-scope, not provider-config. Whether they
  belong in `dharma-agent.toml` or in the orchestrator's invocation input is
  open — the example in §5 includes them pending that answer.
- **Skill bundling detail.** Whether each skill bundle needs a single
  `skill.yaml` manifest file with the invocation contract (this series assumes
  yes, matching the `content_asset`-traceable capture in schema 14-18) or
  whether the capture flow derives those fields from the prompt/example files
  alone is unverified against the capture code — same class of unknown
  proposal 00 §7 flagged for `section_map`.
- **Registration timing.** This series designs and (Parts 2/3) specifies
  content; it does not call `mcp__dharma__register_agent_system` (a separate,
  gated execution step), mirroring proposal 00 §8.
- **`SYSTEM.md` content.** Whether `dharma/agent/system/analyse/SYSTEM.md` is a
  plain declaration (`[system] id = "analyse"`, scenario list) or carries
  something more, given there is no samgraha-facing `analyse` system to carry
  over from (unlike rust_dev's), is left to Part 2/3; §4 shows it as present
  but its exact shape is open.

## 8. Non-Goals

- Does not author or register the `rust-development` (or equivalent) Agent
  System that rust_dev's future `task_step.required_capability` values will
  name — a separate registration (proposal 00 §7).
- Does not create the content under `dharma/agent/system/analyse/` — Part 2 and
  Part 3 specify it; execution (authoring + `register_agent_system`) is gated on
  this design being finalized, as in proposal 00.
- Does not modify anything under `samgraha/` or `dharma/domain/system/dev/rust_dev/`
  — the analyse Agent System reads Domain Systems; it never writes to them.
- Does not call any MCP tool live.

## 9. Traceability

- Depends on, and must stay consistent with: Dharma `docs/proposal/01-agent-model.md`
  (role/goals/backstory/handoff, eight-goal cap), `03-skill-model.md` (single
  responsibility, prompt mandatory, analysis-only), `04-agent-system-registry.md`
  (open registry, non-privileged concern entry), `07-proposal-execution-protocol.md`
  (mandatory proposal gate, Handoff Broker, independent Completion Validator),
  `08-schema-and-crate-architecture.md` (§Agents/§Skills captured shapes),
  `11-provider-config-and-repo-sync.md` (`dharma-agent.toml`), `14-mcp-tool-contract.md`
  (`register_agent_system`, `get_agent_system_info`), and `schema/mcp/{01,12-19}.sql`.
- Source artifact analysed by this system (first target): Kriti
  `dharma/domain/system/dev/rust_dev/` (proposal 00, commit `d8b029f`).
- Feeds: Part 2 (`03-...verification-proposal.md`), Part 3
  (`04-...provisioning-proposal.md`), and eventual authoring +
  `mcp__dharma__register_agent_system` execution once both have produced real
  content under `dharma/agent/system/analyse/`.
