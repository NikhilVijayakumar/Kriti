# Use-case 5d-discussion — Humanize Semantic — discussion

**Depends on**: `humanize-deterministic-discussion` (still flagged after deterministic pass)

**Script**: `gather-humanize-context` -> `humanize-section` (prompt, Layers 2-3 only) -> `persist-humanize-pass` (pass_kind=semantic)

**Inputs**: `discussion`'s deterministic-fixed draft, if `discussion` is still flagged (else a no-op)

**Action**: LLM rewrite (technical DNA injection + voice restoration) for `discussion` — no-op if `discussion` was resolved by the deterministic pass alone or never flagged.

**Completion criteria** (checked by verify script):
- If still flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion') AND pass_kind='semantic'` >= 1. Otherwise trivially complete.

**Verify script**: `script/verify/uc5d_humanize_sem_discussion.py --paper-id <id>`

**Rule**: Gates document-narrative-polish (4e) together with every other domain's 5c/5d.
