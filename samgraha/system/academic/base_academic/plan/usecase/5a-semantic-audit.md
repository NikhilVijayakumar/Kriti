# Use-case 5a — Semantic Audit

**Depends on**: `deterministic-audit` (per domain — this usecase's first
step calls `usecase_status(conn, paper_id, "deterministic-audit")` scoped
to the current domain; hard-fails if that domain's latest
`academic_deterministic_findings.verdict` isn't `PASS`)

**Script**: Per-domain triad — `gather-domain-evidence` (mode=`audit`) →
`semantic-audit` (prompt) → `persist-domain-semantic-score`

**Inputs**:
- Each domain's latest `academic_narratives` draft
- `calculation/semantic/document/{domain}.md` rubric files

**Action**: Score a domain draft against the concrete system's rubric.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE paper_id=? AND scope='section'` >= 1 per
  structural domain that has a PASS deterministic verdict
- Full bar: every configured model has scored every eligible domain

**Verify script**: `script/verify/uc5a_semantic_audit.py --paper-id <id>`

**Rule**: Accumulates indefinitely — re-running adds `run_number`s, never
overwrites. Only runs for domains that passed deterministic audit.
