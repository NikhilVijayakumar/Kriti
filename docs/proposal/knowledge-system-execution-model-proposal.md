# Knowledge System Execution Model Proposal — Script-First, Explicit Workflow

## Purpose

samgraha has **no pipeline/orchestrator**. Per the author guide: it
"discovers your system's scripts, runs them under a fixed contract, and
stores/relays whatever comes back." Its only sequencing behavior is a
single pairwise gate check at dispatch time — "has phase X's dependency
already run, and is it still fresh" (author guide §8.3). It does not run
a use case end-to-end, does not know what order phases go in beyond that
one gate, and never will — that's a deliberate zero-domain-knowledge
design, not a gap to file against samgraha.

That means **all sequencing, all "what runs after what," lives in this
repo as authored data** — never assumed, never implicit. This proposal
covers two things that follow from that constraint:

1. Every system must explicitly declare its use cases and the full
   phase-by-phase workflow for each — machine-readable, not just prose —
   plus a readable plan document derived from it.
2. A content-generation policy change: script does the mechanical work,
   semantic (LLM) is used only where judgment or free-text authoring is
   unavoidable. Today it's inverted — semantic does almost everything.

Same scope boundary as the taxonomy proposal: **this repo's authored
data only.** No samgraha (`E:\Python\samgraha` / `E:\MCP\Samgraha`) code
changes proposed or required.

---

## 1. Current State

### 1.1 Workflow today: prose, not data

`plan/usecase/{repo_new,repo_existing}/{case_1,case_2}/tier_N/{01-generation,02-audit,03-fix}.md`
exists for every tier of every use case (e.g. `base_dev` has 2 cases × 8
tiers × 3 stages = 48 of these files). They're well-written and correct
— e.g. `tier_1/01-generation.md` correctly says Vision generates before
Philosophy within the tier, and names the exact template to use — but
they are **prose for a human to read**, not something any script or
samgraha call can consume. Nothing enforces that the prose matches
reality; nothing generates the `use_cases`/`phases`/`depends_on`
structure the author guide's `init` capability (§8.4) expects.

**No system has a `scripts/init.py`.** The §8.4 machine-readable plan —
the one artifact samgraha actually reads to gate dependencies via
`store_system_plan` / `script_runs` — doesn't exist anywhere yet, on any
of the 8 systems.

### 1.2 Generation today: fully semantic

`tier_1/01-generation.md` for `base_dev` says, verbatim: *"generate a
complete document from scratch using the document-level generation
template."* That's the pattern across every tier — the LLM is handed a
template (`templates/generation/document/{domain}.md`, then per-section
templates under `templates/generation/section/{domain}/*.md`) and
produces the entire document, headings included, even though the
headings are 100% fixed and already known before generation starts —
they're sitting right there in the template. No script participates.

### 1.3 Scripts today: audit-check-only, not the full capability set

`script/` (`mapping.yaml`, `policy.yaml`, `schema/`, `windows/`, `ubuntu/`)
backs individual deterministic **audit checks** (category A/B/C, e.g.
`lint-pass`, `secret-scan`, `build-succeeds`) — real scripts, real
caching (`policy.yaml`'s fingerprint/ttl/always_rerun), but scoped to
"one check, one rule." None of the 6 capabilities the author guide
defines (`init`, `validate`, `calculate`, `report`, `scaffold`,
`plan_generation`) exist as an actual script on any of the 8 systems.
`calculate`'s formulas are already fully specified as data
(`calculation/*.yaml`, stable IDs, documented in
`calculation/README.md`) — the hard part (the formula) is done; there's
just no `calculate.py` that reads it.

### 1.4 Report generation today: also semantic

`templates/audit/deterministic/{document,section}/*-report.md` are
report templates — but nothing renders them mechanically. Report
narrative is produced the same way document generation is: handed to the
LLM as a template to fill in, even though by the time report runs, the
score, band, findings, and trend are already fully computed structured
data (`calculation/summary/*.yaml`'s job) — rendering that into the
existing template is arithmetic + string substitution, not authorship.

---

## 2. Problem

Two compounding issues:

- **No enforced order.** Because sequencing is prose, drift between
  "what the `.md` says should happen" and "what actually gets called" is
  invisible until something breaks — the exact failure mode
  `docs/limitation/mcp/01-system-class-inheritance.md` (LIM-001) already
  documented for a different reason (`eswa_journal`/`pcems_2026` silently
  inheriting the wrong `loop.yaml`).
- **LLM calls for mechanical work.** Reproducing a template's own
  headings, or rendering a report from already-computed numbers, doesn't
  need judgment — it needs a script. Every such call today costs latency,
  tokens, and a (small but nonzero) chance the LLM silently drifts from
  the template's actual structure. None of that risk buys anything, since
  the structure was never in question.

---

## 3. Proposed Changes

### 3.1 Explicit machine-readable workflow (`scripts/init.py`, §8.4)

Every system gets a real `init.py` returning the full
`use_cases[].phases[]` structure (`id`, `kind`, `script`/description,
`depends_on`, `expiry`) — the author guide's §8.4 shape, already
specified, just not authored yet. This becomes **the single source of
truth for phase order.** Concretely, for `base_dev`-class systems this is
a mechanical transform of data that already exists (`plan/core/tiers.yaml`
+ `plan/core/loop.yaml`'s `within_tier_ordering`) — the author guide
already walks through this exact transform in §11A.2, using `base_dev`
itself as the worked example. This proposal extends that transform to
actually happen, and to every class (`hackathon`, `academic` too, once
they have use cases worth declaring — today `python_hackathon` has no
generate stage at all, so its `init.py` is audit-only phases).

### 3.2 Every script execution tracked

Nothing new to build here — `script_runs` + `expiry` is already
samgraha's designed mechanism (author guide §8.3/§8.4 FAQ). The
requirement this proposal adds is **discipline, not new infrastructure**:
every phase of `kind: script` must be invoked through samgraha's
dispatch (`run_system_script` / `run_system_scaffold` /
`run_system_validate` / etc.), never shelled out directly — bypassing
dispatch means `script_runs` never records the run, which silently
breaks every downstream `depends_on` gate that expects it.

### 3.3 A plan/order document — generated, not hand-authored twice

The user-facing ask: a document that says, for a given use case, which
script runs in what order. The `tier_N/*.md` files already try to be
this and already drift-risk against a second source of truth once
`init.py` exists. Proposal: don't hand-maintain both. Once `init.py`
exists, add one small script (`scripts/render_workflow.py`, or a
`report`-family script) that renders `init.py`'s own
`use_cases[].phases[]` into a readable Markdown table —
phase id → kind → script path (if any) → depends_on. That rendered file
*is* the plan/order document, mechanically kept in sync with the actual
executable plan because it's generated from the same data, not written
alongside it by hand. The existing `tier_N/01-generation.md`-style prose
becomes source material to transcribe into `init.py` once, then gets
replaced by the generated version (see §5 — not deleted until the
generated version is verified equivalent).

### 3.4 Script-first content generation — the core policy change

Split what's currently one semantic "generate the whole document" phase
into three phases, two of them script:

| Step | Kind | What it does | Why |
|---|---|---|---|
| **scaffold** | `script` | Reads `templates/generation/document/{domain}.md` + `templates/generation/section/{domain}/*.md`, creates the file with every heading/subheading already in place, section bodies left as stub markers | Structure is 100% known ahead of time — it's already sitting in the template. No judgment involved. |
| **section content** | `semantic` | LLM fills in the prose under each heading the scaffold already created, using that section's template as prompt context | The one genuinely unavoidable use of semantic — free-text authorship *is* the judgment call. |
| **report** | `script` | Reads `calculation/summary/*.yaml` output (score, band, findings, trend — already fully computed by the time this runs) + `templates/audit/**/*-report.md`, renders mechanically | By report time there's no content decision left to make — it's substitution into an already-fixed template. |

`validate`/`calculate` were already conceptually script-only in the
author guide's design (§5.2) and `calculation/*.yaml`'s formulas are
already fully specified as data — this proposal doesn't change their
shape, it just means they finally get implemented as real
`validate.py`/`calculate.py` per system instead of remaining
un-authored.

Code generation, file scaffolding, any file/directory creation — script
only, no exceptions. Matches the `scaffold` capability's existing
contract (author guide §5.2, idempotency via `skipped`).

**Semantic stays, narrowly, for:**
- section content authoring (§3.4 table, row 2)
- semantic audit judgment (`audit/semantic/{document,section}/*.md` —
  already exists, inherently qualitative — "does this architecture
  decision make sense" isn't a rule a script can evaluate)
- anything else that's genuinely a judgment call, not structure

### 3.5 Script language priority: Python first

The author guide (§5.3) allows `.py`/`.sh`/`.ps1`/`.js` and says "mix
languages freely." This proposal narrows that for new work: **write new
capability scripts and check scripts in Python first.** Reach for
`.ps1`/`.sh`/`.js` only when Python genuinely can't do the job (a
Windows-only API with no Python binding, a check that must run inside an
existing Node toolchain, etc.) — not by default, not by whichever
platform the author happened to be on.

Two concrete effects on today's repo:

- `script/{windows,ubuntu}/**` (the per-check audit scripts under
  `base_dev` and every system that inherits its `script/` layout)
  duplicate every check as **two** files today — a `.ps1` under
  `windows/` and a `.sh` under `ubuntu/`, same check, same logic,
  authored and maintained twice. A single Python script under each
  check's path replaces both platform-specific copies with one
  cross-platform file — one script to review, one to keep in sync with
  the rule it backs, not two.
- `python_hackathon/script/*.py` is already 100% Python — it's the
  existing proof this works, not a hypothetical. New capability scripts
  on every other system should match that bar, not the `.ps1`-first
  pattern the `dev` class happens to have today.

Existing `.ps1`/`.sh` checks aren't required to be rewritten as a
blocking prerequisite for §3.1–§3.4 — they keep working via the
5-tier script discovery (author guide §5.5) — but any *new* script
written under this proposal's scope (`init.py`, `scaffold.py`,
`validate.py`, `calculate.py`, `report.py`, and any new audit check)
is Python, and existing `.ps1` checks are candidates to port opportunistically
when touched for another reason, not left as the template for new ones.

---

## 4. Net Effect

- samgraha's lack of a pipeline stops being a liability once ordering is
  explicit, versioned data (`init.py`) instead of prose someone has to
  keep in sync by hand.
- Every phase becomes traceable and re-runnable through the same
  `script_runs`/`expiry` mechanism already designed for it — nothing
  generation-specific needed there.
- LLM calls drop to only the step that actually requires one — cuts
  cost/latency/drift-risk on the ~majority of a generation pass that's
  currently "reproduce a heading you were handed verbatim."

---

## 5. What This Requires Per System (follow-up scope, not built here)

- `scripts/init.py` — missing on all 8 systems today
- `scripts/scaffold.py` — missing on all 8; reads
  `templates/generation/{document,section}/**`, emits skeletons
- `scripts/validate.py`, `scripts/calculate.py` — missing on all 8 as
  aggregate capabilities (today only the per-check `script/` layer
  exists, which `validate.py` would call into, not replace)
- `scripts/report.py` — missing on all 8; reads
  `calculation/summary/*.yaml` + `templates/audit/**/*-report.md`
- `scripts/render_workflow.py` (or equivalent) — new, renders `init.py`
  into the human-readable plan document from §3.3
- For `dev`-class systems, this is one build against `base_dev`
  (inherited by `electron_dev`/`fastapi_dev`/`react_dev`/`rust_dev` per
  the existing `extends` mechanism) rather than 5 separate builds —
  same leverage the taxonomy proposal's base/concrete split already
  gives.

---

## 6. Explicitly Out of Scope Here

- Actual implementation of any `init.py`/`scaffold.py`/`validate.py`/
  `calculate.py`/`report.py` — separate follow-up per system/class, same
  pattern as the taxonomy proposal's §6
- Any samgraha-side code change — `script_runs`, `expiry`, and dispatch
  gating are already designed and (per the author guide) implemented;
  this proposal only obligates authored scripts/data in this repo
- Deleting the existing `tier_N/{01-generation,02-audit,03-fix}.md`
  prose files — keep them as source material until each system's
  generated workflow document (§3.3) is verified equivalent, then
  replace, not delete-and-hope
- Whether `templates/generation/section/*.md` need reshaping for the new
  scaffold/content split (right now they're written as full-document LLM
  prompts, not stub+prompt pairs) — likely needs adjustment, but that's
  template-authoring work for the per-system follow-up, not a decision
  to make in this proposal
