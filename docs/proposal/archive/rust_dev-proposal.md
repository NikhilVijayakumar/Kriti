# Rust Dev Standard Issues — Proposal

Issues found in `E:\Python\Pitha\docs\limitation\samgraha\standard-issues\README.md`.
Analyzed against `E:\Python\Kriti\samgraha\system\rust_dev\`.

---

## Analysis Summary

| ID | Verdict | Severity | Status | Root Cause |
|----|---------|----------|--------|------------|
| STD-001 | **Acknowledged** | Medium | **Engine feature request** | YAML scope field lacks collection-level semantics |
| STD-002 | **Acknowledged** | Medium | **Fixed** | Optional section checks fire unconditionally |
| STD-003 | **Acknowledged — reclassified** | **High** | **Fixed** | rust_dev YAML references dropped domains (prototype) |
| STD-004 | **Acknowledged** | Low | **Engine feature request** | `keyword_absence` uses substring matching without word boundaries |
| STD-005 | **Found during analysis** | High | **Fixed** | Additional prototype references in feature-technical and generation_plan |

---

## STD-001: Architecture Standard Has Collection-Level Checks

**Status:** Acknowledged
**Severity:** Medium → **keeps Medium**
**Domain:** Architecture

### What the Issue Claims

`arch-doc-rust-001` verifies `crate_architecture` section exists but fires on every architecture document. If there are 9 architecture docs, 8 produce false positives.

### Verification

Checked `system/rust_dev/audit/deterministic/document/05-architecture.yaml:99-109`:

```yaml
- id: arch-doc-rust-001
  description: "Crate Architecture required"
  condition: "document contains the crate_architecture section"
  evidence:
    type: section_presence
    required_semantic_types:
      - crate_architecture
```

The file-level `scope: document` (line 4) means this check runs per-document. The `crate_architecture` semantic type is defined in `documentation-standards/05-architecture-standards.md` as a required section — but required at collection level (at least one architecture doc must have it), not per-document.

**Confirmed.** The check definition lacks a mechanism to distinguish "must exist in at least one document" from "must exist in every document."

### Root Cause

The YAML schema has no `scope: collection` concept. The `scope` field at file level (`document` vs `section`) controls evaluation granularity, but there is no per-check scope override for collection-level requirements.

### Fix Required

Two options:

**Option A — Add `scope` field to individual checks (recommended):**

```yaml
checks:
  - id: arch-doc-rust-001
    scope: collection  # Fires once across all docs in domain
    semantic_type: crate_architecture
```

This requires MCP engine support for `scope: collection` on individual checks.

**Option B — Restructure into a separate collection-level YAML file:**

Move collection-level checks to `audit/deterministic/collection/05-architecture.yaml` with `scope: collection` at file level. Document-level checks stay in `document/05-architecture.yaml`.

### Implementation Status

**Not fixed — requires MCP engine change.** Filed as engine feature request. The YAML schema needs a `scope` field on individual checks to support collection-level evaluation.

---

## STD-002: Implementation Standard Requires Optional Sections That Create False Positives

**Status:** Acknowledged
**Severity:** Medium → **keeps Medium**
**Domain:** Implementation

### What the Issue Claims

Optional sections (Change Request Plan, Refactor Plan, Enhancement Plan) have checks that fire on all documents, creating false positives when a document doesn't include those sections.

### Verification

Checked `system/rust_dev/audit/deterministic/section/13-implementation/05-change_request_plan.yaml:9-19`:

```yaml
- id: implementation-sec-change_request_plan-001
  description: "Change Request Plan section exists"
  condition: "document has a section with semantic_type = 'change_request_plan'"
  evidence:
    type: section_presence
    semantic_type: "change_request_plan"
```

The `scope: section` at file level means this check runs per-section. But the check fires per-document: if the document has no `change_request_plan` section, the check still fires and reports a finding.

The documentation standard (`13-implementation-standards.md:475-483`) lists Change Request Plan as optional:

| Section | Required |
|---------|----------|
| Generation Plan | ✓ |
| Security Fix Plan | ✓ |
| Change Request Plan | (empty = optional) |
| Refactor Plan | (empty = optional) |
| Enhancement Plan | (empty = optional) |

**Confirmed.** Optional section checks use `severity: error` and `mandatory: true` with no optionality flag.

### Root Cause

The YAML schema has no `optional` or `condition` field to skip checks when a section is legitimately absent. Every `section_presence` check fires unconditionally.

### Fix Required

**Option A — Add `optional: true` flag to check definitions:**

```yaml
- id: implementation-sec-change_request_plan-001
  optional: true  # Skip if section not in document scope
  evidence:
    type: section_presence
    semantic_type: "change_request_plan"
```

When `optional: true`, the check should:
- Pass (score=1.0, no finding) if section is absent
- Fire normally if section exists but is empty/malformed

**Option B — Use `severity: info` for optional section existence checks:**

Lower severity so optional section absence doesn't block domain ceiling.

### Implementation Status

**Fixed.** Changes made to three section-level YAML files:

| File | Check ID | Change |
|------|----------|--------|
| `section/13-implementation/05-change_request_plan.yaml` | `implementation-sec-change_request_plan-001` | `mandatory: true` → `false`, `severity: error` → `warning`, `weight: 1.5` → `0.5` |
| `section/13-implementation/04-refactor_plan.yaml` | `implementation-sec-refactor_plan-001` | Same changes |
| `section/13-implementation/06-enhancement_plan.yaml` | `implementation-sec-enhancement_plan-001` | Same changes |

Content checks (rule 002) in each file remain `mandatory: true` — if a section IS present, it must have content.

---

## STD-003: Implementation Standard Requires Upstream Docs That May Not Exist

**Status:** Acknowledged — **reclassified from Low to High**
**Domain:** Implementation
**Additional finding:** rust_dev YAML references `prototype` domain which is **dropped from the profile**.

### What the Issue Claims

Implementation standard requires upstream docs from Feature Technical, Security, Build, and QA domains. These may not exist in all projects.

### Verification

Checked `system/rust_dev/audit/deterministic/document/13-implementation.yaml:49-64`:

```yaml
- id: impl-doc-004
  description: "Document derives from required sources"
  condition: "document references upstream Feature Technical, Engineering, and Prototype documents"
  evidence:
    type: cross_reference
    expected:
      - domain: feature-technical
        direction: derives_from
      - domain: engineering
        direction: derives_from
      - domain: prototype
        direction: derives_from
```

**Critical finding:** `prototype` is listed as a required upstream source. But `SYSTEM.md:7` explicitly drops it:

```toml
dropped_from_base = ["06-design", "09-feature-design", "11-prototype"]
```

The `prototype` domain does not exist in the rust_dev profile. This check **guarantees** a finding on every implementation document — it is structurally impossible to satisfy.

Additionally, `feature-technical` is tier_3 and may not exist in simpler projects. The check treats it as mandatory.

### Root Cause

The YAML was likely copied from `base_dev` without removing references to dropped domains. The MCP engine does not validate that `expected.domain` values exist in the active profile.

### Fix Required

**Immediate — remove `prototype` from `impl-doc-004`:**

```yaml
- id: impl-doc-004
  evidence:
    type: cross_reference
    expected:
      - domain: feature-technical
        direction: derives_from
      - domain: engineering
        direction: derives_from
      # prototype removed — dropped from rust_dev profile
```

**Also check section-level references.** `impl-sec-gen-005` in `section/13-implementation/01-generation_plan.yaml:61-73` also references `prototype`:

```yaml
- id: impl-sec-gen-005
  description: "Generation plan references prototype"
  evidence:
    type: cross_reference
    expected:
      - domain: prototype
        direction: derives_from
```

This must also be removed or made conditional.

**Long-term — add profile-aware domain validation:**

The MCP engine should reject `expected.domain` values that don't exist in the active profile's domain list.

### Implementation Status

**Fixed.** Changes made:

| File | Check ID | Change |
|------|----------|--------|
| `document/13-implementation.yaml` | `impl-doc-004` | Removed `domain: prototype` from `expected` list |
| `section/13-implementation/01-generation_plan.yaml` | `impl-sec-gen-005` | Replaced `prototype` reference with `security` domain cross-reference |

Also updated condition text and messages to remove "Prototype" mentions.

---

## STD-004: Vision Standard Has Literal Keyword Matching

**Status:** Acknowledged
**Severity:** Low → **keeps Low**
**Domain:** Vision (affects all domains using `keyword_absence`)

### What the Issue Claims

`keyword_absence` uses substring matching. "aspires" doesn't satisfy "aspiration". "pipelines" triggers "pip" absence check.

### Verification

Checked `system/rust_dev/audit/deterministic/section/01-vision/09-success_criteria.yaml:27-33`:

```yaml
evidence:
  type: keyword_absence
  categories:
    - programming_languages
    - frameworks
    - libraries
```

The `keyword_absence` type references categories (`programming_languages`, `frameworks`, etc.) which are defined elsewhere. These categories contain keyword lists. The MCP engine performs substring matching against these lists.

Searched the codebase: no `word_boundary`, `match_mode`, or regex support exists in the YAML schema for `keyword_absence`.

**Confirmed.** "pipelines" → contains "pip" → false positive on absence check. "aspires" → contains "asp" (if "asp" is in the list) → possible false positive.

### Root Cause

`keyword_absence` was designed for simplicity — substring matching is fast and covers most cases. But it fails on:
- Words containing tech keywords as substrings (`pipelines` → `pip`)
- Morphological variants (`aspires` → `aspiration`)

### Fix Required

**Option A — Add `match` field to keyword definitions (recommended):**

```yaml
evidence:
  type: keyword_absence
  categories:
    - programming_languages
  match: word_boundary  # Default: substring (backwards compatible)
```

**Option B — Use regex patterns in categories:**

Allow categories to contain regex patterns instead of plain strings:

```yaml
keywords:
  - pattern: "\\bpip\\b"
  - pattern: "\\baspiration\\b"
```

**Option C — Pre-expand keyword lists (least invasive):**

Add inflected forms to keyword lists:
- `pip` → also block `pipelines`, `pipeline`, `piping`
- `asp` → also block `aspires`, `aspired`

This is a band-aid and doesn't scale.

### Implementation Status

**Not fixed — requires MCP engine change.** Filed as engine feature request. The `keyword_absence` evidence type needs a `match` field supporting `word_boundary` mode.

---

## Additional Issue Found During Analysis

### STD-005: rust_dev References Dropped Domains in Multiple Checks

**Severity:** High (same root cause as STD-003)
**Domain:** Multiple

During analysis, `prototype` domain references were found in:

| File | Check ID | Reference |
|------|----------|-----------|
| `document/13-implementation.yaml` | `impl-doc-004` | `domain: prototype` |
| `section/13-implementation/01-generation_plan.yaml` | `impl-sec-gen-005` | `domain: prototype` |

Both must be fixed when addressing STD-003.

### Implementation Status

**Fixed.** Additional change made:

| File | Check ID | Change |
|------|----------|--------|
| `document/10-feature-technical.yaml` | `ft-doc-008` | Removed `"prototype"` keyword, added `"verified"` keyword, updated message |

---

## Proposed Fix Order

| Priority | Issue | Effort | Impact | Status |
|----------|-------|--------|--------|--------|
| 1 | STD-003 (+ STD-005) | Low | Eliminates guaranteed false findings | **Fixed** |
| 2 | STD-002 | Medium | Eliminates optional section false positives | **Fixed** |
| 3 | STD-001 | High | Requires MCP engine change for `scope: collection` | **Engine feature request** |
| 4 | STD-004 | Medium | Requires MCP engine change for `match` mode | **Engine feature request** |

**STD-003** was fixed first — it was a data bug (wrong domain references) fixed by editing YAML files. **STD-002** was fixed by making optional section checks non-mandatory. **STD-001** and **STD-004** require MCP engine changes and are filed as engine feature requests.
