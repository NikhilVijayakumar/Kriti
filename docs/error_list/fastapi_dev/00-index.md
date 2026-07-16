# fastapi_dev — Review Index

**Review Date:** 2026-07-15  
**System Reviewed:** `E:\Python\Kriti\samgraha\system\fastapi_dev`  
**Proposal Reviewed:** `E:\Python\Kriti\docs\fastapi_dev-proposal.md`

---

## Overview

This index summarizes all findings from the cross-review of the `fastapi_dev` proposal against its actual implementation. Findings are split into **Gaps** (correctness issues that must be fixed), **Improvements** (things that should be improved for quality), and **Suggestions** (future work or enhancements).

---

## Gaps — Must Fix

| # | Document | Severity | Summary |
|---|----------|----------|---------|
| 1 | [01-dropped-domain-residue.md](./01-dropped-domain-residue.md) | **HIGH** | `script/mapping.yaml`, `script/schema/`, and `audit/deterministic/document/` still contain files/references to dropped domains `06-design` and `09-feature-design` |
| 2 | [02-stub-templates.md](./02-stub-templates.md) | **HIGH** | All 8 new FastAPI-specific generation templates are single-line placeholder stubs — no structure, no examples, no guidance |
| 3 | [03-audit-rule-stubs.md](./03-audit-rule-stubs.md) | **HIGH** | The 3 new semantic audit rule files are minimal 2–3 line stubs. Missing: criterion IDs, severity levels, rationale, remediation. Also missing: async pattern, response model, and API auth audit files |
| 4 | [04-standards-not-integrated.md](./04-standards-not-integrated.md) | **MEDIUM** | Backend-specific content appended to documentation-standards is not in Tables of Contents, has no structural rule references, doesn't follow Template+Examples+Guidance pattern |
| 5 | [05-deterministic-audit-not-updated.md](./05-deterministic-audit-not-updated.md) | **MEDIUM** | Dropped domain YAMLs still in `audit/deterministic/document/`. Relationship YAMLs reference dropped domains. No FastAPI-specific rules added to kept domain YAMLs |
| 6 | [06-tiers-inconsistency.md](./06-tiers-inconsistency.md) | **MEDIUM** | Minor: tiers.yaml lacks a `diff_from_base_dev` note; `00-domain-relationships.md` should clarify intentional cross-numbered file ordering |

---

## Improvements — Should Fix

| # | Document | Severity | Summary |
|---|----------|----------|---------|
| 7 | [07-improvements-and-optimizations.md](./07-improvements-and-optimizations.md) | **MEDIUM** | `script/policy.yaml` needs FastAPI-specific check overrides; `script/mapping.yaml` needs new FastAPI checks wired in; deterministic YAMLs need FastAPI-specific severity weights; system needs an identifier/orientation file |

---

## Suggestions — Nice to Have

| # | Document | Severity | Summary |
|---|----------|----------|---------|
| 8 | [08-additional-suggestions.md](./08-additional-suggestions.md) | **LOW-MEDIUM** | External ref isolation check; CHANGELOG.md; migration guide; broken `09-feature-design-standards.md` cross-links in existing docs; prototype domain rethink for API context; canonical feature folder tree in template |

---

## Priority Order for Fixes

```
Priority 1 (Correctness): #1 → Clean up dropped domain residue
Priority 2 (Usability):   #2 → Expand stub templates to full content
Priority 3 (Coverage):    #3 → Expand audit stubs + add missing audit files
Priority 4 (Integration): #4 → Integrate backend sections properly into standards
Priority 5 (Completeness):#5 → Update deterministic audit YAMLs
Priority 6 (Maintenance): #6 → Tier notes and tiers.yaml diff annotation
Priority 7 (Quality):     #7 → Optimizations (policy.yaml, mapping.yaml, weights)
Priority 8 (Future):      #8 → Suggestions (isolation check, CHANGELOG, migration guide)
```

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| HIGH severity gaps | 3 | ❌ Open |
| MEDIUM severity gaps | 3 | ❌ Open |
| Improvement items | 6 | ⚠️ Open |
| Suggestion items | 7 | 💡 Future |
| **Total findings** | **19** | |
