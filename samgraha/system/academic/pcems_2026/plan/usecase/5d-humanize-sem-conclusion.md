# Use-case 5d-conclusion — Humanize (Semantic) — conclusion

**Depends on**: `5c-humanize-det-conclusion`

**Script**: `humanize-sem` (domain=conclusion)

**Inputs**: conclusion's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to conclusion — ensure contribution summary reads naturally, future work is compelling.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
