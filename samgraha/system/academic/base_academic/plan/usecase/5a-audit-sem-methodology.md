# Use-case 5a-methodology — Semantic Audit — methodology

**Depends on**: `deterministic-audit-methodology` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=methodology) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `methodology`'s draft, `calculation/semantic/document/methodology.md` rubric

**Action**: Score `methodology`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_methodology.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
