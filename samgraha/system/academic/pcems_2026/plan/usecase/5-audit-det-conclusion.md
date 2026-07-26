# Use-case 5-conclusion — Deterministic Audit — conclusion

**Depends on**: `4d-budget-conclusion`

**Script**: `deterministic-audit` (det, domain=conclusion)

**Inputs**: conclusion's stage='budget-fit' draft, `calculation/generation/conclusion.yaml` rule file

**Action**: Run conclusion's mechanical checks (word count, citation markers, no placeholders, no new citations).

**Completion criteria**:
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit.
