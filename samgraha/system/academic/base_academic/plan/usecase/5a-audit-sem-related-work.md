# Use-case 5a-related-work — Semantic Audit — related-work

**Depends on**: `deterministic-audit-related-work` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=related-work) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `related-work`'s draft, `calculation/semantic/document/related-work.md` rubric

**Action**: Score `related-work`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='related-work') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_related_work.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
