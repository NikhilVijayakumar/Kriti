# Use-case 5c-methodology — Humanize (Deterministic) — methodology

**Depends on**: `5b-plagiarism-methodology`

**Script**: `humanize-det` (domain=methodology)

**Inputs**: methodology's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to methodology — fix formulaic descriptions, ensure natural technical writing.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_methodology.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
