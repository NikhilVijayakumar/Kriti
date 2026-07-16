# Optimizations — python_hackathon

Structural and performance improvements for future consideration.

---

## OPT-001 — Unify scoring scale across all artifacts
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — By design. /20 is correct final scale.

## OPT-002 — Make validation a hard gate in loop.yaml
- **Severity:** HIGH
- **Status:** ✅ **FIXED** — Added validation stage to loop.yaml with `on_failure: abort`. Created scoring_validation.yaml with 12 checks.

## OPT-003 — Centralize scoring formulas into YAML
- **Severity:** MEDIUM
- **Status:** ✅ **CLOSED** — Not needed. Calculation in Python for accuracy.

## OPT-004 — Add cross-reference validation to verify_standard.py
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Rewrote verify_standard.py: now checks every domain in weights.yaml has matching files in all 5 expected directories (audit/deterministic, audit/semantic, calculation/aggregation, calculation/deterministic, calculation/semantic).

## OPT-005 — Standardize naming: team_workflow vs team-workflow
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Standardized all YAML values from underscore to hyphen: team_workflow→team-workflow, data_quality→data-quality, ai_explanations→ai-explanations. Grepped to confirm zero remaining underscore matches.

## OPT-006 — Replace semantic ensemble median with mean
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Updated all 10 semantic ensemble YAMLs from median to mean. Consistent with script and proposal.

## OPT-007 — Add total_rules/total_weight fields to YAML headers
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `total_rules` and `total_weight` to all 10 deterministic audit YAMLs.

## OPT-008 — Add version tracking to loop.yaml
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `version: "1.0"` to loop.yaml.
