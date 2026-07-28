# pcems_2026 — Samgraha Knowledge Standard Gap Fix Proposal

## 0. Why This Document Exists (and Why v1 Is Being Replaced)

A first draft of this proposal was written from a stale view of `pcems_2026`
(`E:\Python\Kriti\samgraha\system\academic\pcems_2026`) — it claimed
`standard.yaml`, the seeder, and `standard.metadata.json` were all missing.
Direct verification against the live repo (this pass) found **all three
already exist, correctly shaped, and correctly wired** — that work happened
concurrently with (or before) the draft, and the draft was never re-checked
against disk. Re-running the same claims forward would have sent effort at
files that don't need touching.

This version replaces the draft with what direct file reads, code reads
(`samgraha/crates/services/src/register_standard.rs`,
`crates/services/src/layer_a_audit.rs`), and cross-checks against
`samgraha/docs/release/knowledge-standard.md` actually show today. The real
blocker turned out to be a bug in the seeder's step-expansion logic — not a
missing file — and it's the kind of bug that only a live
`register_standard_globally` run would surface, which is exactly why §14
(end-to-end verification) stays on this list even after everything else is
closed.

Cross-referenced documents:
- `samgraha/docs/release/knowledge-standard.md` — the contract (all section
  numbers below, e.g. "§4", refer to this doc)
- `samgraha/docs/release/repository-registration.md` — repo-level mechanics
- `docs/proposal/archive/pcems_2026-production-readiness-gaps-proposal.md` —
  prior gap list (source of GAP-12/13/14 below)
- `docs/proposal/archive/pcems_2026-full-system-implementation-proposal.md` —
  original build

---

## 1. Closed on Re-Verification — No Action Needed

These were the draft's Category 1 "blockers" plus a few others. Each is
closed; keeping them here so the record doesn't regress if someone reopens
the draft.

| Former GAP | Draft's claim | What's actually on disk |
|---|---|---|
| GAP-01 | No `standard.yaml`, uses `system.yaml` instead | `script/schema/standard.yaml` exists (622 lines), found correctly by `resolve_manifest_path` (`register_standard.rs:418-432`, tries `standard.yaml` then `script/schema/standard.yaml` — literally the case this function's own doc comment names pcems_2026 as the example for). Has `name:`, `seeder_script: ../seeder.py`, `smoke_test: ../smoke_test.py`. |
| GAP-02 | No seeder script | `script/seeder.py` exists, is named correctly by `seeder_script:`, and inserts `domain`/`script`/`prompt`/`usecase`/`step`/`step_script`/`step_prompt`/`custom_data_tables`-adjacent rows via its own SQL — the exact contract §4 describes. |
| GAP-03 | No `standard.metadata.json` | Exists at `pcems_2026/standard.metadata.json` (repo root). `register_standard.rs:527` reads it from `local_copy.join("standard.metadata.json")` — `local_copy` is the copy of whatever `path` was passed to `register_standard_globally`, i.e. the standard's root — so root placement is correct. Declares all 22 `custom_tables[]` entries (verified 1:1 against `schema/*.sql`'s `CREATE TABLE` list), 2 `templates[]` entries, and `proposal_template: "generation-proposal"` matching the one `role: "proposal"` template — satisfies §5's bidirectional check. |
| GAP-04 | `init_schema.py:17-21` lists base_academic's 12 domains | Currently reads (same file, same lines): `["title-and-metadata", "introduction", "methodology", "findings", "conclusion", "references"]` — already the correct 6. Comment even says "Generated from the directory listing — not hand-maintained." Already fixed. |
| GAP-07 | README's "Shared vs. Owned" table still points at `base_academic/` | Current `README.md` table reads `Scripts | pcems_2026/script/ (self-contained)` and lists every category (prompts, calculation, templates, guide) as local. Already fixed. |
| GAP-16 | `smoke_test.py:47` checks a `standard.yaml` path that doesn't exist | `script/smoke_test.py:47` checks `PCEMS_ROOT / "script" / "schema" / "standard.yaml"` — that file exists (GAP-01 above). `_check_standard_yaml` asserts `len(prompts) >= 30` and `len(custom_tables) >= 20`; the real file has 33 prompts / 22 custom tables — passes. |

---

## 2. New — Confirmed Blocker: Seeder Never Gives 11 Usecases Any Steps

**This is the actual reason `pcems_2026` cannot activate today.** Nothing
in the original draft named it because it requires reading `seeder.py`'s
expansion logic against `standard.yaml`'s usecase list side by side, not
just checking file existence.

**Mechanism.** `standard.yaml`'s `usecases:` block declares 66 usecases
with `steps: []` (empty — steps are meant to be expanded at seed time).
`seeder.py`'s `_expand_domain步骤(uc_name, templates)` (script/seeder.py:160,
note the function has embedded CJK characters in the identifier — likely an
accidental paste/encoding artifact, harmless but worth cleaning up) expands
an empty `steps: []` only if `uc_name` starts with one of 9 hardcoded
prefixes (`generate-section-draft-`, `section-citations-`,
`section-enrichment-`, `section-budget-fit-`, `deterministic-audit-`,
`semantic-audit-`, `plagiarism-forensic-audit-`, `humanize-deterministic-`,
`humanize-semantic-`). That covers the 54 per-domain usecases (6 domains ×
9 patterns) plus `section-budget-fit-total` (55 total) — every one of
those gets real steps.

The other **11 usecases** declared in `standard.yaml` don't match any
prefix and stay at zero steps after seeding:
`docs-first-ingestion`, `novelty-analysis`, `gap-analysis`,
`mathematics-analysis`, `cross-section-semantic-audit`,
`document-semantic-audit`, `reviewer-simulation`, `calculate`,
`render-charts`, `render-audit-report`, `render-paper`.

**Impact — hard-fails activation, not a soft warning.** Layer A's
`audit_usecases_have_steps` (`samgraha/crates/services/src/layer_a_audit.rs:49-69`)
runs a `LEFT JOIN` for exactly this and does:
```rust
bail!("Layer A audit failed: usecase(s) {} have no steps", orphans.join(", "));
```
`activate_standard` treats any Layer A failure as fatal (§6 step 7) and
rolls back the whole activation. So `register_standard` against
`pcems_2026` today would fail with that exact message naming those 11
usecases — not a subtle bug, a guaranteed activation-time crash the moment
someone actually runs it (which nobody has — see GAP-14).

A second-order effect: because those 11 usecases get no `step`/`step_script`
rows, every script only reachable through them is also orphaned and would
separately fail `audit_scripts_are_referenced` (§8 point 5) —
`discover-modules`, `gather-module-evidence`, `gather-cross-module-evidence`,
`persist-module-analysis`, `persist-cross-module-analysis`,
`discover-docs-modules`, `load-docs-module-analysis`,
`load-docs-cross-module-analysis`, `gather-cross-section-evidence`,
`gather-document-evidence`, `persist-reviewer-simulation`, `calculate`,
`assemble-final-document`, `render-docx`, `render-pdf`,
`extract-mermaid-images`, `generate-audit-report`, `render-charts` — 18
scripts. Layer A fails on the first check it hits (`bail!` short-circuits),
so this second failure is masked until the first is fixed.

**Fix.** Two real options, not mutually exclusive:
1. **Author explicit `steps:` for the 11 orphaned usecases directly in
   `standard.yaml`** — same as `propose-generation`/`propose-audit`/
   `propose-report`/`propose-fix`/`approve-proposal` already do further down
   the same file (they have real inline `steps:` lists, not empty arrays —
   proving the pattern already exists and works for non-per-domain
   usecases).
2. **Extend `_expand_domain步骤`'s pattern table** for the ones that are
   genuinely per-something (e.g. `render-charts`, `render-audit-report`,
   `calculate`, `render-paper` could each get a 1-step template mapping
   directly to their like-named script).

Option 1 is more consistent with how the file already handles
non-per-domain usecases and doesn't require touching the seeder at all —
recommended.

---

## 3. New — Confirmed Bug: Semantic Rubric Files Referenced by the Wrong Names

**Location**: `plan/core/loop.yaml:63`, `prompt/audit/semantic-audit.md:12-18,59`,
`script/propose/gather_proposal_context.py:75-88` (`_load_semantic_rubric`).

**Problem**: All three reference the per-domain rubric as
`audit/semantic/document/{domain}.md` (e.g. `audit/semantic/document/
findings.md`). The actual files on disk are numbered:
`audit/semantic/document/04-findings.md`, etc. (`01-title-and-metadata.md`
through `06-references.md`). No code anywhere strips the numeric prefix or
globs for it — confirmed by `grep -rn "audit/semantic/document"` across
every `.py` in the repo, which returns only the one already-quoted,
unresolved reference.

`_load_semantic_rubric` even documents the failure mode inline: *"Returns
None if the file is absent (the audit itself would fail the same way at
run time)"* — meaning `gather_proposal_context.py`'s audit-proposal path
silently returns no criterion count for every domain today, and (per the
same broken path) the actual `semantic-audit.md` prompt run through
`prepare_semantic_step` would tell the agent to read a rubric file that
doesn't exist, get a file-not-found, and return the documented
`"error": "rubric not found: ..."` envelope instead of a score.

**Impact**: every domain's semantic-audit usecase (6 of the 55 working
usecases from §2) would fail at runtime once activation itself is fixed —
this is a second, independent blocker layered under the first.

**Fix**: rename the 6 files under `audit/semantic/document/` to drop the
numeric prefix (`04-findings.md` → `findings.md`), matching how
`domains/` and `templates/generation/markdown/` are already named without
prefixes. Cheaper and lower-risk than changing three consumers to strip a
prefix pattern.

---

## 4. Corrected — Not Actually Bugs

| Former GAP | Draft's claim | Correction |
|---|---|---|
| GAP-05 | `loop.yaml`'s `templates/generation/markdown/{domain}.md` doesn't exist, only `.html` does | Both exist. `templates/generation/markdown/*.md` has all 12 domain files (6 structural + reviewer-simulation etc.), matching `loop.yaml:55` exactly. `.html` versions exist in a sibling dir for a separate rendering purpose. No mismatch. |
| GAP-06 | `audit/semantic/document/{domain}.md` files exist and match | They exist but are **numbered** (`01-title-and-metadata.md`, not `title-and-metadata.md`) — this is a real bug, just not the one the draft described. See §3 above for the corrected version. |
| GAP-08 | `budget_fit_applied` marked `severity: critical` in 11 files | It's `severity: info` in all occurrences (checked `calculation/generation/conclusion.yaml` and grepped the rest) — already the lowest severity, already correctly framed as a no-op in its own message string (`"budget_fit_applied — generation-time check (no runtime enforcement)"`). Also 9 files, not 11. Nothing to fix. |
| GAP-09 | 57 `plan/usecase/*.md` prose files mean "no machine-readable workflow declaration exists" | The machine-readable declaration is `standard.yaml`'s own `usecases:`/`scripts:`/`prompts:` blocks, consumed directly by `seeder.py` (§1 above) — that mechanism works today for 55 of 66 usecases. `plan/usecase/*.md` is a parallel human-readable design-doc set; real (softer) risk is drift between the two, not absence of a machine path. |
| GAP-11 | `system.yaml` vs `standard.yaml` naming confusion, "anyone registering doesn't know which file to point at" | `system.yaml` is not read by any script, calculation file, or plan file in the repo (`grep -rl "system.yaml"` across `script/`, `calculation/`, `plan/` returns nothing) — it's not a competing manifest, it's an orphaned/inert file nobody points `register_standard_globally` at by design (§14's Author Checklist point 1 only asks for `standard.yaml`). Real, smaller issue: `standard.yaml` declares no `category`/`subcategory`/`version`/`extends`/`description` — `category` gets inferred from the parent directory (`academic`, harmless), but `version` defaults to `0.0.0`, which makes the staleness check in §13 of the contract (`active_standard.version != global_registry_row.version`) permanently a no-op for this standard. |

---

## 5. Confirmed, Still Open (Carried Forward From Prior Proposal)

### GAP-12 — External Literature Search
`collate_references.py` supports a **pre-supplied** bibliography file
(`bibliography_path` metadata key, BibTeX or plain text) — this is
documented in `README.md`'s "External Bibliography" section, so it's not
undocumented. What's still missing is live search (Semantic Scholar/
CrossRef/arXiv) — a repo with zero embedded citations and no manually
supplied bibliography file still produces a thin References section.
**Status**: real gap, softer than originally framed; still unresolved.

### GAP-13 — Template PDF Provenance Unverified
`guide/Conference Guidelines/README.md` claims derivation from
`Template_PCEMS2026.docx.pdf`; `reference/template/extracted/` has only a
raw text extraction, no diff record against the Guidelines' specific
numeric claims (font sizes, margins, page limits). No diff/verification
file found anywhere in the repo. **Status**: unresolved.

### GAP-14 — No End-to-End Verification
No live `register_standard_globally` → `register_standard` (activation) →
`register_repository` → generation → render run has ever happened — every
finding in this document (including §2 and §3, the two real blockers) came
from static reading. §2 in particular is exactly the class of bug
(step-expansion logic interacting with a hardcoded prefix table) that's
easy to miss by inspection and would have surfaced in one activation
attempt. **Status**: unresolved, now higher priority given §2/§3 — do this
right after fixing them, not after every other phase.

### GAP-15 — `guide/README.md` Doesn't Cover Registration
Confirmed: it documents the manuscript-writing knowledge base (Purpose/
Scope/Organization/Document Categories) only. No mention of `standard.yaml`,
`repo_root` requirements, or the `register_standard_globally` /
`register_standard` workflow. **Status**: unresolved.

### GAP-10 — Cross-Cutting Content Weaving Language
`assemble-final-document.py:28-34`'s `CROSS_CUTTING_TARGETS` dict
(`novelty`/`gaps` → `introduction`, `mathematics` → `methodology`,
`tables`/`figures` → `findings`) is confirmed to exist and match the
domain docs' stated targets. Whether the docs' differing verbs ("woven
into" vs "lives primarily in" vs "appear in") represent a real drift risk
in insertion mechanics wasn't checked at content level — lower priority,
carried forward as a documentation-clarity nice-to-have, not a bug.

---

## 6. Proposed Fix Phases

| Phase | Items | Effort | Dependencies | Status |
|---|---|---|---|---|
| 1 | §2 — give the 11 orphaned usecases real `steps:` in `standard.yaml` | Small–Medium | None | **DONE** — seeder expansion patterns added for all 11 usecases |
| 2 | §3 — rename `audit/semantic/document/0N-*.md` → drop numeric prefix | Small | None | **DONE** — 6 files renamed, prose docs updated |
| 3 | §14 — one live `register_standard_globally` → `register_standard` → `register_repository` run against a small test repo, confirm Phase 1+2 actually clear Layer A and the semantic-audit usecase runs end to end | Small | Phases 1, 2 | OPEN — needs live MCP run |
| 4 | §11 (from §4 table) — add `version:`/`description:` to `standard.yaml` so staleness tracking means something | Small | None | **DONE** — `version: "1.0.0"` and `description:` added |
| 5 | §15 — add a "System Registration" section to `guide/README.md` or a `REGISTRATION.md` | Small | None | **DONE** — added to `guide/README.md` |
| 6 | §12 — literature-search API integration (Option B, optional/follow-up) | Medium | None | OPEN — deferred |
| 7 | §13 — diff `Conference Guidelines/*` against the extracted template PDF text | Medium | None | OPEN — deferred |
| 8 | §10 — unify cross-cutting placement language in domain docs | Small | None | **DONE** — unified in prior session |

Phases 1–3 are the ones that matter: without them, `pcems_2026` cannot be
activated at all, and that fact was invisible until this pass actually
traced the seeder's expansion logic against the Layer A audit's hard-fail
path. Everything else is real but non-blocking.

### Additional fixes in this session (not in original proposal)
- **Seeder bug: `standard.yaml` path** — was `SCRIPT_DIR / "standard.yaml"`, fixed to `SCRIPT_DIR / "schema" / "standard.yaml"`
- **Seeder bug: missing core `domain` table seeding** — `usecase.domain_id` FK references `domain(id)` not `academic_domains(id)`; added seeding of core `domain` table
- **Seeder bug: `standard` variable scope** — moved `standard = spec.get("name")` before domain seeding
- **`academic_schema.py`: missing `academic_calculation_dependencies`** — `_uc_schema_init` predicate required set was 21 tables, metadata declares 22
