# Use-case 5c-methodology — Humanize Deterministic — methodology

**Depends on**: `plagiarism-forensic-audit-methodology` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `methodology`'s draft + flagged spans, if `methodology` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `methodology` a library can do reliably — no-op if `methodology` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_methodology.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
