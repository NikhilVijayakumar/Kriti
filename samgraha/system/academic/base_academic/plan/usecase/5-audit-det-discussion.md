# Use-case 5-discussion — Deterministic Audit — discussion

**Depends on**: `section-budget-fit-discussion` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=discussion)

**Inputs**: `discussion`'s stage='budget-fit' draft, `calculation/deterministic/discussion.yaml` rule file

**Action**: Run `discussion`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_discussion.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
