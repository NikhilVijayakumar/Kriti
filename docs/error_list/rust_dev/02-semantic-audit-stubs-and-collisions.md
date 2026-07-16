# rust_dev — Gap Analysis: Semantic Audit Rule Stubs (Slot Collision & Mini-Stubs)

**Category:** Gaps / Content Quality  
**Severity:** High  
**Date:** 2026-07-15

---

## Summary

The three most critical Rust-specific semantic audit files — **Ownership Patterns**, **Async Patterns**, and **Unsafe Guidelines** — exist in TWO forms each: a properly written version at slot `N` and a useless 3-line mini-stub at slot `N+1`. The mini-stubs appear to be the original `base_dev` placeholders that were not deleted when the new Rust-specific files were created. Any audit tool that loads files sequentially by slot will read the wrong (mini-stub) version.

---

## Affected Files — The Slot Collision Problem

| Proper File (Rust-specific) | Bytes | Mini-Stub (stale base_dev) | Bytes |
|---|---|---|---|
| `07-engineering/09-ownership_patterns.md` | 1,222 | `07-engineering/10-ownership_patterns.md` | 207 |
| `07-engineering/10-async_patterns.md` | 1,103 | `07-engineering/11-async_patterns.md` | 177 |
| `07-engineering/11-unsafe_guidelines.md` | 750 | `07-engineering/12-unsafe_guidelines.md` | 211 |

---

## Gap 1 — `10-ownership_patterns.md` (207-byte stub) is a Functional Duplicate

**File:** `audit/semantic/section/07-engineering/10-ownership_patterns.md`

**Current content (full file):**
```markdown
# Ownership Rules

- **Check:** Are references favored over cloning where lifetimes clearly permit it?
- **Check:** Is shared mutability (e.g., `Arc<Mutex<T>>`) avoided unless architecturally justified?
```

This is a minimal 2-bullet list with no severity, rationale, anti-patterns, or remediation. The slot `09-ownership_patterns.md` has a proper multi-criterion rule set. This file must be removed.

**Fix Required:**
- Delete `audit/semantic/section/07-engineering/10-ownership_patterns.md`.

---

## Gap 2 — `11-async_patterns.md` (177-byte stub) is a Functional Duplicate

**File:** `audit/semantic/section/07-engineering/11-async_patterns.md`

**Current content (full file):**
```markdown
# Async Rules

- **Check:** Is the event loop protected from blocking operations?
- **Check:** Are `Send` and `Sync` bounds correctly applied across async trait boundaries?
```

Missing: severity, rationale, remediation, anti-patterns. The newly created `10-async_patterns.md` supersedes this.

**Fix Required:**
- Delete `audit/semantic/section/07-engineering/11-async_patterns.md`.

---

## Gap 3 — `12-unsafe_guidelines.md` (211-byte stub) is a Functional Duplicate

**File:** `audit/semantic/section/07-engineering/12-unsafe_guidelines.md`

**Current content (full file):**
```markdown
# Unsafe Rules

- **Check:** Is `unsafe` used only where truly necessary?
- **Check:** Is every `unsafe` block preceded by a `// SAFETY:` comment?
```

Missing: severity (`critical`), rationale on `#![forbid(unsafe_code)]`, enforcement strategies.

**Fix Required:**
- Delete `audit/semantic/section/07-engineering/12-unsafe_guidelines.md`.

---

## Gap 4 — `09-security_standards.md` Is a Misplaced Base_Dev Artefact

**File:** `audit/semantic/section/07-engineering/09-security_standards.md`

This file sits in the `07-engineering` semantic section directory but appears to be a base_dev artefact carrying generic security content. There is a dedicated `03-security/` semantic section directory for security rules.

**Fix Required:**
- Verify whether `09-security_standards.md` was inherited from `base_dev` or generated for `rust_dev`.
- If it duplicates content already in `audit/semantic/section/03-security/`, delete it.
- If it contains unique content, move it to `audit/semantic/section/03-security/` under an appropriate slot name.

---

## Required Standard for Semantic Audits

Compare against a proper semantic audit in `07-engineering/09-ownership_patterns.md` — it contains:
- A section heading with domain and criterion ID
- `**Severity:**` declaration
- `**Context & Rationale:**` block
- `**Audit Check:**` with specific questions
- `**Anti-patterns:**` with concrete negative examples
- `**Remediation:**` with fix guidance

All Rust-specific semantic audit files must follow this same pattern.
