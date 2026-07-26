# Use-case 5c-title-and-metadata — Humanize (Deterministic) — title-and-metadata

**Depends on**: `5b-plagiarism-title-and-metadata`

**Script**: `humanize-det` (domain=title-and-metadata)

**Inputs**: title-and-metadata's draft, deterministic humanize rules

**Action**: Apply deterministic humanization passes to title-and-metadata — fix formulaic language, ensure natural phrasing in abstract.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND pass_type='deterministic'` >= 1

**Verify script**: `script/verify/uc5c_humanize_det_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. Iterates until risk flags clear.
