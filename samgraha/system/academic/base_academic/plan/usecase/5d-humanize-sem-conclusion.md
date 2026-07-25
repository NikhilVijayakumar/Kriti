# Use-case 5d-conclusion — Humanize Semantic — conclusion

**Depends on**: `humanize-deterministic-conclusion` (still flagged after deterministic pass)

**Script**: `gather-humanize-context` -> `humanize-section` (prompt, Layers 2-3 only) -> `persist-humanize-pass` (pass_kind=semantic)

**Inputs**: `conclusion`'s deterministic-fixed draft, if `conclusion` is still flagged (else a no-op)

**Action**: LLM rewrite (technical DNA injection + voice restoration) for `conclusion` — no-op if `conclusion` was resolved by the deterministic pass alone or never flagged.

**Completion criteria** (checked by verify script):
- If still flagged: `SELECT COUNT(*) FROM academic_humanize_passes WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND pass_kind='semantic'` >= 1. Otherwise trivially complete.

**Verify script**: `script/verify/uc5d_humanize_sem_conclusion.py --paper-id <id>`

**Rule**: Gates document-narrative-polish (4e) together with every other domain's 5c/5d.
