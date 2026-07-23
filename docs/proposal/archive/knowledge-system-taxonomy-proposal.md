# Knowledge System Taxonomy Proposal

## Purpose

`samgraha/system/` currently holds 8 systems as a flat list:
`base_dev`, `electron_dev`, `fastapi_dev`, `react_dev`, `rust_dev`,
`python_hackathon`, `eswa_journal`, `pcems_2026`.

This proposal defines a class/subclass taxonomy to organize these systems
(and future ones) into a directory structure that reflects how they
actually relate — instead of one flat, undifferentiated list. It is
**directory + metadata only**. It does not touch any individual system's
domains, audit rules, templates, or scoring — those get their own
follow-up proposals per system, referenced in §6.

This builds directly on the already-agreed design in
`docs/limitation/mcp/01-system-class-inheritance.md` (LIM-001): class →
optional subclass → base system → concrete system, with `extends`/`drops`
resolved by name (already implemented — see
`docs/knowledge-system-author-guide.md` §3–4 in the samgraha repo). That
groundwork (`base_dev` + 4 concrete systems declaring `extends: base_dev`)
is already in place. What's missing is the **class/subclass layer** on
top of it, and the directory reorganization to match.

---

## 1. Current State

| System | De facto class (per LIM-001) | Has `system.yaml`? | Domains |
|---|---|---|---|
| `base_dev` | dev (abstract base) | yes | 16 |
| `react_dev` | dev | yes, `extends: base_dev` | 16 |
| `fastapi_dev` | dev | yes, `extends: base_dev`, drops 2 | 14 |
| `electron_dev` | dev | yes, `extends: base_dev` | 16 |
| `rust_dev` | dev | yes, `extends: base_dev`, drops 3 | 13 |
| `python_hackathon` | hackathon | no | 10 (own tree, no inheritance) |
| `pcems_2026` | academic | no | 6 (own tree, no inheritance) |
| `eswa_journal` | academic | no | 11 (own tree, no inheritance) |

The dev class already has real inheritance wired up. Hackathon and
academic each have zero or one member per class and no `system.yaml` at
all — nothing to inherit from yet, so nothing broke by their absence, but
also nothing declares what class they belong to.

---

## 2. Proposed Taxonomy

Three classes, matching what already exists in practice — this is not
inventing new categories, it's naming ones already visible in
`docs/limitation/mcp/01-system-class-inheritance.md`'s evidence table:

```
dev          — generate → audit → fix loop, drives implementation/build/test
hackathon    — audit-only, competitive scoring, leaderboard
academic     — generate paper sections from project evidence, semantic-only audit
```

### 2.1 `dev` — subclassed

| Subclass | Concrete system(s) today | Why this bucket |
|---|---|---|
| `frontend` | `react_dev`, `electron_dev` | UI/component-driven; Electron's renderer is React/web-tech, main process rides along under the same bucket |
| `backend` | `fastapi_dev` | Server-side only, already drops `06-design` + `09-feature-design` |
| `fullstack` | — (none yet) | Reserved for a future system that's genuinely split backend+frontend as separate concerns, not just Electron's main/renderer split |
| `build` | `rust_dev` | Systems/tooling, no UI concerns, already drops `06-design` + `09-feature-design` + `11-prototype` |

`base_dev` stays a single shared base for the whole `dev` class, not
duplicated per subclass — all 4 concrete systems still declare `extends:
base_dev` directly, unchanged. Subclass here is **organizational
grouping only** (which directory a system lives in), not a second
inheritance layer. See §4 for when that would change.

### 2.2 `hackathon` — no subclass

Matches your instruction directly: one flat bucket, no further split.
`python_hackathon` is the only member and stays exactly as-is internally
(it's audit-only with no `generate` stage — a structurally different
shape from `dev`, not just a smaller domain set).

### 2.3 `academic` — subclassed, with a shared `base_academic`

| Subclass | Concrete system(s) today | Why this bucket |
|---|---|---|
| `paper` | `pcems_2026` | Single conference paper, 6 domains, 4 tiers |
| `journal` | `eswa_journal` | Q1 journal submission, 11 domains, 4 tiers, denser relationship graph |

Their full domain sets diverge (`pcems_2026`: title-and-metadata,
introduction, methodology, findings, conclusion, references;
`eswa_journal`: abstract, introduction, related-work,
problem-definition, methodology, experimental-setup, results,
implications, limitations, conclusion, references) — but 4 domains are
common to both by name: **introduction, methodology, conclusion,
references**. On top of that, both are already the same class *shape*
per LIM-001's evidence table: semantic-only audit (no deterministic
layer, no section scope), generate → audit → fix loop, no
competition/leaderboard. That's a real shared base, analogous to
`base_dev`: `base_academic` holds the 4 common domain-standards files
plus the shared `plan/core/loop.yaml` shape, `calculation/` shape
(semantic + summary buckets only, no `deterministic/` bucket), and
`audit/semantic/` conventions. `pcems_2026` and `eswa_journal` each
`extend: base_academic` and *add* their own domain-specific files on top
(`pcems_2026` adds title-and-metadata + findings; `eswa_journal` adds
abstract + related-work + problem-definition + experimental-setup +
results + implications + limitations) — the existing overlay merge
(§4 of the author guide) already supports adding files the base doesn't
have, not just overriding/dropping ones it does, so this needs no new
merge capability.

**What stays per-system, not in `base_academic`:** per the (archived)
Knowledge System Evolution Proposal's Principle 4, `00-domain-relationships.md`
and `plan/core/tiers.yaml` are always system-specific — tier ordering
and cross-domain edges differ per system even when domain names overlap
(e.g. `eswa_journal`'s `methodology → experimental-setup` edge has no
counterpart in `pcems_2026`, which has no experimental-setup domain at
all). `base_academic` provides shared domain *content* and shared
*process shape*, never the relationship graph — each concrete system
keeps authoring its own, same as today.

---

## 3. Proposed Directory Layout

```
samgraha/system/
├── dev/
│   ├── base_dev/                  # abstract, shared base for all 4 dev subclasses
│   ├── frontend/
│   │   ├── react_dev/
│   │   └── electron_dev/
│   ├── backend/
│   │   └── fastapi_dev/
│   └── build/
│       └── rust_dev/
├── hackathon/
│   └── python_hackathon/
└── academic/
    ├── base_academic/              # abstract, shared base for paper + journal
    ├── paper/
    │   └── pcems_2026/
    └── journal/
        └── eswa_journal/
```

Every concrete system's internal contents (`scripts/`, `templates/`,
`documentation-standards/`, `audit/`, `calculation/`, `plan/`) move
unchanged — this is a `git mv` of the top-level directory, not a rewrite
of anything inside it.

---

## 4. Metadata: `class` / `subclass` Fields

Add two optional fields to `system.yaml`, per LIM-001's already-agreed
schema — data-driven, no new samgraha loader logic required beyond
reading these two keys:

```yaml
# samgraha/system/dev/frontend/react_dev/system.yaml
name: react_dev
class: dev
subclass: frontend
extends: base_dev
description: >
  React frontend development system. Inherits all 16 domains from
  base_dev. Adds React-specific templates and component patterns.
```

```yaml
# samgraha/system/dev/frontend/electron_dev/system.yaml
name: electron_dev
class: dev
subclass: frontend
extends: base_dev
description: >
  Electron desktop application system. Inherits all 16 domains from
  base_dev. Adds Electron-specific templates on top.
```

```yaml
# samgraha/system/hackathon/python_hackathon/system.yaml  (new file)
name: python_hackathon
class: hackathon
description: "Audit-only competitive scoring for hackathon submissions."
```

```yaml
# samgraha/system/academic/base_academic/system.yaml  (new file)
name: base_academic
abstract: true
description: >
  Base academic system. Provides the 4 domains common to every academic
  concrete system (introduction, methodology, conclusion, references)
  plus the shared semantic-only audit / generate-audit-fix loop shape.
  Not registered directly — use a concrete system (pcems_2026,
  eswa_journal, ...).
domains:
  - introduction
  - methodology
  - conclusion
  - references
```

```yaml
# samgraha/system/academic/paper/pcems_2026/system.yaml  (new file)
name: pcems_2026
class: academic
subclass: paper
extends: base_academic
description: >
  PCEMS 2026 conference paper generation and audit. Inherits
  introduction/methodology/conclusion/references from base_academic,
  adds title-and-metadata + findings.
```

```yaml
# samgraha/system/academic/journal/eswa_journal/system.yaml  (new file)
name: eswa_journal
class: academic
subclass: journal
extends: base_academic
description: >
  ESWA (Q1 journal) paper generation and audit. Inherits
  introduction/methodology/conclusion/references from base_academic,
  adds abstract + related-work + problem-definition +
  experimental-setup + results + implications + limitations.
```

`hackathon` and `academic` currently have **no `system.yaml` at all** —
creating these 4 new files (`python_hackathon`, `base_academic`,
`pcems_2026`, `eswa_journal`) is new work this proposal introduces, not
something already sitting half-done like the `dev` class's.

### 4.1 In scope: `base_academic` — out of scope: subclass-level bases

`base_academic` (§2.3) is a **class-level** base — shared across the
`paper`/`journal` subclasses, the direct analog of `base_dev` being
shared across `dev`'s subclasses. That's now proposed and in scope
(this section).

**Still deferred, by design (YAGNI):** a *subclass*-level base — e.g.
`academic/journal/base_journal/` for when a second journal system joins
`eswa_journal`, or `dev/frontend/base_frontend/` for a second frontend
framework joining `react_dev`/`electron_dev`. Every subclass today has
either one member or, for `frontend`, two members that already both
extend `base_dev` directly with no `frontend`-specific shared delta
identified yet. A subclass-level base only earns its keep once a
*second* sibling in the same subclass starts duplicating subclass-specific
files by hand — the exact failure mode LIM-001 documented for `dev`
before `base_dev` existed. When that happens: extract the shared delta,
point siblings at it via `extends`, same mechanism already proven twice
over (`base_dev`, and now `base_academic`). Not needed yet, so not built
yet.

---

## 5. Migration Mechanics & Risks

| Step | Risk / thing to verify first |
|---|---|
| `git mv` each system dir into its new nested path | Low — preserves history, no content change |
| Confirm samgraha's system discovery handles a nested path (`system/dev/frontend/react_dev`) vs. the flat `system/{name}` it was built against | **Unverified.** `register_standard` takes an explicit path per the author guide (§9.1), so it likely doesn't care about nesting depth — but confirm against samgraha's loader before moving anything, not after. |
| Confirm `extends: base_dev` still resolves after `base_dev` moves to `dev/base_dev/`, and `extends: base_academic` resolves once `academic/base_academic/` is newly created | Should be name-based per LIM-001's design, not path-based — `base_dev`'s case is a real existing relationship worth a registration test post-move; `base_academic`'s is a brand-new relationship, worth testing fresh rather than assuming it behaves like `base_dev`'s. |
| Add `class`/`subclass` fields | Additive, no schema break — systems without these fields today (none, after §4's new files) would just have `class: null` |
| Per-repo `samgraha.toml` `system = "react_dev"` references | Unaffected — that's a name lookup, not a path, per the author guide's example (§3.1 area) |

Recommendation: do the discovery-path verification (row 2) against a
throwaway copy or a single low-risk system (`python_hackathon`, no
existing inheritance to break) before moving the `dev` class, since
`dev` is the one place inheritance is actually live today.

---

## 6. Explicitly Out of Scope Here

This proposal does **not** cover, each of which becomes its own
follow-up:

- Any change to what domains/tiers/audit rules `pcems_2026` or
  `eswa_journal` currently have beyond the mechanical split into
  `base_academic` + each system's additions (§2.3) — no new domain, no
  changed rule
- Creating subclass-level bases (`base_frontend`, `base_journal`, ...)
  — §4.1, still deferred, not scoped
- Creating a `hackathon` base system — still N/A, single member, no
  peer to share with
- Updating `docs/knowledge-system-author-guide.md` (lives in the
  samgraha repo, not this one) to document the `class`/`subclass` fields
  once this lands
- Per-system refactor proposals (`react_dev-proposal.md` etc., already
  archived at `docs/proposal/archive/`) — those get rewritten
  individually against this taxonomy once it's confirmed, per your
  instruction to do the whole-picture proposal first

---

## 7. Summary of What Changes

- 8 systems move from a flat list into `dev/{frontend,backend,build}/`,
  `hackathon/`, `academic/{paper,journal}/` (`dev/fullstack/` reserved,
  no member yet)
- 1 new base system (`base_academic`) extracted from the 4 domains
  (`introduction`, `methodology`, `conclusion`, `references`) and shared
  process shape common to `pcems_2026` + `eswa_journal`
- 4 new minimal `system.yaml` files (`python_hackathon`, `base_academic`,
  `pcems_2026`, `eswa_journal`) — currently missing entirely
- 2 new fields (`class`, `subclass`) added to all 9 `system.yaml` files
  (8 existing systems + `base_academic`)
- `pcems_2026`/`eswa_journal` gain `extends: base_academic` — their own
  domain content (beyond the 4 shared domains) and their own
  `00-domain-relationships.md`/`tiers.yaml` are unchanged, just now
  layered on a base instead of standing fully alone
- Zero new samgraha loader logic — same `extends`/`drops` mechanism
  already implemented, same explicit-path `register_standard` call,
  just at new paths (and one new base, resolved the same way `base_dev`
  already is)
