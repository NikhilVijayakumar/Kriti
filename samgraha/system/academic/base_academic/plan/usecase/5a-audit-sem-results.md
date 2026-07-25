# Use-case 5a-results — Semantic Audit — results

**Depends on**: `deterministic-audit-results` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=results) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `results`'s draft, `calculation/semantic/document/results.md` rubric

**Action**: Score `results`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='results') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_results.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
