# Use-case 5-references — Deterministic Audit — references

**Depends on**: `4d-budget-references`

**Script**: `deterministic-audit` (det, domain=references)

**Inputs**: references's stage='budget-fit' draft, `calculation/generation/references.yaml` rule file

**Action**: Run references's mechanical checks (DOI format, author-name consistency, year plausibility, no predatory journals).

**Completion criteria**:
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_references.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit.
