# Use-case 5a-conclusion — Semantic Audit — conclusion

**Depends on**: `5-audit-det-conclusion` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=conclusion) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: conclusion's draft, `audit/semantic/document/05-conclusion.md` rubric

**Action**: Score conclusion's draft against its rubric. Checks contribution alignment, impact statement quality, no new claims.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_conclusion.py --paper-id <id>`

**Rule**: Accumulates indefinitely. Only runs if deterministic-audit PASS.
