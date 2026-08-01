# rust_dev — Propose Pipeline: `.samgraha/proposal/tierN/*` (Proposal 5 of 7)

## 0. Series

Part of a 7-proposal set (not the last — see below) — see
[`rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
Depends on all four prior proposals: layout (1), manifest+schema (2),
real per-tier usecases (3), and — the hard dependency this proposal can't
function without — the per-tier usecase map (4), since every propose call
here is required to carry that map as context.

**Correction notice**: §4's `dev_proposal_usecase_scope` link table points
at proposal 4's now-superseded `dev_tier_usecase_map` —
[`6-rust_dev-samgraha-schema-alignment-proposal.md`](6-rust_dev-samgraha-schema-alignment-proposal.md) §6
keeps this proposal's underlying reasoning (a durable link is needed
because `proposal.usecase_id` is a singular FK and `phases[]` gets
validated-then-discarded, same gap
`pcems_2026-proposal-phase-generic-schema-proposal.md` already found for
pcems) but corrects the table shape to link `domain`/`usecase`/`step`
directly. Separately,
[`7-rust_dev-repo-state-propose-then-execute-proposal.md`](7-rust_dev-repo-state-propose-then-execute-proposal.md)
inserts a repo-state assessment step *before* this proposal's
`propose-tierN-generation` — this proposal still owns persist/link/render
mechanics, proposal 7 owns what decides what gets proposed in the first
place (create vs. migrate vs. skip-to-audit, per domain) instead of
assuming "generate" is always the right action.

**Status, checked against the live manifest**: `standard.yaml` now
declares all 21 `propose-tier{N}-{generation,audit,fix}` usecases from §3
(one triad per real tier), `steps: []` — matching proposal 3's own
"declared but not yet wired" precedent, for the same reason: none of §2's
5 steps' scripts/prompts exist yet, and writing them is explicitly out of
scope (§7). §4's table is superseded as described below — do not build it
as written; build `dev_proposal_phase_scope` (proposal 6 §6) instead. Both
tables are equally unbuilt right now — creating either is downstream of
`rust_dev` declaring `seeder_script:`, which is proposal 7's
`dev_repo_domain_state` dependency, not this proposal's to resolve.

## 1. Target shape, confirmed against a real target-repo tree

The user's example path (`E:\Python\Bodha\.samgraha\proposal`) is a real,
populated tree for pcems_2026 evaluating the Bodha repo — checked directly:

```
.samgraha/proposal/
├── step0/
│   ├── novelty/novelty-proposal.md
│   ├── gaps/gaps-proposal.md
│   └── data/{algorithms,figures,literature-review,mathematics,tables}/{name}-proposal.md
├── step1/
│   ├── asset-map/{algorithms,citations,equations,figures,tables}/{name}-asset-map-proposal.md
│   ├── generation/{abstract,conclusion,findings,front-matter,introduction,methodology,references}/{name}-generation-proposal.md
│   ├── section-map/section-map-proposal.md
│   └── section-profile/section-profile-proposal.md
└── step2/
    ├── audit/{per-section/{7 sections}/, role-based/role-based-audit-proposal.md}
    └── fix/{7 sections}/{name}-fix-proposal.md
```

Pattern: `.samgraha/proposal/{step}/{usecase-category}/{usecase-slug}/{usecase-slug}-{kind}-proposal.md`
— one file per usecase, in the target repo (Bodha), not in the standard's
own tree (pcems_2026 lives at `E:\Python\Bodha\.samgraha\pcems_2026\`,
separate from its proposal output). This confirms the user's model
precisely: `.samgraha/proposal/` is **target-repo-scoped output**, written
by whichever standard is currently evaluating that repo. For rust_dev
evaluating a Rust repo, the equivalent tree is
`{rust-repo}/.samgraha/proposal/tierN/{usecase-category}/{usecase-slug}/{usecase-slug}-{kind}-proposal.md`.

## 2. How pcems_2026 builds each of those files (mechanism to port)

Traced end-to-end (`common/script/propose/*.py` + `common/prompt/propose/*.md`
+ `common/templates/propose/*.md`), 5-step usecase pattern, same shape
across every `propose-*` usecase in `standard.yaml` §217-235 (scripts) /
§903-1207 (usecases, `propose-input` through `propose-fix`):

1. **`gather-proposal-context`** (deterministic) — phase-specific context
   assembly. Read in full: `_gather_generation_context` pulls domain list +
   upstream cross-module analyses; `_gather_audit_context` pulls rule/rubric
   counts; `_gather_fix_context` pulls failing findings;
   `_gather_section_context` pulls draft text + map entries + citations.
   Every branch ends by attaching `redraft_of` (prior rejection, if any,
   capped at 5 iterations — `main()`'s `iteration >= 5` early-exit) and
   `module_registry` — shared tail state every phase gets regardless of
   branch.
2. **prompt** (semantic) — drafts the proposal content from that context.
3. **`persist-proposal`** (deterministic) — append-only insert, `status=pending`.
4. **`link-proposal-scope`** (deterministic) — links to per-domain scope rows.
5. **`render-proposal`** (deterministic) — renders to markdown+html via
   `templates/propose/{phase}.md` (chevron/mustache templates — confirmed
   by `fix.md`'s `{{title}}`/`{{#user_comment}}` syntax).

## 3. rust_dev's version — same 5 steps, tier-scoped, map-mandatory

The one structural addition: step 1 must read proposal 4's
`dev_tier_usecase_map` **before** anything else, and that read result must
flow into every downstream step, not just the prompt — directly satisfying
*"any other info based on tier deman in input and look into input and
create proposal."*

```yaml
- name: propose-tierN-generation
  description: "draft a proposal for what tierN's document(s) will contain, always scoped by this tier's usecase map"
  steps:
    - order: 1
      kind: deterministic
      description: "read dev_tier_usecase_map WHERE tier_number=N (proposal 4) — hard-fails if the map is missing or stale (source_hash mismatch), does not silently proceed without it"
      script: gather-tier-usecase-map
    - order: 2
      kind: deterministic
      description: "gather generation-phase context (domain list, upstream tier outputs per tiers.yaml relationships) — same shape as gather-proposal-context's _gather_generation_context, tier-scoped"
      script: gather-tier-proposal-context
    - order: 3
      kind: semantic
      description: "draft the generation proposal for every domain in this tier"
      prompt: tierN-generation-proposal
    - order: 4
      kind: deterministic
      description: "persist proposal (status=pending)"
      script: persist-proposal
    - order: 5
      kind: deterministic
      description: "link proposal to this tier's usecase-map rows (not generic domain scope — usecase-map rows, since proposal 4 made those the addressable unit)"
      script: link-proposal-usecase-scope
    - order: 6
      kind: deterministic
      description: "render to {target-repo}/.samgraha/proposal/tierN/generation/{domain}/{domain}-generation-proposal.md"
      script: render-proposal

# Same shape, three more usecases per tier:
- name: propose-tierN-audit
- name: propose-tierN-fix
```

Step 1's hard-fail behavior is the deliberate difference from pcems's
model — pcems's `gather-proposal-context` has no equivalent upstream
dependency it can fail on (it reads whatever `academic_cross_module_analysis`
rows exist, empty is a valid state: `"(none yet)"` per
`_gather_generation_context`). Here, an empty/stale usecase map means
proposal 3's usecases for this tier changed and proposal 4 hasn't
regenerated — a real inconsistency, not a normal empty-state, so failing
loudly is correct (matches `ADDING-A-USECASE.md`'s general philosophy of
explicit registration over silent fallback — e.g. its §5 allow-list
sentinel note: only `custom:` gets a silent escape hatch, everything else
must be registered or it's an error).

## 4. `link-proposal-usecase-scope` — the one real schema departure from pcems (superseded — see proposal 6 §6)

Kept verbatim as the original design record; the *reasoning* below (a
durable link table is needed because `proposal.usecase_id` is a singular
FK and `phases[]` gets validated-then-discarded) is correct and still the
justification for building a link table at all — but proposal 6 §6 found
the FK target below wrong (points at proposal 4's dropped
`dev_tier_usecase_map`) and corrected it to link real `domain`/`usecase`/
`step` ids directly:

```sql
CREATE TABLE IF NOT EXISTS dev_proposal_phase_scope (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id  INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    domain_id    INTEGER NOT NULL REFERENCES domain(id),
    usecase_id   INTEGER NOT NULL REFERENCES usecase(id),
    step_id      INTEGER REFERENCES step(id)
);
```

Build this table, not `dev_proposal_usecase_scope` below — same reasoning,
corrected shape.

pcems's `academic_proposal_scope` links a proposal to `{domain_id,
usecase_id, step_id}` rows (per `standard.metadata.json`'s
`academic_proposal_scope` entry). rust_dev's equivalent needs a fourth
axis pcems doesn't have: **tier**. New table:

```sql
CREATE TABLE dev_proposal_usecase_scope (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id           INTEGER NOT NULL,
    tier_number            INTEGER NOT NULL,
    usecase_map_id          INTEGER NOT NULL REFERENCES dev_tier_usecase_map(id),
    FOREIGN KEY (usecase_map_id) REFERENCES dev_tier_usecase_map(id)
);
```

Linking to `dev_tier_usecase_map.id` directly (not re-deriving
domain/usecase/step separately) means a proposal's scope is traceable back
to *exactly* the usecase-map snapshot (via that row's `source_hash`) it was
drafted against — if `standard.yaml` changes and the map regenerates
before the proposal is approved, the link still points at the map version
the proposal actually saw, not silently drifting to whatever the map says
now. This closes the same class of gap
`pcems_2026-proposal-phase-generic-schema-proposal.md` §5 found in pcems's
own generic schema (*"samgraha validates `phases[]` against live data and
then discards it"*) — rust_dev's version keeps the link durable from the
start instead of retrofitting it later.

## 5. Prompts + templates — net-new content, structure ported

`common/prompt/propose/tierN-generation-proposal.md`,
`tierN-audit-proposal.md`, `tierN-fix-proposal.md` — same chevron/mustache
templating pcems uses (`fix.md`'s `{{title}}`, `{{#user_comment}}...{{/user_comment}}`
conditional-block syntax), but every template gets one new mandatory
section neither pcems template has: a rendered view of the tier's usecase
map (§3 step 1's output) so a human reviewing the rendered `.md` in
`.samgraha/proposal/tierN/...` can see which usecases/steps this proposal
covers without cross-referencing the DB — directly the "any other info
based on tier demand" requirement, made visible in the artifact itself,
not just used internally by the drafting prompt.

```
# templates/propose/tierN-generation.md
{{title}}

**Tier**: {{tier_number}} ({{tier_domains}})
**Usecase map source**: {{usecase_map_source_hash}}

## This Tier's Usecases
{{#usecases}}
- **{{id}}** ({{kind}}, {{step_count}} steps)
{{/usecases}}

## Proposal
{{content_md}}
```

## 6. Open questions

1. **Decided: hard-fail, don't auto-create.** `render-proposal` must
   hard-fail if `.samgraha/proposal/` (or its template) is missing rather
   than silently no-op — pcems's `render_proposal.py` gap
   (`pcems_2026-proposal-phase-generic-schema-proposal.md` §2 — empty
   `templates/proposal/{markdown,html}/` dirs silently producing zero
   output) is exactly the failure mode to design against, and §3 already
   commits this proposal to hard-fail-over-silent-fallback as its house
   style. Whether the *directory* itself gets created on first run (as
   opposed to the template file, which must already exist) is a smaller,
   genuinely mechanical call left to whoever writes `render-proposal.py` —
   not a design decision blocking anything upstream.
2. **Decided: re-check every propose call.** Proposal 4 §5's cache makes
   this cheap (same-hash no-op in the common case), and `standard.yaml`
   can change between a tier's generation and fix phases — checking once
   at generation time and trusting it through fix would silently drift.
3. **Decided: markdown-only for proposals.** `propose-tierN-*`/`propose-
   tierN-assess` proposals render markdown only, no HTML twin — a proposal
   is a human-review artifact read once, approved or rejected, not a
   long-lived report. This is *not* the same question as whether findings/
   scores get a rich HTML/PDF/DOCX report later — they do, but through a
   separate, DB-backed report pipeline (findings persist to `dev_*` tables
   via `persist-deterministic-findings`/`persist-semantic-score`, proposal
   3 §3; a `render-report`/`render-charts` pair renders from that DB data,
   not from a proposal's markdown). See proposal 6 §7 for that pipeline's
   schema — this proposal's own rendering stays markdown-only.

## 7. Explicitly out of scope

Writing the actual prompt content (§5 shows shape/skeleton only).
`approve-proposal`/`archive-proposal` usecases — pcems's versions
(`common/script/propose/approve_proposal.py`, `archive_proposal.py`) are
generic enough (operate on `proposal_id`, no domain/tier-specific logic
inside either) to reuse as-is once proposal 2's manifest registers them
under rust_dev — no rust_dev-specific redesign needed, so not covered
here. Any change to pcems_2026 itself.
