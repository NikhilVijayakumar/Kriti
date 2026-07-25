# Use-case 5b-problem-definition — Plagiarism Forensic Audit — problem-definition

**Depends on**: `section-budget-fit-problem-definition` (4d) — same relationship as the pre-split pipeline, scoped to one domain

**Script**: `gather-plagiarism-context` -> `deterministic-fingerprint-check` (det) -> `plagiarism-fingerprint-audit` (prompt) -> `targeted-rewrite` (prompt, conditional) -> `persist-plagiarism-findings`

**Inputs**: `problem-definition`'s draft, banned phrases, reference corpus

**Action**: Deterministic pre-screen + semantic forensic audit + conditional targeted rewrite for `problem-definition`.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND pass_type='forensic' ORDER BY run_number DESC LIMIT 1` exists

**Verify script**: `script/verify/uc5b_plagiarism_problem_definition.py --paper-id <id>`

**Rule**: Independently re-runnable per domain.
