# Use-case 4c-title-and-metadata — Section Supplementary Content — title-and-metadata

**Depends on**: `section-citations-title-and-metadata` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=title-and-metadata) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `title-and-metadata`'s stage='cite' draft, 3a/3b findings relevant to `title-and-metadata` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `title-and-metadata` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_title_and_metadata.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
