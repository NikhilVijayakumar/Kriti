# Use-case 5-title-and-metadata — Deterministic Audit — title-and-metadata

**Depends on**: `section-budget-fit-title-and-metadata` (4d) + `section-budget-fit-total`

**Script**: `deterministic-audit` (det, domain=title-and-metadata)

**Inputs**: `title-and-metadata`'s stage='budget-fit' draft, `calculation/deterministic/title-and-metadata.yaml` rule file

**Action**: Run `title-and-metadata`'s mechanical checks (word count, citation markers, no placeholders). Cheap fail-fast before semantic scoring.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_deterministic_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') ORDER BY run_number DESC LIMIT 1` = PASS

**Verify script**: `script/verify/uc5_audit_det_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. PASS gates semantic-audit-{d}.
