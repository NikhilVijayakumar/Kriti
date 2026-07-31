# Use-case 5b-conclusion — Plagiarism Audit — conclusion

**Depends on**: `5a-audit-sem-conclusion`

**Script**: `plagiarism-audit` (domain=conclusion)

**Inputs**: conclusion's draft, reference corpus

**Action**: Run plagiarism detection on conclusion content. Check for unoriginal closing statements.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_conclusion.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
