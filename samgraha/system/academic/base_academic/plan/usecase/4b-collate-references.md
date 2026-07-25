# Use-case 4b-references — Section Citations — references (collation, fan-in)

**Depends on**: all 11 `section-citations-{domain}` usecases (every non-references domain)

**Script**: `collate-references` (det, single step — dedupes + formats every collected citation) -> writes references' stage='cite' narrative directly

**Inputs**: Every domain's `academic_section_citations` rows

**Action**: Build the `references` domain's first-ever draft from what the other 11 domains actually cited — `references` has no stage='generate' row (4a skips it), its content is strictly a function of this collation.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_collate_references.py --paper-id <id>`

**Rule**: Fan-in — this usecase's own script calls usecase_status() for each of the 11 upstream section-citations-* usecases and hard-fails, listing which are still outstanding, rather than collating a partial citation list.
