# base_dev — Review Index

**Review Date:** 2026-07-20
**Implementation:** `E:\Python\Kriti\samgraha\system\base_dev`
**Trigger:** User audit of `plan/usecase` + `audit/deterministic` — questioned whether the pipeline is actually runnable end-to-end.

---

## Overview

`base_dev` has real, working scripts covering the entire pipeline — `scaffold.py`, `generate_structural_sections.py`, `validate.py`, `evaluate_rules.py`, `evaluate_semantic.py`, `calculate.py`, `analyze.py`, `report.py`, `visualize.py`, `report_html.py` — orchestrated end-to-end by `init.py` ("scaffold→structural→content→validate→calculate→report→fix"). And a complete set of use-case stage docs (96 files: 4 use cases × 8 tiers × 3 stages). But the stage docs describe **what** to run (which yaml/md file governs a domain) without ever naming **which script** executes it, in **what order**, or **with what CLI args** — `init.py` itself is never mentioned in `plan/`. Two features referenced by the plan layer — check-name script wiring, and the fix-generation handoff — are unbuilt/ambiguous, not missing docs. The DB layer (separate repo `E:\Python\samgraha`, schema at `schema/knowledge-hub/`) reserves a column for exactly the wiring GAP-002 needs, but its loader doesn't populate it either — the gap spans both repos.

**Result:** 5 gaps found. 0 fixed, 5 open.

---

## Gaps

| # | ID | Severity | Status | Summary |
|---|-----|----------|--------|---------|
| 1 | GAP-001 | **HIGH** | 🔴 **OPEN** | No usecase doc names the executor script for deterministic/semantic audit |
| 2 | GAP-002 | **HIGH** | 🔴 **OPEN** | 20 check-name scripts exist but zero audit rules reference them (`mapping.yaml` self-flagged placeholder) |
| 3 | GAP-003 | **HIGH** | 🔴 **OPEN** | Fix mechanism (`## Audit Fix` slot → regenerate) is an unfilled stub; `analyze.py` offers a second, undocumented fix-plan mechanism — unclear which is authoritative |
| 4 | GAP-004 | **MEDIUM** | 🔴 **OPEN** | `init.py` (the real 10-script orchestrator) is never mentioned in `plan/`; no doc spells out the full pipeline order + CLI chain |
| 5 | GAP-005 | **MEDIUM** | 🔴 **OPEN** | Cross-repo: `rules.script_check_id` column exists in DB schema for GAP-002's wiring but the loader never populates it; runtime persistence (generated docs/scores/fix-plans) unverified |

---

## Summary Statistics

| Category | Total | Closed | Fixed | Remaining |
|----------|-------|--------|-------|-----------|
| Gaps | 5 | 0 | 0 | **5** |

---

## Scope Note

GAP-001 and GAP-004 are pure documentation gaps — the scripts they'd reference already exist and work (including `init.py`, the already-built orchestrator for the whole chain), this is wiring/authoring only, mechanical and consistent across ~32 `02-audit.md` + `plan/core` files.

GAP-002, GAP-003, and GAP-005 are **not** documentation gaps — the underlying mechanism (rule→script wiring end-to-end, including the DB side; a single authoritative finding→fix-plan handoff) does not exist yet in code, on either side of the repo split. Fixing the docs to describe them without building them first would recreate the same false-complete claim this audit was raised to catch.
