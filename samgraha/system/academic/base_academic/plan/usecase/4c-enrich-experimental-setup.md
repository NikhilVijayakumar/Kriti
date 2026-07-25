# Use-case 4c-experimental-setup — Section Supplementary Content — experimental-setup

**Depends on**: `section-citations-experimental-setup` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=experimental-setup) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `experimental-setup`'s stage='cite' draft, 3a/3b findings relevant to `experimental-setup` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `experimental-setup` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_experimental_setup.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
