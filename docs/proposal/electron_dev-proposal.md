# electron_dev — System Proposal

## 1. Class / Position in Taxonomy

Class `dev`, subclass `frontend` (grouped with `react_dev` — the
taxonomy proposal's explicit call: "Electron's renderer is React/web-tech,
main process rides along under the same bucket"), `extends: base_dev`,
no drops. Proposed path `dev/frontend/electron_dev/` (currently flat at
`samgraha/system/electron_dev/`).

## 2. What It Has

16 domains — identical set to `base_dev` (no drops). Tier structure and
relationship graph diff at 497 lines against `base_dev`'s file — larger
than `react_dev`'s cosmetic-only diff, but on inspection this is still
prose/table restructuring (tier descriptions reworded for desktop/IPC
framing), not a structural change to the tiers or edges themselves — the
underlying YAML `tiers:`/`relationships:` block is the same graph.

File inventory delta vs. `base_dev`:
- `documentation-standards/`: 0 files different (identical)
- `script/`: 0 files different (identical — same 18 checks as `base_dev`)
- `calculation/`: 0 files different (identical)
- `templates/audit/`: 0 files different (identical)
- `plan/`: 0 files different (identical)
- `templates/generation/section/`: **17 new section templates**, the
  largest per-system addition of any dev-class system
- `audit/deterministic/section/`: 8 new files — **but see §10, these are
  not actually YAML**
- `audit/semantic/section/`: 11 new files — **but see §10, wrong format**

## 3. What It Inherits vs Overrides vs Adds

Full directory diff against `base_dev`, actually run:

| Area | Result |
|---|---|
| `documentation-standards/*.md` | Identical to `base_dev`, 0 diff |
| `script/**` | Identical to `base_dev`, 0 diff — no Electron-specific check scripts |
| `calculation/**` | Identical to `base_dev`, 0 diff |
| `templates/audit/**` | Identical to `base_dev`, 0 diff |
| `plan/**` | Identical to `base_dev`, 0 diff |
| `00-domain-relationships.md` | Same graph, reworded tier descriptions for desktop/IPC framing |
| `templates/generation/section/**` | **17 net-new files** (full list below) |
| `audit/deterministic/section/**` | **8 net-new files, wrong file format — see §10** |
| `audit/semantic/section/**` | **11 net-new files, wrong file format — see §10** |

The 17 new section templates, confirmed present and read:
`05-architecture/{12-microservices,13-monolith}.md`,
`06-design/07-design-system.md`,
`07-engineering/{09-async-programming,10-security-hardening,11-caching,12-background-processing}.md`,
`09-feature-design/08-desktop-ui.md`,
`10-feature-technical/{18-ipc-implementation,19-process-architecture}.md`,
`12-qa/{10-ipc-testing,11-process-testing,12-cross-platform-testing}.md`,
`13-implementation/08-service-patterns.md`,
`14-build/{10-packaging,11-auto-update}.md`,
`16-product-guide/07-service-catalog.md`.

Content is genuinely Electron-specific and substantial — read in full,
`05-architecture/12-microservices`'s matching semantic audit file
(§10) documents the three-process model (Main/Renderer/Preload), IPC
channel naming conventions, `contextBridge`/`contextIsolation`
requirements, and process lifecycle ordering — this is real domain
expertise, not filler.

Same ~85-file duplication finding as `react_dev`'s proposal applies
here too (`documentation-standards/`, `script/`, `calculation/`,
`templates/audit/`, `plan/` all zero-delta copies of `base_dev`) — not
repeated in full here, see `react_dev-proposal.md` §3 for the same
argument.

## 4. Use Cases

Identical to `base_dev`'s 4 use cases (`plan/` is a 0-diff copy).

## 5. Workflow per Use Case (target `init.py` phase plan)

Same conclusion as `react_dev`: domains/tiers/graph are unchanged from
`base_dev`, so the phase *shape* is inherited wholesale — 8 tiers, same
`within_tier_ordering` exception, generate→audit→fix per phase.
`electron_dev` does not need a hand-authored `init.py` distinct from
`base_dev`'s; the 17 extra sections are additional leaf-level
scaffold/content-fill pairs nested inside their parent domains'
existing phases (e.g. `10-feature-technical`'s generation phase now
scaffolds 19 sections instead of 17), resolved by reading
`electron_dev`'s own `templates/generation/section/` at scaffold time.

## 6. Deterministic Audit via Script

Same as `react_dev`: `script/**` is a 0-diff copy of `base_dev`'s 18
generic checks. No Electron-specific check scripts exist (nothing
IPC-channel-naming-convention-specific, nothing
context-isolation-enabled-specific) despite the semantic audit criteria
in §3/§10 explicitly describing checkable conditions (e.g.
"`nodeIntegration: true`" as a red flag, "`contextIsolation` enabled" as
an expected-quality bullet) — these read as things a script *could*
verify against a repo's actual Electron config/main-process source, not
just judge from prose. Worth flagging as a concrete candidate for new
deterministic checks once `validate.py` exists (see §10).

## 7. Generation via Script (`scaffold.py`)

Same mechanism as every other dev-class system: reads
`templates/generation/document/{domain}.md` + all present
`section/{domain}/*.md` files, creates headings mechanically. The 17
Electron-specific templates are structured as prose paragraphs today
(full-document style), not yet in the stub+prompt shape the
execution-model proposal's §6 note flags as a needed reshape across the
whole `dev` class — this system's section count (17, largest of any
dev-class addition) makes that reshape work proportionally larger here
than for `react_dev`'s 13 or `fastapi_dev`'s/`rust_dev`'s smaller
additions.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculation/**` is a 0-diff copy of `base_dev`'s 7 formulas — identical
stable IDs, identical weighting. No Electron-specific scoring logic
exists.

## 9. Script Language Priority Applied

No new check-script `.py` files are needed for existing checks (§6 — no
Electron-specific check scripts exist yet to port). What *is* needed,
per §6's finding: 2-3 new Python check scripts as net-new capability
(not a port) if the deterministic candidates flagged there
(`nodeIntegration`/`contextIsolation` config verification, IPC
channel-naming-convention lint) get built — these would be
`electron_dev`'s own addition to the 18 inherited checks, not a
`base_dev` override.

## 10. Open Questions / Risks Specific to `electron_dev`

**Primary finding, needs attention before this system's audit layer
can function as designed:**

- **The 8 new `audit/deterministic/section/**/*.rs` files are literally
  Rust source code, not YAML rule definitions.** Confirmed by reading
  `audit/deterministic/section/14-build/10-packaging.rs`: it opens with
  `use serde::{Deserialize, Serialize};` and doc-comments — this is a
  `.rs` source file, structurally incompatible with every other
  deterministic audit file in this system (and all of `base_dev`'s, and
  `react_dev`'s new ones), which are `.yaml` rule files consumed by the
  audit engine. As written, these 8 files cannot be read as audit rules
  by anything expecting the established format.
- **The 11 new `audit/semantic/section/**/*.yml` files are raw YAML
  with the wrong extension AND the wrong internal format.** Confirmed
  by reading `audit/semantic/section/05-architecture/12-microservices.yml`
  in full: it's well-authored, substantive YAML (`engineering_intent`,
  `audit_objectives`, `scoring_criteria` with weighted `C1`-`C6` IDs,
  `output_schema`) — genuinely good content — but every other semantic
  audit file in this system (and `base_dev`'s, and `react_dev`'s) is
  Markdown with `#`/`##` headers (confirmed against
  `base_dev/audit/semantic/section/05-architecture/01-purpose.md`), not
  raw YAML. This isn't a naming nitpick — it's two structurally
  different file formats serving the same role, and whatever parses
  `audit/semantic/section/**` today almost certainly expects Markdown,
  not YAML.
- Net effect: **all 17 of `electron_dev`'s new sections currently have
  content but effectively no working audit layer**, despite `audit/`
  containing 19 files that look like they cover 8 of the 17 sections.
  This should be fixed (convert `.rs`→`.yaml` matching `base_dev`'s
  deterministic shape, convert `.yml`→`.md` matching the semantic
  shape) before `validate.py` is built against this system, or
  `validate.py` will silently skip/fail on these 8 sections.
- Secondary: only 8 of the 17 new sections have any audit coverage at
  all (`microservices`, `security-hardening`, `caching`,
  `background-processing`, `ipc-implementation`, `process-architecture`,
  `ipc-testing`, `process-testing`, `cross-platform-testing`,
  `service-patterns`, `packaging`) — `monolith`, `design-system`,
  `desktop-ui`, `async-programming`, `auto-update`, `service-catalog`
  have templates but no audit rule of either kind, same pattern as
  `react_dev`'s gap.

## 11. Explicitly Out of Scope

Actually fixing the `.rs`→`.yaml` and `.yml`→`.md` format mismatch
(§10) — flagged here as a finding for a dedicated fix, not corrected in
this proposal. Actual script implementation. Any change to domain
content beyond the format-correction just described.
