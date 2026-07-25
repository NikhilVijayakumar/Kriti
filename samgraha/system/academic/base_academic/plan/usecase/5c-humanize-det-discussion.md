# Use-case 5c-discussion — Humanize Deterministic — discussion

**Depends on**: `plagiarism-forensic-audit-discussion` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `discussion`'s draft + flagged spans, if `discussion` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `discussion` a library can do reliably — no-op if `discussion` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_discussion.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
