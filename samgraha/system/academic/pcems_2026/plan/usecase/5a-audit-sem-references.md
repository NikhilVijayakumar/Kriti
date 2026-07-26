# Use-case 5a-references — Semantic Audit — references

**Depends on**: `5-audit-det-references` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=references) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: references's draft, `audit/semantic/document/06-references.md` rubric

**Action**: Score references's draft against its rubric. Checks source legitimacy, citation consistency, recency mix.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_references.py --paper-id <id>`

**Rule**: Accumulates indefinitely. Only runs if deterministic-audit PASS.
