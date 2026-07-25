# Use-case 5c-problem-definition — Humanize Deterministic — problem-definition

**Depends on**: `plagiarism-forensic-audit-problem-definition` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `problem-definition`'s draft + flagged spans, if `problem-definition` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `problem-definition` a library can do reliably — no-op if `problem-definition` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_problem_definition.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
