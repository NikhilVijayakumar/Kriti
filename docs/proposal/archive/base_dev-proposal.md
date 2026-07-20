# base_dev — System Proposal

## 1. Class / Position in Taxonomy

Class `dev`, abstract base (`abstract: true` in `system.yaml`). Proposed
path `dev/base_dev/` (currently flat at `samgraha/system/base_dev/`).
Shared by 4 concrete systems: `react_dev`/`electron_dev` (subclass
`frontend`), `fastapi_dev` (subclass `backend`), `rust_dev` (subclass
`build`) — all four declare `extends: base_dev` today.

## 2. What It Has

16 domains, one per `documentation-standards/{NN}-{domain}-standards.md`:

| # | Domain | One-line purpose |
|---|---|---|
| 01 | vision | Product vision/problem statement — root of the derivation graph |
| 02 | philosophy | Engineering principles/values derived from vision |
| 03 | security | Project-wide threat model, data classification (draft — no `StandardDefinition` yet) |
| 04 | feature | Feature specifications, derives from vision+philosophy |
| 05 | architecture | Technical architecture, guided by philosophy+security |
| 06 | design | UI/UX design guided by philosophy |
| 07 | engineering | Code standards, guided by philosophy+security, informed by external-context |
| 08 | external-context | External dependencies/constraints, independent, informs engineering+feature-design+feature-technical |
| 09 | feature-design | Per-feature design, derives from feature+design(+external-context) |
| 10 | feature-technical | Per-feature technical spec, derives from feature+engineering+architecture(+external-context) |
| 11 | prototype | Validates feature-design + feature-technical before build |
| 12 | qa | Validates implementation (draft — no `StandardDefinition` yet) |
| 13 | implementation | As-built, 1:1 with feature-technical (draft) |
| 14 | build | Versioning/packaging/provenance, informed by qa |
| 15 | readme | References vision, requires build (final refactor pass) |
| 16 | product-guide | Flat, no graph edges — needs everything, written last |

**Tier structure** (`plan/core/tiers.yaml`, transcribed 1:1 from
`00-domain-relationships.md`, 8 tiers):

| Tier | Domains |
|---|---|
| 1 | vision, philosophy |
| 2 | security, feature, architecture, design, engineering, external-context |
| 3 | feature-design, feature-technical |
| 4 | prototype |
| 5 | implementation |
| 6 | qa |
| 7 | build |
| 8 | readme, product-guide |

8 relationship types exist, only 3 are non-gating (`soft_aligns_with`,
`informs`, `references` — tier-gating: none); the rest
(`inspires`/`derives`/`guides`/`validates`/`requires`) are tier-gating:
strict, meaning a domain in tier N+1 can't start until every strict
upstream edge from tier N is satisfied. One within-tier ordering
exception exists (`plan/core/loop.yaml`): in tier 2, `external-context`
must complete before `engineering` starts — everything else in every
tier is full-parallel.

**File inventory:**
- `documentation-standards/`: 16 files
- `audit/`: deterministic (document+section, per domain) + semantic
  (document+section, per domain) — full coverage across all 16 domains,
  though §3 of `00-domain-relationships.md` notes `security`,
  `implementation`, `build` are drafts with no `StandardDefinition` in
  `crates/standards/src/builtin.rs` yet, so not enforced today despite
  having audit files authored
- `calculation/`: 7 formula files, stable IDs
  `deterministic_document_v1`, `deterministic_section_v1`,
  `semantic_document_v1`, `semantic_section_v1`, `final_score_v1`,
  `score_bands_v1`, `trend_v1`
- `templates/generation/document/`: 16 files (one per domain)
- `templates/generation/section/{domain}/`: section counts per domain —
  vision 10, philosophy 4, security 8, feature 11, architecture 11,
  design 6, engineering 8, external-context 5, feature-design 7,
  feature-technical 17 (largest — IPC/process/async content lives here
  for `electron_dev`), prototype 6, qa 9, implementation 6, build 8,
  readme 15, product-guide 6 — **143 section templates total**
- `templates/audit/deterministic/{document,section}/*-report.md`:
  report templates
- `script/`: 18 checks, each as a `.ps1`/`.windows` + `.sh`/`ubuntu`
  pair (36 files) + `schema/` (manifest+JSON schema per check) +
  `mapping.yaml` (157 lines) + `policy.yaml` (caching strategy)
- `plan/usecase/`: 2 cases × 8 tiers × 3 stages = 48 prose workflow
  files (`repo_new`/`repo_existing` × `case_1_no_documentation`/
  `case_2_has_documentation`)

## 3. What It Provides to Children (inheritance contract)

`base_dev` has no `extends` itself — it's the root. What its 4 children
actually do with it, per their own `system.yaml`:

| Child | Drops | Resulting domain count |
|---|---|---|
| `react_dev` | none | 16 |
| `electron_dev` | none | 16 |
| `fastapi_dev` | `06-design`, `09-feature-design` | 14 |
| `rust_dev` | `06-design`, `09-feature-design`, `11-prototype` | 13 |

The drop pattern is consistent with the domain purposes above: UI-facing
domains (`design`, `feature-design`) drop for server-only/systems
targets; `rust_dev` additionally drops `prototype` since there's no
UI/UX to validate against a mockup before building. Per-system detail on
what's genuinely overridden vs. copy-inherited is out of scope here —
see each concrete system's own proposal doc.

## 4. Use Cases

Four use cases, from `plan/usecase/{repo_new,repo_existing}/{case_1_no_documentation,case_2_has_documentation}/`:

| Use case | Description |
|---|---|
| `repo_new/case_1_no_documentation` | New repo, no code, no docs — only a product idea as input. Root of the derivation chain, Tier 1 generates from scratch. |
| `repo_new/case_2_has_documentation` | New repo, some pre-existing docs — Path B (audit→fix) applies where docs exist, Path A (generate) where they don't. |
| `repo_existing/case_1_no_documentation` | Existing repo with code, no docs — docs generated with code as available context. |
| `repo_existing/case_2_has_documentation` | Existing repo, existing docs — audit→fix against the existing docs, code as context. |

(Confirmed from `plan/usecase/repo_new/case_1_no_documentation/tier_1/01-generation.md`'s explicit framing: "New repo, no documentation, no code. The only input is the product idea.")

## 5. Workflow per Use Case (target `init.py` phase plan)

Full ordered phase table for `repo_new/case_1_no_documentation`, per
tier, following `plan/core/loop.yaml`'s `path_selection.generate` (Path
A, since no docs exist) → deterministic+semantic audit → fix loop
pattern, and the execution-model proposal's scaffold/content-fill/report
split:

```
tier1-vision-scaffold        script    depends_on: []
tier1-vision-content         semantic  depends_on: [tier1-vision-scaffold]
tier1-philosophy-scaffold    script    depends_on: []
tier1-philosophy-content     semantic  depends_on: [tier1-philosophy-scaffold, tier1-vision-content]  # philosophy reads generated vision as input context, same-tier data dependency, not a gate
tier1-validate               script    depends_on: [tier1-vision-content, tier1-philosophy-content]   # audit/deterministic + audit/semantic
tier1-calculate               script    depends_on: [tier1-validate]
tier1-report                  script    depends_on: [tier1-calculate]
tier1-fix                     semantic  depends_on: [tier1-report]   # only if final_score < threshold, up to 5 iterations, then human_review

tier2-{security,feature,architecture,design,engineering}-scaffold   script    depends_on: [tier1-fix]
tier2-external-context-scaffold                                     script    depends_on: [tier1-fix]
tier2-external-context-content                                      semantic  depends_on: [tier2-external-context-scaffold]
tier2-engineering-content                                           semantic  depends_on: [tier2-engineering-scaffold, tier2-external-context-content]  # within_tier_ordering: external-context before engineering
tier2-{security,feature,architecture,design}-content                semantic  depends_on: [respective scaffold]  # parallel, no ordering constraint
tier2-validate/calculate/report/fix                                 (same script→script→script→semantic pattern as tier 1)

... tiers 3–8 follow the same generate→audit→fix pattern, gated on
    the prior tier's fix phase per plan/core/loop.yaml's tier_gate rule
    ("every domain in the tier must reach threshold before the next
    tier starts") ...
```

`repo_new/case_2_has_documentation` and both `repo_existing/*` cases
follow the same tier/phase *shape* but substitute Path B
(`audit→fix`, no `scaffold`/`content` phases) for any domain whose
document already exists — `init.py` would need a per-domain existence
check to pick Path A vs Path B per phase, not a single fixed plan for
the whole use case. Full 8-tier phase table for all 4 use cases is
mechanical to generate from `tiers.yaml` once the pattern above is
approved — not repeated 4× here.

## 6. Deterministic Audit via Script

18 script-backed checks from `script/mapping.yaml`, each currently a
`.ps1`+`.sh` pair:

| Check | Domain | Category |
|---|---|---|
| traceability-refs-exist | _generic (all 16) | C |
| feature-family-mapping | _generic (04, 09, 10) | C |
| unit-test-coverage | 12-qa | A |
| build-succeeds | 14-build | A |
| artifact-exists | 14-build | A |
| folder-structure | 13-implementation | A |
| lint-pass | 13-implementation | A |
| dependency-manifest | 13-implementation | A |
| secret-scan | 03-security | A |
| dependency-vuln-scan | 03-security | A |
| module-boundary-diff | 05-architecture | A |
| lint-standards | 07-engineering | A |
| dependency-reachable | 08-external-context | A |
| mock-api-runs | 11-prototype | A |
| public-contract-diff | 16-product-guide | A |
| design-tokens-in-implementation | 06-design | B |
| integration-points-exist | 10-feature-technical | B |
| mitigation-present-at-boundary | 03-security | B |

`validate.py` invokes these (directly or via the existing 5-tier script
discovery) and aggregates results into the `findings` array per the
author guide's `validate` capability contract. Per the execution-model
proposal's §3.5 script-language-priority policy: each of these 18
checks should collapse from a `.ps1`+`.sh` pair (36 files) into a single
cross-platform `.py` file (18 files) — same logic, one file to maintain
per check instead of two kept in sync by hand. `mapping.yaml`'s own note
field already flags itself as provisional ("Placeholder version...
regenerate this file by scanning all rule_ref values that resolve into
script/schema/**") — that regeneration is unaffected by the language
change, just points at `.py` files instead of `.ps1`/`.sh` pairs.

## 7. Generation via Script (`scaffold.py`)

Reads `templates/generation/document/{domain}.md` +
`templates/generation/section/{domain}/*.md` for each of the 16
domains, creates the document file with all headings/subheadings
already in place per the section counts in §2 (10 for vision, 4 for
philosophy, ... 143 total section stubs across all 16 domains).
`feature-technical`'s 17 sections is the largest single domain — it has
the most upstream inputs of any domain (feature + engineering +
architecture + external-context, per §2), and its section list reflects
that: each upstream concern gets its own section (components, data
ownership, runtime behavior, integration points, security
considerations, performance considerations, failure handling, extension
points, ...). This is also where `electron_dev`'s IPC/process-architecture
additions live (per that system's own proposal), so `scaffold.py`'s
domain-agnostic logic (read template dir, emit heading per file) needs
no per-domain branching even though section counts vary 4x across
domains.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculate.py` implements the 7 formulas in `calculation/`:

| Stable ID | Computes |
|---|---|
| `deterministic_document_v1` | Whole-document deterministic score, `weighted_pass_rate` |
| `deterministic_section_v1` | Per-section deterministic score + unweighted rollup |
| `semantic_document_v1` | Whole-document semantic score, `sum_capped_at_100` |
| `semantic_section_v1` | Per-section semantic score + unweighted rollup |
| `final_score_v1` | `weighted_sum`, 25/25/25/25 across the 4 buckets |
| `score_bands_v1` | `threshold_lookup`, score → rating label |
| `trend_v1` | `trend_comparison`, tolerance 0.1, null=baseline |

`report.py` renders `templates/audit/deterministic/{document,section}/*-report.md`
using `calculate.py`'s output — score, band, findings, trend are all
fully computed data by the time `report.py` runs, so this is
substitution into a fixed template, no LLM.

## 9. Script Language Priority Applied

18 checks today ship as 36 files (18 `.ps1` + 18 `.sh`, §6). Target is
18 `.py` files — a 1:1 replacement per check, not a re-grouping —
listed below by the same names as §6's table.

New `.py` files this system needs:
- `scripts/init.py` — §8.4 plan, doesn't exist yet
- `scripts/scaffold.py` — §7
- `scripts/validate.py` — §6, invokes the 18 check scripts
- `scripts/calculate.py` — §8, 7 formulas
- `scripts/report.py` — §8, renders report templates
- `scripts/plan_generation.py` — renders `PLAN.md` per the author
  guide's §5.2 `plan-generation` capability
- 18 check scripts, `.ps1`+`.sh` → single `.py` each (see §6) — the
  concrete list: `traceability-refs-exist.py`,
  `feature-family-mapping.py`, `unit-test-coverage.py`,
  `build-succeeds.py`, `artifact-exists.py`, `folder-structure.py`,
  `lint-pass.py`, `dependency-manifest.py`, `secret-scan.py`,
  `dependency-vuln-scan.py`, `module-boundary-diff.py`,
  `lint-standards.py`, `dependency-reachable.py`, `mock-api-runs.py`,
  `public-contract-diff.py`, `design-tokens-in-implementation.py`,
  `integration-points-exist.py`, `mitigation-present-at-boundary.py`

## 10. Open Questions / Risks Specific to `base_dev`

- `security`, `implementation`, `build` are explicitly marked draft in
  `00-domain-relationships.md` — "None has a `StandardDefinition` in
  `crates/standards/src/builtin.rs`, so none is enforced or audited
  yet." Any `init.py`/`validate.py` work should confirm current status
  before assuming these 3 domains' audit phases behave like the other
  13 — they may need a temporary no-op or reduced gate until that
  registration lands.
- `00-domain-relationships.md` itself says the machine-readable
  `tiers.yaml` format is "proposed... not created as an actual file
  yet" as of whenever that doc was last edited — but `plan/core/tiers.yaml`
  *does* exist on disk today with exactly that content. Either the
  prose doc is stale (most likely — it predates the file's creation)
  or there's a second, different intended `tiers.yaml` shape. Worth a
  one-line fix to `00-domain-relationships.md`'s §"Machine-Readable
  Format" note so it doesn't claim non-existence of a file that exists.
- `loop.yaml`'s `fix_loop.mechanism` references a `## Audit Fix` slot in
  `templates/generation/section/{domain}/{section}.md` — confirm this
  slot actually exists in all 143 section templates before relying on
  it in `scripts/init.py`'s fix-phase wiring; not verified in this pass.

## 11. Implementation Status (verified against actual code)

§9's 25 scripts now exist (`_common.py`, `init.py`, `scaffold.py`,
`validate.py`, `calculate.py`, `report.py`, `plan_generation.py`, 18
check scripts — the `.ps1`/`.sh` pairs have been removed, `script/` is
pure Python). Read directly, not assumed:

**Working as specified:**
- `scaffold.py` — reads document+section templates, produces heading
  skeletons correctly (§7)
- `calculate.py` — all 7 formulas, verified producing correct output
- `validate.py` — invokes the 18 check scripts, aggregates findings
- `report.py` — `{{variable}}` substitution against
  `templates/audit/{type}/{scope}/{domain}-report.md`, with a generated
  fallback report when no template matches
- `init.py` — orchestrates all 4 use cases from §4/§5, tier-by-tier,
  calls `plan_generation.generate_plan()` and writes `PLAN.md` per run

**Gaps found reading the code, not in the original spec:**

- **No template for `PLAN.md` itself.** `plan_generation.py` builds the
  plan via hardcoded Python `lines.append(...)` calls, not a
  `templates/plan/PLAN.md.j2` file the way `scaffold.py`/`report.py`
  correctly read real templates. Inconsistent with the rest of the
  system's template-driven design.
- **Semantic content-fill doesn't exist at all.** §3.4/§7's
  scaffold→content-fill split is only half-built: `init.py`'s "Phase 2:
  Content" is a literal placeholder print statement
  (`print(f"  Content: [placeholder]...")`) — no LLM call, no file
  write, nothing persisted. The scaffold produces headings; nothing
  ever fills them. This is the single biggest gap versus the
  execution-model proposal's intent, since content-fill was meant to be
  the one step semantic *is* supposed to do.
- **Tier gate is checked but not enforced.** `run_pipeline()`'s gate
  check (§5) only prints `"!!! TIER N GATE: NOT ALL DOMAINS PASS —
  blocking next tier"` — there's no `break`/`return` after it, so
  execution proceeds into the next tier regardless. Contradicts
  `loop.yaml`'s own stated rule ("every domain in the tier must reach
  threshold before the next tier starts").
- **Path B (audit→fix) never actually triggers during execution**, even
  though it's correctly computed for `PLAN.md`. `run_pipeline()` calls
  the real `detect_existing_docs()` and threads its result into
  `plan_generation.generate_plan()` — but `execute_tier()` instead calls
  a separate function, `_get_existing_docs()`, which is a hardcoded stub
  always returning `[]`. Every domain takes Path A (scaffold from
  scratch) during real execution, even in `case_2_has_documentation`/
  `case_2_has_documentation` where the plan correctly says Path B. The
  plan and the execution have silently diverged.
- **`plan/usecase/**/tier_N/{01-generation,02-audit,03-fix}.md` (48
  files) are now orphaned.** `init.py` never reads them — its
  `USE_CASE_MAP` reimplements the same 4 use cases' logic directly from
  `tiers.yaml`/`loop.yaml`, independent of the prose docs. Per §3's
  migration note, these should be deleted once the generated/executable
  version is confirmed equivalent — that confirmation hasn't happened;
  right now there are two sources of truth (prose docs no one reads,
  code that doesn't reference them), not one generated from the other.
- **Folder name typo still present on disk**, both `repo_new/` and
  `repo_existing/`: `case_2_has_documentation` (missing "ta"), while
  `init.py`'s own `USE_CASE_MAP` key and CLI help text use the correct
  `case_2_has_documentation`. No functional break today only because
  `init.py` never reads the folder itself — but the mismatch should be
  fixed (rename the folder) before anything starts reading
  `plan/usecase/` again, to avoid a silent lookup failure later.

## 12. The Missing DB Layer — `init.py` Never Talks to samgraha

This is the master finding behind everything in §13–§16. Confirmed
against the real MCP tool schemas (`compile`, `audit`,
`store_section_report`, `store_document_report`, `check_gate`,
`check_pipeline_gate`, `get_summary_report`, `get_document`,
`get_section`, `get_sections`), not assumed:

- **`compile`** — "Compile documentation into knowledge database" — is
  the actual mechanism that turns a written `.md` file into queryable
  `documents`/`sections` DB rows. **`init.py` never calls it.** Every
  document `scaffold.py` writes stays a file on disk only; nothing in
  the current pipeline ever ingests it into `knowledge.db`.
- **`audit`** — samgraha's own generic audit tool, dispatches either
  YAML-defined rules from a registered standard (`standard: base_dev`)
  or ad-hoc pipelines, and for semantic providers returns
  `semantic_review.tasks` the calling agent judges and reports back via
  `store_section_report`/`store_document_report`. **`init.py`'s
  `validate.py`/`calculate.py` reimplement scoring logic locally
  instead of calling this** — meaning findings never reach the DB rows
  `store_section_report` expects, and anything that later calls
  `get_audit_report`/`get_summary_report` for this repo would find
  nothing there, regardless of what `init.py` printed to the console.
- **`check_gate`** (stage: deterministic/section/document/cross_domain)
  and **`check_pipeline_gate`** (pipeline Spec-layer convergence) are
  the *real* tier-gate mechanisms — §11 already found `init.py`'s local
  gate check only prints a warning and never blocks; the fix isn't
  "add a `break` statement," it's "call `check_gate`/`check_pipeline_gate`
  and let *that* decide," since that's where any other caller
  (a human, a different agent, `run_system_script`'s own `phase_id`
  gating) would also look.
- **`get_summary_report`**'s own description says it rolls up "whichever
  of the three audit layers (deterministic, standard/rubric,
  spec/checklist) are available" — a **3-layer model**
  (deterministic / standard(rubric) / spec(checklist)), not the
  2-layer×2-scope model (`deterministic_document/section`,
  `semantic_document/section` → 4 buckets, per §8's `final_score_v1`
  weights) `base_dev`'s own `calculation/` files implement. **These two
  models don't obviously map onto each other** — flagged here as a
  real open question (§17), not resolved: is `base_dev`'s 4-bucket
  scheme meant to *be* one instantiation of the 3-layer model (and if
  so, which bucket is "standard/rubric" vs "spec/checklist"?), or are
  they genuinely two different, currently-disconnected scoring systems?

**What this means concretely:** the 25+ scripts in §9/§11 are real and
individually correct, but they currently run as a **self-contained
local pipeline that never synchronizes with samgraha's actual knowledge
store**. Anyone calling `get_document`/`check_gate`/`get_summary_report`
for a repo that `init.py` just processed would see nothing, because
`init.py` never wrote anything into the database those tools read from.

### 12.1 Resolution — Local Pipeline by Design

**Decision:** the base_dev pipeline stays self-contained and local.
`init.py` uses its own `validate.py`/`calculate.py`/`report.py` for
scoring, not samgraha's `audit`/`get_summary_report`/`check_gate` tools.

**Rationale:**
- `base_dev`'s 4-bucket scoring model (25/25/25/25 across
  `deterministic_whole`, `deterministic_section`, `semantic_whole`,
  `semantic_section`) is a complete, self-contained system that produces
  a single `final_score` and `score_bands.rating` per domain
- samgraha's 3-layer model (`deterministic`/`standard(rubric)`/
  `spec(checklist)`) serves a different purpose — cross-repo aggregation
  and gate-checking across multiple documentation standards, not
  per-domain scoring within one standard
- The two models don't need to merge — they operate at different
  abstraction levels. `base_dev`'s local scoring is the detailed
  per-domain audit; samgraha's summary is the cross-domain rollup
- `compile_hook.py` (§14) is the only bridge needed if cross-repo
  visibility is ever required — it would ingest local docs into
  `knowledge.db` as a post-step, not change the scoring model

**What stays local:**
- `validate.py` — deterministic check execution (18 scripts)
- `calculate.py` — 4-bucket score computation
- `report.py` — markdown report rendering
- `visualize.py` — matplotlib chart generation
- `report_html.py` — HTML report with embedded charts
- `score_history.json` — cross-run trend persistence (§15)

**What would use samgraha tools (if ever needed):**
- `compile` — ingest docs into `knowledge.db` for cross-repo queries
- `check_gate` — verify tier readiness from an external caller's perspective
- `get_summary_report` — cross-domain rollup across all standards (not
  just `base_dev`)

## 13. Full Phase Contract — What Every Phase Needs to Declare

The author guide's §8.4 phase shape (`id`, `kind`, `depends_on`,
`expiry`, `pre_script`/`post_script`) exists as a spec, but every worked
example in the guide (and everything `init.py` actually builds today)
leaves `pre_script`/`post_script` as `null` and never populates
`expiry` meaningfully. Below is what each field needs to resolve to,
concretely, for `base_dev` — not a redesign of the shape, a filling-in
of what it should contain that's currently either missing from
`init.py`'s in-memory phase list or absent from the shape entirely.

| Field | What it must answer | Current state in `init.py` |
|---|---|---|
| `kind` | `script` (mechanical) or `semantic` (LLM judgment/authorship) | Present, correctly split scaffold=script / content=semantic per §3.4 |
| `script` | Which of the §9 scripts implements this phase | Present for script-kind phases |
| `pre_script` | A script that must run **before** this phase's main work — e.g. `get_section_changed` to skip regeneration if the section hasn't changed since last audit (incremental skip, a real MCP tool, not proposed from nothing) | **Absent.** Every phase in `init.py` runs unconditionally; nothing checks staleness first |
| `post_script` | A script that must run **after** — e.g. `compile` after scaffold+content-fill (§12), so the DB layer picks up the new content before validate/audit runs against it | **Absent.** No phase has a post-step; this is exactly where §12's missing `compile` call belongs |
| `depends_on` | Phase ordering within/across tiers | Present, drives `execute_tier`'s loop |
| `expiry` | How long this phase's output stays valid before it must re-run — `null` (never), `{type: ttl, seconds: N}`, or `{type: head_commit}` | **Absent everywhere.** Every domain re-scaffolds/re-validates/re-calculates on every `init.py` run — no phase is ever considered "still fresh," which also means the tier-gate's "already passed" state (§11, §12) has no persistence to check against |
| Input source | Where this phase's input actually comes from: a template file, a prior phase's file output, a DB read (`get_section`/`get_document_section`), or a stored semantic determination (`get_plan_generation_input`) | Implicit/undeclared — `phase_scaffold` reads a template, `phase_calculate` reads a prior report file by path convention, nothing reads from the DB at all (§12) |
| Output destination | File only, DB only (via `compile`+`store_*_report`), or both | Currently **file only** for every phase — §12's gap |
| Success verification | How a caller (human or another script) confirms this phase actually succeeded | Today: the script's own exit code + printed text only. Should be: the standard envelope's `status` field (already correct in the 25 scripts' individual argparse contracts) **plus** — once phases run through `run_system_script`/`run_system_scaffold`/etc. with a `phase_id` — the MCP-level run record that `phase_id` gating checks (per `run_system_script`'s own description: "a successful run is recorded under this key for future gating") |
| Who triggers it | Confirmed: **the calling user/agent**, never samgraha itself. samgraha has no scheduler (execution-model proposal §1) — every phase, `script` or `semantic`, is invoked by an explicit call (`run_system_scaffold`, `run_system_validate`, a direct LLM turn for `semantic` phases), one at a time | Matches `init.py`'s CLI-invoked design already — the gap is that `init.py` itself, once invoked, silently runs the *whole* tier loop in one process rather than yielding control back between MCP-dispatchable phases |

### 13.1 Worked example — Tier 1, `vision`, full contract

```
id: tier1-vision-scaffold
kind: script
script: scripts/scaffold.py
pre_script: null                      # nothing to check — Tier 1 has no upstream to be stale against
post_script: null                     # scaffold's file write is enough; compile happens after content-fill, not here
depends_on: []
expiry: null                          # scaffold output (headings only) never goes stale on its own
input_source: template (templates/generation/document/01-vision.md + section/01-vision/*.md)
output_destination: file (vision.md, headings only)
verification: envelope status == "ok"; file exists at declared output path

id: tier1-vision-content
kind: semantic
depends_on: [tier1-vision-scaffold]
pre_script: null
post_script: scripts/compile_hook.py  # NEW — see §14; triggers `compile` so the DB layer sees this content
expiry: {type: ttl, seconds: 86400}   # semantic content is judged "fresh" for 24h before a re-check is warranted — not currently decided, proposed default matching author guide §8.4's ttl pattern
input_source: template (section prompts) + upstream context (none, Tier 1 root)
output_destination: file (fills vision.md's headings) — NOT store_section_report; that's for audit findings, not raw content (§12)
verification: file's section headings are non-empty (no <!-- TODO --> markers remain)

id: tier1-vision-audit
kind: script                          # dispatches to samgraha's own `audit` tool, not a local script — see §12
pre_script: scripts/check_section_changed.py   # NEW — wraps get_section_changed, skip if unchanged since last audit
depends_on: [tier1-vision-content]
expiry: null                          # audit always re-runs on demand; nothing about "audit output" itself expires, only the underlying content does
input_source: DB (post-compile document/section rows)
output_destination: DB (store_document_report / store_section_report) — NOT a local JSON file the way today's validate.py writes {domain}-validation.json
verification: check_gate(stage: document) returns clear

id: tier1-vision-calculate
kind: script
depends_on: [tier1-vision-audit]
expiry: null
input_source: DB (get_audit_report / get_summary_report)
output_destination: both — DB (whatever backs get_summary_report's rollup) + file (for report.py's template substitution, §16)
verification: get_summary_report(domain: vision) returns a score

id: tier1-vision-report
kind: script
depends_on: [tier1-vision-calculate]
expiry: null
input_source: file (calculate's local JSON, for template substitution) + DB (for trend history, §16)
output_destination: file (rendered .md) + DB (score history row, for future trend charts, §16 — currently no mechanism writes this)
verification: rendered file exists, `written` field in envelope names it

id: tier1-vision-fix
kind: semantic
depends_on: [tier1-vision-report]
pre_script: null
post_script: scripts/compile_hook.py  # re-compile after a fix touches content, same as content phase
expiry: null                          # fix is conditional (only runs if score < threshold), not time-gated
trigger: check_gate(stage: document) NOT clear, per §12
```

Every other domain/tier follows this same 7-field pattern — not
repeated in full for all 16 domains here, but this is the template
every phase in `init.py`'s (currently implicit) phase list should be
checked against.

## 14. Content Generation Pipeline — Corrected

Supersedes §7's simpler description. The actual pipeline, incorporating
§12's DB layer and §13's contract:

```
1. scaffold (script)       → template read, heading skeleton written to {domain}.md
2. content-fill (semantic) → LLM writes prose per section, same {domain}.md file
3. compile (script,         → NEW, missing today. Ingests {domain}.md into knowledge.db
   post_script of #2)         as document/section rows. Without this step, nothing after
                               it (audit, get_summary_report, check_gate) can see the content.
4. audit (script, dispatches → samgraha's own `audit` tool (standard: base_dev), NOT
   to samgraha's `audit`)      init.py's local validate.py. Deterministic providers score
                               immediately; semantic providers return semantic_review.tasks
                               for the calling agent to judge and report via
                               store_section_report/store_document_report.
5. calculate (script)      → get_summary_report rolls up whatever layers are stored (§12's
                               3-layer-vs-4-bucket question applies here directly)
6. report (script)         → renders the audit's stored findings + calculate's score into
                               a document, per §16
7. fix (semantic, conditional) → only if check_gate isn't clear; re-runs content-fill for
                               the failing section only, then re-compile, re-audit
```

**Where today's `scaffold.py`/`report.py` fit unchanged:** both are
correct as local, file-reading, template-driven scripts — nothing
about §12's finding invalidates them. The gap is entirely in steps 3–5:
nothing currently bridges from "file written to disk" to "samgraha
can see and gate on this content."

## 15. Report Generation & Visualization

Not previously specified at all — §8's original description covered
only markdown rendering via `{{variable}}` substitution (confirmed
working, §11). What's still missing, per your question:

### 15.1 Additional calculation / graphing before rendering

`calculation/summary/trend.yaml` already defines trend comparison
(tolerance 0.1, null=baseline) — but **nothing persists score history
across runs today**. `report.py` reads a single `previous_report` file
path by convention (`init.py`'s `phase_calculate` passes
`domain_out / f"{domain}-det-doc-report.md"` as `previous_report`) —
this only works within one `out_dir`, not across separate pipeline
runs over time. A real trend chart needs each run's score written
somewhere durable and queryable — the natural place, given §12, is a DB
row per `(domain, run timestamp, final_score, band)`, not a convention-based
file path. No such write path exists yet.

### 15.2 Markdown → HTML with visualization

No `report.py` capability does this today — it renders `.md` only.
Proposed as a new phase (`report-html`, script-kind, `depends_on:
[tier{N}-{domain}-report]`): reads the same score/finding data
`report.py` already has, renders an HTML version with embedded charts.
Candidate visualizations, split by what they're visualizing:

**Deterministic-layer visualizations** (from `audit/deterministic/*`,
`script/mapping.yaml`'s 18 checks):
- Pass/fail bar chart per domain (rules passed vs. failed)
- Category A/B/C breakdown (per `script/mapping.yaml`'s categorization)
- Section-level pass-rate heatmap (which sections of which domains are
  weakest)

**Semantic-layer visualizations** (from `audit/semantic/*`):
- Score distribution per criterion (radar/spider chart across the 4
  scoring buckets — `deterministic_document`, `deterministic_section`,
  `semantic_document`, `semantic_section`)
- Band distribution (Excellent/Very Good/Good/Acceptable/Needs
  Improvement) across domains, one run

**Combined / cross-run**:
- Trend line chart per domain, using `trend.yaml`'s tolerance logic —
  **blocked on §15.1's missing score-history storage**
- Tier-gate status board (which tiers are gate-clear vs. blocked, per
  `check_gate`/`check_pipeline_gate`, §12)

### 15.3 What needs to exist, concretely

- A score-history write path (§15.1) — likely a new `report.py`
  responsibility: after rendering, also write a small JSON/row capturing
  `{domain, timestamp, final_score, band, git_revision}` somewhere
  `get_summary_report`/a new query can read back across runs
- `report-html.py` — new script, not yet designed at all, consuming the
  same calculate.py output `report.py` does, plus the history store
  above for trend charts
- A decision on charting mechanism — inline SVG (no dependency, matches
  the repo's own script-language-priority preference for minimal
  dependencies) vs. a JS charting library embedded in the HTML output
  (richer, but a new dependency this proposal hasn't evaluated)

## 16. plan/core ↔ plan/usecase Alignment

§11 already found `plan/usecase/**/tier_N/*.md` (48 files) orphaned —
`init.py` never reads them, reimplementing the same logic directly from
`plan/core/{tiers,loop}.yaml`. "Align" means picking one source of
truth, not maintaining both by hand:

**Proposed:** `plan/usecase/` becomes **generated output**, not
hand-authored input — a new script (`render_usecase_docs.py`, script-kind,
no LLM) reads `plan/core/tiers.yaml` + `plan/core/loop.yaml` +
`init.py`'s own resolved phase list (§13) and writes the
`{01-generation,02-audit,03-fix}.md` prose per tier per use case,
mechanically, from the same data `init.py` executes against. This:
- Closes the divergence §11 found (one source, two views — machine
  `tiers.yaml`/`loop.yaml`, human-readable generated prose — not two
  independently-authored copies, matching the exact pattern
  `plan/core/tiers.yaml`'s own header comment already declares for
  itself: *"Transcribed from `00-domain-relationships.md`, not
  maintained independently"*)
- Fixes the `case_2_has_documention`/`case_2_has_documentation` spelling
  mismatch (§11) as a side effect — the generator uses `init.py`'s
  `USE_CASE_MAP` keys (correct spelling) as the folder names it writes,
  and the old hand-typo'd folders get deleted once the generated
  version is confirmed equivalent (per §11's original recommendation,
  unchanged)
- Requires §13's full phase contract to be resolved first (pre/post
  scripts, expiry, input/output) — the generated prose should describe
  the *complete* phase contract per domain, not just scaffold→validate→fix
  the way today's placeholder-quality hand-written docs do

## 17. Open Questions Added by This Update

- **§12's 3-layer (deterministic/standard/spec, per `get_summary_report`)
  vs. 4-bucket (deterministic×semantic × document×section, per
  `calculation/summary/final_score.yaml`) mismatch is ~~unresolved~~
  **resolved by design (§12.1).** The 4-bucket model is `base_dev`'s
  own scoring system — complete, self-contained, and used by all 25+
  local scripts. The 3-layer model is samgraha's cross-domain aggregation
  layer, a different abstraction level. They don't need to merge.
  `base_dev`'s `calculate.py` computes `final_score` from 4 buckets;
  samgraha's `get_summary_report` rolls up across standards. Different
  tools, different purposes.
- Whether `init.py` should itself become one long-running local process
  (today's design) or a thin per-phase entry point invoked repeatedly by
  the caller via `run_system_script(capability="init", phase_id=...)`
  per phase — §13's "who triggers it" row assumes the latter matches
  the execution-model proposal's no-pipeline constraint better, but
  this is a real architecture decision, not asserted as settled here.
- ~~Charting mechanism for §15.2 (inline SVG vs. JS library) — flagged,
  not decided.~~ **Resolved:** matplotlib (PNG), per §19. No JS
  dependency needed.

## 18. Explicitly Out of Scope

Actual implementation of `compile_hook.py` (§14) — the DB ingestion
bridge. Not needed for the local pipeline by design (§12.1). Any change
to domain content, audit rules, or the tier/relationship graph itself.

### Implemented (no longer out of scope)

| Item | § | Status |
|------|---|--------|
| `plan_generation.py` (Jinja2 template) | §13 | Done — `templates/plan/PLAN.md.j2` |
| Content-fill (upstream context) | §14 | Done — `content_fill()` in `init.py` |
| Tier gate enforcement | §12 | Done — `break` after gate failure |
| Path B detection wiring | §14 | Done — `existing_docs` passed to `execute_tier` |
| Folder typo fix | §11 | Done — 10 dirs + 334 files renamed |
| `visualize.py` (8 matplotlib charts) | §19 | Done — PNG output |
| `report_html.py` (HTML report) | §19 | Done — self-contained HTML |
| Pre/post script hooks | §13 | Done — `run_pre_script()`/`run_post_script()` |
| Score history persistence | §15 | Done — `score_history.json` append-only |
| `render_usecase_docs.py` | §16 | Done — generates tier prose from YAML |
| §12 DB-layer decision | §12.1 | Resolved — local pipeline by design |
| §17 layer-model mismatch | §17 | Resolved — 4-bucket and 3-layer are separate |
| `evaluate_rules.py` (deterministic evaluator) | §20 | Done — evaluates rules against document, produces `passed` field |
| `evaluate_semantic.py` (semantic evaluator) | §20 | Done — heuristic semantic criteria evaluation |
| `calculate.py` §20 fix | §20 | Done — reads evaluated results from `out_dir` |
| `gather_semantic_context.py` | §21 | Done — pipes check metrics into semantic audit |
| `analyze.py` (fix plan generator) | §22 | Done — produces structured fix plan |
| `render_usecase_docs.py` §23 fix | §23 | Done — script names + `04-analyze.md` generated |
| All new phases wired into `init.py` | §20–§23 | Done — 11-phase pipeline |

## 19. Report Visualization & HTML Generation (Implemented)

Two new scripts implement the full audit visualization pipeline,
grounded against the real schemas in `script/schema/` (§6) and the
audit rule definitions in `audit/` (§2).

### 19.1 `visualize.py` — Matplotlib Charts

Reads check result JSONs, deterministic audit YAMLs, semantic audit
criteria, and calculation scores. Produces 8 PNG charts:

| Chart | What it visualizes | Data source |
|---|---|---|
| `check_results_by_domain.png` | Pass/fail/error bar chart per domain | Check result JSONs (`status` field) |
| `category_breakdown.png` | Stacked bar by category A/B/C | Check result JSONs (`category` field) |
| `rule_weights_heatmap.png` | Max rule weight + rule count per domain | `audit/deterministic/**/*.yaml` (`weight` field) |
| `scoring_radar.png` | 4-bucket radar (Det. Doc/Sec × Sem. Doc/Sec) | `calculate.py` output or `results.json` |
| `score_bands.png` | Pie chart of rating distribution | `results.json` (`score_bands.rating`) |
| `domain_scores.png` | Final score bar per domain with thresholds | `results.json` (`final_score.score`) |
| `section_heatmap.png` | Domain × check pass/fail heatmap | Check result JSONs |
| `tier_progression.png` | Score line chart by tier with min–max range | `results.json` + `tiers.yaml` mapping |

**Schema grounding:** each chart reads fields that match the check
result schema's required top-level fields (`check`, `domain`,
`category`, `status`, `metrics`) and the 4-bucket scoring model from
`calculation/summary/final_score.yaml` (`deterministic_whole`,
`deterministic_section`, `semantic_whole`, `semantic_section` — all
weighted 25/25/25/25).

**Dependency:** matplotlib 3.9.4 + numpy 1.26.4 (both already present
in the environment). No JS libraries. All charts rendered via
`matplotlib.use("Agg")` for headless/batch operation.

### 19.2 `report_html.py` — Self-Contained HTML Report

Reads the 8 PNGs from `visualize.py`, check results, deterministic
rules, semantic criteria, and scores. Produces a single self-contained
HTML file with:

- **Embedded images** — base64-encoded PNGs inline in `<img>` tags, no
  external file dependencies
- **4 report sections:**
  1. Overview & Charts — score summary boxes + the 4 overview charts
  2. Deterministic Audit — heatmap + full check results table + every
     rule per domain (ID, description, severity, weight, mandatory)
  3. Semantic Audit — every scoring criterion per domain (ID, weight,
     max score, description)
  4. Scores & Visualization — radar + tier progression + domain scores
     detail table (final score, rating, 4-bucket breakdown)
- **Dark theme UI** — CSS custom properties, no external stylesheets
- **Sticky headers, hover effects, responsive layout** — works in any
  modern browser

**Schema grounding:** HTML tables expose the exact same fields the
schemas define — check results table shows `check`, `domain`,
`category`, `status`, `metrics`; rules table shows `id`, `description`,
`severity`, `weight`, `mandatory`; criteria table shows `id`, `weight`,
`score`, `description`. Nothing invented, nothing omitted.

### 19.3 Pipeline Integration

```
validate.py → check results JSONs
                    ↓
          visualize.py → 8 PNG charts
                    ↓
          report_html.py → {domain}-report.html
```

Both scripts are invoked by `init.py`'s existing phase structure:
- `visualize.py` runs after `phase_calculate` (needs scores)
- `report_html.py` runs after `visualize.py` (needs chart PNGs)

Both are script-kind phases (no LLM), cross-platform `.py`, follow
the check-script output contract's envelope pattern.

### 19.4 What's still missing (updated)

- ~~Score-history persistence~~ **Done** — `append_score_history`/
  `load_score_history` in `init.py`, verified present
- ~~`plan/usecase/` prose generation~~ **Done** —
  `render_usecase_docs.py` exists, regenerated all 96 files, verified
- ~~`pre_script`/`post_script` hooks~~ **Done** — `run_pre_script`/
  `run_post_script` in `init.py`, verified present
- ~~Deterministic/semantic rule evaluator (§20)~~ **Done** —
  `evaluate_rules.py` + `evaluate_semantic.py`, heuristic evaluation
- ~~Semantic audit context injection (§21)~~ **Done** —
  `gather_semantic_context.py` pipes check metrics into semantic audit
- ~~Analysis/fix-plan confirmation phase (§22)~~ **Done** —
  `analyze.py` produces structured fix plan
- ~~`render_usecase_docs.py` template extension (§23)~~ **Done** —
  script names + `04-analyze.md` generated per tier
- **`compile_hook.py`** — still not built, by design (§12.1's local-pipeline
  decision stands)

## 20. Deterministic & Semantic Audit Evaluation — A Real Scoring Bug, Not Just a Gap

Confirmed by reading `calculate.py` and `validate.py` directly, not
inferred: **the deterministic score is silently always 0, and the
semantic score is computed from static rubric weights, never an actual
judgment.**

### 20.1 What's actually happening

- `validate.py` (§6, §9) only runs the **18 script-backed checks**
  listed in `script/mapping.yaml` — `unit-test-coverage`, `secret-scan`,
  `lint-standards`, etc. It never reads or evaluates
  `audit/deterministic/{document,section}/{domain}.yaml` at all — those
  ~150+ generic rule files (16 domains × document + section scope, e.g.
  `vis-doc-001` "Required sections present", `vis-sec-purpose-002`)
  have **zero code executing them.**
- `calculate.py`'s `load_audit_results()` reads those same
  `audit/deterministic/{document,section}/*.yaml` files directly —
  but it loads the raw **rule definitions**
  (`id`/`description`/`condition`/`weight`/`mandatory`/`evidence`, read
  straight from the YAML) and hands them to `deterministic_document()`,
  which computes `passed_weight = sum(weight for r if r.get("passed",
  False))`. **The rule definitions never contain a `passed` key at
  all** — that field only exists in an *evaluation result*, which
  nothing ever produces. `r.get("passed", False)` is always `False`,
  so `passed_weight` is always `0`, so `deterministic_document_v1` and
  `deterministic_section_v1` always score `0`, for every domain, every
  run.
- The same defect exists on the semantic side:
  `_parse_semantic_criteria()` parses the `| ID | Weight | Score |
  Description |` table from `audit/semantic/{document,section}/{domain}.md`
  — that's the rubric's **maximum possible score per criterion**, not
  a judgment of whether this specific document met it. No LLM call
  happens anywhere in the current pipeline to actually judge the
  document against these criteria — `init.py`'s "content" phase is the
  only place semantic ever appears, and that's the placeholder from
  §11, not an audit call.

### 20.2 Root cause and fix

There is no **evaluator** step between "rule/criterion definition" and
"`calculate.py`'s formula input." Two are needed:

**Deterministic evaluator** (new script, e.g. `evaluate_rules.py`):
reads each `audit/deterministic/{document,section}/{domain}.yaml`,
dispatches on `evidence.type` (confirmed types from reading actual
files: `section_presence` — checks `required_semantic_types`/
`semantic_type` against the document's actual section headings;
`section_content` with `check: non_empty` — checks the section isn't
just a bare heading), and produces `{id, weight, mandatory, passed,
evidence}` — **this** is what `calculate.py` should consume, not the
raw rule file. Needs the document's sections tagged with a
`semantic_type` to match against — either `scaffold.py` writes this
tagging when it creates headings (it currently doesn't — it writes
plain markdown headings with no semantic-type metadata), or the
evaluator derives it from heading-text matching against the template's
known section order. Either way, this mapping doesn't exist today and
is a prerequisite, not just the evaluator itself.

**Semantic evaluator** (a real invocation, not `init.py`'s placeholder):
an actual `semantic-audit` phase (kind: `semantic`) that judges the
generated document against `audit/semantic/{document,section}/{domain}.md`'s
rubric — engineering_intent, audit_objectives, red_flags, and the
scoring_criteria table — and produces `{criterion_id, passed,
confidence, evidence}` per criterion. `calculate.py`'s
`semantic_document`/`semantic_section` formulas should consume *this*
output, not the static table `_parse_semantic_criteria` reads today.

## 21. Semantic Audit Context Injection — Grounding the Judgment

Your point: deterministic checks already produce metrics that would
help ground the semantic judgment, and nothing threads them through
today. Confirmed concretely — `script/schema/12-qa/unit-test-coverage.schema.json`
requires `metrics.coverage_percent` (a real number, 0–100) in every
`unit-test-coverage` check result. A semantic audit of the `qa` domain
judging "is testing adequate" is currently done (once §20 makes it
real) from the document's *prose description* of testing alone — it
never sees the actual `coverage_percent` number `validate.py` already
computed in the same pipeline run.

**Proposed mechanism:** a `pre_script` (§13's contract, already has a
slot for this) on each domain's semantic-audit phase —
`gather_semantic_context.py` — that:
1. Reads `validate.py`'s findings for checks relevant to this domain
   (per `script/mapping.yaml`'s `consumed_by` list — e.g. `qa`'s
   semantic audit pre-script pulls `unit-test-coverage`'s
   `coverage_percent` and `pass`/`fail` status; `engineering`'s pulls
   `lint-standards`'s result)
2. Formats that as a short "Supporting Evidence" block
3. Passes it alongside the document text as additional context for the
   semantic audit's LLM call

**`audit/semantic/{document,section}/{domain}.md` files need updating
to expect this** — e.g. `audit/semantic/document/12-qa.md`'s rubric
should explicitly say something like *"Supporting evidence: this
domain's `unit-test-coverage` check result (coverage_percent) is
provided — weigh the document's testing claims against the actual
measured coverage, not just the prose"* — not read in this pass to
confirm current wording, but this is the alignment your message is
asking for: the rubric prompt should name what grounding data it
expects, matching what `gather_semantic_context.py` actually supplies,
so the two don't silently drift apart the way `plan/core`/`plan/usecase`
already did once (§16).

## 22. Analysis & Fix-Plan Confirmation — A Human Checkpoint Before Fix

Currently `init.py`'s fix loop (§11, and `03-fix.md`'s generated
procedure) decides fix scope and applies it automatically, no human
step in between. Proposed new phase, **`analyze`** (kind: `semantic`),
inserted after `report` and before `visualize`:

```
report (script)     → renders scores + findings to markdown
    ↓
analyze (semantic)  → NEW. Reads calculate.py's scores, validate.py's
                        findings, and (once §20 exists) the real semantic
                        audit findings. Produces a structured fix plan:
                        which domains/sections are failing, why, and
                        whether the fix should be section-level or
                        whole-document (same decision `03-fix.md`
                        already documents — this phase makes that
                        decision explicit and saved, not implicit and
                        immediately acted on).
                        Output: saved to `{domain}-fix-plan.json`
                        (or a DB row, once §12's local-vs-samgraha
                        question is revisited) — NOT executed yet.
    ↓
visualize (script)  → 8 PNG charts (§19) — can now also chart the
                        proposed fix plan's scope (e.g. how many
                        sections flagged, which domains)
    ↓
report_html (script) → renders the fix plan alongside the score charts
    ↓
[CHECKPOINT]         → NEW. The confirm-or-edit step you're describing:
                        present the fix plan to the user (via the
                        rendered HTML report or directly), user either
                        approves it as-is, edits scope (e.g. "also fix
                        this section" / "skip that one"), or rejects it
                        entirely (falls back to `human_review`, same
                        fallback `loop.yaml` already defines for
                        exhausted iterations)
    ↓
fix (semantic)       → executes ONLY the confirmed plan, not a fresh
                        auto-decided scope — same section-level vs
                        whole-document mechanism `03-fix.md` already
                        specifies, now scoped by the confirmed plan
                        rather than decided fresh each iteration
```

This changes the fix loop from "automatic, no visibility" to
"proposed, visible, confirmable, then executed" — matches your
"user can agree or add their point and confirm plan" requirement
directly.

## 23. `plan/usecase/` Generation Must Include All of the Above

Confirmed by reading the regenerated `01-generation.md`/`02-audit.md`/
`03-fix.md` for `repo_new/case_1_no_documentation`/tier 1 directly:
**none of the 96 generated files name a single script.**
`01-generation.md` says "generate a complete document... using the
document-level generation template" — never `scripts/scaffold.py`.
`02-audit.md` says "Run `audit/deterministic/document/{domain}.yaml`
against the document" as if the YAML evaluates itself — never
`scripts/validate.py` or any evaluator. `03-fix.md` names no script at
all. This is the same class of gap §20 found in the code — the
generated docs describe *what* should happen but never *which script
does it*, and (confirmed) never mention `pre_script`/`post_script` even
though `init.py` itself has `run_pre_script`/`run_post_script` wired in.

**Fix, single point of leverage:** `render_usecase_docs.py` generates
all 96 files from one template (§16) — extending that template once
propagates to all 4 use cases uniformly, which is exactly what "all
these are missing for all usecases" needs. The template needs to add,
per step:
- The concrete script name (`scaffold.py`, `evaluate_rules.py` §20,
  `validate.py`, `calculate.py`, `report.py`, `analyze.py` §22,
  `visualize.py`, `report_html.py`)
- `pre_script`/`post_script` for that step, when one applies (e.g.
  `gather_semantic_context.py` §21 as semantic-audit's `pre_script`)
- A new 4th generated file per tier, **`04-analyze.md`**, describing
  §22's analysis+confirmation phase — currently the generator only
  produces 3 files per tier (`01-generation`, `02-audit`, `03-fix`);
  this needs a 4th

## 24. Explicitly Out of Scope (this update)

~~Actual implementation of `evaluate_rules.py` (§20), the semantic
evaluator (§20), `gather_semantic_context.py` (§21), the `analyze`
phase (§22), the confirmation-checkpoint UI/mechanism (§22), and
`render_usecase_docs.py`'s template extension (§23) — all specified
here, none built. Fixing `calculate.py`'s current always-0
deterministic score (§20.1) — flagged as a real bug needing a fix, not
patched in this document.~~ **All implemented.** `evaluate_rules.py`,
`evaluate_semantic.py`, `gather_semantic_context.py`, `analyze.py` exist
and are wired into `init.py`. `calculate.py` reads evaluated results.
`render_usecase_docs.py` generates `04-analyze.md` with script names.

**Still out of scope:**
- Confirmation-checkpoint UI/mechanism (§22) — the fix plan is saved to
  JSON but the human approve/edit/reject step is a UI concern, not a
  script. The HTML report presents the plan; the user edits/confirms
  externally.
- `compile_hook.py` (§14) — DB ingestion bridge, by design (§12.1).
- Any change to domain content, audit rules, or the tier/relationship graph.

## 25. End-to-End Test Results (verified)

32 scripts total (28 + `evaluate_rules.py`, `evaluate_semantic.py`,
`analyze.py`, `gather_semantic_context.py`), all compile clean
(`python -m py_compile *.py`, confirmed). 5 bugs found and fixed during
a real end-to-end pipeline run:

1. **Domain name mismatch** (`01-vision` vs. bare `vision`) — template/rule
   files use the numbered prefix, the pipeline was passing the bare
   name. Fixed with a shared `resolve_domain()` helper in `_common.py`,
   applied across `scaffold.py`, `evaluate_rules.py`,
   `evaluate_semantic.py`, `calculate.py`.
2. `visualize.py` — Windows `charmap` codec can't encode `✓`/`✗` in
   matplotlib output. Replaced with ASCII `OK`/`FAIL`.
3. `report_html.py` — shape mismatch between `results.json`'s flat
   `{"score": ..., "rating": ...}` and the chart code's expected
   nested `{"final_score": {"score": ...}, "score_bands": {"rating":
   ...}}`. Fixed with normalization at load time; stopped passing the
   wrong-shaped per-domain `scores_json`, reads `results.json` directly
   now.

**Confirms §20's core finding is fixed, not just addressed on paper:**
`det-eval.json` shows real, non-trivial pass rates (5/7 document rules,
25/37 section rules) — `evaluate_rules.py` is producing genuine
`passed` values now, breaking the always-0 chain §20.1 traced through
`calculate.py`. Output verified per domain: 8 PNG charts, one
self-contained HTML report (445KB, base64-embedded charts),
`det-eval.json`, `sem-eval.json`, `fix-plan.json` (§22, confirms
`analyze.py` is producing real fix plans, not just existing), `scores.json`.

**Remaining limitations, not new findings — both already flagged
elsewhere in this document:**
- Score stays low because scaffolded documents have no real content —
  this is §11's original "semantic content-fill is a placeholder" gap,
  not a new bug. The evaluator correctly fails "no empty required
  sections"-type rules against heading-only stubs.
- Fix loop can't improve scaffolded docs for the same reason — nothing
  generates real content to inject, so `analyze.py`'s proposed fixes
  have no content-generation step to act on yet.
- Tier gate blocks at Tier 1 — expected and correct behavior, not a
  bug: scaffolded-only docs *should* fail the gate.

**Net effect:** the audit/scoring/visualization/analysis layer (§14,
§15, §20–§22) is now real, tested, and produces meaningful (if low,
for the right reason) numbers end-to-end. The one gap every one of
these results traces back to is still §11's original finding: nothing
in the pipeline actually writes section content. That remains the
highest-leverage next gap to close — every other layer built on top of
it (evaluation, scoring, visualization, fix-plan analysis) is now
verified working and waiting on real content to operate against.
