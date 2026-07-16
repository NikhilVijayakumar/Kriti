# Suggestions — python_hackathon

Quality improvements to bring implementation closer to proposal intent.

---

## SUG-001 — Create standard.yaml
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Not needed. Standards in documentation-standards/.

## SUG-002 — Create calculation/relative/ YAML
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Not needed. Calculation in Python for accuracy.

## SUG-003 — Create calculation/normalization/ YAML
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Not needed. Calculation in Python for accuracy.

## SUG-004 — Create calculation/validation/ YAML and script validation
- **Severity:** HIGH
- **Status:** ✅ **FIXED** — Created `calculation/validation/scoring_validation.yaml` with 12 validation rules and `script/validate_scores.py`.

## SUG-005 — Fix template score scales /20 → /150
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Not needed. /20 is correct final scale.

## SUG-006 — Resolve semantic median vs mean inconsistency
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Updated all 10 semantic ensemble YAMLs from median to mean. Now consistent with script and proposal.

## SUG-007 — Add MLflow rule to MLOps deterministic YAML
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `mlp-002` (MLflow configuration exists) to 06-mlops.yaml.

## SUG-008 — Add docker-compose rule to Infrastructure YAML
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `inf-003` (Docker Compose configuration exists) to 01-infrastructure.yaml.

## SUG-009 — Add missing relationships to tiers.yaml
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added 3 missing relationships to tiers.yaml.

## SUG-010 — Remove stale "Feature" reference
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Changed `Feature (Implicit via Runtime)` to `Runtime` in 00-domain-relationships.md.

## SUG-011 — Add prompt_version/standard_version to semantic audit schema
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `metadata_fields` block to all 10 semantic audit YAMLs with model_identifier, provider, prompt_version, execution_timestamp, standard_version.

## SUG-012 — Add more deterministic rules to Engineering domain
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added 3 new rules: linter config (eng-003), type checker config (eng-004), pre-commit hooks (eng-005). Total now 5 rules.

## SUG-013 — Remove hardcoded Windows path from verify_standard.py
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Replaced with `Path(__file__).resolve().parent.parent`.

## SUG-014 — Add coverage percentage extraction to audit_testing.py
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `--cov=.` and `--cov-report=json:-` when pytest-cov available. Extracts coverage.totals.percent_covered from JSON report.

## SUG-015 — Add standard_version to deterministic audit YAMLs
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `standard_version: "1.0"` to all 10 deterministic audit YAMLs.

## SUG-016 — Create fixes/ and generation/ stub directories
- **Severity:** LOW
- **Status:** ✅ **CLOSED** — Not needed. Hackathon audit only.
