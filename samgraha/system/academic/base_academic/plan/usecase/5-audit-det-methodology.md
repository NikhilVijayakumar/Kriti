# Use-case 5-methodology — Deterministic Audit — methodology

**Depends on**: `section-budget-fit-methodology` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=methodology)

**Inputs**: `methodology`'s stage='budget-fit' draft, `calculation/deterministic/methodology.yaml` rule file

**Action**: Run `methodology`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_methodology.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
