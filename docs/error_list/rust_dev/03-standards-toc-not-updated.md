# rust_dev — Gap Analysis: Standards Not Integrated in Table of Contents

**Category:** Gaps / Integration  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

The Rust-specific sections added to `documentation-standards/` files are fully absent from the **Table of Contents** in the majority of the standards files. An author using any of these standards as a guide will not see the Rust-specific sections listed in the TOC, and no tooling can auto-jump to them. The sections were appended at the end of each file but the TOC at the top was never updated to include them.

---

## Affected Files

The following audit checks each standards file's TOC against its actual Rust-specific section headings:

| File | Rust Section Added? | In TOC? | Status |
|------|---------------------|---------|--------|
| `01-vision-standards.md` | ✅ Systems Engineering Vision | ❌ Missing from TOC | **GAP** |
| `02-philosophy-standards.md` | ✅ Systems Philosophy Addendum | ❌ Missing from TOC | **GAP** |
| `03-security-standards.md` | ✅ Systems Security | ❌ Missing from TOC | **GAP** |
| `04-feature-standards.md` | ✅ Systems Feature Definition | ❌ Missing from TOC | **GAP** |
| `05-architecture-standards.md` | ✅ Crate Architecture, Trait Design | ❌ Missing from TOC | **GAP** |
| `07-engineering-standards.md` | ✅ Ownership Patterns, Async Patterns, Unsafe Guidelines | ❌ Missing from TOC | **GAP** |
| `08-external-context-standards.md` | ✅ Technology Categories | ❌ Missing from TOC | **GAP** |
| `10-feature-technical-standards.md` | ✅ Crate Implementation, Error Implementation | ✅ In TOC | OK |
| `12-qa-standards.md` | ✅ Property Testing, Benchmark Testing | ✅ In TOC | OK |
| `13-implementation-standards.md` | ✅ Crate Folder Structure | ✅ In TOC | OK |
| `14-build-standards.md` | ✅ Crate Publishing | ✅ In TOC | OK |
| `15-readme-standards.md` | ✅ Systems README Conventions | ✅ In TOC | OK |
| `16-product-guide-standards.md` | ✅ Development Workflow | ✅ In TOC | OK |

**7 out of 13 files** have Rust-specific sections that are NOT listed in their Table of Contents.

---

## Gap 1 — `01-vision-standards.md` TOC Does Not List "Systems Engineering Vision"

**Fix Required:**
- Add `- [Systems Engineering Vision](#systems-engineering-vision)` to the TOC in `01-vision-standards.md`.

---

## Gap 2 — `02-philosophy-standards.md` TOC Does Not List "Systems Philosophy Addendum"

**Fix Required:**
- Add `- [Systems Philosophy Addendum](#systems-philosophy-addendum)` to the TOC in `02-philosophy-standards.md`.

---

## Gap 3 — `03-security-standards.md` TOC Does Not List "Systems Security"

**Fix Required:**
- Add `- [Systems Security](#systems-security)` to the TOC in `03-security-standards.md`.

---

## Gap 4 — `04-feature-standards.md` TOC Does Not List "Systems Feature Definition"

**Fix Required:**
- Add `- [Systems Feature Definition](#systems-feature-definition)` to the TOC in `04-feature-standards.md`.

---

## Gap 5 — `05-architecture-standards.md` TOC Does Not List "Crate Architecture" or "Trait Design"

**Fix Required:**
- Add the following to the TOC in `05-architecture-standards.md`:
  ```
  - [Crate Architecture](#crate-architecture)
  - [Trait Design](#trait-design)
  ```

---

## Gap 6 — `07-engineering-standards.md` TOC Does Not List Any of the Three New Sections

**Fix Required:**
- Add the following to the TOC in `07-engineering-standards.md`:
  ```
  - [Ownership Patterns](#ownership-patterns)
  - [Async Patterns](#async-patterns)
  - [Unsafe Guidelines](#unsafe-guidelines)
  ```

---

## Gap 7 — `08-external-context-standards.md` TOC Does Not List "Technology Categories"

**Fix Required:**
- Add `- [Technology Categories](#technology-categories)` to the TOC in `08-external-context-standards.md`.

---

## Root Cause

The `integrate_rust_standards.py` script used a regex pattern to find the TOC block and append entries. The regex was:
```python
r'(## Table of Contents\n\n> \*(?:Deterministic rules|Structural rules).*?\*\n\n(?:- \[.*?\]\(#.*?\)\n)+)'
```

This pattern requires a specific format after the TOC heading (a `> *...*` directive block). Files 01–08 have a different TOC format (a plain bulleted list without the directive block), so the regex **did not match** and the TOC was silently not updated.
