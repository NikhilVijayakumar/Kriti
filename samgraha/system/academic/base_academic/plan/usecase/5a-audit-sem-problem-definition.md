# Use-case 5a-problem-definition — Semantic Audit — problem-definition

**Depends on**: `deterministic-audit-problem-definition` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=problem-definition) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `problem-definition`'s draft, `calculation/semantic/document/problem-definition.md` rubric

**Action**: Score `problem-definition`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_problem_definition.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
