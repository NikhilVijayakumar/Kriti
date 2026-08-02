# rust_dev — Repo-State-Scoped Workflow Restructure (Proposal 8 of 8)

## 0. Series

Part of the same set — see
[`archive/1-rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
Proposals 1-7 executed and are archived
(`docs/proposal/archive/{1..7}-rust_dev-*.md`, commit `5780be1`) — this
proposal is new work on top of that landed state, not a design pass
against still-open proposals. Depends on proposal 1 (the
`tierN/`/`domain/`/`common/` layout this proposal restructures further)
and proposal 3 (the per-domain usecases this proposal re-sequences, not
renames). **Corrects proposal 1 §4** (drops the NN-prefix decision —
restoring it, see §3) and **corrects proposal 7** (drops its unified
single-branching-prompt model and its `migrate-document-{domain}`
usecases — see §5, §6). Owner-directed, not a gap found by re-reading
source; captures a live working session's architecture decision.

## 1. What exists today (traced against live files)

Root, post proposal 1 (confirmed live):

```
rust_dev/
├── common/{calculation,schema,script,schema-manifest}/
├── domain/{vision,philosophy,...,product-guide}.md   # 13 files, flat, no NN-prefix
├── tier1/{audit,templates,plan}/                      # bare at root
├── tier2/ ... tier8/                                  # same shape, no tier4
├── plan/core/{tiers.yaml,loop.yaml,README.md}         # bare at root
├── script/{mapping.yaml,policy.yaml}                  # bare at root
├── templates/audit/README.md                          # bare at root
└── 00-domain-relationships.md, SYSTEM.md, ...
```

Three things the owner flagged as wrong with this, this session:

1. **`domain/*.md` lost its ordering cue.** Proposal 1 §4 dropped the
   `NN-` prefix on the theory that once files live under `tierN/`, the
   folder already encodes order. That reasoning doesn't hold for
   `domain/` itself — `domain/` was never nested per-tier (confirmed
   live: it's a flat 13-file list, both before and after proposal 1) — so
   dropping the prefix removed the only ordering cue a flat directory
   listing had, for no compensating gain.
2. **`tierN/`, `plan/`, `script/`, `templates/` sit bare at root.** Every
   tier's `audit/`/`templates/`/`script`-adjacent content (domain-specific,
   but **not** repo-state-specific — the same `vision.yaml` deterministic
   rule applies whether the target repo is brand new or has ten years of
   docs) is currently a root-level peer of `common/`, not inside it.
   Separately, `plan/core/*`, `script/{mapping,policy}.yaml`, and
   `templates/audit/README.md` are root-level singletons with no
   repo-state or tier scoping at all.
3. **The repo-state split is nested backwards, and one-dimensional in the
   wrong place.** Today's `tierN/plan/usecase/{repo_new,repo_existing}/
   {case_1_no_documentation,case_2_has_documentation}/{01,02,03}.md` (12
   files per tier × 7 tiers = 84 files, confirmed live count) nests
   repo-state *inside* tier. Proposal 7 kept these files as CoT reference
   material but otherwise collapsed the whole 2×2 matrix into one
   `propose-tierN-assess` usecase with one branching prompt, deciding
   per-domain (§7's decision, this same session, now revised — see §5).

## 2. Proposed layout

Root has exactly five top-level entries — `common/`, `domain/`, and three
repo-state-scoped folders. Nothing else lives bare at root:

```
rust_dev/
├── common/
│   ├── calculation/                       # unchanged — proposal 1 §3's reasoning still holds
│   ├── schema-manifest/standard.yaml       # unchanged
│   ├── schema/                             # unchanged (cross-tier check schemas + new dev_*.sql)
│   ├── script/                             # unchanged (_generic checks, _adapter.py, dev_schema.py, seeder.py)
│   └── tier1/ ... tier8/                   # MOVED here from root — audit/templates/script/prompt
│       ├── audit/{deterministic,semantic}/{document,section}/{domain}.*
│       ├── templates/{generation,audit}/{document,section}/{domain}/*
│       ├── script/                          # this tier's check scripts (proposal 3 §4)
│       └── prompt/                          # generate-{domain}/semantic-audit/fix-{domain} prompts
├── domain/
│   ├── 01-vision.md                        # NN-prefix restored, see §3
│   ├── 02-philosophy.md
│   ├── 03-security.md
│   ├── 04-feature.md
│   ├── 05-architecture.md
│   ├── 07-engineering.md                   # gap at 06 (design, dropped domain) preserved, see §3
│   ├── 08-external-context.md
│   ├── 10-feature-technical.md             # gap at 09 (feature-design, dropped) preserved
│   ├── 12-qa.md
│   ├── 13-implementation.md
│   ├── 14-build.md
│   ├── 15-readme.md
│   └── 16-product-guide.md                 # gap at 11 (prototype, dropped) preserved
├── repo_new/
│   └── tier1/ ... tier8/
│       └── plan/                            # create -> audit -> fix, sequential, tier-gated
├── repo_existing/
│   └── tier1/ ... tier8/
│       └── plan/                            # audit -> fix/create per domain
├── repo_existing_no_doc/
│   ├── bootstrap/                           # NEW — cross-tier, runs once before tier1
│   │   └── plan/                            # "create an in-depth README" — see §4
│   └── tier1/ ... tier8/
│       └── plan/                            # same as repo_existing after bootstrap completes
├── 00-domain-relationships.md, SYSTEM.md, CHANGELOG.md, CONTRIBUTING.md,
│   migration-guide.md, standard.metadata.json, system.yaml
```

Nothing bare at root under `plan/`, `script/`, or `templates/` — every
file that lived there moves into `common/` (if repo-state-agnostic) or
one of the three repo-state folders (if not), per the owner's own rule:
*"there should not be a script/plan/template in global — it's in common
or the other 3 folders."*

- `plan/core/tiers.yaml`, `loop.yaml` → `common/plan/core/` (cross-tier
  engine config, same reasoning proposal 1 §3 already gave for keeping
  `loop.yaml` singular rather than per-tier — that reasoning is about
  tier-scope, not repo-state-scope, so it still applies once nested under
  `common/`).
- `script/mapping.yaml`, `policy.yaml` → `common/script/` (cross-domain
  indexes, proposal 1 §3's reasoning unchanged).
- `templates/audit/README.md` → `common/templates/audit/README.md` — the
  one place this proposal's `common/` tree needs a bare `templates/` dir
  of its own, since this file documents the audit template *system*
  across every tier, not one tier's content.

## 3. `domain/*.md` — NN-prefix restored, correcting proposal 1 §4

Proposal 1 §4 recommended dropping the prefix once tier folders existed
to encode order. That reasoning doesn't survive contact with §1's fact:
`domain/` was never tier-nested, prefix or no prefix — it's the flat list
of *domain standards* (what "good" looks like per domain), sitting beside
`common/` and the three repo-state folders, not inside any of them.
Restoring the prefix for a flat directory is a legitimate readability
call, independent of whether tiers got restructured.

**Recommend keeping the original, gapped numbering**
(`01,02,03,04,05,07,08,10,12,13,14,15,16` — gaps at `06`/`09`/`11` for
`design`/`feature-design`/`prototype`, the three domains `rust_dev` drops)
rather than renumbering to a clean `01-13`. Same reasoning as proposal 1
§6 item 3's tier-4 decision (this session): the number stays a stable
identifier shared with `base_dev` and every other `dev`-class sibling —
`07-engineering.md` means the same thing in `rust_dev` and `base_dev`,
where a clean `01-13` renumber would drift the moment you compare the two.

**Cost, same discipline as proposal 1 §4/§5**: 214 files reference
`domain/{name}.md` today (confirmed live grep, `templates/generation/
section/**/*.md`'s `Source:` lines + `templates/audit/**/*-report.md`'s
`Standard:` lines + `00-domain-relationships.md` + `CONTRIBUTING.md`),
all needing the `NN-` segment re-added. Mechanical, but not optional —
apply in the same pass as the move, not as a follow-up.

## 4. Three repo-state workflows

```
repo_new:            create -> audit -> fix (iterate, ≤5, human_review fallback) -> finalize -> next tier
repo_existing:        audit -> fix | create (per domain, iterate) -> finalize -> next tier
repo_existing_no_doc:  bootstrap(create in-depth README) -> [same as repo_existing from here]
```

- **`repo_new`** — no code, no docs. Every domain is trivially "create."
  Strict sequential: a tier's `create -> audit -> fix` loop must finalize
  (score ≥ threshold, per `loop.yaml`'s existing `fix_loop` config) before
  the next tier starts — `loop.yaml`'s `tier_gate` rule, unchanged from
  proposal 1.
- **`repo_existing`** — code exists, some docs exist, conformance unknown
  per domain. Audit first (no assumption that "create" is ever the right
  first move), then per domain: `fix` if a conforming-shaped doc scored
  below threshold, or the same `fix-{domain}` usecase run against nothing
  if the domain has no doc at all — **no separate "migrate" usecase**, see
  §6.
- **`repo_existing_no_doc`** — code exists, *zero* documentation anywhere.
  Distinct from `repo_existing` because there's nothing to audit yet, and
  distinct from `repo_new` because there's a whole codebase a first-pass
  README should ground itself in before any tier starts. One new,
  cross-tier, one-time step — `bootstrap`, not nested under any `tierN/` —
  drafts an in-depth README from the existing code, **then** the workflow
  is identical to `repo_existing` from tier 1 onward (same `plan/`
  content, not a third copy — see §6's usecase-reuse recommendation).

This replaces the old 2×2 `{repo_new,repo_existing} ×
{case_1_no_documentation,case_2_has_documentation}` matrix with a 3-way
split. Old `repo_new/case_2_has_documentation` (a brand-new repo that
somehow already has docs) drops out entirely — recommend treating that as
a degenerate case of `repo_existing` in practice (code may not exist yet,
but the docs-exist condition is what actually matters for the workflow
choice), not a fourth folder.

## 5. What happens to proposal 7's `propose-tierN-assess`

Proposal 7 §7 decided (this same session, prior turn) *"one prompt,
branches on repo-state at runtime — not two separate prompts."* This
proposal reverses that, now that the workflows are shown to diverge more
than a single CoT branch comfortably covers — `repo_existing_no_doc`'s
bootstrap step in particular has no equivalent step in the other two
flows at all, not just a different answer to the same question.

**Recommend**: three top-level propose usecases per tier, not one —
`propose-repo-new-tier{N}`, `propose-repo-existing-tier{N}`, and
`repo_existing_no_doc` reusing `propose-repo-existing-tier{N}` unchanged
*after* its one-time `bootstrap-readme` usecase completes (not a third
propose variant — the decision each tier needs to make is the same one
`repo_existing` already makes, given a README now exists to audit
against). Each lives under its own repo-state folder's `plan/`, per §2 —
`repo_new/tier{N}/plan/propose-repo-new-tier{N}.md`-shaped, not a shared
file with an internal branch.

## 6. What happens to proposal 3's per-domain usecases and proposal 7's `migrate-document-{domain}`

**Unchanged, not renamed**: `generate-document-{domain}`,
`deterministic-audit-{domain}`, `semantic-audit-{domain}`,
`fix-{domain}` stay exactly as proposal 3 declared them. The mechanics of
generating, auditing, or fixing one domain's document don't depend on
which repo-state folder triggered the call — only the *orchestration*
(which usecase runs first, in what order) is repo-state-specific, and
that's what §4/§5 relocate, not the atomic actions themselves.

**Dropped**: proposal 7 §6's `migrate-document-{domain}` (13 usecases,
already declared in `standard.yaml` — removal is this proposal's one
concrete `standard.yaml` edit once accepted). Owner's own framing: *"no
migration needed as we are proposing it for rust"* — a non-conforming
existing doc under `repo_existing` just fails `deterministic-audit-
{domain}`/`semantic-audit-{domain}` and runs through the ordinary
`fix-{domain}` loop like any other failing domain, content-preserving
restructuring included. `migrate-document-{domain}`'s distinct
step shape (`gather-existing-doc` -> restructure -> `persist-fix`) was
solving a problem `fix-{domain}`'s existing shape (`gather-fix-context`
-> regenerate -> `persist-fix`) already covers once there's no separate
"preserve original structure" requirement — which there isn't, per this
decision.

## 7. Cross-reference cost (mechanical, must be exhaustive — same discipline as proposal 1 §5)

Confirmed live counts, not estimates:

| Change | Files affected | What moves |
|---|---|---|
| `domain/*.md` NN-prefix restored | 214 (`grep -rl "domain/[a-z-]*\.md"`) | `domain/{name}.md` → `domain/NN-{name}.md` in every `Source:`/`Standard:` line, `00-domain-relationships.md`, `CONTRIBUTING.md` |
| `tierN/` → `common/tierN/` | 279 (`grep -rlE "\btier[0-9]/"`) | every `audit/`/`templates/`/`script/`/`prompt/` path reference gains a `common/` prefix |
| `tierN/plan/usecase/*` → `repo_{state}/tierN/plan/` | 84 (12 files × 7 tiers, confirmed live count in `tier1/`) | repo-state moves from inner path segment to outer folder; `case_1_no_documentation`/`case_2_has_documentation` labels retire in favor of the 3-way split (§4) |
| `plan/core/*`, `script/{mapping,policy}.yaml`, `templates/audit/README.md` | 6 files, plus every reference to them (`loop.yaml` is referenced throughout `standard.yaml`'s comments, `common/script/seeder.py`'s domain-tier loader reads `plan/core/tiers.yaml` directly — that path literally changes) | root-level singletons move under `common/` |

`common/script/seeder.py`'s `_load_domain_tier_map()` (built this
session, proposal 6/"start with seeder.py") reads
`RUST_DEV_ROOT / "plan" / "core" / "tiers.yaml"` — this is a **real, live
code dependency**, not just a doc reference. If this proposal executes,
that one-line path needs to become `RUST_DEV_ROOT / "common" / "plan" /
"core" / "tiers.yaml"` in the same change, or the seeder breaks silently
(file-not-found) the next time it runs. Flagging explicitly since it's
the first proposal in this series to land after real, tested code exists
to break.

## 8. Open questions

1. **`repo_existing_no_doc`'s `bootstrap` step — one usecase or does it
   need its own tier-like structure?** §4/§5 treat it as a single
   cross-tier `bootstrap-readme` usecase producing one README, then
   handing off to `repo_existing`'s per-tier flow. Recommend keeping it
   that singular — an in-depth README is one artifact, not a per-domain
   one — but flagging since nothing else in this series has a
   before-tier-1, non-tier-scoped usecase to precedent against.
2. **Does the bootstrap README get audited by any domain's usecase, or is
   it purely an input to later generation, never itself a `readme`
   domain deliverable?** `readme` is already domain 15/tier 8 in the
   existing model — is `repo_existing_no_doc`'s bootstrap README the
   *same* artifact tier 8's `readme` domain eventually audits/finalizes,
   or a throwaway scaffold superseded by tier 8's real pass? Real
   ambiguity, not flagged anywhere in the owner's framing — needs an
   explicit call before `bootstrap`'s usecase shape can be written.
3. **`propose-repo-new-tier{N}`'s "trivial" scan** — §5 assumes it still
   runs (not skipped), matching proposal 7 §3's original *"no
   special-cased new-repos-skip-proposing shortcut"* stance. Does that
   stance still hold now that `repo_new` is its own top-level folder with
   its own usecase, rather than a branch of one shared usecase? Recommend
   yes, unchanged — the folder split is about where the *files* live, not
   a reason to reopen a decision about whether the *step* runs.

## 9. Explicitly out of scope

Actually executing any of §2's moves, §3's rename, or §7's cross-reference
updates — this proposal is the design; execution is a separate pass, same
convention proposal 1 established. Writing `bootstrap-readme`'s script or
prompt content. Deciding open question 2 (bootstrap-vs-tier8-readme
relationship) — flagged for owner call, not resolved here. Any change to
`common/calculation/`, `common/schema/`, or the physical
`generate-document-{domain}`/`deterministic-audit-{domain}`/
`semantic-audit-{domain}`/`fix-{domain}` usecase definitions beyond their
directory location (§6 — mechanics unchanged, only orchestration moves).
