# Use-case 4c-limitations — Section Supplementary Content — limitations

**Depends on**: `section-citations-limitations` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=limitations) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `limitations`'s stage='cite' draft, 3a/3b findings relevant to `limitations` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `limitations` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='limitations') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_limitations.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
