# Use-case 5c-limitations — Humanize Deterministic — limitations

**Depends on**: `plagiarism-forensic-audit-limitations` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `limitations`'s draft + flagged spans, if `limitations` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `limitations` a library can do reliably — no-op if `limitations` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='limitations') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_limitations.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
