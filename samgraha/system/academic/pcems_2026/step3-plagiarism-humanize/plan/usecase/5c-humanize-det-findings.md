# Use-case 5c-findings — Humanize (Deterministic) — findings

**Depends on**: `5b-plagiarism-findings`

**Script**: `humanize-det` (domain=findings)

**Inputs**: findings's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to findings — fix formulaic result descriptions, ensure objective presentation.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_findings.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
