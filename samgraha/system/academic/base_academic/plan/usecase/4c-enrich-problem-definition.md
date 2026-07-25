# Use-case 4c-problem-definition — Section Supplementary Content — problem-definition

**Depends on**: `section-citations-problem-definition` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=enrich, domain=problem-definition) -> `section-enrichment` (prompt) -> `persist-section-draft` (stage=enrich)

**Inputs**: `problem-definition`'s stage='cite' draft, 3a/3b findings relevant to `problem-definition` (no-op pass-through if none relevant)

**Action**: Weave in equations, tables, and diagram references into `problem-definition` where its content actually calls for them. A no-op for domains with nothing relevant still produces a stage='enrich' row (uniform completion predicate).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_problem_definition.py --paper-id <id>`

**Rule**: Runs after this domain's own 4b. Independently re-runnable.
