# Fourth-Pass Discovery — Feature Design(09) Pipeline Residue in 7 Standards Docs

**Discovered:** 2026-07-16, during final sanity sweep after verifying docs 15-17's fix claims.
**Status:** ✅ FIXED (same session).

## What was found

None of the 3 prior audit passes (docs 01-14) or the third-pass audit (docs 15-17) scoped a check across *all* `documentation-standards/*.md` files for the dropped `09-feature-design` domain — doc 14/17's fixes only targeted `13-implementation-standards.md` and `10-feature-technical-standards.md`. A final grep swept the whole tree and found "Feature Design" referenced as a **real, structural pipeline stage** — not incidental prose — in 7 other standards docs that had never been audited for this:

- `01-vision-standards.md` — Outputs list bullet, Relationships table row
- `04-feature-standards.md` — Prohibited Content rationale table, Outputs consumer list (×2), 2 ASCII pipeline diagrams (`Vision → Feature → Feature Design → Architecture → ...`), Relationships table row, Usage prose, Prohibited Content table row ("UI implementation | Belongs to Feature Design")
- `05-architecture-standards.md` — Inputs prose, ASCII pipeline diagram
- `07-engineering-standards.md` — Non-Goals list, Out of Scope list, ASCII pipeline diagram
- `08-external-context-standards.md` — Outputs list, ASCII pipeline diagram, Relationships table row
- `13-implementation-standards.md` — Summary prose, which also had `Prototype findings` and `Design principles` in the same sentence (dropped domains 11 and 06 respectively — same defect, same line)
- `16-product-guide-standards.md` — Inputs list ("Feature / Feature Design")

All of these treated a domain that cannot exist in `rust_dev` (dropped per `SYSTEM.md`'s `dropped_from_base = ["06-design", "09-feature-design", "11-prototype"]`) as a real pipeline stage between Feature and Architecture — the same defect class as everything fixed in docs 01-17, just never swept across this file set.

## Fix applied

All "Feature Design" pipeline references removed from all 7 files: bullet points, table rows, ASCII pipeline diagrams collapsed to skip the dropped stage, and prose rephrased to name only domains that exist in `rust_dev`. The `13-implementation-standards.md` summary sentence also had `Prototype findings` and `Design principles` removed (dropped domains 11 and 06).

One occurrence was left intentionally: `10-feature-technical-standards.md:105` — `"Don't: ...conflate with Architecture or Feature Design"` — a negative-example "don't confuse this domain with X" instruction, already assessed in doc 17 (B1) as harmless incidental phrasing rather than residue.

## Verification

Repo-wide grep for `Feature Design`, `Prototype findings`, `Design principles` across `documentation-standards/*.md` returns only the one intentional line above.
