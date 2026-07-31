# Use-case 5-introduction — Deterministic Audit — introduction

**Depends on**: `4d-budget-introduction`

**Script**: `deterministic-audit` (det, domain=introduction)

**Inputs**: introduction's stage='budget-fit' draft, `calculation/generation/introduction.yaml` rule file

**Action**: Run introduction's mechanical checks (word count, citation markers, no placeholders, no methodology leakage).

**Completion criteria**:
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_introduction.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit.
