# Use-case 5-problem-definition — Deterministic Audit — problem-definition

**Depends on**: `section-budget-fit-problem-definition` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=problem-definition)

**Inputs**: `problem-definition`'s stage='budget-fit' draft, `calculation/deterministic/problem-definition.yaml` rule file

**Action**: Run `problem-definition`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_problem_definition.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
