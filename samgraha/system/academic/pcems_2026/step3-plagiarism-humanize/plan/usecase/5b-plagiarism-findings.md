# Use-case 5b-findings — Plagiarism Audit — findings

**Depends on**: `5a-audit-sem-findings`

**Script**: `plagiarism-audit` (domain=findings)

**Inputs**: findings's draft, reference corpus

**Action**: Run plagiarism detection on findings content. Check for unoriginal result descriptions or copied analysis.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_findings.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
