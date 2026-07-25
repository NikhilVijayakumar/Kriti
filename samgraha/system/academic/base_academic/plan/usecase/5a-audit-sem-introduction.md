# Use-case 5a-introduction — Semantic Audit — introduction

**Depends on**: `deterministic-audit-introduction` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=introduction) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `introduction`'s draft, `calculation/semantic/document/introduction.md` rubric

**Action**: Score `introduction`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_introduction.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
