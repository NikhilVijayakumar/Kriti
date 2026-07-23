# Use-case 6 — Calculate

**Status: NOT YET IMPLEMENTED.** No `calculate` script exists, no
`calculate` usecase is registered in `standard.yaml`. This document
specifies the intended shape (`base_academic-data-pipeline-proposal.md`
§5, §10), not a built usecase — `run_full_workflow.py`'s Phase 8 loop
already calls `steps_of(steps, "calculate")`, finds an empty list, and
silently no-ops.

**Script (planned)**: `calculate.py` (deterministic, single step)

**Inputs (planned)**:
- `calculation/summary/{final_score,score_bands,trend}.yaml`
- `calculation/validation/scoring_validation.yaml`
- Latest `academic_semantic_runs` row per (paper, domain, model) —
  `MAX(run_number)`, not an average across history
- Deterministic audit results, once `calculation/deterministic/*` exists
  (also not yet built — see `domains/*.md`'s "Expected Evidence
  (Deterministic)" sections, which specify what these checks should be,
  not built as scripts)

**Action (planned)**: Runs `scoring_validation.yaml`'s bounds/mandatory
pre-checks, then `final_score_v1`/`score_bands_v1`/`trend_v1` per the
existing (already-identical-across-systems) formula files. Writes one row
to `academic_score_history` per run — per domain, plus one with
`domain_id IS NULL` for the whole-paper `final_score`. Never updates a
prior row (matches `academic_semantic_runs`'s append-only pattern, §5 of
the data-pipeline proposal).

**Completion criteria (planned)**:
- One new `academic_score_history` row per structural domain + one
  whole-paper row, per run
- `trend_delta` populated against the immediately prior snapshot for the
  same (paper, domain)

**Verify script (planned)**: `verify_usecase_6_calculate.py --standard base_academic --paper-id <id>`

**Rule**: Runs after usecase 4 (`semantic-audit`) has scored every
domain at least once. Re-runnable at any time — recalculating from
already-stored scores, no re-audit needed.
