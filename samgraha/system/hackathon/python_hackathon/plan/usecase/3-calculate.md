# Use-case 3 — Calculate

**Script**: `run_reporting.py [--mode {det,sem,both}]`

**Inputs**:
- Use-case 2a gate passed (required)
- Use-case 2b data as-of-now (whatever exists, no gate)
- `calculation/aggregation/domain/*.yaml`

**Action**: `get_all_scores_as_dict()` -> `run_z_adjustment()` -> `build_leaderboard()`

**Completion criteria**:
- `build_leaderboard()` output contains exactly one entry per team registered in use-case 1
- Every entry has non-null `final_score`
- For every domain the team has any audit data for, non-null `z_score`/`adjusted_score`

**Verify script**: `verify_usecase_3_calculate.py --standard python_hackathon`
- Re-runs or loads persisted calculation
- Diffs team list against `standard_participants`
- Checks no None/missing numeric field
- Exits 1 + names specific team/domain/field if missing

**Z-score population rule**: Teams with zero audit data for a domain are included with raw_score=0.0 (see loop.yaml).
