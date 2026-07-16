# rust_dev — Gap Analysis: Dropped Domain Residue

**Category:** Gaps / Correctness  
**Severity:** High  
**Date:** 2026-07-15

---

## Summary

The `rust_dev` implementation was supposed to drop `06-design`, `09-feature-design`, **and** `11-prototype` completely. While `documentation-standards/` files and `audit/deterministic/document/` YAMLs were deleted, a large amount of artefacts from those three domains still exist in the `audit/deterministic/section/` and other subdirectories. These are orphaned structures that could confuse audit tooling or LLM agents.

---

## Gap 1 — `audit/deterministic/section/` Still Contains All Three Dropped Domain Subdirectories

**Directory:** `audit/deterministic/section/`

The following three subdirectories fully exist and contain real section-level YAML rule files:

| Directory | File Count | Sample Contents |
|---|---|---|
| `audit/deterministic/section/06-design/` | 6 files | `01-design_principles.yaml`, `02-ux_principles.yaml`, `03-accessibility.yaml`, `04-purpose.yaml`, `05-constraints.yaml`, `06-traceability.yaml` |
| `audit/deterministic/section/09-feature-design/` | 7 files | `01-user_experience.yaml`, `02-workflow.yaml`, `03-states.yaml`, `04-purpose.yaml`, `05-non_goals.yaml`, `06-constraints.yaml`, `07-traceability.yaml` |
| `audit/deterministic/section/11-prototype/` | 6 files | `01-scope.yaml`, `02-mock_apis.yaml`, `03-data_model.yaml`, `04-purpose.yaml`, `05-constraints.yaml`, `06-traceability.yaml` |

These files contain UI/UX-specific rules (`ux_principles`, `mock_apis`, `user_experience`) that have zero relevance to a pure systems engineering methodology.

**Fix Required:**
- Delete `audit/deterministic/section/06-design/` entirely.
- Delete `audit/deterministic/section/09-feature-design/` entirely.
- Delete `audit/deterministic/section/11-prototype/` entirely.

---

## Gap 2 — `script/mapping.yaml` Comment Block Still References "16 Domains"

**File:** `script/mapping.yaml` (line 13)

The mapping file's header comment still reads:
```yaml
  # Category C: generic cross-document checks (all 16 domains)
```

`rust_dev` only has **13 domains**. This stale comment will mislead developers and audit tools that rely on documentation.

**Fix Required:**
- Update the comment to read `# Category C: generic cross-document checks (all 13 active domains)`.

---

## Gap 3 — `documentation-standards/02-philosophy-standards.md` Contains Broken Cross-Link

**File:** `documentation-standards/02-philosophy-standards.md` (line 523)

Contains a `Related Standards` section with this broken link:
```markdown
- [Design Standard](06-design-standards.md) - guided by Philosophy
```

`06-design-standards.md` was deleted from `documentation-standards/`. This is a dead link.

**Fix Required:**
- Remove the broken `06-design-standards.md` entry from the Related Standards section in `02-philosophy-standards.md`.

---

## Gap 4 — `audit/deterministic/document/13-implementation-relationships.yaml` Comment References Prototype

**File:** `audit/deterministic/document/13-implementation-relationships.yaml` (line 8)

The file header comment reads:
```yaml
# Implementation derives from Feature Technical + Engineering + Prototype.
```

`Prototype` was a dropped domain in `rust_dev`. This is a stale architectural comment that misrepresents the system's domain topology.

**Fix Required:**
- Update the comment to read: `# Implementation derives from Feature Technical + Engineering.`

---

## Gap 5 — Semantic Audit Section Directories Have Numbered File Conflicts

**Directory:** `audit/semantic/section/07-engineering/`

The directory contains **both** the original base_dev files AND newly created Rust-specific files, with **conflicting slot numbers**:

| Slot 09 | Slot 10 | Slot 11 | Slot 12 |
|---|---|---|---|
| `09-ownership_patterns.md` (NEW — 1222 bytes, proper) | `10-async_patterns.md` (NEW — 1103 bytes, proper) | `11-unsafe_guidelines.md` (NEW — 750 bytes, proper) | — |
| `09-security_standards.md` (OLD base_dev file) | `10-ownership_patterns.md` (OLD mini-stub — 207 bytes) | `11-async_patterns.md` (OLD mini-stub — 177 bytes) | `12-unsafe_guidelines.md` (OLD mini-stub — 211 bytes) |

The result is that slots 10–12 each contain TWO files: the older base_dev stubs (10–12) and the newly written versions (09–11). The OLD stubs at slots 10, 11, 12 are now dead duplicates that mask the correct files at 09, 10, 11. Any tool scanning by slot number will read the wrong file.

**Fix Required:**
- Delete `audit/semantic/section/07-engineering/10-ownership_patterns.md` (the 207-byte stub).
- Delete `audit/semantic/section/07-engineering/11-async_patterns.md` (the 177-byte stub).
- Delete `audit/semantic/section/07-engineering/12-unsafe_guidelines.md` (the 211-byte stub).
- Verify that `09-security_standards.md` is a valid base_dev file that should remain, or rename it to avoid collision.
