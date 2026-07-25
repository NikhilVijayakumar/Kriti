# Use-case 5-results — Deterministic Audit — results

**Depends on**: `section-budget-fit-results` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=results)

**Inputs**: `results`'s stage='budget-fit' draft, `calculation/deterministic/results.yaml` rule file

**Action**: Run `results`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='results') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_results.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
