# Use-case 4b-abstract — Section Citations — abstract

**Depends on**: `generate-section-draft-abstract` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=abstract) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `abstract`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `abstract`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='abstract')` >= 1

**Verify script**: `script/verify/uc4b_cite_abstract.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
