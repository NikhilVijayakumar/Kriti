# Use-case 5c-abstract — Humanize Deterministic — abstract

**Depends on**: `plagiarism-forensic-audit-abstract` (FAIL after targeted rewrite)

**Script**: `gather-humanize-context` -> `nlp-fingerprint-fix` (det — sentence-length variance, parallel-structure breaking)

**Inputs**: `abstract`'s draft + flagged spans, if `abstract` is flagged (else a no-op)

**Action**: Mechanical AI-fingerprint fixes for `abstract` a library can do reliably — no-op if `abstract` was never flagged.

**Completion criteria** (checked by verify script):
- If flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='abstract') AND pass_kind='deterministic'` >= 1. If never flagged: trivially complete.

**Verify script**: `script/verify/uc5c_humanize_det_abstract.py --paper-id <id>`

**Rule**: Only meaningfully runs for domains still flagged after plagiarism-forensic-audit-{d}; a no-op elsewhere.
