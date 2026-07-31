# Use-case 4a-methodology — Generate Section Draft — methodology

**Depends on**: `novelty-analysis` + `gap-analysis` (cross-cutting analyses from base_academic)

**Script**: `gather-domain-evidence` (mode=generate, domain=methodology) -> `generate-section` (prompt, template=`templates/generation/markdown/methodology.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `methodology`, `templates/generation/markdown/methodology.md`

**Action**: Generate the `methodology` section's initial content — proposed method, architecture, design decisions, parameters. Grounded in repo evidence.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_methodology.py --paper-id <id>`

**Rule**: Runs after cross-cutting analyses have results. Independently re-runnable.
