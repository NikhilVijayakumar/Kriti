# Use-case 4b-introduction — Cite References — introduction

**Depends on**: `4a-generate-introduction`

**Script**: `gather-domain-evidence` (mode=cite, domain=introduction) -> `enrich-with-citations` -> `persist-section-draft` (stage=cite)

**Inputs**: introduction's stage='generate' draft, reference database

**Action**: Add inline citations to introduction's problem context and gap statement. Verify citation markers are well-formed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_introduction.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
