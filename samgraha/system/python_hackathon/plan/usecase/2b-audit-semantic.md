# Use-case 2b — Audit, Semantic

**Script**: Agent-driven sessions

**Inputs**:
- `audit/semantic/document/*.yaml` rubrics
- Whichever agent/model session runs them

**Action**: One `standard_domain_scores` row per (team, domain, model) scored so far.

**Completion criteria — two tiers**:
- *Minimum bar (unblocks use-case 3)*: at least 1 semantic row per domain per team
- *Full bar (informational only, never blocks)*: every configured model has scored every domain every team

**Verify script**: `verify_usecase_2b_audit_semantic.py --standard python_hackathon [--team <name>]`
- Reports both tiers per team
- Exit code reflects minimum bar only (0 = every domain has >=1 model per team)
- Full-ensemble number reported but never gates

**Rule**: Starts after 2a for that team. Accumulates indefinitely. No "complete" end-state.
