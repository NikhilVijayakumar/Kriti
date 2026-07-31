# Use-case 5d-findings — Humanize (Semantic) — findings

**Depends on**: `5c-humanize-det-findings`

**Script**: `humanize-sem` (domain=findings)

**Inputs**: findings's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to findings — ensure analysis reads naturally, results are presented clearly.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_findings.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
