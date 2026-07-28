# Use-case 5a-methodology — Semantic Audit — methodology

**Depends on**: `5-audit-det-methodology` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=methodology) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: methodology's draft, `audit/semantic/document/methodology.md` rubric

**Action**: Score methodology's draft against its rubric. Checks design justification, reproducibility, variable definitions.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_methodology.py --paper-id <id>`

**Rule**: Accumulates indefinitely. Only runs if deterministic-audit PASS.
