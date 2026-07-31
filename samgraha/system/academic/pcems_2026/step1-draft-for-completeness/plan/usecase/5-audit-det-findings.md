# Use-case 5-findings — Deterministic Audit — findings

**Depends on**: `4d-budget-findings`

**Script**: `deterministic-audit` (det, domain=findings)

**Inputs**: findings's stage='budget-fit' draft, `calculation/generation/findings.yaml` rule file

**Action**: Run findings's mechanical checks (word count, citation markers, no placeholders, table/figure formatting).

**Completion criteria**:
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_findings.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit.
