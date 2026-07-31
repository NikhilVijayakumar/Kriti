# Use-case 4a-findings — Generate Section Draft — findings

**Depends on**: `novelty-analysis` + `gap-analysis` (cross-cutting analyses from base_academic)

**Script**: `gather-domain-evidence` (mode=generate, domain=findings) -> `generate-section` (prompt, template=`templates/generation/markdown/findings.md`) -> `persist-section-draft` (stage=generate)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings scoped to `findings`, `templates/generation/markdown/findings.md`

**Action**: Generate the `findings` section's initial content — experimental setup, results, analysis, tables, figures. Absorbs base_academic's experimental-setup + results + discussion.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND stage='generate'` >= 1

**Verify script**: `script/verify/uc4a_generate_findings.py --paper-id <id>`

**Rule**: Runs after cross-cutting analyses have results. Independently re-runnable.
