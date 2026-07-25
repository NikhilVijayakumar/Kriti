# Use-case 5a-conclusion — Semantic Audit — conclusion

**Depends on**: `deterministic-audit-conclusion` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=conclusion) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `conclusion`'s draft, `calculation/semantic/document/conclusion.md` rubric

**Action**: Score `conclusion`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_conclusion.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
