# Use-case 2a — Audit, Deterministic

**Script**: `run_hackathon.py --deterministic-only`

**Inputs**:
- Every team registered per use-case 1
- `audit/deterministic/document/*.yaml` rules
- `audit_*.py` runners

**Action**: Per team, per domain with a runner script: evaluate rules, upsert one `standard_domain_scores` row (`kind='deterministic'`).

**Completion criteria**:
- For team(s) in scope, every domain that has an `audit_*.py` script (all 10) has exactly one `kind='deterministic'` row in `standard_domain_scores`

**Verify script**: `verify_usecase_2a_audit_deterministic.py --standard python_hackathon [--team <name>]`
- Reports `N/10` domains per team
- Exits 0 only if `10/10` for every team in scope
- Exits 1 + lists missing (team, domain) pairs otherwise

**Rule**: Always runs FIRST per team, before 2b.
