# rust_dev — Review Index

**Review Date:** 2026-07-15  
**System Reviewed:** `E:\Python\Kriti\samgraha\system\rust_dev`  
**Proposal Reviewed:** `E:\Python\Kriti\docs\rust_dev-proposal.md`

---

## Overview

This index summarizes all findings from the cross-review of the `rust_dev` proposal against its actual implementation. Findings are split into **Bugs** (correctness issues), **Gaps** (missing implementations), **Improvements** (quality enhancements), and **Suggestions** (future work).

**Last updated:** 2026-07-16 — After a FOURTH pass: independent re-verification of the "all fixed" claim below. 3 verification agents re-read every cited file's current on-disk state against docs 15/16/17. Result: the "all fixed" claim was **overstated** — several fixes were partial (one occurrence corrected, sibling occurrences missed) or subtly wrong (a fix that swapped one bug for another). Specifically found and then corrected in this pass: `crate-dependency-graph.sh`'s exit-code fix (doc 16 BUG-2) still swallowed the real exit code via `|| true` before reading `$?`; `04-feature-relationships.yaml`'s dangling-section fix (doc 15 BUG-8) pointed the corrected section name at the wrong domain (`feature-technical` instead of `qa`, where `test_strategy` actually lives); a new, previously-unflagged slot-07 collision in `16-product-guide` (`07-development_workflow.yaml` vs `07-product_context.yaml`, both deterministic and semantic) sat untouched next to files that were being edited for another bug; a cross-link in `01-vision-standards.md` still pointed at a since-renamed file; one semantic-duplicate `.md` file was left behind when its sibling was deleted; 2 files still had "Feature Design" in condition prose after the `domain:` key itself was fixed; all 4 `tier_2/02-audit.md` use-case files still listed the dropped `design` domain; all 4 `tier_8/01-generation.md` files still had broken template paths; `tier_5/01-generation.md` still listed `Prototype`/`Feature Design`/bare `Design` as upstream inputs; 1 of 6 "14 upstream documents" occurrences was missed; `15-readme-standards.md`'s Node/npm→Rust fix never propagated to the 4 files (1 whole-doc + 3 section templates) that duplicate the same example content; and 4 stray TODO placeholders in `16-product-guide-standards.md` were never addressed. **All of the above are now fixed as of this pass** — see the corrected status per-doc below. Remaining open items are genuinely engine-level (STD-001, STD-004) or documented low-priority/cosmetic deferrals.

---

## Bugs — Must Fix

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 1 | [01-dropped-domain-residue.md](./01-dropped-domain-residue.md) | **HIGH** | ✅ **FIXED** | Directories already deleted. Cross-links and stale comments resolved. |
| 2 | [02-semantic-audit-stubs-and-collisions.md](./02-semantic-audit-stubs-and-collisions.md) | **HIGH** | ✅ **FIXED** | Duplicate mini-stubs already deleted. Slot collision resolved. |
| 8 | [08-script-file-extension-bugs.md](./08-script-file-extension-bugs.md) | **CRITICAL** | ✅ **FIXED** | Added `*.rs` to all 6 affected scripts (bash + PowerShell). Added Cargo.toml parsing to dependency-manifest. Added Rust web framework patterns to public-contract-diff. |
| 9 | [09-missing-rust-script-implementations.md](./09-missing-rust-script-implementations.md) | **CRITICAL** | ✅ **FIXED** | All 4 scripts implemented: `cargo-audit.sh/.ps1`, `unsafe-code-scan.sh/.ps1`, `cargo-fmt.sh/.ps1`, `crate-dependency-graph.sh/.ps1`. |
| 10 | [10-template-base-dev-residue.md](./10-template-base-dev-residue.md) | **HIGH** | ✅ **FIXED** | TypeScript/ESLint → Rust/Clippy. Spring Boot → Tokio/Axum. Python → Rust 1.75+. Metadata leak still present (low priority). |
| 11 | [11-audit-rule-id-and-structure-bugs.md](./11-audit-rule-id-and-structure-bugs.md) | **HIGH** | ✅ **FIXED** | All 8 rule ID prefixes corrected. Duplicate slot 10 renamed to 11. All `suggestion` severities changed to `warning`. Header structure normalization deferred (low impact). |
| 12 | [12-cross-reference-and-integration-bugs.md](./12-cross-reference-and-integration-bugs.md) | **MEDIUM** | ✅ **FIXED** | 5 audit templates fixed (02→01-vision). tiers.yaml tier 4 added. Engineering cross-references fixed (rationale→tradeoffs). |

---

## Gaps — Must Fix

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 3 | [03-standards-toc-not-updated.md](./03-standards-toc-not-updated.md) | **MEDIUM** | ✅ **FIXED** | All 7 files now list their Rust sections in the TOC (08-external-context already had it — doc was stale). |
| 4 | [04-template-structural-depth.md](./04-template-structural-depth.md) | **MEDIUM** | ✅ **FIXED (pre-existing)** | Re-verified: all 12 templates already have header block, H1 heading, Relationships table, Generation note, and Audit Fix stub. Doc was stale. |
| 5 | [05-deterministic-audit-severity-gaps.md](./05-deterministic-audit-severity-gaps.md) | **MEDIUM** | ✅ **FIXED** | unsafe_guidelines severity correct (critical/2.0). eng-doc-004 rewritten to only flag non-Rust tech leakage. mapping.yaml/policy.yaml/lint-standards manifest all confirmed wired. |

---

## Improvements — Should Fix

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 6 | [06-improvements-and-optimizations.md](./06-improvements-and-optimizations.md) | **MEDIUM** | ✅ **FIXED** | policy.yaml, SYSTEM.md tiers, migration-guide confirmed present. Ownership-over-GC principle added. Relationship IDs added for crate_architecture/trait_design/crate_implementation/error_implementation. `calculation/` weights documented as a real capability gap (no code exists to change). |
| 13 | [13-script-manifest-and-policy-gaps.md](./13-script-manifest-and-policy-gaps.md) | **MEDIUM** | ✅ **FIXED** | `requires_network` fixed in 2 manifests. Duplicate `$excludeDirs` removed. Cargo.toml parsing added. |

---

## Suggestions — Nice to Have

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 7 | [07-additional-suggestions.md](./07-additional-suggestions.md) | **LOW-MEDIUM** | ✅ **FIXED (pre-existing)** | cargo-audit in correct domain, script schemas exist, CONTRIBUTING.md exists, 00-domain-relationships.md has the Rust cross-domain section. Re-verified live, doc was stale. |

---

## Second-Pass Findings (New)

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 14 | [14-second-pass-findings.md](./14-second-pass-findings.md) | **HIGH** | ✅ **FIXED** | 6 new bugs: YAML indent artifact (9 files), invalid duplicate Tier 4 in tiers.yaml, 25 leftover generation/audit/script files for the 3 REMOVED domains, functionally-unfulfillable `Design(06)` audit criterion in 12-qa, 13-implementation standard + 4 templates requiring removed domains as inputs, and 4 usecase walkthroughs still describing a whole Tier 4 (Prototype) that doesn't exist in rust_dev. |

---

## Third-Pass Findings — Verified Fixed (after 4th-pass correction)

**Trigger:** re-verification of `docs/rust_dev-proposal.md` (STD-001..STD-005) plus a full fresh audit, run as 3 parallel agents scoped to (1) `audit/deterministic` + `audit/semantic`, (2) `script/**` + `calculation/**`, (3) `documentation-standards/**` + `templates/**` + `plan/**`. A follow-up 4th-pass independently re-verified every fix claimed below (see the "Last updated" note above) and corrected the incomplete/wrong ones found.

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 15 | [15-third-pass-audit-checks.md](./15-third-pass-audit-checks.md) | **HIGH** | ✅ **FIXED — verified** (2 deferred) | STD-002/003/005 bugs all fixed: `feature_design` refs deleted from `domain:` keys **and** condition prose (2 files needed the prose follow-up). 6 slot collisions renamed/deleted (incl. a previously-unflagged 16-product-guide slot-07 collision found during verification). 3 invalid `target_domain` values corrected. `16-product-guide` optional sections made non-mandatory (1 semantic orphan `.md` also deleted). `testing_strategy` dangling ref corrected to `qa`/`test_strategy` (first attempt had renamed the section but kept the wrong domain — `feature-technical` has no `test_strategy` section, only `qa` does). `external`→null fixed. Stale cross-link in `01-vision-standards.md` (pointed at a since-renamed file) also fixed. STD-001/STD-004 remain engine feature requests (not fixable in YAML); GAP-3 (`product_context` semantic_type hyphen/underscore spelling) remains open, low priority. |
| 16 | [16-third-pass-audit-scripts.md](./16-third-pass-audit-scripts.md) | **CRITICAL** | ✅ **FIXED — verified** (1 deferred) | 4 CRITICAL npm→Rust script regressions fixed on both bash+PowerShell (build-succeeds, lint-standards, lint-pass, artifact-exists). `cargo-fmt.sh` exit-code masking and `unsafe-code-scan.sh` quoting fixed and confirmed correct. `crate-dependency-graph.sh`'s `set -e`/exit-code fix **needed a second pass** — the first attempt added `\|\| true` without capturing `$?` first, so the exit code was still always read as 0; corrected to `set +e`/capture/`set -e`, matching the `cargo-fmt.sh` pattern. 4 schema/output mismatches fixed. 4 manifests completed with requires_network/depends_on/timeout_seconds. Dead cargo-clippy policy entry fixed. Header normalization deferred (low impact). |
| 17 | [17-third-pass-audit-templates-standards.md](./17-third-pass-audit-templates-standards.md) | **HIGH** | ✅ **FIXED — verified** | `10-feature-technical-standards.md` dropped-domain cleanup confirmed complete (~15 refs). `SYSTEM.md` tier numbering corrected. Usecase walkthroughs: initial pass missed `design` in all 4 `tier_2/02-audit.md` files, broken template paths in all 4 `tier_8/01-generation.md` files, `Prototype`/`Feature Design`/bare `Design` residue in `tier_5/01-generation.md`, and 1 of 6 "14 upstream documents" occurrences — all found in follow-up verification and fixed. `15-readme-standards.md` Node/npm residue fix confirmed in the standards doc itself, but had NOT propagated to the 4 files (1 whole-doc template + 3 section templates) duplicating the same example content — fixed. 6 duplicate TOC entries removed, `08-external-context` TOC entry added, audit report stale-rule descriptions updated, generation-template `feature_design` refs removed — all confirmed complete. 4 stray TODO placeholders in `16-product-guide-standards.md` (not previously claimed as fixed) also removed. |

---

## Fourth-Pass Discovery (New — found and fixed same session)

| # | Document | Severity | Status | Summary |
|---|----------|----------|--------|---------|
| 18 | [18-fourth-pass-pipeline-residue.md](./18-fourth-pass-pipeline-residue.md) | **MEDIUM** | ✅ **FIXED** | Found while verifying docs 15-17: 7 standards docs never covered by any prior pass (`01-vision`, `04-feature`, `05-architecture`, `07-engineering`, `08-external-context`, `13-implementation`, `16-product-guide`) referenced dropped domain "Feature Design(09)" as a real pipeline stage — bullet lists, relationship tables, and ASCII pipeline diagrams. `13-implementation-standards.md` also had `Prototype findings`/`Design principles` (domains 11, 06) in the same sentence. All removed/rephrased. |

---

## Fix Summary

### What Was Fixed in the First Pass

| Category | Count | Details |
|----------|-------|---------|
| Script file extensions (`*.rs`) | 12 files | 6 bash + 6 PowerShell scripts |
| Missing Rust scripts | 8 files | 4 bash + 4 PowerShell implementations |
| Audit rule ID prefixes | 8 files | Added domain prefixes |
| Duplicate section slot | 1 file | Renamed 10→11 |
| Invalid severity values | 7 files | `suggestion` → `warning` |
| Template base_dev residue | 3 files | TypeScript/Spring Boot/Python → Rust |
| Audit template wrong standard | 5 files | `02-vision` → `01-vision` |
| Engineering cross-references | 2 files | `rationale` → `tradeoffs` |
| tiers.yaml missing tier 4 | 1 file | Added engineering tier |
| Manifest requires_network | 2 files | `false` → `true` |
| Duplicate variable | 1 file | Removed redundant `$excludeDirs` |
| Cargo.toml parsing | 2 files | Added `cargo` branch to case/switch |
| Rust web framework patterns | 2 files | Added Actix/Rocket/Axum route detection |
| **Total fixes applied** | **54** | |

### What Was Already Fixed Before This Pass

| Item | Status |
|------|--------|
| `06-design/`, `09-feature-design/`, `11-prototype/` directories in audit/ | Already deleted |
| Semantic audit stubs (10/11/12) in 07-engineering | Already deleted |
| `unsafe_guidelines.yaml` severity (critical/2.0) | Already correct |
| `cargo-audit` manifest location (03-security) | Already correct |
| SYSTEM.md domain_tiers block | Already present |
| CONTRIBUTING.md | Already exists |
| migration-guide.md domain mapping | Already expanded |
| policy.yaml Rust entries | Already has 6 entries |
| lint-standards manifest executable | Already specified |
| 00-domain-relationships.md Rust relationships | Already added |

### What Was Fixed in the Third Pass (2026-07-16)

| Category | Count | Details |
|----------|-------|---------|
| Script npm→Rust defaults | 8 files | build-succeeds.sh/.ps1, lint-standards.sh/.ps1, lint-pass.sh/.ps1, artifact-exists.sh/.ps1 |
| Script correctness bugs | 3 files | cargo-fmt.sh exit code, crate-dependency-graph.sh set -e, unsafe-code-scan.sh quoting |
| Schema/output field mismatches | 4 files | cargo-audit, crate-dependency-graph, cargo-fmt, unsafe-code-scan schemas |
| Manifest missing fields | 4 files | requires_network, depends_on, timeout_seconds for 4 schemas |
| Dead policy entry | 1 file | cargo-clippy→lint-standards in policy.yaml |
| Audit YAML dropped-domain refs | 3 files | impl-doc-004, impl-sec-gen-005, ft-doc-008 |
| Audit YAML optional sections | 3 files | 05-change_request_plan, 04-refactor_plan, 06-enhancement_plan |
| Slot collisions renamed | 3 files | 04-feature/11, 01-vision/05, 15-readme/05 |
| Invalid target_domain values | 5 files | feature_technical→feature-technical, external→null, testing_strategy→test_strategy |
| Deleted orphaned files | 4 files | 16-product-guide/04,05 + semantic/16-product-guide/04, semantic/10-feature-technical/18,19 |
| Dropped-domain refs in standards | 1 file | 10-feature-technical-standards.md (~15 refs + section removed) |
| SYSTEM.md tier numbering | 1 file | Renumbered tiers 4-7 → 5-8 |
| Template base_dev residue | 2 files | 07-engineering.md (TypeScript→Rust), 01-vision.md (bad metrics fixed) |
| Generation template feature_design refs | 4 files | Removed from 04-feature and 08-external-context templates |
| Audit report template stale rules | 3 files | ft-doc-008, impl-sec-gen-005, impl-doc-004 descriptions updated |
| Usecase walkthrough fixes | 19 files | Removed dropped domains, fixed template paths, corrected doc counts |
| Standards TOC fixes | 7 files | Removed 6 duplicate entries, added 1 missing entry |
| Standards dropped-domain cleanup | 2 files | 10-feature-technical (B1), 15-readme (B11) Node/npm residue |
| **Total fixes applied** | **~80 files** | |

### What Was Fixed in the Second Pass (2026-07-16)

| Category | Count | Details |
|----------|-------|---------|
| Standards TOC entries added | 6 files | 08-external-context already had its entry |
| YAML rule-ID indentation artifact | 9 files | `-     id:` → `- id:` |
| `plan/core/tiers.yaml` duplicate Tier 4 | 1 file | Removed bogus `tier: 4 domains: [engineering]` block |
| Leftover dropped-domain files deleted | 25 files | `audit/semantic/document/`, `templates/generation/document/`, `templates/audit/**`, `script/{ubuntu,windows}/` — for 06-design, 09-feature-design, 11-prototype |
| `12-qa` Design(06)→Feature-Technical(10) re-point | 12 files | Standards doc, 2 section templates, 2 whole-doc templates, semantic audit doc+section, 3 report templates |
| `13-implementation` dropped-domain inputs removed | 5 files | Standards doc + 4 templates: Feature Design(09)/Prototype(11)/Design(06) removed or replaced with Feature Technical(10) |
| `plan/usecase/*` Tier 4 (Prototype) walkthrough removed | 20 files | 4 `tier_4/` dirs deleted; `design`/`feature-design` rows removed from tier_2/tier_3; dangling "Tier 4" reference fixed to "Tier 5" |
| eng-doc-004 rewritten | 1 file | error/mandatory → warning/optional; added Rust-ecosystem exceptions list |
| Ownership-over-GC principle added | 1 file | Philosophy addendum |
| Missing relationship IDs added | 2 files | crate_architecture, trait_design, crate_implementation, error_implementation |
| **Total additional fixes** | **~76 files touched** | |

### Remaining Open (deferred, low priority)

| Item | Priority | Effort |
|------|----------|--------|
| Header structure normalization (Structure A vs B, ~20 files) | Low | Medium — no confirmed tooling reads the missing fields |
| Template metadata leak in 04-feature | Low | Low — wrap in comments |
| Philosophy addendum buried at end of file rather than near the top | Low | Low — stylistic only |
| `calculation/` has no per-domain weight mechanism | Low | Unknown — would need engine-level design work, not a content fix |

### Remaining Open (engine feature requests — not fixable in YAML)

| Item | Priority | Effort |
|------|----------|--------|
| STD-001: `scope: collection` for per-domain metrics | Medium | Requires MCP engine feature request |
| STD-004: `match: word_boundary` for `keyword_absence` checks | Medium | Requires MCP engine feature request |

---

## Summary Statistics

| Category | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| CRITICAL bugs | 2 | 2 | 0 |
| HIGH severity bugs | 4 | 4 | 0 |
| MEDIUM severity gaps | 3 | 3 | 0 |
| MEDIUM improvements | 8 | 8 | 0 |
| Suggestions | 7 | 7 | 0 |
| Second-pass bugs (new) | 6 | 6 | 0 |
| **Pass 1+2 subtotal** | **30** | **30** | **0 (4 low-priority items deferred, see above)** |
| Third-pass bugs (doc 15, audit YAML) | 9 | 9 | 0 (STD-001/004 are GAPS, not bugs — engine feature requests) |
| Third-pass bugs (doc 16, scripts — incl. 4 CRITICAL) | 13 | 13 | 0 (header normalization suggestion — low, not a bug) |
| Third-pass bugs (doc 17, templates/standards) | 14 | 14 | 0 |
| Third-pass gaps (docs 15-17: STD-001, STD-004, GAP-3 semantic_type spelling) | 3 | 0 | 3 (2 engine requests + 1 low-priority) |
| Third-pass optimizations/suggestions (docs 15-17, cosmetic) | 9 | 0 | 9 (cosmetic, no functional impact) |
| Fourth-pass discovery (doc 18, pipeline residue in 7 files) | 1 | 1 | 0 |
| **Grand total** | **79** | **67** | **12 (2 engine requests + 4 low-priority + 1 low-priority gap + 9 cosmetic)** |

**Bottom line:** all 37 bugs found across the third-pass audit (docs 15-17) plus the fourth-pass discovery (doc 18) are now genuinely fixed and independently re-verified — a follow-up verification pass caught 13 fixes that were incomplete or subtly wrong on the first attempt (see the "Last updated" note above for the full list) and corrected them, and a final sanity sweep caught one more systemic issue (Feature-Design-domain pipeline residue in 7 standards docs never covered by any prior pass) and fixed it too. Combined with pass 1+2's 30 fixed bugs, that's 67 of 79 total findings fixed. The 12 remaining are all non-bugs: 2 engine-level feature requests (STD-001 `scope: collection`, STD-004 `word_boundary` matching) that cannot be fixed in YAML content, 5 low-priority deferrals (header normalization, template metadata leak, philosophy addendum placement, per-domain weights, `product_context` semantic_type spelling), and 9 cosmetic optimization/suggestion notes with no functional impact.
