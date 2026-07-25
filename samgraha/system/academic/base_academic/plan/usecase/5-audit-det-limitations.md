# Use-case 5-limitations — Deterministic Audit — limitations

**Depends on**: `section-budget-fit-limitations` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=limitations)

**Inputs**: `limitations`'s stage='budget-fit' draft, `calculation/deterministic/limitations.yaml` rule file

**Action**: Run `limitations`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='limitations') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_limitations.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
