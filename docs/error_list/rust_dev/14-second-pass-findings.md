# rust_dev — Second-Pass Findings (Post Fix-Pass Re-Verification)

**Category:** Bugs + Gaps (newly discovered)
**Severity:** Mixed (see per-item)
**Date:** 2026-07-16

---

## Context

This pass re-verified the proposal (`docs/rust_dev-proposal.md`) against the live implementation at `samgraha/system/rust_dev`, closed the remaining open items from docs 03-07, and re-checked every item the index (`00-index.md`) had previously marked FIXED or PARTIAL. Several previously-"FIXED" items had drifted or were never fully closed, and several new bugs turned up that were not in any prior doc. All items below are now fixed except where noted.

---

## Closed from previously-open docs

| Source | Item | Fix Applied |
|---|---|---|
| 03 | TOC missing Rust sections in 6 files (01-vision, 02-philosophy, 03-security, 04-feature, 05-architecture, 07-engineering) | Added TOC entries; verified anchors match actual `##` headings. `08-external-context-standards.md` already had its entry — doc 03 was stale on that one file. |
| 04 | Template structural depth (12 templates) | **Already fixed before this pass** — all 12 templates already have H1 heading, header block, `## Relationships`, `Generation note`, and `## Audit Fix` stub. Doc 04 was stale; no action needed. |
| 05 Gap 2 | `eng-doc-004` contradicts Rust paradigm | Rewrote the rule in-place (this file is already system-specific under `rust_dev/`, no cross-system flag needed): severity `error`→`warning`, `mandatory: true`→`false`, added an `exceptions` keyword allowlist (tokio, thiserror, anyhow, sqlx, etc.) so it only flags *non*-Rust technology leakage. |
| 06 Improvement 2 | Philosophy addendum missing "Ownership over GC" | Added as the first bullet in the Systems Philosophy Addendum in `02-philosophy-standards.md`. |
| 06 Improvement 3 | New templates have no relationship IDs backing their cross-references | Added `arch-crate-architecture-derives-component-model`, `arch-trait-design-derives-crate-architecture` to `05-architecture-relationships.yaml`; `ft-crate-implementation-derives-crate-architecture`, `ft-error-implementation-derives-trait-design` to `10-feature-technical-relationships.yaml`. |
| 06 Improvement 4 | `calculation/` per-domain weights | Verified: no per-domain weight mechanism exists in `calculation/`. Documented as a future capability gap (unchanged from prior pass's conclusion — no code to modify). |
| 06 Improvement 5, 6 | `SYSTEM.md` domain tiers, `migration-guide.md` depth | **Already fixed before this pass.** Both present and adequate. |
| 07 | `cargo-audit` domain, `unsafe-code-scan`/`crate-dependency-graph`/`cargo-fmt` schemas, `00-domain-relationships.md` Rust section, `CONTRIBUTING.md` | **Already fixed before this pass** — all manifests, schemas, and docs exist and are correctly wired. Doc 07 was stale on these items. |

---

## New Bug 1 — YAML rule-ID indentation artifact (9 files)

**Files:** all 8 files listed in doc 11's Bug 1 fix, plus `03-security/10-systems_security.yaml` which doc 11 didn't list.

The previous fix pass corrected the rule ID prefixes (`sec-` → `{domain}-sec-`) but the sed/script used left a malformed list-item indent: `-     id: eng-sec-unsafe-guidelines-001` (5 spaces after the dash) instead of `- id: ...`. Still valid YAML, but inconsistent with every other rule file in the system.

**Fix:** normalized all 9 occurrences to `  - id: ...`.

---

## New Bug 2 — `plan/core/tiers.yaml` has a duplicate, invalid Tier 4

**File:** `plan/core/tiers.yaml`

```yaml
  - tier: 3
    domains: [feature-technical]
  - tier: 4
    domains: [engineering]        # <- engineering already in tier 2
  - tier: 5
```

The source of truth, `00-domain-relationships.md`'s own "Machine-Readable Format" block, has **no tier 4** — tiers jump 1, 2, 3, 5, 6, 7, 8 intentionally, because base_dev's tier 4 (`11-prototype`) was dropped and the proposal's Tier Reordering table does not renumber. A prior fix pass (index item 12, "tiers.yaml tier 4 added") misread the gap as a missing entry and inserted a duplicate `engineering` block instead of leaving the gap alone.

**Fix:** removed the bogus tier 4 block. `tiers.yaml` now matches `00-domain-relationships.md` exactly.

---

## New Bug 3 — Whole generation/audit template files still exist for the 3 REMOVED domains

**Severity:** HIGH — this is the same category as doc 01 ("dropped-domain-residue"), which was marked FIXED but only cleaned `audit/deterministic/`. It missed four other locations:

| Location | Files found |
|---|---|
| `audit/semantic/document/` | `06-design.md`, `09-feature-design.md`, `11-prototype.md` |
| `templates/generation/document/` | `06-design.md`, `09-feature-design.md`, `11-prototype.md` |
| `templates/audit/deterministic/{document,section}/` | `06-design-report.md`, `09-feature-design-report.md`, `11-prototype-report.md` (×2 dirs) |
| `templates/audit/semantic/{document,section}/` | same 3 domains (×2 dirs) |
| `templates/audit/summary/` | same 3 domains |
| `script/ubuntu/` and `script/windows/` | `06-design/design-tokens-in-implementation.{sh,ps1}`, `11-prototype/mock-api-runs.{sh,ps1}` |

21 leftover markdown files + 4 leftover scripts for domains the proposal explicitly removes ("Domains REMOVED (3 of 16)"). None were referenced by `script/mapping.yaml` or `script/policy.yaml`, so they were dead weight rather than wired-in — but their mere presence means a generation/audit run against `rust_dev` could still be pointed at a `06-design`, `09-feature-design`, or `11-prototype` document, defeating the entire point of the domain removal.

**Fix:** deleted all 25 files.

---

## New Bug 4 — `12-qa` audit rules reference the dropped `Design(06)` domain (functionally broken criterion)

Beyond the prose-only issue already fixed in `12-qa-standards.md`, the **actual semantic audit criteria** (the C3 scoring rule for E2E Testing) were wired to check "E2E journeys traceable to Design(06) workflows" in:

- `audit/semantic/document/12-qa.md`
- `audit/semantic/section/12-qa/06-e2e_testing.md`
- `templates/audit/semantic/document/12-qa-report.md`
- `templates/audit/semantic/section/12-qa-report.md`
- `templates/audit/summary/12-qa-report.md`
- `templates/generation/document/12-qa.md`
- `templates/generation/document/13-implementation.md`

Since `Design(06)` documents are never generated in `rust_dev`, this criterion could never pass — a structurally unfulfillable audit rule.

**Fix:** re-pointed C3 (and all matching prose) at `Feature-Technical(10)` runtime behavior instead of `Design(06)` UX/workflows across all 7 files, replacing "user journeys" language with "runtime workflows" (CLI/API examples instead of registration/checkout examples) to fit a systems context with no UI.

---

## New Bug 5 — `13-implementation-standards.md` and 4 of its generation templates required 3 removed domains as inputs

**File:** `documentation-standards/13-implementation-standards.md` (~15 occurrences) plus `templates/generation/section/12-qa/01-purpose.md`, `12-qa/05-e2e-testing.md`, `13-implementation/03-generation_plan.md`, `13-implementation/05-change_request_plan.md`, and the whole-document assemblies `templates/generation/document/12-qa.md` / `13-implementation.md`.

The Implementation standard's Plan Scenarios, Generation Plan template, Change Request template, Responsibilities, Inputs, Traceability, and Relationships sections all still listed `Feature Design(09)`, `Prototype(11)`, and `Design(06)` as required or optional upstream inputs — despite these being 3 of the 16 domains the proposal explicitly drops. This directly contradicts the Domain Scope table.

**Fix:** replaced `Feature Design(09)` references with `Feature Technical(10)` (where the proposal says that content now lives), removed `Prototype(11)` and `Design(06)` entirely (no replacement — proposal states "systems require full implementation from start," no design/prototype stage exists), and adjusted worked examples from web-app UX scenarios to systems scenarios (message producers, crate consumers).

---

## New Bug 6 — `plan/usecase/*` walkthroughs still walk through a whole Tier 4 (Prototype) that doesn't exist in rust_dev

**Files:** all 4 usecase scenarios (`repo_existing/case_1`, `repo_existing/case_2`, `repo_new/case_1`, `repo_new/case_2`), each had a `tier_4/{01-generation,02-audit,03-fix}.md` directory walking through generating and auditing an `11-prototype` document, plus a `design` row in each `tier_2/02-audit.md` and a `feature-design` row in each `tier_3/{01-generation,02-audit}.md`.

`rust_dev`'s canonical tier list (`00-domain-relationships.md`'s machine-readable block, mirrored in `plan/core/tiers.yaml` after Bug 2's fix) has no tier 4 at all — base_dev's tier 4 was `11-prototype`, dropped without renumbering. These usecase walkthroughs were still base_dev's tier structure, unadapted.

**Fix:**
- Deleted all 4 `tier_4/` directories.
- Removed the `design` row from each `tier_2/02-audit.md` (4 files).
- Removed the `feature-design` row from each `tier_3/01-generation.md` and `tier_3/02-audit.md` (8 files).
- Fixed the dangling "Tier 4 can begin" tier-gate reference in each `tier_3/03-fix.md` to read "Tier 5 can begin" (4 files).

---

## Verification

Final repo-wide sweep after all fixes:

```
grep -rln "Design(06)\|Feature Design(09)\|Prototype(11)" --include="*.md" --include="*.yaml" .
```

Returns zero matches outside of `CHANGELOG.md`, `migration-guide.md`, and `SYSTEM.md` — all three legitimately document the domain-removal decision as history/mapping, not residue.

---

## Remaining Open (unchanged from prior pass, low priority, not re-attempted here)

| Item | Why deferred |
|---|---|
| Header structure normalization (Structure A vs B, ~20 section rule files) | Cosmetic; no confirmed tooling reads `header.section_type`/`header.scope` today. Documented in doc 11 Bug 4. |
| `04-feature` metadata leak (`semantic_type`/`scope` blocks rendering in output) | Doc 10 Bug 7; requires generation-engine-level stripping, not a content fix. |
| `02-philosophy-standards.md` addendum position (buried after generic content) | Doc 07 Suggestion 6; stylistic, no functional impact. |
