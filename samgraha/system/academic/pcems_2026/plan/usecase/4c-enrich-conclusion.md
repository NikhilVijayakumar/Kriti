# Use-case 4c-conclusion — Enrich Content — conclusion

**Depends on**: `4b-cite-conclusion`

**Script**: `gather-domain-evidence` (mode=enrich, domain=conclusion) -> `enrich-section` -> `persist-section-draft` (stage=enrich)

**Inputs**: conclusion's stage='cite' draft, base_academic enrichment patterns

**Action**: Ensure contribution alignment with Introduction, strengthen impact statement, verify no new claims. Apply PCEMS-specific criteria.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
