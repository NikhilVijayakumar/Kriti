# Use-case 4b-methodology — Cite References — methodology

**Depends on**: `4a-generate-methodology`

**Script**: `gather-domain-evidence` (mode=cite, domain=methodology) -> `enrich-with-citations` -> `persist-section-draft` (stage=cite)

**Inputs**: methodology's stage='generate' draft, reference database

**Action**: Add inline citations to methodology — cite prior techniques being extended, cite tools/libraries used.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_methodology.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
