# Use-case 4b-findings — Cite References — findings

**Depends on**: `4a-generate-findings`

**Script**: `gather-domain-evidence` (mode=cite, domain=findings) -> `enrich-with-citations` -> `persist-section-draft` (stage=cite)

**Inputs**: findings's stage='generate' draft, reference database

**Action**: Add inline citations to findings — cite baseline methods, cite dataset sources, cite tools used.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_findings.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
