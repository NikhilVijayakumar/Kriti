# Use-case 5a-references — Semantic Audit — references

**Depends on**: `deterministic-audit-references` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=references) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: `references`'s draft, `calculation/semantic/document/references.md` rubric

**Action**: Score `references`'s draft against its rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_references.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit-{d} PASS.
