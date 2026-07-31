# Use-case 5c-introduction — Humanize (Deterministic) — introduction

**Depends on**: `5b-plagiarism-introduction`

**Script**: `humanize-det` (domain=introduction)

**Inputs**: introduction's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to introduction — fix formulaic language, ensure natural problem framing.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_introduction.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
