# Use-case 5b-title-and-metadata — Plagiarism Audit — title-and-metadata

**Depends on**: `5a-audit-sem-title-and-metadata`

**Script**: `plagiarism-audit` (domain=title-and-metadata)

**Inputs**: title-and-metadata's draft, reference corpus

**Action**: Run plagiarism detection on title-and-metadata content. Check for unoriginal phrasing in abstract and keywords.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_title_and_metadata.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
