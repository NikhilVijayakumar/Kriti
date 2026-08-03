# rust_dev/analyse — End-to-End Verification Proposal (Proposal 05)

## 0. Status

**Draft.** Runs *after* both systems this repo has built are actually registered with Dharma's MCP — `rust-dev-domain` (proposals 00-01) and `analyse` (proposals 02-04). Every prior proposal in this series verified its own artifact structurally (file counts, schema shapes, cross-references) but explicitly stopped short of calling `register_domain_system`/`register_agent_system` live (each one's own §8 Non-Goals). This proposal is the first to specify actually registering both, then running mock repositories through the real MCP tool flow to prove the two systems work *together*, end to end — not just that each is internally well-formed.

## 1. What prompted this

Owner's ask (paraphrased): once both the Domain System and Agent System are created and registered, verify them — use `/home/dell/PycharmProjects/Kriti/test` with mock repositories, A/B-testing several scenarios, to check whether the Domain System and Agent System actually work as expected. **Correction to this proposal's first draft:** only Dharma's own *generated* per-repo artifacts (the `.dharma/` sync output each mock repo's registration creates) are disposable and gitignored — the mock-repo fixtures themselves, and everything else under `test/`, are real, tracked test content, not scratch.

## 2. What exists today (confirmed live, this session)

- `test/dharma/{domain-system,agentic-system}/` already exist as empty directories — a skeleton, not yet populated. `.gitignore` now has `test/**/.dharma/` (fixed this session) — scoped to the generated sync artifact only, not the whole `test/` tree, per correction above.
- Both target systems are structurally complete and committed (verified last session): `dharma/domain/system/dev/rust_dev/` (13 maps, 136 profiles, `task.yaml`: 4 Epics, 82 Usecases, 82 Tasks, 0 `task_step`s), `dharma/agent/system/analyse/` (9 agents, 13 skill bundles), `dharma-domain.toml` and `dharma-agent.toml` at Kriti's root. **Neither is registered yet** — confirmed by design (every prior proposal's Non-Goals) and by this session's tool access: `mcp__dharma__register_domain_system`/`register_agent_system`/`register_repo`/`review_capability_manifest`/`assign_task`/`run_skill`/`repo_status`/`task_instance_status`/`sync_repo` are all available and callable, none have been called.
- `task.yaml`'s 82 Tasks have **0 `task_step` rows** (confirmed at the proposal 01 gold-check: `steps=0`) — so `task_step.required_capability` doesn't exist as data yet at all, not merely unresolved. This changes what a live run can actually exercise (see §5).
- `rust-development` (the concern rust_dev's `task_step`s would eventually name) is still unregistered — carried as an open item through proposals 00/01/03/04, unchanged.
- Considered and rejected as mock-repo material: `samgraha/system/dev/rust_dev/{repo_new,repo_existing,repo_existing_no_doc}/` — real fixture crates built for proposal 9's codegen script testing (tier1-8/plan structure, Rust build artifacts). Different concern (testing deterministic scripts against real crates) from this proposal's (testing Dharma's registration + analyse pipeline against a repo's *documentation* state) — reusing them would conflate two test suites for no shared benefit. Fresh, minimal mock repos are simpler and match this proposal's actual scope.

## 3. Preconditions — one-time registration, not part of the repeated per-scenario test

Before any mock repo runs, both systems must exist in `mcp.db` (once, not per scenario):

1. `register_domain_system(name="rust-dev-domain", version="0.1.0", description=<dharma-domain.toml's>, content_root="dharma/domain/system/dev/rust_dev")`.
2. `register_agent_system(name="analyse", concern="analysis", description=<dharma-agent.toml's>, content_root="dharma/agent/system/analyse", is_privileged_request=false)`.
3. Confirm both via `list_domain_systems`/`list_agent_systems` (or `get_domain_system_info("rust-dev-domain")`/`get_agent_system_info("analyse")` for the full tree) before proceeding.

This is real, live MCP state creation — the one thing every prior proposal deliberately deferred. It happens once; §5's per-scenario loop runs against the same registered pair repeatedly.

## 4. Proposed test layout under `test/` (tracked; only each mock repo's generated `.dharma/` is gitignored)

```
test/dharma/
├── domain-system/                       # mock repos, one per repo-state scenario
│   ├── mock-repo-new/                   # empty — no rust_dev docs at all (Epic repo-new)
│   ├── mock-repo-existing-with-docs/    # has some rust_dev docs already (Epic repo-existing, happy/corner path)
│   └── mock-repo-existing-no-docs/      # existing repo, zero docs (Epic repo-existing's edge case / bootstrap-readme)
└── agentic-system/                      # analyse's own output when run against each mock repo above
    ├── mock-repo-new/
    ├── mock-repo-existing-with-docs/
    └── mock-repo-existing-no-docs/
```

Three scenarios, not one, because `rust-dev-domain`'s own Epic split (proposal 00 §5 step 3) *is* a three-way distinction in practice even though it collapsed to two Epics structurally — `repo-existing` alone covers both "has docs" and "has no docs" internally (via `reconcile-{domain}`'s own corner/edge acceptance criteria, and `bootstrap-readme`). A real end-to-end test needs a fixture for each of the three conditions those acceptance criteria actually branch on, or the "no-doc case doesn't need its own Epic" design (proposal 00's decision) is never actually exercised.

`agentic-system/<mock>/` holds whatever `analyse` produces when pointed at that mock repo's registration — the verification report (Scenario A) and the execution blueprint (Scenario B) — so each scenario's expected-vs-actual is a direct file comparison, not something held only in a chat transcript.

## 5. Test procedure, per mock repo

1. `register_repo(repo_path=test/dharma/domain-system/<mock>, repo_name=<mock>, domain_system_name="rust-dev-domain")` → `repo_registration_id`, `status: 'pending'`.
2. `repo_status(repo_path)` → confirm the Default/Bootstrap Agent System proposed a Capability Manifest naming `analyse` (or record what it actually proposed, if not).
3. `review_capability_manifest(repo_path, agent_system_name="analyse", decision="approve", human_approved=true, reviewed_by=<owner>)` → triggers automatic sync (proposal 11/14).
4. `repo_status(repo_path)` again → confirm `synced_content` landed, manifest `approved`.
5. `assign_task(repo_path, task_ref=<a Task from rust-dev-domain appropriate to this scenario>)` — e.g. `propose-and-generate-vision` for `mock-repo-new`, `reconcile-vision` for `mock-repo-existing-with-docs`, `bootstrap-readme` for `mock-repo-existing-no-docs`. **Expected result: no eligible agent, reported as a gap** — `rust-development` isn't registered (§2), so this is the *correct* outcome to check for, not a failure to work around.
6. Invoke `analyse`'s own Scenario A/B skills against this mock repo's now-registered-and-synced `rust-dev-domain` (see §7's open question on the exact tool-call shape); write the output into `test/dharma/agentic-system/<mock>/`.
7. Compare against §6's acceptance criteria for this scenario.

## 6. Acceptance criteria (what a passing run looks like, per scenario)

**All three scenarios:**
- Scenario A's report reproduces the invariants already verified statically (13 maps, 136 profiles, 4 Epics, 82 Usecases, 82 Tasks) and additionally reports, as `gap` findings (not silent passes, not crashes): 0 `task_step`s per Task (§2 — there is nothing to resolve a `required_capability` from yet, a step-level gap, distinct from a concern-level gap), and every Task's `required_capability` dependency unresolved (`rust-development` unregistered).
- Scenario B's blueprint attempts to assign every one of the scenario-relevant Tasks and reports each as a gap for the same reason — `assign_task` (step 5) and Scenario B's `assignment-planner` should agree with each other on this, not diverge.

**`mock-repo-new` only:** the assigned/gapped Task set is drawn from Epic `repo-new`'s 13 Usecases.
**`mock-repo-existing-with-docs` only:** drawn from `repo-existing`'s `reconcile-{domain}` Usecases, and the mock repo's pre-existing (deliberately non-conformant, in at least one section) document surfaces a `corner_case`-shaped finding distinct from `mock-repo-existing-no-docs`'s `edge_case`-shaped one.
**`mock-repo-existing-no-docs` only:** `bootstrap-readme` is the Task exercised; no other domain document exists to reconcile against.

## 7. Open questions (named, not silently resolved)

- **How is a cross-cutting Agent System invoked at all, absent its own Domain System?** `assign_task`/`run_skill`/`task_instance_status` are all scoped to a Task Instance, and a Task Instance derives from a Domain System's own `task`/`epic`/`usecase` rows (`schema/repo/00-task_instance.sql`) — but `analyse` has no Epic/Usecase/Task of its own (Agent Systems don't carry that hierarchy; only Domain Systems do, per `docs/proposal/02-task-model.md`). Neither proposal 02, 03, nor 04 resolved how Scenario A/B's skills actually get invoked without a Task Instance to hang off of. Two candidates, neither verified: (a) `run_skill` against a `task_instance_id` that belongs to a `rust-dev-domain` Task (used only as a repo/context handle, `skill_ref` pointing at `analyse`'s skill regardless of whose Task Instance it is), or (b) some invocation path this series never named. §5 step 6 is written generically pending this answer — this is the single largest blocker to writing the exact tool-call sequence, bigger than the registration mechanics in §3.
- **Does `register_repo`'s `repo_path` need to be a real git repository, or any directory?** Unverified against the actual `services` crate implementation — the three mock repos (§4) are plain directories today; if a git repo is required, that's a one-line `git init` per mock repo, not a design change.
- **Minimal mock-repo content.** `mock-repo-existing-with-docs` needs "some rust_dev docs already, deliberately non-conformant in at least one section" (§6) — which domain, how non-conformant, and how many domains populated vs. missing is not specified here; left to whoever authors the fixtures, using `domain/profile/*/*.yaml`'s own `validation.rules` as the target to deliberately violate (same source proposal 01 used to author acceptance criteria).

## 8. Non-Goals

- Does not resolve the `rust-development` registration gap — expected to surface as a gap in every scenario's output (§6), not something this proposal fixes first.
- Does not automate the test procedure into a script — §5 specifies the MCP tool-call sequence; scripting it is separate follow-through.
- Does not author the mock repos' actual fixture content — layout only (§4); content authoring (especially `mock-repo-existing-with-docs`'s deliberately-non-conformant document) is separate work, per §7's open item.
- Does not resolve §7's Agent-System-invocation question — names it as this proposal's actual blocker, doesn't guess an answer to unblock §5 step 6 prematurely.

## 9. Traceability

- Depends on: Proposal 00 (`rust-dev-domain`, archived), Proposal 01 (Task contracts), Proposals 02-04 (`analyse`, live) — all structurally verified, none registered until this proposal's §3.
- Dharma tool surface used: `register_domain_system`, `register_agent_system`, `list_domain_systems`, `list_agent_systems`, `get_domain_system_info`, `get_agent_system_info`, `register_repo`, `repo_status`, `review_capability_manifest`, `sync_repo`, `assign_task`, `run_skill`, `task_instance_status` (`dharma/docs/proposal/14-mcp-tool-contract.md`).
- Feeds: whatever follow-up closes §7's invocation-mechanism question and §8's fixture-authoring gap; eventually, the `rust-development` Agent System registration this whole series has carried as open since proposal 00 §7.
