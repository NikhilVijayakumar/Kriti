# Use-case 5c-conclusion — Humanize (Deterministic) — conclusion

**Depends on**: `5b-plagiarism-conclusion`

**Script**: `humanize-det` (domain=conclusion)

**Inputs**: conclusion's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to conclusion — fix formulaic closing language, ensure natural summary.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
