# Use-case 5a-title-and-metadata — Semantic Audit — title-and-metadata

**Depends on**: `5-audit-det-title-and-metadata` (PASS)

**Script**: `gather-domain-evidence` (mode=audit, domain=title-and-metadata) -> `semantic-audit` (prompt) -> `persist-domain-semantic-score` (scope=section-full)

**Inputs**: title-and-metadata's draft, `audit/semantic/document/01-title-and-metadata.md` rubric

**Action**: Score title-and-metadata's draft against its rubric. Checks title specificity, keyword quality, metadata completeness.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND scope='section-full'` >= 1

**Verify script**: `script/verify/uc5a_audit_sem_title_and_metadata.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds run_numbers, never overwrites. Only runs if deterministic-audit PASS.
