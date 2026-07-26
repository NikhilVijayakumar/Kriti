# Use-case 5d-title-and-metadata — Humanize (Semantic) — title-and-metadata

**Depends on**: `5c-humanize-det-title-and-metadata`

**Script**: `humanize-sem` (domain=title-and-metadata)

**Inputs**: title-and-metadata's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to title-and-metadata — ensure abstract reads naturally, title is engaging.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
