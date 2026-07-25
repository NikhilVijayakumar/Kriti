# Use-case 5-experimental-setup — Deterministic Audit — experimental-setup

**Depends on**: `section-budget-fit-experimental-setup` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=experimental-setup)

**Inputs**: `experimental-setup`'s stage='budget-fit' draft, `calculation/deterministic/experimental-setup.yaml` rule file

**Action**: Run `experimental-setup`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_experimental_setup.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
