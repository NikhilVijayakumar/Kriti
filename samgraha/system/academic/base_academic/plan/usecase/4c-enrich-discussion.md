# Use-case 4c-discussion — Section Supplementary Content — discussion

**Depends on**: `section-citations-discussion` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=discussion) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `discussion`'s stage='cite' draft, 3a/3b findings relevant to `discussion` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `discussion` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_discussion.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
