# Use-case 5b — Plagiarism Forensic Audit

**Depends on**: `assemble-paper-structure` (per domain — each domain must
have a draft before plagiarism checking)

**Script**: 5-step per-domain — `deterministic-fingerprint-check` (det) →
`gather-plagiarism-context` → `plagiarism-fingerprint-audit` (prompt) →
`targeted-rewrite` (prompt, conditional) → `persist-plagiarism-findings`

**Inputs**:
- Each domain's latest `academic_narratives` draft
- Banned phrases, reference corpus

**Action**: Deterministic pre-screen (burstiness, n-gram repetition,
banned phrases) + semantic forensic audit + conditional targeted rewrite.

**Completion criteria** (checked by verify script):
- Every domain has a forensic plagiarism verdict:
  `SELECT verdict FROM academic_plagiarism_findings WHERE paper_id=? AND pass_type='forensic'` exists
  for all domains

**Verify script**: `script/verify/uc5b_plagiarism.py --paper-id <id>`

**Rule**: Runs after assemble-paper-structure. 5-step per-domain expanded
at runtime.
