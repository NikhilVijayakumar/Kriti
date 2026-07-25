# Use-case 5-conclusion — Deterministic Audit — conclusion

**Depends on**: `section-budget-fit-conclusion` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=conclusion)

**Inputs**: `conclusion`'s stage='budget-fit' draft, `calculation/deterministic/conclusion.yaml` rule file

**Action**: Run `conclusion`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
