# analyse — Domain System Verification (Proposal 03 of 3: Scenario A)

## 0. Status

**Draft.** Part 2 of the 3-part `analyse` Agent System series. Part 1
(`02-analyse-agent-system-overview-proposal.md`) pins the system's two
scenarios, its recursive completion/verification semantics, its content-root
layout at `dharma/agent/system/analyse/`, and its `dharma-agent.toml`, plus the
series' source convention: `schema/mcp/*.sql` and `docs/proposal/*` references
resolve to `/home/dell/PycharmProjects/dharma/`. This
part designs **Scenario A — verify the Domain System**: the agents and skills
that check and validate a Domain System as an artifact, each and every domain,
its Section Maps, its Section Profiles, each Epic/Usecase/Task/Task-Step, and
the system as a whole. Design-only; nothing under `dharma/agent/system/analyse/`
is authored yet.

## 1. What Scenario A is for

A Domain System is a collection of Epics, Usecases, Tasks, Task-Steps, Section
Maps, and Section Profiles — declared content, captured into `mcp.db` and
synced into consuming repos. That content can be wrong in bounded, checkable
ways: a Section Map referencing a Section Profile that does not exist, a
Usecase whose Tasks don't cover its description, a Task with no Task-Steps or
an empty Acceptance Criteria set, an Epic whose Usecases don't add up to its
objective, a profile whose `validation.rules` reference sections the map
doesn't declare. Scenario A's agents and skills enumerate every such element of
a Domain System and check it against the model the Domain System itself is
supposed to satisfy (`docs/proposal/02`, `05`, `13`; `schema/mcp/{05..11}.sql`).

"Verify the domain system" is an enumerable job, not an open-ended review: the
subject is finite (13 domains, 13 maps, 136 profiles, 4 epics, 82 usecases,
0 tasks today for rust_dev), and each check is either satisfied (with evidence)
or not. The 0-Tasks/empty-contract state is exactly what `docs/proposal/
01-rust_dev-task-contract-acceptance-criteria-proposal.md` (this repo) designs
the fix for — Scenario A reports it; that proposal designs how to resolve it.
The verifier agents do not write to the Domain System; they produce a
verification report that says, per element, passed/failed plus the evidence
for the verdict. Scenario B (Part 3) then uses the same Domain System listing to
answer a different question (what agents/skills are needed to execute it) —
Scenario A and B are two scenarios of one Agent System, not two systems.

## 2. What a verifier checks (the enumeration, per artifact)

Every artifact below is enumerated from the Domain System's captured content
via `get_domain_system_info` (the full domain/section/section_profile/
epic/usecase/task tree, `docs/proposal/14-mcp-tool-contract.md`) and checked
against the schema shapes in `schema/mcp/{05..11}.sql`. The checklist is the
same one this proposal's acceptance criteria verify programmatically later:

**Domain level (`domain`, `schema/mcp/05-domain.sql`):**
- id/name resolvable, belongs to the Domain System, tier metadata consistent
  with the system's `SYSTEM.md` where carried.
- Every domain appears in exactly one Section Map; no domain has a map without
  profiles or profiles without a map entry.

**Section Map level (`section`, `schema/mcp/06-section.sql`):**
- `sections[]`: unique ids, non-decreasing `order`, single `parent_id`/`level`
  root (level-1, `parent_id = "root"` in the rust_dev projection), every
  `profile:` reference resolves to a real `section_profile` row of the same
  id/domain, `required`/`generated` consistent with the owning profile.
- Map-level `validation.{hierarchy,ordering,structure,required}` matches the
  actual section set (no field in the validation block contradicts the rows).

**Section Profile level (`section_profile`, `schema/mcp/07-section_profile.sql`):**
- `writing_objective`/`knowledge_goal`/`reader_goal` present; `required_inputs`,
  `expected_outputs`, `subsections`, `completion`, `review` structurally valid;
  `validation.rules` entries carry `id`/`condition`/`message`/`severity`/
  `weight`/`mandatory`/`evidence` (proposal 00 §4's pass-through shape).
- Every rule's target section/evidence reference resolves inside the map.

**Epic/Usecase/Task level (`epic`, `usecase`, `task`, `task_step`,
`schema/mcp/{08..11}.sql`):**
- Every Epic has an objective and ≥1 Usecase; every Usecase has ≥1 Task
  (proposal 00 §5 step 3: 0 Task nodes is an *invalid* state, not an empty
  one); every Task has a `task_step` sequence and an input/output contract;
  every `task_step.required_capability` resolves to a registered Agent System
  concern — unresolved = a gap (reported here, closed by Scenario B/Part 3).
- No orphaned Usecase (every Usecase's `epic_id` resolves), no orphaned Task,
  no Epic/Usecase/Task naming collision within the system.
- The recursive completion semantics of Part 1 §3 hold as *declared* structure:
  the system's own verify-`{task,usecase,epic}`-completion skills are present
  and the hierarchy they verify is the one declared here.

**System level:**
- The tree is internally consistent (counts reconcile: 13 maps ↔ 136 profiles,
  4 epics ↔ 82 usecases, every profile referenced exactly once — the exact
  invariants verified for rust_dev at commit `d8b029f`).
- `SYSTEM.md`/`dharma-domain.toml` declarations match the captured rows
  (`section_map` path, `domains`/`domain_exclusion` scope).

## 3. Agents (Scenario A)

Five agents execute Scenario A. Each is `agent/*.yaml` at the content root,
repository-independent (never names a specific Domain System or repo), and
binds only analysis-only skills. Per `schema/mcp/12-agent.sql` each carries
`role`, `handoff_trigger_condition`, `handoff_candidate_role`; per
`docs/proposal/01` each carries ≤8 numbered goals with a `backstory` entry per
goal.

| Agent | Role (one sentence) | Handoff trigger → candidate | Key goals (≤8, abridged) |
|---|---|---|---|
| `orchestrator` | Coordinates a Scenario A run: enumerates the Domain System, fans the elements out to the verifiers, collects verdicts, and produces the system-level verification report. | When the system-level checks exceed its scope → `domain-system-verifier`; when the run finishes → report render. | Enumerate the full domain/element set; dispatch each element to the right verifier; collect and merge verdicts; emit the system report with evidence. |
| `domain-system-verifier` | Verifies the Domain System as a whole (cross-domain invariants, `SYSTEM.md`/toml-vs-captured consistency, count reconciliation). | On a per-domain defect found → `domain-verifier`; on a profile-level defect → `section-verifier`. | Check cross-domain invariants; reconcile declared vs captured counts; aggregate per-domain verdicts into the system verdict. |
| `domain-verifier` | Verifies one domain end to end: its map ↔ profile set and the checks that apply to that domain as a unit. | On a section-map defect → `section-verifier`; on a hierarchy defect → `hierarchy-verifier`. | Confirm the domain's map and profile sets match; check the domain's tier/declaration metadata; hand profile rows to `section-verifier` and hierarchy rows to `hierarchy-verifier`. |
| `section-verifier` | Verifies Section Map and Section Profile content: id/order/parent refs, profile↔map agreement, `validation.rules` well-formedness. | On an epic/usecase/task row in scope (rules reference tasks) → `hierarchy-verifier`. | Check map `sections[]` invariants; check profile field presence and rule shape; resolve every `profile:`/evidence reference. |
| `hierarchy-verifier` | Verifies Epic/Usecase/Task/Task-Step structure: parent links, ≥1 Task per Usecase, task_step/contract presence, `required_capability` resolution. | On an unresolved `required_capability` → records the gap (Scenario B/Part 3 consumes it); no handoff. | Check epic/usecase/task parent chain; check task contract + task_step completeness; flag unresolved capability concerns as gaps. |

The orchestrator is Scenario A's "agent reviewed to manage all" (Part 1 §1):
every verifier reports to it, and it owns the merged report. No verifier
self-certifies — each lower verifier's verdict is evidence input to the next
level's verdict, exactly as Part 1 §3's recursion requires.

## 4. Skills (Scenario A)

Each skill is a `skill/<name>/` bundle (`skill.yaml` + `prompt.md` + `examples/`,
optional `script.py`), single-responsibility, `is_analysis_only: true`, with an
invocation contract in `invocation_input_json`/`invocation_output_json`. The
`script.py` path is where deterministic checks (order monotonicity, reference
resolution, count reconciliation) can later be authored without changing any
prompt — the prompt is the mandatory, always-present path.

| Skill | Responsibility (one sentence) | Invocation input → output | Path |
|---|---|---|---|
| `analyse-domain-system` | Enumerate and parse a Domain System into a normalized element list (domains, maps, profiles, epics, usecases, tasks, steps). | `{domain_system}` → `{elements, counts}` | Prompt; optional script later |
| `verify-section-map` | Check a domain's Section Map against the map invariants (unique ids, ordered, root links, resolvable profile refs, validation-block agreement). | `{map}` → `{verdict, findings[]}` | Prompt + script |
| `verify-section-profile` | Check one Section Profile's field shape and rule well-formedness, and resolve its references. | `{profile, map}` → `{verdict, findings[]}` | Prompt + script |
| `verify-epic-usecase-task` | Check one Epic's subtree (epic→usecases→tasks→steps): parent chain, ≥1 Task per Usecase, contract/step completeness, capability resolution. | `{epic}` → `{verdict, findings[], gaps[]}` | Prompt + script |
| `verify-task-completion` | Evaluate the recursive leaf: a Task is complete ⟺ every task_step is complete and the task's output meets its Output Contract/Acceptance Criteria. | `{task, evidence}` → `{verdict, evidence}` | Prompt |
| `verify-usecase-completion` | Evaluate: a Usecase is complete ⟺ all its Tasks are complete and verified and the usecase itself is fully verified. | `{usecase, task_verdicts[]}` → `{verdict, evidence}` | Prompt |
| `verify-epic-completion` | Evaluate: an Epic is complete ⟺ all its Usecases (and their Tasks) are complete and verified and the epic itself is verified. | `{epic, usecase_verdicts[]}` → `{verdict, evidence}` | Prompt |
| `render-verification-report` | Render the merged per-domain + system-level verification report from collected verdicts. | `{verdicts}` → `{report}` | Prompt + template |

Agent→Skill bindings (the allowlist, `schema/mcp/19-agent_skill_binding.sql`):

- `orchestrator` → `analyse-domain-system`, `render-verification-report`,
  `verify-epic-completion`
- `domain-system-verifier` → `verify-epic-usecase-task` (system scope),
  `analyse-domain-system`
- `domain-verifier` → `verify-section-map`, `verify-epic-usecase-task`
- `section-verifier` → `verify-section-map`, `verify-section-profile`
- `hierarchy-verifier` → `verify-epic-usecase-task`, `verify-task-completion`,
  `verify-usecase-completion`, `verify-epic-completion`

## 5. Workflow (Scenario A)

```
orchestrator ─analyse-domain-system─▶ element list
  └─ per domain ─▶ domain-verifier
        ├─ section-verifier ─verify-section-map/verify-section-profile─▶ verdicts
        └─ hierarchy-verifier ─verify-epic-usecase-task─▶ task/usecase/epic
           completion verdicts (verify-{task,usecase,epic}-completion)
  domain verdicts ─▶ domain-system-verifier ─system invariants─▶ system verdict
  orchestrator ─render-verification-report─▶ report (per-domain + system-level)
```

Every verdict carries evidence (which map row, which profile field, which
task_step), in the audit-style `{id, condition, message, severity, weight,
mandatory, evidence}` shape rust_dev's profiles already carry (proposal 00 §4).
A failed check is either a defect (fixable in the Domain System) or a gap
(unresolved `required_capability`, missing Task contract) that Scenario B is
designed to address — the report tags each finding `defect` or `gap`.

## 6. Acceptance criteria (Scenario A)

1. Content-root files per Part 1 §4 exist: `agent/{orchestrator,
   domain-system-verifier, domain-verifier, section-verifier,
   hierarchy-verifier}.yaml` and `skill/{analyse-domain-system,
   verify-section-map, verify-section-profile, verify-epic-usecase-task,
   verify-task-completion, verify-usecase-completion, verify-epic-completion,
   render-verification-report}/` bundles.
2. Every agent: `role`, ≤8 numbered `goal`s, `backstory` per goal,
   `handoff_trigger_condition`, `handoff_candidate_role`; every binding in §4's
   allowlist resolves to a skill bundle that exists in the tree.
3. Every skill: exactly one `responsibility`, `is_analysis_only: true`, a
   `prompt.md`, ≥1 `examples/` entry, `invocation_input_json`/
   `invocation_output_json` matching §4's table.
4. The three verify-`{task,usecase,epic}`-completion skills state Part 1 §3's
   recursion verbatim as their responsibility.
5. Running the Scenario A workflow against `dharma/domain/system/dev/rust_dev/`
   reproduces the invariants verified at `d8b029f` (13 maps ↔ 136 profiles, 4
   epics ↔ 82 usecases, every profile referenced exactly once) and reports the
   known open items (0-task usecases, unresolved `required_capability` concerns)
   as `gap` findings, not silent passes.
6. Verification of the above programmatically against the live filesystem.

## 7. Open questions (Scenario A)

- **Where findings land.** Scenario A produces a report as its output contract;
  whether the orchestrator additionally writes it into a consumer repo's
  `.dharma/` (like `agent-summary.md` in proposal 11) or returns it as the run's
  output is unverified against the Task execution model — left open, default is
  run output.
- **Script-vs-prompt split per check.** Which of the §4 checks get a
  `script.py` first (deterministic: order/reference/count) vs. stay prompt-only
  is an authoring decision deferred to execution.
- **Duplicate with proposal 00's audit model.** The Domain System's own section
  profiles carry `validation.rules` (audit-style). Scenario A verifies the
  *declaration* (that the rules exist and are well-formed), not the *content* of
  a repository's documents (that the rules pass against real docs — Dharma's
  audit subsystem, schema 20-25, which proposal 00 deliberately does not use).
  Whether Scenario A should also invoke `run_audit` when available is open.

## 8. Non-Goals (Scenario A)

- Does not verify the *content quality* of documents a consuming repo produced —
  only the Domain System declaration (what proposal 00 built).
- Does not fix defects it finds; it reports them (fixing is Domain System
  authoring, the Agent-Management Agent System's write path).
- Does not author or register agents/skills beyond Scenario A's five.
- Does not call any MCP tool live.

## 9. Traceability (Scenario A)

- Source of the checklist: `schema/mcp/{05,06,07,08,09,10,11}.sql`,
  `docs/proposal/{02,05,13}` in `dharma`; proposal 00 §4/§5 (profile pass-through
  shape, 0-Tasks-invalid rule, profile-default-none).
- Source of the verification-semantics skills: Part 1 §3.
- Consumed by: Scenario B (Part 3) reads this scenario's `gaps[]` as its
  starting input. Subject: `dharma/domain/system/dev/rust_dev/` (commit
  `d8b029f`).
