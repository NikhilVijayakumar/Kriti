# Use-case 4b-methodology — Section Citations — methodology

**Depends on**: `generate-section-draft-methodology` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=methodology) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `methodology`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `methodology`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology')` >= 1

**Verify script**: `script/verify/uc4b_cite_methodology.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
