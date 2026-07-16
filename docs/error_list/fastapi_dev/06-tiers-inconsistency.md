# fastapi_dev — Gap Analysis: Tiers Inconsistency

**Category:** Gaps / Correctness  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

The updated `plan/core/tiers.yaml` correctly removes `design` and `feature-design` from the tiers. However, a subtle inconsistency was introduced: **Tier 4 was not re-numbered**. The proposal states:

| Tier | fastapi_dev |
|------|-------------|
| 1 | vision, philosophy |
| 2 | security, feature, architecture, engineering, external-context |
| 3 | feature-technical |
| 4 | prototype |
| 5 | implementation |
| 6 | qa |
| 7 | build |
| 8 | readme, product-guide |

The current `tiers.yaml` has `prototype` at Tier 4, `implementation` at Tier 5, etc. This is **correct per the proposal**, but the `00-domain-relationships.md` traceability chain diagram was rewritten showing:

```
Tier 3 ── Feature Technical
Tier 4 ── Prototype
Tier 5 ── Implementation
```

However, the `00-domain-relationships.md` prose Tier table says:

> **Tier 4 — Validation.**
> `11-prototype`

But then the **Machine-Readable Format** YAML inside `00-domain-relationships.md` reads:

```yaml
tiers:
  - tier: 3
    domains: [feature-technical]
  - tier: 4
    domains: [prototype]
  - tier: 5
    domains: [implementation]
```

This is actually correct and consistent. However, the issue is with **`00-domain-relationships.md` still containing the heading** `**Tier 5 — Realization (draft, not yet registered).**` — in the prose Tier table, the tier numbering jumps from Tier 4 to Tier 5 without explaining that Tier 4 is Prototype (which was previously labeled differently in `base_dev`). This is a readability issue that could confuse future maintainers.

---

## Gap 1 — Tier 3 in fastapi_dev Contains Only One Domain

In `base_dev`, Tier 3 was `[feature-design, feature-technical]`. In `fastapi_dev`, Tier 3 is now just `[feature-technical]`. The `00-domain-relationships.md` correctly reflects this, but the **plan/core/tiers.yaml** `note:` field still says "Transcribed from 00-domain-relationships.md" — which is fine. However, the note should ideally call out the delta from `base_dev` so maintainers understand why the tier structure differs.

**Fix Required:**
- Add a `diff_from_base_dev: true` note or comment block in `tiers.yaml` documenting what was removed and why.

---

## Gap 2 — `00-domain-relationships.md` Authoring Order Table Numbering Is Inconsistent

In `00-domain-relationships.md`, the Tiered Authoring Order tables reference file numbers that don't map cleanly to the new tier structure:

```markdown
**Tier 5 — Realization (draft, not yet registered).**

| # | File | Derived From |
|---|------|--------------|
| 12 | `13-implementation-standards.md` | ...
```

The `#` column shows `12` but the file is `13-implementation-standards.md`. This mirrors the numbering from `base_dev` where `12-qa` and `13-implementation` are intentionally cross-numbered (QA at tier 6 despite being numbered 12, implementation at tier 5 despite being numbered 13). This is a known quirk, but it should be **explicitly documented as intentional** to prevent confusion.

**Fix Required:**
- Add a note to the Tiered Model section explaining that the `NN-` prefix on filenames reflects the final authored order, not the tier number, and that QA (12) is authored at Tier 6 after Implementation (13).

---

## Gap 3 — `prototype` Relationship to `feature-technical` Missing in Relationships Table

In `base_dev`, prototype validates both `feature-design` and `feature-technical`. In `fastapi_dev`, `feature-design` is dropped, but `prototype` should still validate `feature-technical`. The current `00-domain-relationships.md` relationship table includes this:

```
| prototype | validates | feature-technical |
```

This is correct. However, the `plan/core/tiers.yaml` relationships list is also correct. **No action needed here** — this was properly handled. Logging for completeness.
