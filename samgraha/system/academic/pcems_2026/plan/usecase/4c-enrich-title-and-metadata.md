# Use-case 4c-title-and-metadata — Enrich Content — title-and-metadata

**Depends on**: `4b-cite-title-and-metadata`

**Script**: `gather-domain-evidence` (mode=enrich, domain=title-and-metadata) -> `enrich-section` -> `persist-section-draft` (stage=enrich)

**Inputs**: title-and-metadata's stage='cite' draft, base_academic enrichment patterns

**Action**: Strengthen title specificity, refine keywords, polish abstract language. Apply PCEMS-specific quality criteria.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
