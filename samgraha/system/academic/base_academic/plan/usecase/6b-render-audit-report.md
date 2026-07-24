# Use-case 6b — Render Audit Report

**Depends on**: `render-charts` (chart images must exist before report
templates can embed them)

**Script**: `generate-audit-report.py` (deterministic)

**Inputs**:
- `academic_score_history` (latest per domain)
- `academic_semantic_runs` (latest per domain)
- `academic_deterministic_findings` (latest per domain)
- `academic_plagiarism_findings` (latest per domain)
- `templates/report/markdown/{deterministic,semantic,summary}.md`
- `templates/report/html/{deterministic,semantic,summary}.html`

**Action**: Score-driven report. Populate 3 audit report templates
(deterministic, semantic, summary) via chevron.render(). Each template
renders both markdown and HTML.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_report_history WHERE paper_id=? AND report_kind LIKE 'audit-%'` >= 6
  (3 sub-reports × 2 formats)

**Verify script**: `script/verify/uc6b_render_audit_report.py --paper-id <id>`

**Rule**: Runs after render-charts. Independent of paper render track.
