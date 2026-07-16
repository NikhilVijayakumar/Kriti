# Third-Pass Audit — Standards Docs, Templates, Plan/Usecase Walkthroughs

**Review Date:** 2026-07-16 (third pass)
**Scope:** `documentation-standards/**`, `templates/**` (generation + audit, all 13 active domains), `plan/**` (core + usecase), `00-domain-relationships.md`, `SYSTEM.md`, `CHANGELOG.md`, `CONTRIBUTING.md`.

**Headline finding:** directory-level cleanup (dropped-domain files/folders) holds — no regression there. All residue found this pass is **prose/content-level**: standards text, report-template descriptions, and usecase walkthrough documents still describing the pre-drop (base_dev) domain set/numbering — harder to catch than a directory listing, and evidently outside every prior pass's grep patterns (which searched for domain names/numbers verbatim, not structural artifacts like tables, prerequisite lists, or "N upstream documents" counts).

---

## BUGS

### B1 — `documentation-standards/10-feature-technical-standards.md` still treats dropped domain "Feature Design(09)" as legitimate (~15 occurrences, entire section untouched by prior pass)
Doc 14's fix hit `13-implementation-standards.md` + 4 templates but missed this file entirely:
- Line 47: TOC entry `- [Feature Design Considerations](#feature-design-considerations)`
- Line 833: `Make the plan specific enough for Prototype to validate and Implementation to follow.`
- Line 953: `Feature Design is not a required input. It is considered only where user experience decisions directly influence architectural realization...`
- Line 1004: ASCII diagram box `Feature Design (optional)`
- Line 1013, 1044, 1057-1058, 1070, 1093, 1107, 1125, 1140, 1156: repeated "Feature Design"/"Prototype" mentions in Inputs/Relationships/Audit Rules/Common Mistakes
- Lines 1250-1263: entire `## Feature Design Considerations` section with UX examples (routing, accessibility, localization, offline behavior) — none apply to a UI-less Rust systems methodology.

**Fix:** delete the `## Feature Design Considerations` section + TOC entry, strip "Feature Design" from Inputs/Relationships/Audit Rules/Common Mistakes, replace "Prototype" mentions with plain "Implementation" (no substitute domain exists).

### B2 — `SYSTEM.md`'s `domain_tiers` block contradicts the authoritative tier source
**File:** `SYSTEM.md:12-19`:
```toml
[domain_tiers]
tier_3 = ["10-feature-technical"]
tier_4 = ["13-implementation"]
tier_5 = ["12-qa"]
tier_6 = ["14-build"]
tier_7 = ["15-readme", "16-product-guide"]
```
Authoritative source (`00-domain-relationships.md:143-150`, mirrored in `plan/core/tiers.yaml:14-23`) has no tier 4 (intentional gap after prototype dropped) and puts implementation at 5, qa at 6, build at 7, readme/product-guide at 8. SYSTEM.md was written before doc 14's tiers.yaml fix and never updated — asserts a tier 4 that doesn't exist, wrong numbering throughout.
**Fix:**
```toml
tier_3 = ["10-feature-technical"]
tier_5 = ["13-implementation"]
tier_6 = ["12-qa"]
tier_7 = ["14-build"]
tier_8 = ["15-readme", "16-product-guide"]
```

### B3 — All 4 `plan/usecase` Tier-2 walkthroughs still list dropped domain "design" + reference nonexistent template paths (base_dev numbering)
**Files:** `plan/usecase/{repo_existing,repo_new}/case_{1_no_documentation,2_has_documention}/tier_2/{01-generation,02-audit,03-fix}.md`

`01-generation.md` (e.g. `repo_new/case_1_no_documentation`) line 5: `**Domains:** security, feature, architecture, design, engineering, external-context`; line 24 Design bullet; line 35 `| design | templates/generation/document/07-design.md | Philosophy |`; line 48 lists Design in parallel execution order. `02-audit.md`'s per-domain table (lines 27-33) already has no `design` row — header/prose now inconsistent with its own table within the same file. `03-fix.md` lines 5, 39 same "design" residue.

Independent of "design": template paths use base_dev's pre-drop numbering, don't exist:
| Referenced (broken) | Actual file |
|---|---|
| `06-security.md` | `03-security.md` |
| `07-design.md` | *(dropped, no file)* |
| `08-engineering.md` | `07-engineering.md` |
| `15-external-context.md` | `08-external-context.md` |
| `16-readme.md` | `15-readme.md` |
| `17-product-guide.md` | `16-product-guide.md` |

Confirmed broken in `tier_2/01-generation.md` (all 4 use cases, 4 wrong paths each) and `tier_8/01-generation.md` (all 4, 2 wrong paths each).

**Fix:** remove "design" from all Domains headers/prose/table rows/execution-order sentence in all 12 tier_2 files; correct all 6 template paths across `tier_2/01-generation.md` (×4) and `tier_8/01-generation.md` (×4).

### B4 — `plan/usecase/*/tier_3/03-fix.md` still lists dropped domain "feature-design" (missed by prior "New Bug 6" fix)
**Files:** all 4 use cases' `tier_3/03-fix.md`, lines 5 (and 26 in the `case_1` variants):
```
**Domains:** feature-design, feature-technical
...
Once every domain in Tier 3 (feature-design, feature-technical) has final score...
```
Prior fix hit `01-generation.md`/`02-audit.md` in all 4 use cases but never `03-fix.md`.
**Fix:** change to `**Domains:** feature-technical` / `Once every domain in Tier 3 (feature-technical) has final score...` in all 4 files.

### B5 — `plan/usecase/repo_new/case_1_no_documentation/tier_5/01-generation.md` and `tier_6/01-generation.md` still list "Prototype"/"Feature Design" as upstream input
`tier_5/01-generation.md:27` `- **Prototype** — prototype plan, validation results`; line 33 references Prototype in the implementation row. `tier_6/01-generation.md:19` Feature Design bullet, line 21 Prototype bullet.
**Fix:** remove Prototype/Feature Design bullets and cross-reference from both files.

### B6 — `plan/usecase/repo_new/case_1_no_documentation/tier_3/01-generation.md` has collateral damage from domain-removal fix
- Missing `**Domains:**` header line entirely (every sibling tier file has one).
- Line 8 still lists "Design" as a completed Tier-2 domain.
- Line 20 Design bullet still present in Upstream Context.
- Table now has 1 row (feature-technical only) but line 38 still says "Two documents, one per domain" — should be "One document."
- Lines 33-35: `## Within-Tier Ordering` heading with blank body (ordering text describing feature-design vs feature-technical sequencing was deleted, no replacement).

**Fix:** add back `**Domains:** feature-technical` header; drop "Design" from line 8 and delete Design bullet at line 20; fix "Two documents" → "One document"; fill or delete the empty `## Within-Tier Ordering` section (e.g. "No ordering constraint — single domain in this tier.").

### B7 — `plan/usecase/*/tier_8/01-generation.md` says "all 14 upstream documents" but rust_dev has only 13 domains total (11 upstream to Tier 8)
All 4 use cases, 6 occurrences total ("all 14 upstream documents"). `SYSTEM.md` states `domains = 13`; tier 8 owns 2 (readme, product-guide), so upstream = 11, not 14 (base_dev residue: 16 total − 2 = 14, pre-drop).
**Fix:** change all 6 occurrences to "all 11 upstream documents".

### B8 — Audit report templates for `10-feature-technical`/`13-implementation` describe rule semantics that no longer match the already-fixed YAML rules, still name dropped "Prototype"
- `templates/audit/deterministic/document/10-feature-technical-report.md:119` — row still says `ft-doc-008 | ... reference Prototype as validation gate` but actual rule (`audit/deterministic/document/10-feature-technical.yaml:112-124`) was rewritten to a generic "document mentions validation" check with no Prototype reference.
- `templates/audit/deterministic/section/13-implementation-report.md:59` — says `impl-sec-gen-005: References Prototype Documentation scope or mock APIs`, but real rule (`section/13-implementation/01-generation_plan.yaml:61-72`) checks Security Documentation references, zero Prototype mention.
- `templates/audit/deterministic/document/13-implementation-report.md:76` — says `impl-doc-004: References upstream Feature Technical, Engineering, and Prototype documents`, but real rule (`document/13-implementation.yaml:49-62`) only expects feature-technical + engineering.

This is worse than stale prose — the rendered audit report describes checks the engine doesn't actually perform and references a domain that can't exist.
**Fix:** rewrite rule-description text in all 3 files to match actual current rule conditions.

### B9 — 4 generation section templates + 3 audit YAML rules declare relationships to dropped domain "feature_design"
- `templates/generation/section/04-feature/02-functional_requirements.md:14`, `06-outputs.md:14`
- `templates/generation/section/08-external-context/01-purpose.md:17`, `03-constraints.md:17`
- `audit/deterministic/document/08-external-context.yaml:78` (`ext-doc-005`, `domain: feature_design`)
- `audit/deterministic/section/04-feature/11-traceability.yaml:43` (`feat-sec-trace-003`)
- `audit/deterministic/section/08-external-context/05-traceability.yaml:32` (`ext-sec-trace-002`)

Same defect class as doc 14 Bug 4 (unfulfillable criterion naming a dropped domain), recurring unnoticed in 04-feature/08-external-context. (Cross-check: this overlaps BUG-6 in `15-third-pass-audit-checks.md` — same 3 YAML files, found independently by both audit agents; template-side residue in this doc is the additional new finding.)
**Fix:** remove `feature_design`/`design_rationale` rows from the 4 templates' Relationships tables and `domain: feature_design` entries from the 3 YAML rules.

### B10 — `[Standards Reference Standard](standards.md)` is a broken link in 12 of 13 `documentation-standards/*.md` files
Present in `01-vision`, `02-philosophy`, `04-feature`, `05-architecture`, `07-engineering`, `08-external-context`, `10-feature-technical`, `12-qa`, `13-implementation`, `14-build`, `15-readme`, `16-product-guide` standards docs (only `03-security-standards.md` lacks it). `standards.md` doesn't exist anywhere in the repo.
**Fix:** either create `documentation-standards/standards.md`, or remove the line from all 12 files.

### B11 — `documentation-standards/15-readme-standards.md`: "Correct" example blocks use Node.js/npm and JDK/Gradle, not Rust — whole file never touched by doc 10's fix
- Installation section (lines 461-480): Node.js 18/npm 9, `npm install @acme/scheduler`
- Build section (lines 531-545): JDK 17/Gradle 8.2+, `./gradlew build`, `build/libs/scheduler.jar`
- Development section (lines 798-817): `npm install`/`npm test`

Doc 10 fixed this exact defect class elsewhere (TypeScript→Rust, Spring Boot→Tokio/Axum, Python→Rust) but never audited `15-readme-standards.md`. Same content duplicated in `templates/generation/document/15-readme.md` (lines 298-303, 350, 549-555) and `templates/generation/section/15-readme/{08-installation,09-build,13-development}.md`.
**Fix:** replace with Rust equivalents (`rustup`/`cargo install`, `cargo build --release` → `target/release/...`, `cargo build`/`cargo test`) in all listed files.

### B12 — Whole-document generation templates duplicate base_dev-residue examples fixed only at section-level
- `templates/generation/document/07-engineering.md:243-245` — still "TypeScript Official Style Guide... ESLint configured via .eslintrc.cjs" (doc 10 Bug 1 fixed only the section template).
- `templates/generation/document/07-engineering.md:83-84` — still "Project Alpha uses Python 3.12+..." (doc 10 Bug 3 fixed only the section template).
- `templates/generation/document/01-vision.md:297-300` — still marks valid Rust metrics ("API response time under 200ms", "95% code coverage") as an "Incorrect example" (doc 10 Bug 6 fixed only the section template, which now has a 3rd genuinely-bad example; this whole-doc duplicate still has the original 2-item version).

**Fix:** apply doc 10's corrections to these whole-document templates too.

### B13 — Duplicated TOC entries for newly-added Rust addendum headings in 6 standards docs
| File | TOC line 1 | Duplicate TOC line | Actual heading |
|---|---|---|---|
| `01-vision-standards.md` | 7 | 39 | line 869 `## Systems Engineering Vision` |
| `02-philosophy-standards.md` | 7 | 33 | line 538 `## Systems Philosophy Addendum` |
| `03-security-standards.md` | 7 | 38 | line 733 `## Systems Security` |
| `04-feature-standards.md` | 7 | 44 | line 1225 `## Systems Feature Definition` |
| `05-architecture-standards.md` | 7-8 | 44-45 | lines 1039/1091 `## Crate Architecture` / `## Trait Design` |
| `07-engineering-standards.md` | 7-9 | 43-45 | lines 986/1031/1076 `## Ownership Patterns` / `## Async Patterns` / `## Unsafe Guidelines` |

Doc 14's TOC fix inserted new entries near the top but an original append-at-the-end pass apparently also ran/was never removed — each entry now appears twice pointing to the same anchor. New regression, not previously reported.
**Fix:** delete the second (later) occurrence in all 6 files.

### B14 — `documentation-standards/08-external-context-standards.md`: new Rust addendum heading missing from TOC (doc 03/14's "already fixed" claim wrong for this file)
Body has two near-duplicate H2 sections: line 812 `## Systems Technology Categories` (new Rust addendum: Tokio/Serde/anyhow/bindgen) immediately followed by line 822 `## Technology Categories` (pre-existing generic section). TOC line 7 only links to the pre-existing one — the new addendum has no TOC entry at all. Docs 03/14 confirmed "already had it," but that was about the pre-existing heading, not the new addendum.
**Fix:** add `- [Systems Technology Categories](#systems-technology-categories)` to the TOC.

---

## GAPS

### G1 — `documentation-standards/16-product-guide-standards.md` has 4 unresolved `<!-- TODO: Add content for this section. -->` placeholders
Lines 124, 187, 236, 311. Unlike the intentional `## Audit Fix` stub pattern used consistently across templates, these are inside the standards document body itself.
**Fix:** fill in the missing content, or replace with the `*(To be written by the domain expert...)*` pattern already used in `15-readme-standards.md`.

---

## OPTIMIZATIONS

### O1 — `templates/generation/document/05-architecture.md:105` "Incorrect" example still names Spring Boot instead of a Rust-relevant over-specific example
Not functionally broken (correctly labeled incorrect), but per doc 10's original intent a Rust-relevant example (e.g. Tokio/Axum/sqlx) would land the teaching point better than a Java stack (Apache Kafka/Spring Boot/PostgreSQL/AWS EKS/Kubernetes) in a Rust doc standard.

### O2 — Whole-document assembly templates (`templates/generation/document/*.md`) are a recurring blind spot for content fixes
B12 shows this in 3 places across at least 3 separate prior passes. Recommend one sweep comparing every whole-document template's inline Correct/Incorrect examples against its section-level counterpart.

---

## SUGGESTIONS

### S1 — Normalize fictional product example names (DataSync/CloudBridge/Project Alpha/Project Nova/Acme Scheduler) in one pass if ever revisited, rather than piecemeal — not currently confusing, just inconsistent.

### S2 — Normalize `**Domains:**` header presence across all `plan/usecase` tier stage files as a lint rule — this is the second review pass where a domain-removal edit silently dropped or left inconsistent a header/count line elsewhere in the same file (B6/B7).

---

## Summary

| Category | Count | Notes |
|---|---|---|
| BUGS | 14 | B1/B2 highest-value (whole standards file still describing a dropped domain as valid; SYSTEM.md self-contradicting the tier source of truth). B3-B7 show the `plan/usecase` domain-removal fix from doc 14 was materially incomplete. B10/B13/B14 are new TOC/link defects not reported in any prior pass. |
| GAPS | 1 | TODO markers in 16-product-guide-standards.md |
| OPTIMIZATIONS | 2 | Cosmetic/consistency, no functional impact |
| SUGGESTIONS | 2 | Process recommendations for future passes |
