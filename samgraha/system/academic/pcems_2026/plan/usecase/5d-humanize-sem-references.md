# Use-case 5d-references — Humanize (Semantic) — references

**Depends on**: `5c-humanize-det-references`

**Script**: `humanize-sem` (domain=references)

**Inputs**: references's draft, semantic humanize prompt

**Action**: Apply semantic humanization pass to references — ensure formatting reads naturally, no awkward constructions.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_humanize_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND pass_type='semantic'` >= 1

**Verify script**: `script/verify/uc5d_humanize_sem_references.py --paper-id <id>`

**Rule**: Re-runnable. Final polish before aggregation.
