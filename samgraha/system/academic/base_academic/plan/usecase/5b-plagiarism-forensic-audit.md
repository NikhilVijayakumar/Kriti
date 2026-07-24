# Use-case 5a — Plagiarism Forensic Audit

**Script**: 5-step per-domain flow —
`gather-plagiarism-context` (det) →
`deterministic-fingerprint-check` (det — burstiness, n-gram repetition,
banned phrases) →
`plagiarism-fingerprint-audit` (sem — hollow-sentence detection,
structural mechanicalness) →
`targeted-rewrite` (sem, conditional — only if step 2 or 3 flagged
any High/Critical) →
`persist-plagiarism-findings` (det)

**Inputs**:
- Current draft for the domain
- `templates/audit/plagiarism-fingerprint.md` (Pass 1)
- `templates/generation/document/targeted-rewrite.md` (Pass 2)

**Action**: Split into deterministic pre-screen (cheap) + semantic
judgment (expensive). Pass 2 is conditional — only runs if prior steps
flagged anything.

**Completion criteria**:
- One `academic_plagiarism_findings` row per (domain, pass_type, check_kind)
- PASS/FAIL verdict + flagged spans present

**Rule**: Runs after assemble-paper-structure. Accumulates per re-run.
