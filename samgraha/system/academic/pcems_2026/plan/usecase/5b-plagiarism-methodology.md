# Use-case 5b-methodology — Plagiarism Audit — methodology

**Depends on**: `5a-audit-sem-methodology`

**Script**: `plagiarism-audit` (domain=methodology)

**Inputs**: methodology's draft, reference corpus

**Action**: Run plagiarism detection on methodology content. Check for unoriginal technique descriptions.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_methodology.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
