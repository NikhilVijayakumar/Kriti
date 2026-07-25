# Use-case 5-abstract — Deterministic Audit — abstract

**Depends on**: `section-budget-fit-abstract` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=abstract)

**Inputs**: `abstract`'s stage='budget-fit' draft, `calculation/deterministic/abstract.yaml` rule file

**Action**: Run `abstract`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='abstract') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_abstract.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
