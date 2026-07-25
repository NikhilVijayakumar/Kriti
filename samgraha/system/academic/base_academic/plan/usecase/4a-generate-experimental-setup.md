# Use-case 4a-experimental-setup — Generate Section Draft — experimental-setup

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=generate, domain=experimental-setup) -> `generate-section` (prompt, template=`templates/generation/markdown/experimental-setup.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `experimental-setup`, `templates/generation/markdown/experimental-setup.md`

**Action**: Generate the `experimental-setup` section's initial deep content — structure, argument, claims grounded in evidence. In-repo grounding markers only (external literature -> 4b, math/table weaving -> 4c).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='experimental-setup') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_experimental_setup.py --paper-id <id>`

**Rule**: Runs after 3a+3b have results. Independently re-runnable — a re-run of this domain does not touch any other domain's draft.
