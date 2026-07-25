# Use-case 4b-conclusion — Section Citations — conclusion

**Depends on**: `generate-section-draft-conclusion` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=conclusion) -> `persist-section-citations` (source_kind=in-repo)

**Inputs**: `conclusion`'s stage='generate' draft

**Action**: Extract in-repo grounding markers already present in `conclusion`'s draft, persist them as real, queryable citations (previously silently dropped).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion')` >= 1

**Verify script**: `script/verify/uc4b_cite_conclusion.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
