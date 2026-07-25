# Use-case 5a-limitations — Semantic Audit — limitations

**Depends on**: `deterministic-audit-limitations` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=limitations) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `limitations`'s draft, `calculation/semantic/document/limitations.md` rubric

**Action**: Score `limitations`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='limitations') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_limitations.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
