# Use-case 4a-references — Generate Section Draft — references

**Depends on**: `4b-cite-introduction` + `4b-cite-methodology` + `4b-cite-findings` + `4b-cite-conclusion` + `4b-cite-title-and-metadata` (all citation stages)

**Script**: `gather-domain-evidence` (mode=generate, domain=references) -> `generate-section` (prompt, template=`templates/generation/markdown/references.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: All cited references from other sections, `templates/generation/markdown/references.md`

**Action**: Collate all inline citations from other sections into a formatted reference list. Verify DOI completeness, recency mix, no duplicates.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_references.py --paper-id <id>`

**Rule**: Runs after all other domains' citation stages. Re-runnable.
