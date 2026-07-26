# Use-case 5b-introduction — Plagiarism Audit — introduction

**Depends on**: `5a-audit-sem-introduction`

**Script**: `plagiarism-audit` (domain=introduction)

**Inputs**: introduction's draft, reference corpus

**Action**: Run plagiarism detection on introduction content. Check for unoriginal gap statements or copied problem descriptions.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_introduction.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
