# Use-case 6a — Render Audit Report

**Script**: `generate-audit-report.py` + `render_charts.py` (deterministic)

**Inputs**:
- `academic_score_history` (latest per domain)
- `academic_semantic_runs` (latest per domain)
- `academic_deterministic_findings` (latest per domain)
- `academic_plagiarism_findings` (latest per domain)
- `templates/report/markdown/{deterministic,semantic,summary}.md`
- `templates/report/html/{deterministic,semantic,summary}.html`

**Action**: Score-driven report, not prose-driven. Populate 3 audit report
templates (deterministic, semantic, summary) via chevron.render(),
generate conditionally-selected charts (domain-score-bar always,
score-trend-line if run_count > 1, deterministic-findings-heatmap on any
FAIL, model-agreement-radar if > 1 model). Each template renders both
markdown and HTML.

**Completion criteria**:
- 3 `academic_report_history` rows per format (audit-deterministic, audit-semantic, audit-summary)
- All selected chart images exist on disk

**Rule**: Independent of paper render track. Shares mermaid/PDF mechanics
with render-paper.
