# Use-case 4b-experimental-setup — Section Citations — experimental-setup

**Depends on**: `generate-section-draft-experimental-setup` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=experimental-setup) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `experimental-setup`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `experimental-setup`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup')` >= 1

**Verify script**: `script/verify/uc4b_cite_experimental_setup.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
