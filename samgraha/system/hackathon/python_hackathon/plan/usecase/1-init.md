# Use-case 1 — Init

**Script**: `run_hackathon.py` (startup path)

**Inputs**:
- `.env` `PYTHON_HACKATHON_TEAMS_JSON` path
- `teams.json` content

**Action**: `get_conn()` creates/opens DB + schema; `_sync_teams()` registers any team from `teams.json` not already in `standard_participants`.

**Completion criteria**:
1. DB file exists and is openable
2. Tables `standard_participants`, `standard_domain_scores`, `standard_narratives` exist
3. Every `team_name` in `teams.json` has exactly one matching row in `standard_participants` for this `standard`

**Verify script**: `verify_usecase_1_init.py --standard python_hackathon`
- Exits 0 + prints "PASS" if all criteria met
- Exits 1 + lists missing teams otherwise
