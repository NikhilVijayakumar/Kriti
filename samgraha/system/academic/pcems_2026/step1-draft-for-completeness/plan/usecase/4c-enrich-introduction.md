# Use-case 4c-introduction — Enrich Content — introduction

**Depends on**: `4b-cite-introduction`

**Script**: `gather-domain-evidence` (mode=enrich, domain=introduction) -> `enrich-section` -> `persist-section-draft` (stage=enrich)

**Inputs**: introduction's stage='cite' draft, base_academic enrichment patterns

**Action**: Strengthen gap specificity, sharpen contribution statements, ensure no methodology leakage. Apply PCEMS-specific criteria.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND stage='enrich'` >= 1

**Verify script**: `script/verify/uc4c_enrich_introduction.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
