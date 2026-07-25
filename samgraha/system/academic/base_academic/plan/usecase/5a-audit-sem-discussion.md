# Use-case 5a-discussion — Semantic Audit — discussion

**Depends on**: `deterministic-audit-discussion` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=discussion) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `discussion`'s draft, `calculation/semantic/document/discussion.md` rubric

**Action**: Score `discussion`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_discussion.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
