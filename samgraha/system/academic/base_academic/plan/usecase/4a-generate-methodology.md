# Use-case 4a-methodology — Generate Section Draft — methodology

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=generate, domain=methodology) -> `generate-section` (prompt, template=`templates/generation/markdown/methodology.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `methodology`, `templates/generation/markdown/methodology.md`

**Action**: Generate the `methodology` section's initial deep content — structure, argument, claims grounded in evidence. In-repo grounding markers only (external literature -> 4b, math/table weaving -> 4c).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_methodology.py --paper-id <id>`

**Rule**: Runs after 3a+3b have results. Independently re-runnable — a re-run of this domain does not touch any other domain's draft.
