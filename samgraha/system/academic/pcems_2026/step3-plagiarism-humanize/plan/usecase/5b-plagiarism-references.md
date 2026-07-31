# Use-case 5b-references — Plagiarism Audit — references

**Depends on**: `5a-audit-sem-references`

**Script**: `plagiarism-audit` (domain=references)

**Inputs**: references's draft, reference corpus

**Action**: Run plagiarism detection on references content. Check for fabricated references or copied bibliographic entries.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references')` >= 0

**Verify script**: `script/verify/uc5b_plagiarism_references.py --paper-id <id>`

**Rule**: Informational — findings logged but do not gate pipeline.
