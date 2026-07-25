# Use-case 5a-experimental-setup — Semantic Audit — experimental-setup

**Depends on**: `deterministic-audit-experimental-setup` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=experimental-setup) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `experimental-setup`'s draft, `calculation/semantic/document/experimental-setup.md` rubric

**Action**: Score `experimental-setup`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_experimental_setup.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
