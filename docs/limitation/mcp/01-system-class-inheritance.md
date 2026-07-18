# Limitation — samgraha MCP has no system-class / inheritance model

Scope: the samgraha MCP tool itself (`register_standard`, `sync_standards`, the
knowledge-hub loader schema), not any single knowledge system in this repo.
Logged here per user request instead of attempting a workaround in-repo —
fixing this properly means loader/schema changes in samgraha
(`E:\MCP\Samgraha`), outside this repo's remit.

---

## LIM-001 — No base-system-class with inheritance; every system is a fully standalone tree
- **Severity:** HIGH — confirmed active maintenance-multiplier risk, not hypothetical (see Proposed design)
- **Status:** 🔶 OPEN — logged, not implemented

### What's missing
`samgraha/system/{name}/` has no way to declare "this system extends/inherits
from that system." Every system — `documentation-standards/`, `audit/`,
`calculation/`, `plan/`, `templates/`, `script/` — is authored as a fully
independent tree. There is no `system.toml` (or equivalent) field like
`extends: base_dev` or `class: dev`, and `register_standard` has no override-
by-exception resolution: it always loads one system's tree in full, never a
base tree plus a delta.

### Observed evidence
This repo currently has three de facto system **classes**, distinguished by
`plan/core/loop.yaml` shape and calculation/audit depth — but the classing is
informal, enforced by nothing:

| Class | Systems | Shape |
|---|---|---|
| **dev** | `base_dev`, `electron_dev`, `fastapi_dev`, `react_dev`, `rust_dev` | Full scope: `documentation-standards` → `audit` (deterministic + semantic, document + section) → generate/audit/fix loop → drives implementation/build/test. `plan/core/loop.yaml` is **byte-for-byte identical** across all 5. |
| **hackathon** | `python_hackathon` | Audit-only, no generation. Ingests a target repo, scores it, ranks it against others (`calculate: type: relative, scope: competition`), produces a leaderboard. |
| **academic-paper** | `eswa_journal`, `pcems_2026` | Generates paper sections from existing project documentation/evidence, semantic-only audit (no deterministic layer, no section scope), fix loop. No competition, no leaderboard. |

Two concrete symptoms of the missing mechanism, both hit and fixed this
session:

1. **Silent class mismatch.** `eswa_journal` and `pcems_2026` originally
   shipped with `python_hackathon`'s `loop.yaml` copy-pasted verbatim —
   `repository` ingestion, competitive `relative`/`competition` scoring, a
   hackathon-specific `cap: 20` normalization — none of which apply to a
   single-paper generate-and-audit workflow, and with no `generate` stage at
   all (the one thing an academic-paper class actually needs). A base-class
   check (or even just a `class:` field the loader could validate the
   `stages:`/`path_selection:` shape against) would have caught this at
   registration time instead of it sitting unnoticed until a manual review.
2. **Unenforced convergence in the dev class.** `base_dev` is de facto
   already the base for `electron_dev`/`fastapi_dev`/`react_dev`/`rust_dev` —
   their `loop.yaml` files are identical, and their `calculation/` /
   `templates/` shapes closely mirror `base_dev`'s. Nothing expresses or
   verifies that relationship; a fix to `base_dev/plan/core/loop.yaml` today
   requires manually copy-pasting into 4 other files, with no signal if one
   is missed and drifts.

### Proposed design (user-specified, agreed)

**Taxonomy — class → optional subclass → base system → concrete system.**
- **Class** is the top level: `dev`, `hackathon`, `academic`. (Matches the 3
  classes already observed informally in this repo.)
- **Subclass** is optional, per class, not mandatory. `dev` might have
  `frontend` / `backend` / `fullstack`; `academic` might have `paper` /
  `journal`. A class with no meaningful subclass split just skips this level
  (`hackathon` today has none).
- Each subclass — or the class itself, if no subclass — has its own **base
  system**: a `documentation-standards`/`audit`/`calculation`/`plan`/
  `templates`/`script` tree that is the shared starting point for every
  concrete system under it. `base_dev` is this repo's existing (accidental,
  copy-pasted-by-hand) example for the `dev` class.
- A **concrete system** (`rust_dev`, `react_dev`, `electron_dev`,
  `fastapi_dev`, ...) declares which base it inherits from and supplies only
  its *delta*: files it overrides (e.g. Rust-specific
  `documentation-standards`, Rust-specific audit rules) plus whatever it adds
  that the base doesn't have. Anything it doesn't override is resolved from
  the base at compile/register time.

**Compile-time behavior is unchanged.** The base system is never compiled on
its own and never shipped as an independent compiled standard. When a
concrete system is compiled/registered, the loader first assembles an
in-memory tree — base content, then the concrete system's override content
layered on top, override wins on any path conflict — and *then* runs exactly
the same compile pass that runs today against a single standalone tree. The
output (`standards.db` rows, `calculation_rules`, `score_bands`, etc.) is
identical in shape to what a fully-standalone system produces now; only the
*source assembly step* changes, not the compiled result or the passes that
produce it.

**The motivating problem, concretely:** today, `electron_dev`, `fastapi_dev`,
`react_dev`, and `rust_dev` each got their `plan/core/loop.yaml` (and much of
their `calculation/`/`templates/` shape) by copying `base_dev`'s files by
hand. If `base_dev` changes — a new tier, a fixed formula, a corrected
threshold — every one of those 4 copies has to be found and re-patched
manually, with no tooling signal if one is missed. This is the exact failure
mode LIM-001's evidence section already caught once (`eswa_journal`/
`pcems_2026` silently inheriting the wrong class's `loop.yaml` via
copy-paste). Base+override inheritance fixes it at the source: change
`base_dev` once, every system that extends it picks it up automatically
unless it explicitly overrides that file.

### Proposed implementation mechanism (user-specified): data-driven, not samgraha-code-driven

The user's explicit constraint: inheritance must be **managed in data**, not
by adding class/subclass/inheritance-aware logic into samgraha's own Python
loader source. Concretely:

- `documentation-standards/`, `audit/`, `templates/`, `script/` content stays
  exactly what it is today — markdown (and the occasional YAML) authored the
  same way it's authored now. No format change to existing content.
- A new **YAML metadata file** sits alongside each system's `samgraha.toml`
  (or, for the base itself, alongside its own manifest), declaring
  `class`, `subclass` (optional), and `extends` (which base system this
  concrete system inherits from) plus, optionally, an explicit list of which
  paths it overrides. This is the *only* new artifact — everything else about
  a system's tree is unchanged.
- Resolution (base tree + this system's overlay, override-wins-on-conflict)
  is a generic, class-agnostic merge driven entirely by what the metadata
  file says — the merge code has no `if class == "dev"` branches; it just
  reads `extends:` and layers directories. That's what makes it "data, not
  code": today adding a 4th class would mean new logic in samgraha; under
  this design it means a new base directory and systems pointing `extends:`
  at it, nothing in samgraha's source changes.
- This can be implemented as a preprocessing step ahead of the *existing*
  `register_standard` (assemble the merged tree on disk or in-memory, then
  hand it to the loader exactly as today), which is the version that touches
  the least samgraha code — the 10-pass loader itself stays byte-for-byte
  what it is now, and the compile-time behavior guarantee from the section
  above (identical output shape) falls out for free.

**Format choice — metadata file: YAML (decided).**
Original proposal was markdown for content (unchanged, agreed) + a JSON
metadata file. Revised and **agreed with the user: YAML for the metadata
file**, for two reasons grounded in this repo as it exists today, not a
general format preference:
1. **Comments.** Every existing engine-read data file in `samgraha/system/`
   (`loop.yaml`, `tiers.yaml`, `weights.yaml`, `score_bands.yaml`, every file
   under `calculation/`) is YAML specifically because inline `#` comments and
   `note:` fields carry *why* a value is what it is — a convention this
   session leaned on constantly (e.g. `21-plan_settings.sql`'s own comment
   explaining its composite FK, or `18-calculation_rules.sql`'s comment
   recording the exact python_hackathon bug that shaped its schema). A
   metadata file recording *why* `rust_dev` overrides one specific audit file
   and not another is exactly the kind of thing worth a comment next to it.
   JSON has no comment syntax — that rationale would have to live in a
   separate file, disconnected from the data it explains.
2. **Zero new parsing surface.** `knowledge-hub-loader.py` already calls
   `yaml.safe_load()` throughout (passes 1, 7, 8, 10, ...) and never imports
   `json`. A YAML metadata file reuses the exact same parser, same error
   handling, same trust boundary already in place. A JSON metadata file adds
   a second parsing code path for one new file, in a loader that currently
   has none.

Markdown remains the format for all existing system content (documentation-
standards, audit, templates) — unchanged from the original proposal. Only
the new metadata file moved from JSON to YAML.

**Closed format inventory.** The full proposal now uses exactly three
formats, each already established in this repo for exactly this role, and
nothing else (no JSON, no new format introduced for this feature):
- **Markdown** — all system content (`documentation-standards/`, `audit/`,
  `templates/`), unchanged.
- **YAML** — the new per-system metadata file (`class`/`subclass`/`extends`/
  overrides), same role YAML already plays everywhere else the loader reads
  structured config (`loop.yaml`, `tiers.yaml`, `calculation/*.yaml`).
- **TOML** — `samgraha.toml`, the existing repo-level manifest, unchanged.

Thin glue code to *execute* the merge (read the metadata file, layer base
tree + overlay, hand the result to the existing loader) is fine — the
constraint is that the merge is generic and reads its behavior from these
data files, not that zero code may exist. What's ruled out is class-aware
*logic*: branching in samgraha's source on which class/subclass a system
belongs to. The class taxonomy, what extends what, and what's overridden all
live in the YAML/TOML data; the code stays a dumb, class-agnostic resolver.

### Known gap even under the proposed design: bases can't be abstract-only

The user's stated end goal is that `base_dev` (and any other class/subclass
base) should **not** exist as a system an end user can pick directly — only
concrete, tech-specific systems (`rust_dev`, `react_dev`, ...) are meant to be
selectable. The base should be purely an internal inheritance root.

This is **not possible** under the current architecture, inheritance-aware or
not: `register_standard`/the knowledge-hub loader has no notion of an
"abstract" system that's valid only as an inheritance source and invalid to
register/compile standalone. Every directory under `samgraha/system/` must be
independently complete enough to pass all 10 loader passes on its own (this
is exactly what let `base_dev` register and work as a normal, if generic,
system this session). Making bases genuinely non-standalone would need a
second, smaller change on top of inheritance itself: an `abstract: true` flag
(or equivalent) that `register_standard` refuses to compile/register directly,
only ever as a resolved-into base for something that extends it.

### Current workaround
None at the tooling level. Each system's files are authored/reviewed by hand;
cross-system consistency (or intentional divergence) is a manual audit, not
something `register_standard` or `sync_standards` can check. `base_dev`
remains a fully standalone, directly-registrable system in the interim.

---

## LIM-002 — Multi-repo write/sync to the shared standards store: unverified
- **Severity:** UNKNOWN — not yet reproduced, logged as a requirement to
  verify and fix if confirmed
- **Status:** 🔶 OPEN — logged, not tested

### Requirement
`register_standard` writes into a shared `standards.db` "next to the MCP
binary by default, so every repo's `sync_standards` can pull it" (per the
tool's own description) — i.e. the shared store is explicitly meant to be a
multi-repo write target, not something only this repo (`Kriti`) populates.
This session only exercised writes from `E:\Python\Kriti`. The requirement,
as stated by the user: register/sync from a *second*, independent local repo
must work the same way register/sync from `Kriti` does in this session —
same shared global store, same `sync_standards` pull-down behavior, no
special-casing for "the repo that happened to write first."

### What's suspect, unverified
Nothing here was reproduced — this is logged pre-emptively per the user's
request, not from an observed failure. Plausible failure points worth
checking when this is tested from a second repo:
- `register_standard`'s `system_id`/`standard_id` allocation (`Pass 0` in
  this session's own logs assigned `system_id=1,2,3` sequentially per system
  registered from `Kriti`) — if a second repo's loader run also starts
  numbering from a fresh/empty local state rather than reading the *shared*
  store's existing max id, two repos could allocate colliding ids for
  different systems.
- Any repo-path-relative assumption in how the shared `standards.db`'s
  location or lock is resolved — "next to the MCP binary" should be
  repo-independent by construction, but that's exactly the kind of implicit
  single-writer assumption worth a concurrency/second-writer test rather than
  taking on faith.
- `sync_standards`'s staleness/versioning check (`check_knowledge_staleness`)
  when the shared store has been written to by a *different* repo since this
  repo's last sync — confirm it still detects and pulls correctly, not just
  in the single-writer case already exercised.

### Current workaround
None — untested. Needs an actual second local repository registered against
the same shared store to confirm one way or the other; out of scope for this
session (no second repo available to test against).
