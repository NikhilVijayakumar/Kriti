# Use-case 4c-conclusion — Section Supplementary Content — conclusion

**Depends on**: `section-citations-conclusion` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=conclusion) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `conclusion`'s stage='cite' draft, 3a/3b findings relevant to `conclusion` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `conclusion` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_conclusion.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
