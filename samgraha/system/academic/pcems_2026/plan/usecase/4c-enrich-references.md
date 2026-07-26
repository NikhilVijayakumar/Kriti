# Use-case 4c-references — Enrich Content — references

**Depends on**: `4b-cite-references`

**Script**: `gather-domain-evidence` (mode=enrich, domain=references) -> `enrich-section` -> `persist-section-draft` (stage=enrich)

**Inputs**: references's stage='cite' draft, base_academic enrichment patterns

**Action**: Verify source legitimacy, check recency mix (50%+ from last 5 years), ensure DOI completeness. Apply PCEMS-specific criteria.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_references.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
