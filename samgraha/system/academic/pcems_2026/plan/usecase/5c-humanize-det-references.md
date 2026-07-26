# Use-case 5c-references — Humanize (Deterministic) — references

**Depends on**: `5b-plagiarism-references`

**Script**: `humanize-det` (domain=references)

**Inputs**: references's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to references — fix inconsistent formatting, ensure consistent style.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_references.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
