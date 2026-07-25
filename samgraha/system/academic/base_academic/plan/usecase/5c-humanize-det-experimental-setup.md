# Use-case 5c-experimental-setup — Humanize Deterministic — experimental-setup

**Depends on**: `plagiarism-forensic-audit-experimental-setup` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `experimental-setup`'s draft + flagged spans, if `experimental-setup` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `experimental-setup` a library can do reliably — no-op if `experimental-setup` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_experimental_setup.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
