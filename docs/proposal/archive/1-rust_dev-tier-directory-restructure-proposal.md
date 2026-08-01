# rust_dev — Tier-Directory Restructure (Proposal 1 of 7)

## 0. Series

Seven proposals convert `rust_dev` from a flat, non-samgraha-registered
domain-doc tree into a tiered samgraha standard shaped like `pcems_2026`,
correctly wired to the real samgraha engine and its own repo-state-aware
propose gate. Dependency order — each depends on the previous landing
first:

1. **This doc** — directory restructure (`tierN/` replaces flat trees,
   `documentation-standards/` → `domain/`, `common/` holds cross-tier assets)
2. [`rust_dev-standard-manifest-registration-proposal.md`](2-rust_dev-standard-manifest-registration-proposal.md) — `standard.yaml` + `standard.metadata.json` + MCP registration (schema details corrected by proposal 6)
3. [`rust_dev-calculation-audit-usecase-wiring-proposal.md`](3-rust_dev-calculation-audit-usecase-wiring-proposal.md) — `calculation`/`audit` become usecases with deterministic/semantic steps
4. [`rust_dev-tier-usecase-map-generator-proposal.md`](4-rust_dev-tier-usecase-map-generator-proposal.md) — per-tier usecase map (mostly superseded by proposal 6 §3 — becomes a query, not a new table)
5. [`rust_dev-propose-pipeline-proposal.md`](5-rust_dev-propose-pipeline-proposal.md) — `propose-tierN-*` usecases writing to the target repo's `.samgraha/proposal/` (scope-link table corrected by proposal 6 §6; preceded by proposal 7's assess step)
6. [`6-rust_dev-samgraha-schema-alignment-proposal.md`](6-rust_dev-samgraha-schema-alignment-proposal.md) — corrects 2 and 4 against the real samgraha engine schema (`usecase`/`step`/`script`/`prompt`/`domain`/`proposal`, `E:\Python\samgraha`), not just `pcems_2026`'s `academic_*` tables
7. [`7-rust_dev-repo-state-propose-then-execute-proposal.md`](7-rust_dev-repo-state-propose-then-execute-proposal.md) — collapses the old 4-case (`repo_new`/`repo_existing` × `case_1`/`case_2`) matrix into a per-domain, evidence-based propose step ahead of every tier's create/migrate/audit/fix cycle

**Read order for a reviewer new to this series**: 1 → 2 → 3 → 6 (corrects
2) → 4 (then re-read in light of 6 §3) → 5 → 7. Proposals 2 and 4 are kept
as originally written rather than rewritten in place — proposal 6 states
exactly what it corrects and why, so the reasoning trail (including the
mistake) stays visible instead of silently disappearing.

## 1. What exists today (traced against live files)

`rust_dev` (`samgraha/system/dev/rust_dev/`) already has a tier concept —
`plan/core/tiers.yaml` and `SYSTEM.md`'s `[domain_tiers]` both declare:

| Tier | Domains |
|---|---|
| 1 | vision, philosophy |
| 2 | security, feature, architecture, engineering, external-context |
| 3 | feature-technical |
| *(4 — absent, not renumbered)* | — |
| 5 | implementation |
| 6 | qa |
| 7 | build |
| 8 | readme, product-guide |

But the tier is only used as **metadata** (a column in `tiers.yaml`, a
grouping in `plan/usecase/{repo_existing,repo_new}/{case_1,case_2}/tier_N/`
prose files). Every other tree is organized flat, by kind, spanning all 13
domains at once:

```
rust_dev/
├── documentation-standards/{01,02,03,04,05,07,08,10,12,13,14,15,16}-*-standards.md
├── audit/{deterministic,semantic}/{document,section}/{domain}.{yaml,md}
├── calculation/{deterministic,semantic}/{document,section}.yaml + summary/*.yaml
├── templates/{audit,generation}/{document,section}/{domain}/*
├── script/{schema,ubuntu,windows}/{domain}/{check}.*
└── plan/{core/{tiers.yaml,loop.yaml}, usecase/{...}/tier_N/*.md}
```

`pcems_2026` (the reference model) instead organizes by **pipeline step**:
`step0-extract/`, `step1-draft-for-completeness/`, `step3-plagiarism-humanize/`,
`step4 - final paper/` — each owning the `script/` and `prompt/` for only the
usecases that belong to it, with `common/` holding what's genuinely
cross-step (`schema/`, shared `script/`, shared `prompt/propose/`,
shared `templates/`). `standard.yaml`'s header states the intent
explicitly: *"Fully self-contained — every scripts:/prompts: location:
points inside pcems_2026's own tree... forked into local copies so no
standard reaches into another's files."*

`rust_dev` has no equivalent unit. Its tier is the right unit to use —
tiers gate on completion the same way pcems's steps do (`loop.yaml`'s
`tier_gate`: *"every domain in the tier must reach threshold before the
next tier starts"*, directly analogous to a step boundary).

## 2. Proposed layout

Map `stepN-slug/` → `tierN/` (numeric, no slug — pcems's steps have a
memorable stage name; rust_dev's tiers don't, they're just numbered cuts
of the same dependency graph in `00-domain-relationships.md`, so a bare
`tierN` is more honest than inventing a slug per tier):

```
rust_dev/
├── common/
│   ├── schema/                      # from script/schema/_generic/*  (cross-tier checks)
│   ├── script/                      # cross-tier scripts (propose/*, see proposal 5)
│   ├── prompt/                      # cross-tier prompts (propose/*, see proposal 5)
│   ├── templates/                   # reserved for proposal 5's propose/ templates — empty at execution time, nothing else qualifies as truly cross-tier (see §3)
│   └── schema-manifest/
│       └── standard.yaml            # proposal 2
├── domain/                          # renamed from documentation-standards/, see §4
│   ├── 01-vision.md
│   ├── 02-philosophy.md
│   ├── 03-security.md
│   ├── 04-feature.md
│   ├── 05-architecture.md
│   ├── 07-engineering.md
│   ├── 08-external-context.md
│   ├── 10-feature-technical.md
│   ├── 12-qa.md
│   ├── 13-implementation.md
│   ├── 14-build.md
│   ├── 15-readme.md
│   └── 16-product-guide.md
├── tier1/                           # vision, philosophy
│   ├── audit/{deterministic,semantic}/{document,section}/{vision,philosophy}.*
│   ├── templates/{generation,audit}/{document,section}/{vision,philosophy}/*
│   ├── script/                      # this tier's usecase scripts — EMPTY at execution time (vision/philosophy have no script/*/NN/ dirs today), populated by proposal 3
│   ├── prompt/                      # this tier's usecase prompts — EMPTY at execution time, populated by proposal 3
│   └── plan/usecase/{repo_existing,repo_new}/{case_1_no_documentation,case_2_has_documentation}/{01-generation,02-audit,03-fix}.md
├── tier2/                           # security, feature, architecture, engineering, external-context — script/ populated for 4 of 5 domains (03-security, 05-architecture, 07-engineering, 08-external-context have real script/{schema,ubuntu,windows}/NN/ dirs today; 04-feature does not)
├── tier3/                           # feature-technical
├── tier5/                           # implementation
├── tier6/                           # qa
├── tier7/                           # build
├── tier8/                           # readme, product-guide — script/ partially populated (16-product-guide has script/{schema,ubuntu,windows}/16-product-guide/ today; 15-readme does not)
├── plan/
│   ├── core/{tiers.yaml,loop.yaml,README.md}   # stays at root, deliberately NOT per-tier — see §3's loop.yaml note
│   └── usecase-map/                            # NEW, generated — proposal 4
├── calculation/                     # stays flat at root — see §3, generic not per-domain
├── script/{mapping.yaml,policy.yaml}            # stays at root — cross-tier indexes, see §3
├── 00-domain-relationships.md
├── SYSTEM.md, system.yaml, CHANGELOG.md, CONTRIBUTING.md, migration-guide.md
└── standard.metadata.json           # proposal 2
```

Per-domain trees slice cleanly into their tier because every domain
belongs to exactly one tier (`tiers.yaml` is a total partition of the 13
domains) — `audit/{deterministic,semantic}/{document,section}/{domain}.*`,
`templates/{generation,audit}/{document,section}/{domain}/*`, and
`script/{schema,ubuntu,windows}/{domain}/*` all move verbatim into the
matching `tierN/`. `plan/usecase/*/tier_N/*.md` moves into `tierN/plan/usecase/*/`,
dropping the now-redundant `tier_N` path segment (the parent dir already
says it).

## 3. What stays at root/common, and why

Two trees are **not** domain-keyed and must not be sliced per tier:

- **`calculation/`** — confirmed by reading `calculation/deterministic/document.yaml`
  and `calculation/README.md`: formulas are generic (`weighted_pass_rate`,
  `sum_capped_at_100`, `weighted_sum`, `threshold_lookup`), domain-specific
  input comes from `audit/` at read time via a path template
  (`inputs.from: audit/deterministic/document/{domain}.yaml`), not from
  anything calculation-side. README's own words: *"Generic, not per-domain:
  One formula per bucket type; domain-specific inputs come from `audit/`."*
  Splitting it 13 ways would create 13 identical copies of 7 files —
  pure duplication for no gain. Stays at root (or moves to `common/` — open
  question, §6).
- **`script/mapping.yaml`, `script/policy.yaml`** — both are cross-domain
  indexes by construction: `mapping.yaml`'s `consumed_by` list spans all 13
  domains for a single generic check (e.g. `traceability-refs-exist`);
  `policy.yaml`'s cache overrides are keyed by check name, not domain.
  Slicing these would require either duplicating rows across tiers or
  inventing a merge step nothing currently needs. Stays at root/common.
  **Caveat**: `mapping.yaml`'s own header says its `rule_id`s are
  *"illustrative IDs from the proposal's examples, not real audit rules
  yet... wiring happens in Phase 6"* — the file is a placeholder. The
  structural argument for "stays common" (an index keyed by check name,
  not domain, is inherently cross-tier) holds regardless of whether the
  rows are real, but the specific "spans all 13 domains" evidence cited
  here is illustrative content, not verified live wiring. Proposal 3 §5
  is where this file becomes real.
- **`script/schema/_generic/*` and `script/{ubuntu,windows}/_generic/*`**
  (`feature-family-mapping`, `traceability-refs-exist`) — genuinely
  cross-cutting checks consumed by multiple domains across multiple tiers
  (`mapping.yaml` confirms `traceability-refs-exist` is `consumed_by` all
  13 domains, same placeholder caveat as above). Moves to `common/schema/`,
  `common/script/{ubuntu,windows}/_generic/`.
- **`templates/audit/summary/*-report.md`** — `templates/audit/README.md`
  states these are already "domain-parameterized" (Jinja2 `{{ domain }}`
  variable, not per-domain files) — 13 files exist today
  (`01-vision-report.md` … `16-product-guide-report.md`) but each is a
  thin per-domain instantiation of one generic summary shape, one file per
  domain. **Decision: these move to `tierN/templates/audit/summary/`**,
  matching how the `document`/`section` templates already slice — not to
  `common/templates/` (§2's tree reserves `common/templates/` for
  proposal 5's propose-output templates only; nothing in the current tree
  qualifies as common at execution time). Only the scoring-*formula* layer
  (`calculation/`) is truly single-copy-common — the report *templates*
  that reference those formulas by stable ID are domain-specific files and
  slice per tier same as every other template.
- **`plan/core/loop.yaml`** — stays at root, not per-tier, deliberately
  asymmetric with pcems (which keeps its loop-equivalent scoped inside
  each step). Reason: `loop.yaml`'s `tier_gate` rule (*"every domain in
  the tier must reach threshold before the next tier starts"*) and its
  `within_tier_ordering` (external-context before engineering, tier 2)
  are cross-tier by definition — the gate logic for tier N necessarily
  references tier N+1's start condition, so a single tier's copy of
  `loop.yaml` would need to know about its neighbors, defeating the
  point of scoping it. One file, one engine driver, referenced by every
  tier — see §5 for why this makes it the single largest cross-reference
  surface in the whole restructure.

## 4. `documentation-standards/` → `domain/`

Direct rename, matching `pcems_2026/domains/` (pcems: `domains/01-title-and-metadata.md`
… `11-figures.md`). Two decisions to make explicitly, not silently:

- **Filename suffix**: keep `-standards.md` or drop it now that the parent
  dir name (`domain/`) already says what these are? pcems drops it
  (`01-title-and-metadata.md`, not `01-title-and-metadata-standards.md`).
  Recommend dropping, for consistency with the reference model — but this
  is a rename touching every cross-reference (`00-domain-relationships.md`'s
  tables, `script/mapping.yaml`'s comments, `migration-guide.md`), so list
  it as a single atomic sub-step, not scattered edits.
- **NN- prefix meaning**: `00-domain-relationships.md` states explicitly
  *"Filenames in this directory carry a NN- prefix showing the order docs
  get written in, not audit priority."* That authoring-order numbering
  currently **disagrees** with tier order for two files: `12-qa-standards.md`
  is tier 6 (validates *after* implementation), `13-implementation-standards.md`
  is tier 5 (built *before* qa) — so the NN prefix goes 12(qa), 13(impl)
  while the tier order goes impl(5), qa(6). This is real today, not a
  restructure artifact — but once each domain file lives inside its own
  `tierN/` folder, the tier folder itself now encodes order, and the NN
  prefix becomes redundant/misleading metadata sitting on top of a
  structure that already orders things differently. Recommend dropping the
  NN prefix entirely (`vision.md`, `qa.md`, …) once domains live under
  `tierN/`, keeping "authoring order" as a documented fact in
  `00-domain-relationships.md`'s prose table only, not encoded twice.
  **Decision: dropped — see §6.** It was a naming call, *and* a mechanical
  one: 128 of the 130
  `templates/generation/section/**/*.md` files carry a
  `> **Source:** documentation-standards/NN-*.md` front-matter line
  (confirmed count, e.g. `templates/generation/section/01-vision/01-purpose.md`),
  every one of the 65 `templates/audit/{deterministic,semantic}/{document,section}/`
  + `summary/` report files (5 dirs × 13 domains) references
  `documentation-standards/NN-*.md` by the same convention (confirmed
  against `templates/audit/deterministic/document/01-vision-report.md`'s
  `**Standard:** documentation-standards/01-vision-standards.md` line —
  document-level reports carry the same reference as section-level, not
  just the section/summary tiers), and `CONTRIBUTING.md`'s own contributor
  instructions (`"Create the template in templates/generation/section/NN-domain/"`,
  `"Create the .md rule in audit/semantic/section/NN-domain/"`) codify the
  NN-prefixed convention as the thing new contributors are told to follow.
  Dropping the prefix touches all of it in the same change — costed fully
  in §5, not treated as a side effect of the rename.

## 5. Cross-reference updates required (mechanical, but must be exhaustive)

Every file that hardcodes an old path must be updated in the same change
that moves the file, or the move breaks something silently (same failure
mode pcems_2026 hit and fixed by forking to local copies — see this doc's
epigraph quote in §1). An earlier pass of this table (5 rows, hand-picked)
missed the largest blast-radius files entirely — `plan/core/loop.yaml`
(the engine driver), all 84 `plan/usecase/*/tier_N/{01,02,03}.md` files,
all 130 `templates/generation/section/**/*.md` files, and all 65
`templates/audit/{deterministic,semantic}/{document,section}/` + `summary/`
report files. **Do not hand-pick this list at execution time** — run
`rg -l "audit/|documentation-standards/|templates/|tier_"` across the
whole tree first and reconcile the hit list against the table below;
treat any file the grep finds that isn't in this table as a sign the
table is still incomplete, not as a file to skip.

### 5.1 Path-template resolution rule (new — closes a gap the first pass left undefined)

Several files resolve a path via `{domain}` substitution at *runtime*, not
via a glob — `plan/core/loop.yaml`'s `path_selection.audit.deterministic_document:
audit/deterministic/document/{domain}.yaml`, and every
`calculation/*/*.yaml`'s `inputs.from: audit/deterministic/document/{domain}.yaml`.
Once `audit/` is sliced per tier, `{domain}` alone no longer resolves —
`security.yaml` lives at `tier2/audit/deterministic/document/security.yaml`,
and nothing in `loop.yaml` or `calculation/` currently knows `security`
belongs to tier 2. **Rule**: every runtime `{domain}`-template consumer
must resolve `domain → tier` via `plan/core/tiers.yaml` first, then
substitute `tier{t}/audit/...` — not glob. This is a different operation
from `mapping.yaml`'s `generated_from: tier*/audit/**/*.{yaml,md}`
(a *scan-time* regeneration glob, fine to leave as a glob since it's a
one-shot "find all the rule files" sweep, not a per-request lookup) — the
two must not be conflated into the same fix. `loop.yaml` and every
`calculation/*/*.yaml` need the domain→tier resolver; `mapping.yaml`
needs (and already gets) a glob.

### 5.2 Full inventory

| File(s) | What it references | New value |
|---|---|---|
| `plan/core/loop.yaml` | `templates/generation/document/{domain}.md`, all 4 of `audit/{deterministic,semantic}/{document,section}/{domain}.*`, `templates/audit/{deterministic,semantic}/{document,section}/{domain}-report.md` (×5 report-template lines), `templates/generation/section/{domain}/{section}.md` | resolve `{domain}` → tier via `tiers.yaml`, emit `tier{t}/...` per §5.1 — **the single largest edit in this restructure** |
| `plan/usecase/*/*/tier_N/{01-generation,02-audit}.md` (28+28 = 56 files) | `templates/generation/document/NN-*.md`, all 4 `audit/...` paths (confirmed live in `tier_1/02-audit.md`'s per-domain table) | `tierN/templates/...`, `tierN/audit/...` — these files are themselves relocating into `tierN/plan/usecase/...` (§2), so path text and file location move together |
| `plan/usecase/*/*/tier_N/03-fix.md` (28 files, but only 2 confirmed to reference old paths — the rest are likely path-free prose; verify all 28 during the `rg` sweep, don't assume the other 26 are clean without checking) | same `templates/...`/`audit/...` paths where present | same as the row above — moves with its file |
| `templates/generation/section/**/*.md` (130 files, 128 carry the `Source:` line) | `> **Source:** documentation-standards/NN-*.md` front-matter, `> **Relationships:** audit/deterministic/document/NN-relationships.yaml` (confirmed pattern via `01-vision/01-purpose.md`) | `domain/{name}.md` (or bare `{name}.md` if NN-prefix drops, §4), `tierN/audit/deterministic/document/{name}-relationships.yaml` |
| `templates/audit/{deterministic,semantic}/{document,section}/NN-*-report.md` + `summary/NN-*-report.md` (65 files — 5 dirs × 13 domains: det/document, det/section, sem/document, sem/section, summary; confirmed all 5 dirs reference old paths, not just section+summary) | `documentation-standards/NN-*.md`, `audit/{det,sem}/{doc,section}/NN-*` | `domain/{name}.md`, `tierN/audit/...` |
| `calculation/{deterministic,semantic}/{document,section}.yaml` (4 files) + `calculation/README.md` | `inputs.from: audit/deterministic/document/{domain}.yaml`-style templates | apply §5.1's resolver — `calculation/` itself stays common (§3), only its `inputs.from` values need the tier segment inserted at read time |
| `00-domain-relationships.md` | bare `NN-name-standards.md` filenames in its tier tables (not `documentation-standards/`-prefixed paths — corrected from an earlier pass of this table, which implied the wrong prefix) | `domain/{name}.md` |
| `CONTRIBUTING.md` | `templates/generation/section/NN-domain/`, `audit/semantic/section/NN-domain/` contributor-facing conventions (§4) | `tierN/templates/generation/section/{name}/`, `tierN/audit/semantic/section/{name}/` |
| `migration-guide.md` | `05-architecture`, slot numbers "09-12 in `07-engineering`" | domain names unaffected (content, not path), but table headers implying flat layout should note tier |
| `script/mapping.yaml` | header comment `generated_from: audit/**/*.{yaml,md}` | `generated_from: tier*/audit/**/*.{yaml,md}` — scan-time glob, not §5.1's resolver (see §5.1) |
| `templates/audit/README.md` | `templates/audit/{deterministic,semantic,summary}/...` structure diagram | per-tier paths, plus the common/per-tier split from §3 |
| `plan/core/README.md` | describes `tiers.yaml`/`loop.yaml` as the sole plan files | update once `plan/usecase-map/` exists (proposal 4) |
| `CHANGELOG.md` | not yet read in this pass — audit during execution with the same `rg` sweep, don't assume clean | — |

## 6. Open questions — all resolved

The first two were decided and the move executed (working tree confirmed
against this doc's §2/§3/§5, git status shows the renames staged); the
third sat unresolved until owner review closed it separately:

1. **`calculation/` location: `common/calculation/`.** Recommendation
   taken as-is. Verified live: `common/calculation/{README.md,
   deterministic/,semantic/,summary/}` — no `calculation/` left at root.
2. **NN-prefix: dropped.** `domain/*.md` files are bare names
   (`domain/vision.md`, not `domain/01-vision-standards.md`); same drop
   carried into every relocated `tierN/` path (`tier1/audit/deterministic/
   document/vision.yaml`, not `01-vision.yaml`). Verified live.
3. **Tier 4's permanent absence — decided: keep the gap, don't renumber.**
   Root cause (traced this pass): `base_dev`'s `tiers.yaml` has tier 4 =
   `prototype`, and `rust_dev`'s original `system.yaml` explicitly drops
   `prototype` (with `design`/`feature-design`) — systems programming, no
   UI/prototyping concerns. `prototype` was tier 4's only domain, so
   dropping it left a hole rather than shifting tiers 5-8 down. Owner
   decision: keep the gap. Tier numbers stay identical across every
   `dev`-class sibling (`base_dev`, `rust_dev`, `electron_dev`,
   `fastapi_dev`, `react_dev`) — tier 5 means "implementation" everywhere,
   a stable cross-standard identifier — rather than `rust_dev` reading as
   a locally-tidy 1-7 sequence that drifts from its siblings. Cost: any
   code walking tiers must read the actual list from `tiers.yaml`, never
   assume contiguous integers — already true throughout this series (every
   tier-aware query/generator reads `tiers.yaml` directly, none assume
   `range(1, N)`), so this decision changes nothing already built.
   `tierN/` folders on disk run `tier1, tier2, tier3, tier5, tier6, tier7,
   tier8` — no `tier4/`, confirmed live, stays this way.

§5's cross-reference table was applied in full and verified against the
working tree: `plan/core/loop.yaml` now resolves `{domain}` → `tier{t}`
per §5.1 before substituting (`tier{t}/audit/...`, `tier{t}/templates/...`),
`script/mapping.yaml`'s `generated_from` is the `tier*/audit/**/*` glob,
and `00-domain-relationships.md`, `CONTRIBUTING.md`, `SYSTEM.md`,
`templates/audit/README.md`, `plan/core/README.md` all carry non-trivial
diffs consistent with the new paths.

## 7. Scope note

This doc originally scoped itself to design-only, with actual file moves
called out as a separate mechanical PR once §6 was decided. That sequencing
didn't hold in practice — the move landed in the same working tree as this
doc (see §6). Still out of scope: any change to domain *content*,
`standard.yaml` authoring (proposal 2), and wiring `calculation`/`audit`
into usecases/steps (proposal 3) — the files are relocated, not yet made
runnable through samgraha's step-execution model.
