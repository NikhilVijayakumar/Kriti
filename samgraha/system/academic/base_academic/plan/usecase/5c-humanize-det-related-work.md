# Use-case 5c-related-work — Humanize Deterministic — related-work

**Depends on**: `plagiarism-forensic-audit-related-work` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `related-work`'s draft + flagged spans, if `related-work` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `related-work` a library can do reliably — no-op if `related-work` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='related-work') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_related_work.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
