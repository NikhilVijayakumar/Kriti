# Use-case 5-related-work — Deterministic Audit — related-work

**Depends on**: `section-budget-fit-related-work` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=related-work)

**Inputs**: `related-work`'s stage='budget-fit' draft, `calculation/deterministic/related-work.yaml` rule file

**Action**: Run `related-work`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='related-work') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_related_work.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
