# Gaps — python_hackathon

Things declared in the proposal but missing from the implementation.

---

## GAP-001 — standard.yaml manifest missing
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Standards are defined in `documentation-standards/` following the same template as all other systems.

## GAP-002 — pillars/ directory missing
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Pillars are considered as domains and are added to `documentation-standards/`.

## GAP-003 — calculation/relative/ YAML missing
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Calculation logic is intentionally kept in Python (`statistics.py`) for accuracy.

## GAP-004 — calculation/normalization/ YAML missing
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Normalization logic is intentionally kept in Python (`leaderboard.py`) for accuracy.

## GAP-005 — calculation/validation/ YAML missing
- **Severity:** HIGH
- **Status:** ✅ **FIXED** — Created `calculation/validation/scoring_validation.yaml` with 12 validation checks (weight sum, score bounds, z-score cap, semantic bonus bounds, final score bounds, team/domain counts). Created `script/validate_scores.py` for validation execution. Added validation stage to loop.yaml with abort-on-failure.

## GAP-006 — loop.yaml missing workflow stages
- **Severity:** HIGH
- **Status:** ✅ **FIXED** — Updated loop.yaml: added `repository`, `validate` (with scoring_validation.yaml source and abort-on-failure), and `report` stages. Added `version: "1.0"`.

## GAP-007 — Global leaderboard template uses /20 not /150
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. /20 is correct final scale (150 is intermediate).

## GAP-008 — Team final summary template uses /20 not /150
- **Severity:** HIGH
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. /20 is correct final scale.

## GAP-009 — 00-domain-relationships.md references non-existent "Feature" domain
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Changed `Feature (Implicit via Runtime)` to `Runtime` in ASCII diagram.

## GAP-010 — tiers.yaml missing 3 relationships
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added 3 missing relationships: data-quality→informs→mlops, ai-explanations→validates→runtime, team-workflow→guides→engineering.

## GAP-011 — fixes/ directory missing
- **Severity:** MEDIUM
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Hackathon audit only, no fixes from our side.

## GAP-012 — generation/ directory missing
- **Severity:** MEDIUM
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Hackathon audit only, no generation from our side.

## GAP-013 — templates/prompts/ directory missing
- **Severity:** MEDIUM
- **Status:** ✅ **CLOSED** — Documentation error, not a real gap. Hackathon audit only, no generation from our side.

## GAP-014 — Semantic audit YAMLs missing execution metadata fields
- **Severity:** MEDIUM
- **Status:** ✅ **FIXED** — Added `metadata_fields` block (model_identifier, provider, prompt_version, execution_timestamp, standard_version) to all 10 semantic audit YAMLs.

## GAP-015 — No Pillar Aggregation YAML
- **Severity:** LOW
- **Status:** ✅ **CLOSED** — Not needed. Pillar aggregation handled at domain level.

## GAP-016 — No explicit "Repository" stage in loop.yaml
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added `repository` stage as first entry in loop.yaml.

## GAP-017 — audit_model_artifact.py uses file size as VRAM proxy
- **Severity:** LOW
- **Status:** ✅ **FIXED** — Added 4-tier memory detection: torch.cuda → torch CPU (physically installed memory) → psutil → file-size fallback. Logs which method was used. 12GB threshold preserved.
