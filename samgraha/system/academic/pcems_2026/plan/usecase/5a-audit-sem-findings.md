# Use-case 5a-findings — Semantic Audit — findings

**Depends on**: `5-audit-det-findings` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=findings) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: findings's draft, `audit/semantic/document/findings.md` rubric

**Action**: Score findings's draft against its rubric. Checks experimental setup completeness, baseline comparison, analysis depth.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_findings.py --paper-id <id>`

**Rule**: Accumulates indefinitely. Only runs if deterministic-audit PASS.
