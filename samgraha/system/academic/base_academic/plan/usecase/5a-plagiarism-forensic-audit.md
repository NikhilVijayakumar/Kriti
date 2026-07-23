# Use-case 5a — Plagiarism Forensic Audit

**Script**: Per-domain triad — `gather-plagiarism-context` →
`plagiarism-fingerprint-audit` (Pass 1 prompt) → `persist-plagiarism-findings`

**Inputs**:
- Current draft for the domain
- `templates/audit/plagiarism-fingerprint.md` (Pass 1 — forensic audit:
  linguistic fingerprint scan, burstiness score, hollow-sentence detection)
- `templates/generation/document/targeted-rewrite.md` (Pass 2 — targeted
  rewrite of only the sentences Pass 1 flags High/Critical)

**Action (intended design, per
`base_academic-data-pipeline-proposal.md` §9)**: Pass 1 produces a risk
report + per-sentence flags, not a rewrite. Pass 2 rewrites only the
flagged sentences, leaving the rest of the section untouched — cheaper
than a full-section rewrite, escalating to usecase 5b only if Pass 2 isn't
enough.

**⚠ Known implementation gap**: `expand_triads()` in
`run_full_workflow.py` looks up `targeted-rewrite`'s prompt id
(`targeted_prompt = _lookup_prompt_id(con, "targeted-rewrite")`) but never
uses it in the per-domain triad — only 3 steps are inserted per domain
(pre / Pass-1-forensic / post), not the 5 a full Pass-1-then-Pass-2 flow
would need. `targeted-rewrite.md` exists as a template and is registered
as a prompt in `standard.yaml`, but nothing currently dispatches it. Until
`expand_triads()` is extended to insert a second semantic step (conditional
on Pass 1 producing any High/Critical flags) between the forensic step and
the post-script, this usecase only runs Pass 1.

**Completion criteria**:
- One `academic_plagiarism_findings` row per domain per run
  (`pass_type='forensic'` once the gap above is fixed and Pass 2 is wired,
  `pass_type` should distinguish `forensic` from `targeted-rewrite` rows)
- PASS/FAIL verdict + flagged spans present for every structural domain

**Verify script**: `verify_usecase_5a_plagiarism_forensic_audit.py --standard base_academic --paper-id <id>`
- Reports PASS/FAIL per domain
- Exits 0 if every domain has been checked at least once, regardless of
  verdict (FAIL routes to 5b, it isn't itself a failure of this usecase)

**Rule**: Runs after usecase 3 (`deepen-sections`) for every domain — audits
the deepened draft, not the raw generated one. Accumulates per re-run.
