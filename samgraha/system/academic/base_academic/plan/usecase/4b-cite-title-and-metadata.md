# Use-case 4b-title-and-metadata — Section Citations — title-and-metadata

**Depends on**: `generate-section-draft-title-and-metadata` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=title-and-metadata) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `title-and-metadata`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `title-and-metadata`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata')` >= 1

**Verify script**: `script/verify/uc4b_cite_title_and_metadata.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
