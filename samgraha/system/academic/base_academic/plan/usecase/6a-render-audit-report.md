# Use-case 6a — Render Audit Report

**Script**: `generate-audit-report.py` + `render_charts.py` (deterministic)

**Inputs**:
- `academic_score_history` (latest per domain)
- `academic_semantic_runs` (latest per domain)
- `academic_deterministic_findings` (latest per domain)
- `academic_plagiarism_findings` (latest per domain)
- `templates/audit/report/_audit-report-schema.md`

**Action**: Score-driven report, not prose-driven. Populate audit report
template, generate conditionally-selected charts (domain-score-bar always,
score-trend-line if run_count > 1, deterministic-findings-heatmap on any
FAIL, model-agreement-radar if > 1 model). Assemble markdown + charts →
HTML → PDF.

**Completion criteria**:
- One `academic_report_history` row (report_kind='audit') per format generated
- All selected chart images exist on disk

**Rule**: Independent of paper render track. Shares mermaid/PDF mechanics
with render-paper.
