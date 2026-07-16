# Third-Pass Audit — Audit YAML Rules (`audit/deterministic/**`, `audit/semantic/**`)

**Review Date:** 2026-07-16 (third pass)
**Scope:** `E:\Python\Kriti\samgraha\system\rust_dev\audit\deterministic\{document,section}\**` and `audit\semantic\{document,section}\**`, all 13 active domains.
**Method:** Read all prior history (00-index + 01-14), then read every file in scope. Every finding confirmed by directly reading cited file/lines.

---

## STD-00x Verification Summary

| Item | Status |
|---|---|
| STD-001 (`scope: collection`) | **Still not fixed.** `audit/deterministic/document/05-architecture.yaml:99-109` (`arch-doc-rust-001`) still `scope: document` (file-level, line 4), `mandatory: true`, no per-check scope override anywhere in `audit/`. Confirmed engine-feature-request gap, not a regression. |
| STD-002 (optional sections) | **Broadly fixed** across `10-feature-technical`, `07-engineering`, `16-product-guide` (mostly) — all pair `mandatory: false` with `severity: info/warning` matching each domain's standards doc. **Exception: BUG-4 below** — `16-product-guide` has a contradictory duplicate. |
| STD-003/005 (dropped domain residue) | **Not fully fixed — new residue found (BUG-6).** Prose-pattern greps ("Feature Design(09)") were clean, but the bare YAML value `domain: feature_design` still appears in 3 files — never matched by the prior sweep's search pattern. |
| STD-004 (`keyword_absence` word-boundary) | **Still not fixed.** All 57 usages use plain `categories:` substring matching. No `match`/`word_boundary`/regex field exists. Confirmed engine-feature-request gap, not a regression. |

---

## BUGS

### BUG-1 — Duplicate slot `11` in `04-feature` (regression from prior "fix")
`04-feature\11-systems_feature_definition.yaml` and `04-feature\11-traceability.yaml` collide. Doc 11 renamed an old slot-10 collision to 11 without checking 11 was already taken by `traceability`.
**Fix:** renumber `11-systems_feature_definition.yaml` → `12-systems_feature_definition.yaml` (slot 12 is free).

### BUG-2 — Duplicate slot `05` in `01-vision`
`01-vision\05-target_audience.yaml` and `01-vision\05-systems_vision.yaml` collide. `documentation-standards\01-vision-standards.md` links both at lines 224 and 871. `05-systems_vision.yaml` is the appended Rust-specific addendum (added per doc 07/14) and reused a taken slot instead of the next free one.
**Fix:** renumber to `11-systems_vision.yaml`, update cross-link at `01-vision-standards.md:871`.

### BUG-3 — Duplicate slot `05` in `15-readme` + stale bare rule-ID prefix
`15-readme\05-key_capabilities.yaml` and `15-readme\05-systems_readme.yaml` collide. `05-systems_readme.yaml` also uses bare `sec-systems-readme-001` prefix (the exact bug class doc 11 fixed in 8 other files but missed here), and old Structure-B header (`domain`/`section`, no `standard_id`/`scope`).
**Fix:**
```yaml
system_id: samgraha-documentation
domain: readme
section_type: systems_readme
standard_id: documentation-standards
scope: section
kind: deterministic
rules:
  - id: readme-sec-systems-readme-001
    ...
```
Renumber file to `16-systems_readme.yaml`.

### BUG-4 — `16-product-guide`: `product_context`/`public_contract` each defined twice with contradictory mandatory/severity
Old files `04-product_context.yaml` (`pg-sec-context-*`) / `05-public_contract.yaml` (`pg-sec-contract-*`) say `mandatory: false` / `severity: warning` ("Missing optional..."). New files `07-product_context.yaml` (`product-guide-sec-product_context-*`) / `08-public_contract.yaml` say `mandatory: true` / `severity: error` ("Missing required...") — and it's the **new** files the standards doc actually links to (`16-product-guide-standards.md` lines 193, 242, 585).

`16-product-guide-standards.md:357-371` Required Sections table marks both as **optional** (blank Required column) — so the linked file contradicts its own standard. Same defect class as original STD-002, reintroduced via duplication. Matching semantic-side duplicates also exist: `semantic/section/16-product-guide/04-product_context.md` (thin generic stub) vs `07-product_context.md` (rich Rust rubric).

Also: `07-development_workflow.yaml` still has bare-prefix id `sec-development-workflow-001`.

**Fix:** Delete `04-product_context.yaml`, `05-public_contract.yaml`, and their semantic `.md` counterparts (orphaned pre-Rust duplicates, unreferenced by standards doc). Change `07-product_context.yaml`/`08-public_contract.yaml` to match documented optionality:
```yaml
- id: product-guide-sec-product_context-001
  message: "Missing optional 'Product Context' section"
  severity: warning
  weight: 0.5
  mandatory: false
```
(same for `public_contract-001`). Fix `07-development_workflow.yaml` id → `product-guide-sec-development_workflow-001`.

Note: standards table spells semantic types `product-context`/`public-contract` (hyphen); all YAML/`.md` files use `product_context`/`public_context` (underscore) — see GAP-3.

### BUG-5 — Semantic slot collision `18`/`19` in `10-feature-technical`: orphaned base_dev rubrics, no deterministic/generation counterpart, no standards-table row
`semantic/section/10-feature-technical/18-data_governance.md` and `19-observability.md` collide with the legitimate Rust files `18-crate_implementation.md`/`19-error_implementation.md`. No `data_governance`/`observability` section exists anywhere in `documentation-standards\10-feature-technical-standards.md`'s Required Sections table (lines 798-822) or in `deterministic/section/10-feature-technical/`. Same defect class doc 02 already fixed once in `07-engineering`.
**Fix:** delete both orphaned `.md` files, or if intentionally kept, renumber to free slots (20, 21) + add deterministic counterpart + standards-table row.

### BUG-6 — Dangling `domain: feature_design` (dropped domain) — STD-003/005 not fully closed
3 files still reference the dropped `09-feature-design` domain via the bare YAML identifier `feature_design` (no parenthetical "(09)"), which the prior sweep's prose-pattern grep never matched:
- `audit/deterministic/section/04-feature/11-traceability.yaml:43`
- `audit/deterministic/document/08-external-context.yaml:78` (`ext-doc-005`)
- `audit/deterministic/section/08-external-context/05-traceability.yaml:32`

Same guaranteed-fail defect as original STD-003 — no `09-feature-design` documents are ever generated in rust_dev, so these checks can never pass.
**Fix:** remove `domain: feature_design` entries + "Feature Design" condition-prose mentions from all 3 files, mirroring the `impl-doc-004` STD-003 fix.

### BUG-7 — `target_domain: feature_technical` (underscore) invalid — should be `feature-technical` (hyphen)
3 occurrences use the wrong separator, inconsistent with the canonical `feature-technical` used everywhere else (confirmed self-declared in `10-feature-technical-relationships.yaml:2` and used correctly by `05-architecture-relationships.yaml`, `07-engineering-relationships.yaml`, `13-implementation-relationships.yaml`):
- `audit/deterministic/document/04-feature-relationships.yaml:27`
- `audit/deterministic/document/08-external-context-relationships.yaml:20`
- `audit/deterministic/document/08-external-context-relationships.yaml:34`

**Fix:** change all 3 to `target_domain: feature-technical`.

### BUG-8 — Dangling `target_section: testing_strategy` — section doesn't exist
`audit/deterministic/document/04-feature-relationships.yaml:28` (`feat-acceptance-criteria-derives-feature-technical`) targets `testing_strategy`, which is not among `10-feature-technical`'s 19 real sections. Closest match is `12-qa/01-test_strategy.yaml`'s `test_strategy` (different domain, different spelling).
**Fix:**
```yaml
  - id: feat-acceptance-criteria-derives-feature-technical
    from_section: acceptance_criteria
    type: derives_from
    target_domain: qa
    target_section: test_strategy
    owner: section
```
(or repoint to `feature-technical`/`feature_specification` if that was the real intent.)

### BUG-9 — `target_domain: external` is not a valid domain id
`audit/deterministic/document/08-external-context-relationships.yaml:38-43` (`ext-traceability-traces-external`) invents a fake domain `external` (real domain is `external-context`, self-declared in same file). Intent is "traces to a source outside the system" — `01-vision-relationships.yaml:93` already handles this correctly via explicit `target_domain: null` / `target_section: null` (`vis-traceability-no-upstream`).
**Fix:**
```yaml
  - id: ext-traceability-traces-external
    from_section: traceability
    type: traceable_to
    target_domain: null
    target_section: null
    owner: section
```

---

## GAPS

### GAP-1 — STD-001 remains unimplemented (confirmed, not a regression)
No `scope: collection` mechanism anywhere in `audit/`. Engine-level change required, per proposal.

### GAP-2 — STD-004 remains unimplemented (confirmed, not a regression)
`keyword_absence` (57 usages) has no `match`/`word_boundary`/regex field. Engine-level change required.

### GAP-3 — `semantic_type` spelling inconsistency (hyphen vs underscore) in `16-product-guide`
Standards doc (`16-product-guide-standards.md:367-368`) documents `product-context`/`public-contract` (hyphen); every rule file uses `product_context`/`public_contract` (underscore). Whichever the heading→semantic_type compiler emits, one side silently never matches, defeating `section_presence` checks. Needs verification against the compiler, then a one-line correction to whichever side is wrong.

---

## OPTIMIZATIONS

### OPT-1 — No repo-wide guard against slot-number collisions
Same bug class (two files sharing a numeric slot prefix) found and fixed once for `07-engineering` (doc 02), now recurs 6 more times (`01-vision`, `04-feature`, `15-readme`, `16-product-guide` ×2, `10-feature-technical` semantic). A one-line CI check — `ls <domain-dir> | sed -E 's/^([0-9]+)-.*/\1/' | sort | uniq -d` per section directory — catches all of these immediately.

### OPT-2 — No repo-wide guard against invalid `domain:`/`target_domain:` values
BUG-6, BUG-7, BUG-9 are all `domain:`/`target_domain:` values not matching any of the 13 active domain ids in `SYSTEM.md`. A validation step (diff all `domain:`/`target_domain:` values against the 13 canonical ids, allow `null`) would have caught dropped-domain residue permanently — prose greps used in prior passes missed non-prose YAML-identifier residue.

---

## SUGGESTIONS

### SUG-1 — Turn OPT-1/OPT-2 into an actual pre-commit/CI script
Third pass finding the same two bug classes (slot collision, dangling domain reference) — a lightweight `grep`/`sort`/`uniq` script under `script/` is cheap insurance against a fourth recurrence.

### SUG-2 — Reconcile `16-product-guide-standards.md` semantic_type spelling with YAML files (GAP-3) in the same pass as BUG-4, since both touch the same two sections.
