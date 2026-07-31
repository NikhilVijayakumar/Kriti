# Use-case 5d-methodology — Humanize (Semantic) — methodology

**Depends on**: `5c-humanize-det-methodology`

**Script**: `humanize-sem` (domain=methodology)

**Inputs**: methodology's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to methodology — ensure design decisions read naturally, technical descriptions are clear.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_methodology.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
