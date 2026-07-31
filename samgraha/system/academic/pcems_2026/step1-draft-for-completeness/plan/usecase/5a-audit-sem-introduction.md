# Use-case 5a-introduction — Semantic Audit — introduction

**Depends on**: `5-audit-det-introduction` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=introduction) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: introduction's draft, `audit/semantic/document/introduction.md` rubric

**Action**: Score introduction's draft against its rubric. Checks problem context quality, gap specificity, contribution statement.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_introduction.py --paper-id <id>`

**Rule**: Accumulates indefinitely. Only runs if deterministic-audit PASS.
