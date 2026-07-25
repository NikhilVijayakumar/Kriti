# Use-case 4a-problem-definition — Generate Section Draft — problem-definition

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-analysis` (3a) + `diagram-architecture-analysis` (3b)

**Script**: `gather-domain-evidence` (mode=generate, domain=problem-definition) -> `generate-section` (prompt, template=`templates/generation/markdown/problem-definition.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `problem-definition`, `templates/generation/markdown/problem-definition.md`

**Action**: Generate the `problem-definition` section's initial deep content — structure, argument, claims grounded in evidence. In-repo grounding markers only (external literature -> 4b, math/table weaving -> 4c).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_problem_definition.py --paper-id <id>`

**Rule**: Runs after 3a+3b have results. Independently re-runnable — a re-run of this domain does not touch any other domain's draft.
