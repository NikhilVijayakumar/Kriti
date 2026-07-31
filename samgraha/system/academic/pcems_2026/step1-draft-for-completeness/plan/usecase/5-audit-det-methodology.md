# Use-case 5-methodology — Deterministic Audit — methodology

**Depends on**: `4d-budget-methodology`

**Script**: `deterministic-audit` (det, domain=methodology)

**Inputs**: methodology's stage='budget-fit' draft, `calculation/generation/methodology.yaml` rule file

**Action**: Run methodology's mechanical checks (word count, citation markers, no placeholders, equation formatting).

**Completion criteria**:
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_methodology.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit.
