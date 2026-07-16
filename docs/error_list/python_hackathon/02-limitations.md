# Limitations — python_hackathon

Things implemented but incomplete, broken, or contradictory vs the proposal.

---

## LIM-001 — Validation stage completely absent
- **Severity:** HIGH
- **Status:** ✅ **FIXED** — Created `calculation/validation/scoring_validation.yaml` with 12 checks, `script/validate_scores.py`, and validation stage in loop.yaml with abort-on-failure.

## LIM-002 — loop.yaml cap:20 conflicts with weights.yaml final_scale:150
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — By design. /20 is final scale, 150 is intermediate.

## LIM-003 — Semantic ensemble: median (YAML) vs mean (script) vs proposal says "Mean"
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Updated all 10 semantic ensemble YAMLs from `median_score = median(scores)` to `mean_score = mean(scores)`. Now consistent with script and proposal.

## LIM-004 — Semantic bonus decomposition differs from proposal
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Semantic ensemble YAMLs now use mean (matching script and proposal). The per-domain decomposition in leaderboard.py is the correct implementation (proposal describes concept, script implements it). YAML and script now consistent.

## LIM-005 — Infrastructure audit: only 2 rules for weight-8 domain
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `inf-003` (Docker Compose configuration exists) with glob check for docker-compose.yaml/yml, compose.yaml/yml.

## LIM-006 — MLOps audit: only 1 rule (DVC), MLflow absent from YAML
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `mlp-002` (MLflow configuration exists) with glob check for mlruns/, mlflow.ini, mlflow.yaml, mlprojects/.

## LIM-007 — Engineering audit: only 2 rules for weight-12 domain
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added 3 new rules: `eng-003` (Python linter config), `eng-004` (Type checking config), `eng-005` (Pre-commit hooks). Total now 5 rules.

## LIM-008 — Templates stale (scale mismatch, missing sections)
- **Severity:** MEDIUM
- **Status:** ✅ **CLOSED** — By design. Templates are correct with /20.

## LIM-009 — verify_standard.py only validates YAML syntax
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Rewrote verify_standard.py: now validates YAML syntax + cross-references (checks every domain in weights.yaml has matching files in all 5 expected directories). Prints formatted summary report with PASS/FAIL verdict.

## LIM-010 — verify_standard.py hardcoded Windows path
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Replaced hardcoded `E:\Python\Kriti\...` with `Path(__file__).resolve().parent.parent`. Uses pathlib throughout.

## LIM-011 — audit_testing.py requires optional pytest-json-report plugin
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `_check_module_installed()` to detect optional plugins before pytest runs. `--json-report` only added if plugin installed. `--cov` only added if pytest-cov available. Falls back to `-q` summary parsing with clear logging of what was collected vs skipped.
