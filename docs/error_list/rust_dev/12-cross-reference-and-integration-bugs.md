# rust_dev — Bug Report: Cross-References, Tiers, and Integration Issues

**Category:** Bugs / Integration  
**Severity:** MEDIUM  
**Date:** 2026-07-15

---

## Summary

Multiple files reference non-existent targets, contain stale paths, or have structural gaps that break cross-file integration. These range from broken links to missing tier definitions.

---

## Bug 1 — 5 Audit Template Files Reference Wrong Standard Number

**Files (all on line ~4):**
- `templates/audit/summary/01-vision-report.md`
- `templates/audit/deterministic/document/01-vision-report.md`
- `templates/audit/deterministic/section/01-vision-report.md`
- `templates/audit/semantic/document/01-vision-report.md`
- `templates/audit/semantic/section/01-vision-report.md`

**Current reference:** `02-vision-standards.md`  
**Correct reference:** `01-vision-standards.md`

**Root cause:** Copy-paste from philosophy domain (02) when creating audit templates.

**Fix Required:**
- Change `02-vision-standards.md` to `01-vision-standards.md` in all 5 files.

---

## Bug 2 — `tiers.yaml` Missing Tier 4

**File:** `plan/core/tiers.yaml`

The tier structure jumps from tier 3 to tier 5. `SYSTEM.md` declares tier 4 as `07-engineering`, but `tiers.yaml` has no tier 4 entry.

**Fix Required:**
- Add tier 4 entry mapping to `07-engineering`.

---

## Bug 3 — `external-ref-isolation.manifest.yaml` Hardcoded Developer Path

**File:** `script/schema/external-ref-isolation.manifest.yaml` (line ~9)

Contains:
```yaml
- "E:\\\\Python\\\\"
```

This is a personal Windows path specific to one developer's machine. It will:
- False-positive on every other system
- Miss violations on the actual system if files move

**Fix Required:**
- Replace hardcoded path with a configurable parameter or repository-relative path.

---

## Bug 4 — `00-domain-relationships.md` Still Lists Dropped Domains as Active

**File:** `00-domain-relationships.md` (lines ~72-82)

The dependency table still has rows for `06-design` as an active domain with relationships to other domains.

**Fix Required:**
- Remove all `06-design` entries from the dependency table.

---

## Bug 5 — `migration-guide.md` Incomplete / Trailing Sentence

**File:** `migration-guide.md` (line ~30)

Current text trails off mid-thought:
```
and all feature-technical documents are moved from `feature-technical/` to the same
```

**Problem:** "the same" what? The sentence is incomplete.

**Fix Required:**
- Complete the sentence and expand the migration guide with domain mapping table.

---

## Bug 6 — Generation Templates Reference Non-Existent `*-relationships.yaml`

**Files:** All 16 `templates/generation/document/*.md` files

Each has a header line like:
```
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`
```

But `audit/deterministic/document/` contains only report `.md` files — no `*-relationships.yaml` files exist.

**Fix Required:**
- Either create the relationship YAML files, or remove the Relationships header from generation templates.

---

## Bug 7 — Wrong Cross-References in Engineering Templates

**File:** `templates/generation/section/07-engineering/01-guiding_principles.md` (line ~15)  
**File:** `templates/generation/section/07-engineering/02-rationale.md` (line ~14)

Both reference `philosophy / rationale` — but the Philosophy document's section is named `tradeoffs`, not `rationale`.

**Fix Required:**
- Change `philosophy / rationale` to `philosophy / tradeoffs` in both files.

---

## Bug 8 — `script/mapping.yaml` Header Says "16 Domains"

**File:** `script/mapping.yaml` (line ~13)

Comment reads: `# Category C: generic cross-document checks (all 16 domains)`  
Should read: `# Category C: generic cross-document checks (all 13 active domains)`

**Fix Required:**
- Update the comment to reflect 13 active domains.

---

## Bug 9 — Missing `generation/section/` for 3 Dropped Domains

**Directories missing:**
- `templates/generation/section/06-design/`
- `templates/generation/section/09-feature-design/`
- `templates/generation/section/11-prototype/`

The `generation/document/` templates exist for these domains but there are no standalone section templates. If any audit or generation tool expects section-level templates, it will fail.

**Fix Required:**
- Either create section templates for completeness, or remove the `generation/document/` templates for dropped domains.

---

## Bug 10 — `CONTRIBUTING.md` References Non-Existent "audit workflow" Section

**File:** `CONTRIBUTING.md` (line ~35)

States "see the audit workflow in CONTRIBUTING.md" but the file contains no such section.

**Fix Required:**
- Either add the audit workflow section or remove the reference.

---

## Summary

| # | Bug | Severity | Effort |
|---|-----|----------|--------|
| 1 | Wrong standard number in 5 audit templates | HIGH | 5 edits |
| 2 | tiers.yaml missing tier 4 | MEDIUM | 1 addition |
| 3 | Hardcoded developer path | HIGH | 1 edit |
| 4 | Dropped domains still in relationships | MEDIUM | Deletion |
| 5 | Incomplete migration guide sentence | LOW | 1 edit |
| 6 | Non-existent relationship YAML refs | MEDIUM | 16 edits or 16 creates |
| 7 | Wrong philosophy cross-reference | LOW | 2 edits |
| 8 | Stale "16 domains" comment | LOW | 1 edit |
| 9 | Missing section templates for dropped domains | MEDIUM | Decision needed |
| 10 | CONTRIBUTING.md broken self-reference | LOW | 1 edit |
