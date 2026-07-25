# Use-case 4b-results — Section Citations — results

**Depends on**: `generate-section-draft-results` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=results) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `results`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `results`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='results')` >= 1

**Verify script**: `script/verify/uc4b_cite_results.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
