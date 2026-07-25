# Use-case 4b-problem-definition — Section Citations — problem-definition

**Depends on**: `generate-section-draft-problem-definition` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=problem-definition) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `problem-definition`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `problem-definition`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition')` >= 1

**Verify script**: `script/verify/uc4b_cite_problem_definition.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
