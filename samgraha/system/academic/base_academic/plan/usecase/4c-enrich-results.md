# Use-case 4c-results — Section Supplementary Content — results

**Depends on**: `section-citations-results` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=results) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `results`'s stage='cite' draft, 3a/3b findings relevant to `results` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `results` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='results') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_results.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
