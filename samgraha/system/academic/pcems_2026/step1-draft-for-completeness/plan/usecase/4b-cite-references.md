# Use-case 4b-references — Validate Citations — references

**Depends on**: `4a-generate-references`

**Script**: `validate-references` (domain=references)

**Inputs**: references's stage='generate' draft, all other sections' citation lists

**Action**: Cross-check that every inline citation in other sections has a corresponding reference entry, and vice versa. Report orphaned references and missing entries.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_references.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
