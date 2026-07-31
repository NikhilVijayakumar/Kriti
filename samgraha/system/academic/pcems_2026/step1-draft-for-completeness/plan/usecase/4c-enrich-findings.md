# Use-case 4c-findings — Enrich Content — findings

**Depends on**: `4b-cite-findings`

**Script**: `gather-domain-evidence` (mode=enrich, domain=findings) -> `enrich-section` -> `persist-section-draft` (stage=enrich)

**Inputs**: findings's stage='cite' draft, base_academic enrichment patterns

**Action**: Ensure baseline comparison completeness, strengthen analysis depth, verify table/figure quality. Apply PCEMS-specific criteria.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_findings.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
