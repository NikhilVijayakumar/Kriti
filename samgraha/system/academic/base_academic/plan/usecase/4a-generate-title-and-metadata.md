# Use-case 4a-title-and-metadata — Generate Section Draft — title-and-metadata

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=generate, domain=title-and-metadata) -> `generate-section` (prompt, template=`templates/generation/markdown/title-and-metadata.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `title-and-metadata`, `templates/generation/markdown/title-and-metadata.md`

**Action**: Generate the `title-and-metadata` section's initial deep content — structure, argument, claims grounded in evidence. In-repo grounding markers only (external literature -> 4b, math/table weaving -> 4c).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_title_and_metadata.py --paper-id <id>`

**Rule**: Runs after 3a+3b have results. Independently re-runnable — a re-run of this domain does not touch any other domain's draft.
