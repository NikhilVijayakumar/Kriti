# Use-case 5c — Humanize

**Depends on**: `plagiarism-forensic-audit` (only for domains with FAIL
verdict after targeted rewrite)

**Script**: Per-domain triad — `gather-humanize-context` → `humanize-section`
(prompt) → `persist-humanize-pass`

**Inputs**:
- Domains with plagiarism FAIL verdicts
- Flagged spans from plagiarism findings

**Action**: Full 3-layer humanize rewrite — triggered only for domains
still above risk threshold after targeted rewrite in 5b.

**Completion criteria** (checked by verify script):
- All flagged domains have >= 1 humanize pass:
  `SELECT DISTINCT domain_key FROM academic_plagiarism_findings WHERE paper_id=? AND verdict='FAIL'`
  — each must have `SELECT COUNT(*) FROM academic_humanize_passes WHERE paper_id=? AND domain_key=?` >= 1

**Verify script**: `script/verify/uc5c_humanize.py --paper-id <id>`

**Rule**: Only runs for domains still flagged after plagiarism forensic audit.
Re-runnable — adds new passes, never overwrites.
