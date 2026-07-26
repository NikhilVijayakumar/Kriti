# Use-case 5d-introduction — Humanize (Semantic) — introduction

**Depends on**: `5c-humanize-det-introduction`

**Script**: `humanize-sem` (domain=introduction)

**Inputs**: introduction's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to introduction — ensure gap statement is compelling, contributions are clear.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_introduction.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
