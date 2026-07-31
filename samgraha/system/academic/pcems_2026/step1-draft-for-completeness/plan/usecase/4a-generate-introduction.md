# Use-case 4a-introduction — Generate Section Draft — introduction

**Depends on**: `novelty-analysis` + `gap-analysis` (cross-cutting analyses from base_academic)

**Script**: `gather-domain-evidence` (mode=generate, domain=introduction) -> `generate-section` (prompt, template=`templates/generation/markdown/introduction.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `introduction`, `templates/generation/markdown/introduction.md`

**Action**: Generate the `introduction` section's initial content — problem context, gap statement, contributions, paper outline. Grounded in evidence from analyses.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_introduction.py --paper-id <id>`

**Rule**: Runs after cross-cutting analyses have results. Independently re-runnable.
