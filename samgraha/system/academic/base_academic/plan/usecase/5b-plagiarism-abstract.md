# Use-case 5b-abstract — Plagiarism Forensic Audit — abstract

**Depends on**: `section-budget-fit-abstract` (4d) — same relationship as the pre-split pipeline, scoped to one domain

**Script**: `gather-plagiarism-context` -> `deterministic-fingerprint-check` (det) -> `plagiarism-fingerprint-audit` (prompt) -> `targeted-rewrite` (prompt, conditional) -> `persist-plagiarism-findings`

**Inputs**: `abstract`'s draft, banned phrases, reference corpus

**Action**: Deterministic pre-screen + semantic forensic audit + conditional targeted rewrite for `abstract`.

**Completion criteria** (checked by verify script):
- `SELECT verdict FROM academic_plagiarism_findings WHERE domain_id=(SELECT id FROM academic_domains WHERE key='abstract') AND pass_type='forensic' ORDER BY run_number DESC LIMIT 1` exists

**Verify script**: `script/verify/uc5b_plagiarism_abstract.py --paper-id <id>`

**Rule**: Independently re-runnable per domain.
