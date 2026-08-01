# rust_dev — Repo-State-Aware Propose-Then-Execute Lifecycle (Proposal 7 of 7)

## 0. Series

Last of the set — see
[`1-rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
Depends on proposal 3 (real per-tier usecases), proposal 6 (usecase map is
a query against `usecase.data.tier` + `dev_repo_domain_state`, proposal 6
§5). Extends/refines proposal 5 — proposal 5's `propose-tierN-generation`
still owns persist/link/render; this proposal owns what happens *before*
that: repo-state assessment + the CoT decision that fills the proposal's
content.

**Status**: `standard.yaml` now declares 7 `propose-tier{N}-assess`
usecases (one per real tier) + 13 `migrate-document-{domain}` usecases
(one per domain), all `steps: []` per this series' established pattern
(§9 excludes script/prompt content). `custom_tables:` gained its first
real entry, `dev_repo_domain_state` (proposal 6 §5's design) — also in
`standard.metadata.json`'s `custom_tables[]`. This is the table that
finally justifies `rust_dev` declaring `seeder_script:` (proposal 6 §1's
condition), but `seeder_script:` itself is still not declared — the
table's existence in the catalog doesn't require the Python file to exist
yet, only *creating* rows in it does, and nothing creates rows until
`scan-tier-repo-state` (§4 step 1) is written, which is still §9's
explicit out-of-scope territory.

## 1. What the live plan actually does today — no propose gate exists

Traced `base_dev` and `rust_dev`'s `plan/usecase/{repo_new,repo_existing}/
{case_1_no_documentation,case_2_has_documentation}/tier_N/{01,02,03}.md`
directly (both systems — `base_dev`'s tree is the same shape,
`rust_dev`'s is a straight subset per tier list). Confirmed by reading all
four `tier_1` variants plus `03-fix.md`:

| Case | Stage 1 (`01-generation.md`) | Stage 2 (`02-audit.md`) | Stage 3 (`03-fix.md`) |
|---|---|---|---|
| `repo_new/case_1_no_documentation` | generate from scratch | *(same for all 4)* | *(same for all 4)* |
| `repo_new/case_2_has_documentation` | per-domain: migrate if pre-existing docs found, else generate — "Same as `repo_new/case_1_no_documentation/tier_1/01-generation.md`" for the generate branch | " | " |
| `repo_existing/case_1_no_documentation` | generate from scratch (code exists, docs don't; Tier 1 domains ignore code anyway) | " | " |
| `repo_existing/case_2_has_documentation` | migrate: *"Every domain starts with existing docs (Path B). No generation from scratch."* | " | " |

`03-fix.md`'s own words: *"No difference → same fix procedure across all
use cases."* `02-audit.md` (read for `repo_existing/case_1`): identical
structure across all four. **Only stage 1 varies, and only by a
pre-selected whole-tree label** (`case_1` vs `case_2`) — nothing in the
tree shows *what selects the case*, no `classify-repo`-equivalent script
exists in `rust_dev` (unlike `pcems_2026`'s real `classify-repo` usecase,
2-state `NO_DOCS`/`HAS_DOCS`, `min_doc_words: 200` threshold in its
`standard.yaml`). More importantly: **there is no proposal/approval gate
anywhere in this flow.** Stage 1 executes its prescribed prose procedure
mechanically once the case label is picked; nothing drafts a plan, nothing
asks a human to review it first. Proposal 5 added `propose-tierN-*`
usecases modeled on `pcems_2026`'s `propose-*` gates, but never actually
wired them to precede stage 1 here — this proposal closes that.

## 2. The gap, restated precisely

Two separate problems, both real:

1. **Case selection is a whole-tier label, not a per-domain decision.**
   A repo could have conforming docs for `vision` but nothing for
   `philosophy` — the 4-case model has no way to express "mixed" within a
   tier; it's forced into `case_1` or `case_2` as an all-or-nothing choice
   the prose files don't even show how to make.
2. **Nothing proposes before acting.** Even granting a correct case label,
   stage 1 just executes — no chain-of-thought about *why* this is the
   right action for this specific repo, no artifact a human can read and
   push back on before content gets written.

## 3. Proposed model — two lifecycles, not four, decided per domain

Collapse the 2×2 case matrix into two entry lifecycles keyed only on
`repo_new` vs `repo_existing` (a genuinely different starting condition —
no code, vs. code that may or may not have conforming docs). The
`case_1`/`case_2` distinction stops being a pre-selected label and becomes
a **per-domain finding** the propose step's repo scan produces:

```
NEW REPO:
  propose-tierN-create  →  (human review/approve)  →  create  →  audit  →  fix ⟲ (≤5, human_review fallback)

EXISTING REPO:
  propose-tierN-assess  →  (human review/approve)  →  [per domain: create | migrate | skip-to-audit]  →  audit  →  fix ⟲ (≤5, human_review fallback)
```

Both converge on the **same** audit↔fix loop (proposal 3's
`deterministic-audit-{domain}`/`semantic-audit-{domain}`/`fix-{domain}`
usecases, `loop.yaml`'s existing `fix_loop` config: `max_iterations: 5`,
`fallback: human_review`) — that part of the current design was already
right and stays. What changes is only what happens *before* the loop
starts, and that "before" step now produces a reviewable artifact instead
of executing prose.

For a new repo, the propose step still runs (not skipped) — its repo scan
trivially finds nothing for every domain, so its recommended action is
"create" everywhere, but it still goes through the same review/approve
gate as an existing repo's mixed-findings proposal. No special-cased
"new repos skip proposing" shortcut — consistency matters more than saving
one step for the simpler case.

**Naming correction**: the diagram above labels the new-repo entry usecase
`propose-tierN-create`, distinct from existing-repo's `propose-tierN-assess`
— but the paragraph right above it says no such special-casing exists (one
step, same gate, for both cases), and §4 only ever defines
`propose-tierN-assess`. The diagram's second name was a drafting slip, not
a second usecase — implemented as one `propose-tierN-assess` per tier,
matching the prose and §4, not the diagram's naming.

## 4. The propose step itself

Two steps, not one — a deterministic scan followed by a semantic decision,
matching the `kind: deterministic` / `kind: semantic` split every other
usecase in this series uses:

**`data: {tier: N}` correction**: the YAML below (and §6's
`migrate-document-{domain}`) shows a `data:` block on the usecase — but
proposal 6 §2, which this proposal names as a dependency, already read
`register_standard.rs`'s `UsecaseDecl` struct directly and found no
generic `data:` passthrough exists; an unrecognized key is silently
dropped by serde at registration, not stored. Implemented without `data:`
— `tier` stays a field `seeder.py` computes at seed time (proposal 6 §2's
mechanism), same as every other usecase in this series.

```yaml
- name: propose-tierN-assess
  description: "scan repo state for this tier's domains, draft a per-domain action proposal via chain-of-thought"
  steps:
    - order: 1
      kind: deterministic
      description: "for each domain in this tier: does a doc exist at the expected path, does its content look template-shaped (heading structure, required sections present) — cheap structural check, not a conformance audit. Persist to dev_repo_domain_state (proposal 6 §5)."
      script: scan-tier-repo-state
    - order: 2
      kind: deterministic
      description: "query this tier's usecase map (proposal 6 §3's query) + tiers.yaml's relationships for upstream-tier context"
      script: gather-tier-usecase-map
    - order: 3
      kind: semantic
      description: "role-based CoT: given the standard's expectations (step 2) and the repo's actual state (step 1), decide per domain: create / migrate / skip-to-audit, with rationale"
      prompt: tierN-assess-proposal
    - order: 4
      kind: deterministic
      description: "persist proposal (status=draft) — phases[] per domain, each phase's usecases[]/steps[] naming the recommended action's usecase (generate-document-{domain} or a migrate-specific usecase, see §6)"
      script: persist-proposal
    - order: 5
      kind: deterministic
      description: "link proposal to domain/usecase/step scope (dev_proposal_phase_scope, proposal 6 §6)"
      script: link-proposal-phase-scope
    - order: 6
      kind: deterministic
      description: "render to {target-repo}/.samgraha/proposal/tierN/assess/{domain}/{domain}-assess-proposal.md — human reads this, discusses, approves/rejects per proposal 5 §3's hard-fail-if-map-missing philosophy"
      script: render-proposal
```

Prompt skeleton (`tierN-assess-proposal.md`) — role-based, chain-of-thought
structure, not a single-shot classification call:

```
You are reviewing tier {{tier_number}} ({{tier_domains}}) for {{repo_root}}
against the rust_dev standard.

## What this tier expects
{{#usecases}}
- {{id}} ({{kind}}): {{description}}
{{/usecases}}

## What the repo actually has
{{#domain_scan}}
- {{domain_key}}: doc_exists={{doc_exists}}, structural_conformance_signal={{conforms}}
  {{#gap_notes}}notes: {{gap_notes}}{{/gap_notes}}
{{/domain_scan}}

## Reasoning
Think through each domain: does documentation exist? If yes, does its
structure suggest it already fits the tierN template (section headings,
required content), or would restructuring lose more than it preserves? If
no documentation exists, is there code/context elsewhere in the repo this
tier's generation should draw on (Tier 1 domains: no — technology-independent
by design, matching 00-domain-relationships.md's framing; later tiers: yes)?

## Recommendation
For each domain, state: create | migrate | skip-to-audit, and why.
```

## 5. Old `plan/usecase/*/tier_N/*.md` files — reference material, not dead

The existing 4-case prose files (§1) don't get deleted — they're exactly
the kind of domain-specific guidance (*"Vision and Philosophy are
technology-independent by design"*, the migration-process steps in
`case_2_has_documentation/01-generation.md`) a CoT prompt benefits from
having as grounded reference text, not reasoning from nothing. Recommend:
keep them, feed the relevant tier's file(s) into step 3's prompt context
as domain-authored guidance the model reads before deciding, rather than
mechanically executed procedure an external classifier picks between.
Concretely: `case_1`'s "generate" procedure and `case_2`'s "migrate"
procedure both stay — they just get selected *by the model, per domain, at
propose time*, instead of pre-selected *for the whole tier, by whatever
currently decides the case label* (§1 — never identified in this pass;
likely doesn't exist yet in `rust_dev`, since no `classify-repo` usecase
was found).

## 6. New usecases needed downstream of the recommendation

`propose-tierN-assess`'s output names, per domain, which action-usecase to
run — `generate-document-{domain}` (proposal 3 §3) already exists for
"create." "Migrate" needs its own usecase (not in proposal 3, which only
defined `generate-document-{domain}`, `deterministic-audit-{domain}`,
`semantic-audit-{domain}`, `fix-{domain}`):

```yaml
- name: migrate-document-{domain}
  description: "restructure existing non-conforming {domain} documentation into the domain/{domain}.md template shape, preserving original content"
  data: {tier: N, domain: "{domain}"}
  steps:
    - order: 1
      kind: deterministic
      description: "read existing doc at its discovered path"
      script: gather-existing-doc
    - order: 2
      kind: semantic
      description: "map existing content to template sections, restructure, flag anything that doesn't fit any section"
      prompt: migrate-{domain}
    - order: 3
      kind: deterministic
      description: "persist restructured content, same landing spot as generate-document-{domain}'s output"
      script: persist-fix
```

"Skip-to-audit" needs no new usecase — it's just proceeding straight to
`deterministic-audit-{domain}` (proposal 3) with no preceding
create/migrate step, which the fix loop already handles: an existing
conforming doc that scores below threshold is indistinguishable, from the
audit/fix loop's point of view, from a freshly generated one that scores
below threshold — same `fix-{domain}` usecase, same iteration cap.

## 7. New-repo vs. existing-repo divergence — decided

**Decided (owner direction): one prompt, branches on repo-state at
runtime — not two separate prompts.** `tierN-assess-proposal.md`
(§4's skeleton) already fits this without changes: its `{{#domain_scan}}`
loop feeds per-domain `doc_exists`/`conforms` data straight from step 1's
scan, and its `## Reasoning` section already asks the model to branch on
exactly this ("If no documentation exists, is there code/context
elsewhere..."). For a new repo, `doc_exists=false` for every domain falls
out of the same scan step 1 already runs (§4's own §3 note: *"its repo
scan trivially finds nothing for every domain"*) — no separate script
path, no separate prompt file, the same CoT structure just resolves
differently because its input differs. One `propose-tierN-assess` usecase,
one prompt, for both `repo_new` and `repo_existing` — matching §3's
"no special-cased new-repos-skip-proposing shortcut" stance exactly.

## 8. Open questions

1. **Decided: cheap deterministic proxy, not a full audit.**
   `scan-tier-repo-state`'s "structural conformance signal" stays a
   required-heading-presence / word-count check (against `calculation`'s
   existing word-budget machinery, proposal 3) — running a full semantic
   audit at propose time would make the propose step as expensive as the
   thing it's deciding whether to run. Full semantic judgment stays in the
   real `semantic-audit-{domain}` usecase, not duplicated here. (Script
   content itself is still out of scope, §9 — this decides the shape, not
   the implementation.)
2. **Decided: yes, same redraft mechanism as proposal 5.** A rejected
   `propose-tierN-assess` supports the `_redraft_context`/`iteration >= 5`
   escalation pcems uses and proposal 5 already ports — no separate
   redesign for the assess step.
3. **Decided: per-domain files, matching Bodha's real tree.** Even though
   a tier's assess proposal is drafted in one batched semantic call
   (covering every domain in the tier), `render-proposal` still emits one
   file per domain under `assess/{domain}/`, same pattern pcems's own
   `propose-section` usecase uses for its 6 structural domains in one
   call, rendered separately — not one combined tier-level file.

## 9. Explicitly out of scope

`scan-tier-repo-state`'s actual conformance-check implementation (§8.1,
flagged not designed). Actually writing `tierN-assess-proposal.md`'s full
content (§7 decided its shape — one prompt, runtime branch — not its
content). Any change to proposal 3's `generate-document-{domain}`,
`deterministic-audit-{domain}`, `semantic-audit-{domain}`, `fix-{domain}`
usecases — this proposal only adds what precedes them and one new sibling
usecase (`migrate-document-{domain}`, §6).
