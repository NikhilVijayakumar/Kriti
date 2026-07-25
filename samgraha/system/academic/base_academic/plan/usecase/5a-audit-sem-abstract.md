# Use-case 5a-abstract — Semantic Audit — abstract

**Depends on**: `deterministic-audit-abstract` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=abstract) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `abstract`'s draft, `calculation/semantic/document/abstract.md` rubric

**Action**: Score `abstract`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='abstract') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_abstract.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
