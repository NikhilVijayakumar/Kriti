# rust_dev — Task Contract & Acceptance Criteria Proposal (Proposal 01)

## 0. Status

**Draft.** Follow-up to Proposal 00 (`docs/proposal/archive/00-rust_dev-dharma-domain-system-proposal.md`, archived — implementation complete: `dharma/domain/system/dev/rust_dev`'s `domain/map/` (13 files), `domain/profile/` (136 files), `task.yaml` (4 Epics, 82 Usecases, 0 Tasks), and `dharma-domain.toml` all exist and verify clean). Proposal 00's own §5 step 3 / §7 / §8 named the gap this proposal addresses: every Usecase needs at least one `task` row with a populated `input_contract_json`/`output_contract_json`/`acceptance_criteria_json` before `task.yaml`'s content is valid against Dharma's schema at all — `dharma/schema/mcp/10-task.sql` makes these three fields NOT NULL, and `acceptance_criteria_json` requires ≥1 entry in *each* of `happy_path`/`corner_case`/`edge_case`. Nothing in Samgraha supplies this data — no `standard.yaml` usecase carries a contract or acceptance criteria in any form — so this is fresh authored content, not a port. Design only, no schema/code, no Task content actually authored yet.

## 1. What prompted this

Confirmed live: `task.yaml` currently has 82 Usecases and 0 Tasks — a schema-invalid state if registered against Dharma as-is (`task.usecase_id` requires at least implicitly that a Usecase have *some* executable content; more directly, a Usecase with zero Tasks has nothing a Task Runtime could ever assign). Proposal 00 explicitly deferred this (§8: "Does not author the actual Task ... content ... real, mandatory authoring work this design proposal names ... but does not perform"). This proposal designs *how* that authoring should happen — the contract shape, the reusable pattern behind the 82 Usecases, and the source material already available to build from — before anyone starts writing 82 (or, per §4 below, 6) JSON Schema documents by hand with no plan.

**Source convention.** Every `schema/mcp/*.sql`, `schema/repo/*.sql`, and `docs/proposal/*` reference in this document resolves to the Dharma source project at `/home/dell/PycharmProjects/dharma/`, not to this repo (whose `docs/proposal/` holds only the rust_dev/analyse proposal series) — same convention the `analyse` series (02-04) states explicitly; added here since this document predates that series and never carried it.

## 2. What exists today (confirmed live, this session)

- `task.yaml`'s 82 Usecases are **not 82 independent problems** — they collapse into 6 parameterized archetypes (13 domains each = 78) plus 4 standalone Usecases:
  - `propose-and-generate-{domain}` × 13 (Epic `repo-new`)
  - `reconcile-{domain}` × 13 (Epic `repo-existing`)
  - `generate-document-{domain}` × 13, `deterministic-audit-{domain}` × 13, `semantic-audit-{domain}` × 13, `fix-{domain}` × 13 (Epic `document-maintenance`, 52)
  - `bootstrap-readme` (Epic `repo-existing`), `calculate`, `render-report`, `render-charts` (Epic `cross-domain`) — 4 standalone
- Rich per-domain source material already exists, produced by Proposal 00's own work:
  - `domain/map/<domain>-map.yaml` — per-section `id`/`title`/`required`/`generated`/`source`/`profile`/`purpose`.
  - `domain/profile/<domain>/<section>.yaml` — `writing_objective`, `completion.checklist`, and `validation.rules[]` (each rule: `id`/`condition`/`message`/`severity`/`weight`/`mandatory`/`evidence`) — read directly off `domain/profile/vision/purpose.yaml` this session: 4 rules, 3 `mandatory: true` / `severity: error`, 1 `mandatory: false` / `severity: warning`. This is a direct, ready-made source for acceptance criteria.
  - `knowledge_goal`/`reader_goal` are still **authored placeholders** in every profile (Proposal 00 §5 step 2's honesty framing, e.g. `"Authored placeholder - no source exists in the rust_dev standard for this field..."`) — a real dependency this proposal inherits, not something proposal 00 finished.
  - `samgraha/system/dev/rust_dev/00-domain-relationships.md`'s derivation chain (`vision` → `philosophy` → `security`/`feature` → `architecture`/`engineering` → `feature-technical` → `implementation` → `build`; `qa` validates `implementation`) names exactly which upstream documents a `propose-and-generate-{domain}`/`reconcile-{domain}` Task's input should require.
  - `samgraha/system/dev/rust_dev/common/calculation/summary/final_score.yaml`'s `weighted_sum` formula (25/25/25/25 across deterministic/semantic × whole/section) is a direct, ready-made source for `calculate`'s contract.
- Confirmed: no `standard.yaml` usecase, anywhere, carries an input contract, output contract, or acceptance criteria in any field. This proposal's content has no Samgraha precedent to derive from or verify against — it must be judged on its own reasoning, not checked against a source file the way Proposal 00's Map/Profile side could be.

## 3. Task contract shape (per `dharma/schema/mcp/10-task.sql`, `dharma/docs/proposal/02-task-model.md`'s Hard Constraints)

- `input_contract_json` / `output_contract_json`: JSON Schema documents, validated by the `schemas` crate (proposal 08) at write time — not free text.
- `acceptance_criteria_json`: `{ happy_path: [...], corner_case: [...], edge_case: [...] }` — each array needs ≥1 entry; the `schemas` crate rejects a Task missing any of the three.
- `template_ref`: optional (an Agent may substitute its own template) — not populated by this design; no Domain-System-suggested template exists to reference.

## 4. Proposed authoring pattern — one contract template per archetype, instantiated per domain

Rather than 82 independently-authored Tasks, this proposal designs 6 parameterized templates (each instantiated once per domain, using that domain's own `domain/map`/`domain/profile` content as parameters) plus 4 standalone Tasks:

1. **`propose-and-generate-{domain}`** (greenfield)
   - *Input:* a new repository's path, plus the upstream documents `00-domain-relationships.md` names for `{domain}` (empty for `vision`, the root).
   - *Output:* a document conforming to `domain/map/{domain}-map.yaml`'s required sections.
   - *Acceptance:* **happy** — every required section present, every `mandatory: true` rule in that section's profile passes. **corner** — a `mandatory: false` rule fails (e.g. `vis-sec-purpose-004`, severity `warning`) but the document still generates. **edge** — an upstream document this domain derives from is itself missing or non-conformant; the Task must fail closed, not generate against an invalid upstream.

2. **`reconcile-{domain}`** (brownfield)
   - *Input:* an existing repository's path and this domain's current document state, if any.
   - *Output:* same shape as `propose-and-generate-{domain}`.
   - *Acceptance:* **happy** — document exists, every mandatory rule already passes (no-op, verified compliant). **corner** — document exists but fails one or more mandatory rules (routes to `fix-{domain}`). **edge** — document doesn't exist at all — same handling as `propose-and-generate-{domain}`'s edge case, generated from scratch. This is exactly the "existing repo, may or may not have this doc" condition Proposal 00 §5 step 3 assigned to one Task rather than a separate Epic — this is where that condition actually gets handled.

3. **`generate-document-{domain}`** (the atomic operation `document-maintenance` owns) — same output contract as #1/#2; narrower input (just the upstream documents, no repo-state branching) — the reusable unit `propose-and-generate-{domain}`/`reconcile-{domain}` conceptually build on.

4. **`deterministic-audit-{domain}`**
   - *Input:* the domain's current document.
   - *Output:* a verdict + per-rule findings (pass/fail, which rule, evidence) — an ordinary Task output, **not** a `repo.db` `audit_run`/`audit_deterministic_result` row (see §5).
   - *Acceptance:* **happy** — all mandatory rules pass, verdict `compliant`. **corner** — a non-mandatory rule fails, verdict `compliant-with-warnings`. **edge** — document missing or a mandatory rule fails, verdict `non-compliant`, triggers `fix-{domain}`.

5. **`semantic-audit-{domain}`**
   - *Input:* the document plus its profile's `writing_objective`/`knowledge_goal`/`reader_goal`.
   - *Output:* a qualitative score + findings, shaped around the profile's `completion.checklist`/`review.questions`.
   - *Acceptance:* same happy/corner/edge shape as #4, but named explicitly as **bounded by the `knowledge_goal`/`reader_goal` placeholder dependency** (§2) — a semantic audit judged against a placeholder objective is only as good as that placeholder, not a defect of this proposal's design.

6. **`fix-{domain}`**
   - *Input:* the document plus the failing findings from #4/#5.
   - *Output:* a corrected document.
   - *Acceptance:* **happy** — previously-failing mandatory rules now pass. **corner** — the fix resolves the mandatory failure but introduces a new non-mandatory one (flagged, not silently accepted). **edge** — the fix cannot resolve the failure within a bounded number of attempts — escalates to a human, does not loop forever.

**Standalone (4):**
- **`bootstrap-readme`** — input: an existing, undocumented repository's actual source code; output: a README; acceptance: happy (meets `readme`'s map's required sections), corner (partial — sections scaffolded as TBD, not fabricated), edge (no discoverable repo structure to bootstrap from — escalates, doesn't invent content).
- **`calculate`** — input: the 13 domains' already-computed deterministic + semantic scores (a direct dependency on #4/#5's outputs, named explicitly); output: `final_score` per the 25/25/25/25 `weighted_sum`; acceptance: happy (all 13 available), corner (see §6 — behavior on a missing domain score not decided here), edge (a score outside 0-100 — reject as invalid input).
- **`render-report`** / **`render-charts`** — input: `calculate`'s output plus score history; output: a markdown report / chart images; acceptance: renders successfully, and a missing-data case produces an explicit gap note, never a silent omission.

## 5. Execution model — ordinary Task Runtime, not the Audit Subsystem

Explicit callback to Proposal 00 §5 step 3's decision, restated so it isn't silently relitigated while authoring these Tasks: `deterministic-audit-{domain}`/`semantic-audit-{domain}` execute through the normal Task Instance lifecycle (`assign_task` → `submit_proposal_draft` → `review_task_proposal` → `run_skill` → `submit_completion_validation`, per `schema/repo/00-task_instance.sql`/`01-proposal_revision.sql`/`02-proposal_approval.sql`/`03-execution_state.sql`/`06-completion_validation.sql` and the MCP Tool Contract's Task Execution group), never through `mcp.db`'s `audit_definition`/`repo.db`'s `audit_run` pipeline. "Verdict"/"findings" in #4/#5 above are just that Task's own `output_contract_json` shape, checked by the Completion Validator against its `acceptance_criteria_json` — no `audit_run` row gets written for this Domain System's audits. `schema/repo/08-13`'s Audit Subsystem execution tables remain available generically for a Domain System that *does* choose that model; this one doesn't, per Proposal 00's decision.

## 6. Open questions (named, not silently resolved)

- **`calculate`'s behavior on a missing domain score** — exclude it from the weighted sum, treat it as zero, or block `calculate` entirely until all 13 are present? Not decided here.
- **Inline JSON Schema per Task vs. shared schema fragments.** Authoring 82 fully-inline `input_contract_json`/`output_contract_json` pairs duplicates the same "a rust_dev document conforming to `domain/map/{domain}-map.yaml`" shape 13+ times. §4's archetype structure suggests a small set of shared, parameterized schema fragments reused across domains is the better fit — not designed here, a follow-up implementation decision.
- **Semantic audit's placeholder dependency** (§2, §4 item 5) — who fills `knowledge_goal`/`reader_goal` in each of the 13 domains' profiles, and when, is a Proposal 00 open item this proposal now also depends on, not newly introduced here.
- **Who authors the 82 (or 6-template × 13 + 4) Task contracts, and when** — this proposal designs the pattern (§4); instantiating it across all 82 Usecases is real, separate work this proposal does not perform.

## 7. Non-Goals

- Does not author any of the 82 Tasks' actual contract content — designs the archetype pattern (§4) and execution model (§5) only.
- Does not register the `rust-development` (or equivalent) Agent System `task_step.required_capability` depends on — carried over from Proposal 00 §7, still open, unaffected by this proposal.
- Does not change `domain/map`, `domain/profile`, or `task.yaml`'s Epic/Usecase structure — Proposal 00's work, done, unmodified here.
- Does not resolve the shared-schema-fragment question (§6) — names it, doesn't decide it.

## 8. Traceability

- Depends on: Proposal 00 (archived, `docs/proposal/archive/00-rust_dev-dharma-domain-system-proposal.md`), `dharma/schema/mcp/10-task.sql` (contract shape), `dharma/docs/proposal/02-task-model.md` (Hard Constraints), `dharma/schema/repo/{00-task_instance,01-proposal_revision,02-proposal_approval,03-execution_state,06-completion_validation}.sql` (the Task Runtime tables these Tasks execute through, since this Domain System doesn't use the Audit Subsystem, per §5).
- Source material for the authoring pattern: this repository's own `dharma/domain/system/dev/rust_dev/domain/map/*`, `domain/profile/*/*` (Proposal 00's output), `samgraha/system/dev/rust_dev/00-domain-relationships.md` (derivation chain), `samgraha/system/dev/rust_dev/common/calculation/summary/final_score.yaml` (`calculate`'s formula).
- Feeds: the actual authoring pass (82 Tasks, or 6 templates × instantiation) once this pattern is agreed; eventual `mcp__dharma__register_domain_system` execution, already gated on this per Proposal 00 §8, now also gated on this proposal's output.
