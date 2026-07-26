# Use-case 4b-title-and-metadata — Cite References — title-and-metadata

**Depends on**: `4a-generate-title-and-metadata`

**Script**: `gather-domain-evidence` (mode=cite, domain=title-and-metadata) -> `enrich-with-citations` -> `persist-section-draft` (stage=cite)

**Inputs**: title-and-metadata's stage='generate' draft, reference database

**Action**: Add inline citations to title-and-metadata's abstract and keywords. Verify citation markers are well-formed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
