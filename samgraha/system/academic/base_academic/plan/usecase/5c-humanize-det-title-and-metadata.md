# Use-case 5c-title-and-metadata — Humanize Deterministic — title-and-metadata

**Depends on**: `plagiarism-forensic-audit-title-and-metadata` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `title-and-metadata`'s draft + flagged spans, if `title-and-metadata` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `title-and-metadata` a library can do reliably — no-op if `title-and-metadata` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_title_and_metadata.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
