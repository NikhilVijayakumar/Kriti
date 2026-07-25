# Use-case 4c-related-work — Section Supplementary Content — related-work

**Depends on**: `section-citations-related-work` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=related-work) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `related-work`'s stage='cite' draft, 3a/3b findings relevant to `related-work` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `related-work` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='related-work') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_related_work.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
