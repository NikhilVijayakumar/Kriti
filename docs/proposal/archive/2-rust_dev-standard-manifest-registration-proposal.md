# rust_dev — Standard Manifest + Samgraha Registration (Proposal 2 of 7)

## 0. Series

Part of a 7-proposal set — see
[`rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0
for the full list and dependency order. This proposal assumes proposal 1's
`tierN/` + `domain/` + `common/` layout already lands.

**Correction notice**: §3-§5 below assume `rust_dev` needs its own
`academic_schema.py`-style DB layer, modeled on `pcems_2026`. It doesn't —
[`6-rust_dev-samgraha-schema-alignment-proposal.md`](6-rust_dev-samgraha-schema-alignment-proposal.md)
found the real samgraha engine already provides generic `usecase`/`step`/
`script`/`prompt`/`domain`/`proposal` tables shared across every standard.
Read this proposal for the `standard.yaml` shape (§3) — still correct —
and the net-new work in §4 (`_adapter.py`-equivalent contract, `.sh`/`.ps1`
→ `.py` porting) — also still correct; but its registration sequence (§5)
and schema framing (§4's schema-layer bullets) are superseded — see
proposal 6 §4-§5.

## 1. What exists today (traced against live registry + files)

Checked the live samgraha registry directly:

```
mcp__samgraha__list_standards  → {"count":1,"standards":[{"name":"pcems_2026", ...}]}
mcp__samgraha__list_repositories → {"count":0,"repositories":[]}
```

**`rust_dev` is not a samgraha standard.** Only `pcems_2026` is registered.
`rust_dev/system.yaml` exists but is a different, older format entirely:

```yaml
name: rust_dev
extends: base_dev
description: >
  Rust systems development system. Drops design, feature-design,
  and prototype domains (systems programming — no UI concerns).
drops: [06-design, 09-feature-design, 11-prototype]
```

This is a class-inheritance manifest (`extends`/`drops`), not a samgraha
`standard.yaml` (`scripts:`/`prompts:`/`usecases:`/`custom_tables:`). Nothing
in `rust_dev` today declares scripts, prompts, or usecases in a form the
MCP tools (`get_standard_usecases`, `get_standard_scripts`,
`get_standard_prompts`, `run_script_step`, `prepare_semantic_step`,
`complete_semantic_step`) can read. rust_dev's scripts
(`script/{schema,ubuntu,windows}/**`) are check *implementations* keyed by
domain/OS, invoked by some other mechanism outside samgraha (the original
`docs/proposal/archive/rust_dev-proposal.md` §9 describes a not-yet-built
`init.py`/`scaffold.py`/`validate.py`/`calculate.py` toolchain — that
toolchain was never wired to samgraha's MCP layer either).

Net effect: **rust_dev today cannot be driven through
`mcp__samgraha__*` at all.** Proposals 3–5 (usecase wiring, usecase-map
generation, propose pipeline) all require a `standard.yaml` to attach to —
this proposal is the load-bearing one the rest of the series depends on.

## 2. What pcems_2026's `standard.yaml` actually is

Read in full (`common/schema-manifest/standard.yaml`, 1242 lines). Four
top-level blocks:

- **`scripts:`** — flat list of `{name, location, purpose}`. `location` is
  relative to the manifest file's own directory (`../../step0-extract/...`),
  confirming pcems's "fully self-contained" design (§1 of proposal 1).
- **`prompts:`** — same shape, `{name, location}`, pointing at `.md` files
  under each step's `prompt/` tree.
- **`custom_tables:`** — `{table_name, purpose, owner_script}`, documents
  every `academic_*` table and which script writes it first (used for
  ordering/schema-init dependency, not enforced by the manifest itself).
- **`usecases:`** — the wiring layer. Each usecase is `{name, description,
  steps: [{order, kind: deterministic|semantic, description, script|prompt}]}`.
  `kind: deterministic` steps reference a `script:` name (must exist in
  `scripts:`); `kind: semantic` steps reference a `prompt:` name (must
  exist in `prompts:`). Some usecases have `steps: []` — declared but not
  yet wired (e.g. `extract-tables`, `generate-section-draft-novelty`) —
  this is a valid, load-bearing state pcems itself uses for "usecase exists
  as a name other things can reference, implementation pending."

`common/ADDING-A-USECASE.md` is the checklist pcems itself follows when
adding to this file — 7 numbered steps, schema → script → prompt →
usecase → allow-lists → smoke test → integration. Reuse verbatim for
rust_dev (see §5).

`standard.metadata.json` is a second, smaller file — `custom_tables`
(subset with `required_columns`, used for schema validation, not the full
`purpose`/`owner_script` detail `standard.yaml` carries), `templates`
(`{name, purpose, role}` — proposal, report, audit-report roles), and
`proposal_template` (which template name `render_proposal.py` defaults to).

## 3. Proposed `rust_dev` `standard.yaml` shape

Lives at `common/schema-manifest/standard.yaml` (matching pcems's path
exactly, post-proposal-1 restructure). Skeleton — full script/prompt/usecase
enumeration depends on proposal 3's wiring decisions, so only the shape and
header are proposed here:

```yaml
# rust_dev — samgraha standard manifest.
#
# Rust systems-engineering documentation system: 13 domains across 7 tiers
# (tier 4 intentionally absent — see 00-domain-relationships.md and
# docs/proposal/archive/rust_dev-proposal.md §10 for why).
# Deterministic + semantic audit layer, 25/25/25/25 four-bucket weight
# split (calculation/summary/final_score.yaml — see proposal 1 §3 for why
# calculation/ stays common rather than per-tier).
#
# Fully self-contained — every scripts:/prompts: location: points inside
# rust_dev's own tree (tierN/, common/). No cross-standard references.
# Paths are relative to this file's location (common/schema-manifest/).

name: rust_dev
version: "1.0.0"
description: "Rust systems-engineering documentation standard — 13 domains, 7 tiers, deterministic + semantic audit, 25/25/25/25 four-bucket weight split"
seeder_script: ../script/seeder.py         # net-new, see §4
smoke_test: ../smoke_test.py               # net-new, see §4

scripts:
  # --- schema-init usecase ---
  - name: init-schema
    location: ../script/init_schema.py
    purpose: "create dev_* tables if missing, seed rust_dev's 13 domains + 7 tiers"
  # --- tier1 usecases (vision, philosophy) ---
  - name: generate-document-vision
    location: ../../tier1/script/generate_document.py
    purpose: "..."
  # ... one entry per tier's scripts, see proposal 3

prompts:
  # ... one entry per tier's prompts, see proposal 3

custom_tables:
  # ... net-new dev_* tables, see §4

usecases:
  # ... see proposal 3 (calculation/audit wiring) and proposal 4 (usecase-map)
```

## 4. Net-new pieces pcems has that rust_dev needs from scratch

Unlike proposal 1 (pure file relocation) and proposal 3 (wraps existing
check scripts), these have **no existing rust_dev equivalent at all** —
greenfield:

| Piece | pcems reference | rust_dev status |
|---|---|---|
| `common/script/init_schema.py` | creates `academic_*` tables, seeds domains | none — rust_dev has no schema/DB layer today |
| `common/script/_adapter.py` (`parse_step_args`/`write_envelope` contract) | every script imports this | none — rust_dev's `script/{ubuntu,windows}/*.{sh,ps1}` are shell scripts, not Python steps following samgraha's envelope contract |
| `common/script/academic_schema.py`-equivalent (`dev_schema.py`) | typed DB access + allow-lists | none |
| `common/schema/*.sql` (`dev_*` tables) | one row per paper/domain/analysis/etc. | none — no persistence layer exists for rust_dev evaluations today |
| `common/script/seeder.py`, `smoke_test.py` | registration-time seed + 7/7 smoke check | none |
| `standard.metadata.json` | custom_tables/templates/proposal_template | none |

This is the real cost center of the series: rust_dev's existing
`script/{schema,ubuntu,windows}/{domain}/*` checks are **shell/PowerShell
scripts with JSON schema output** (`.sh`/`.ps1` + `.schema.json` +
`.manifest.yaml`), not Python steps that speak samgraha's `--in`/envelope
contract. Proposal 3 addresses wrapping them; this proposal only flags
that the wrapping is necessary before any `scripts:` entry pointing at them
can work through `mcp__samgraha__run_script_step`.

## 5. Registration sequence

Once `standard.yaml` + `standard.metadata.json` + the `dev_*` schema exist:

1. `mcp__samgraha__validate_standard_metadata` — confirm `standard.metadata.json` shape before registering (catches the kind of gap the pcems `templates/proposal/` proposal found the hard way — see `pcems_2026-proposal-phase-generic-schema-proposal.md` §2: declared-but-physically-empty is a real failure mode to check for up front, not discover after the fact)
2. `mcp__samgraha__register_standard` — local registration
3. `mcp__samgraha__seed_standard` — run `seeder_script`, populate `dev_*` domain/tier lookup rows
4. `mcp__samgraha__register_standard_globally` — once verified, promote to the global registry (matching pcems_2026's current `verify_status: "passed"` state)
5. Run `smoke_test.py` — same 7-checks-PASS bar `ADDING-A-USECASE.md` §6 requires of pcems

## 6. Open questions

1. **Resolved in practice**: `dev_*` — `dev_repo_domain_state` (proposal 6
   §5's design, built into `standard.yaml`/`standard.metadata.json` by
   proposal 7) shipped as the first real custom table, `dev_*`-prefixed.
   No second dev-class standard has registered yet to test the
   "survives a sibling joining" reasoning, but the prefix itself is live,
   not still a choice.
2. **Resolved — the opposite of both options offered**: this question
   assumed tier needed its own table or a column on a `dev_domains` table.
   Proposal 6 §2 found neither — `dev_domains` never got built at all;
   `domains:` is samgraha's own generic `domain` table (13 real rows,
   confirmed live), and `tier` doesn't live in SQL schema at all — it's a
   key inside `usecase.data`'s JSON, written by `rust_dev`'s own
   `seeder.py` (not yet built) at seed time, resolved from
   `plan/core/tiers.yaml`. Nothing rust_dev-specific to design here beyond
   what proposal 6 already nailed down.
3. Kept as-is, per the original recommendation — nothing since has needed
   `owner_script` to mean anything more than informational.

## 7. Explicitly out of scope

Writing `dev_schema.py`, `_adapter.py`, the `.sql` files, or any concrete
script content (proposal 3 for the check-script wrapping; this proposal
only establishes that the manifest + schema layer must exist first).
Deciding the full `usecases:` list (proposal 3). Usecase-map generation
(proposal 4). Propose pipeline (proposal 5).
