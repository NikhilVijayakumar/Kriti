# Use-case 6 — HTML Report Generation

**Script**: `run_reporting.py` (calls `render_reports.py` `render_html_all()`)

**Inputs**:
- Use-case 5's chart PNGs (must exist on disk)
- Same DB data as use-case 5

**Action**: `render_html_all()` produces 31 HTML files per team (30 domain pages + 1 team-final-summary) + 1 shared `global-leaderboard.html`.

**Completion criteria**:
- Every expected HTML file exists, non-zero size
- No unrendered `{{...}}` tokens
- Every `<img src="data:image/png;base64,...">` tag has non-empty base64 payload

**Verify script**: `verify_usecase_6_html_report.py --standard python_hackathon`
- File sweep + leftover-token check (shared helper with use-case 5)
- Regex check for `base64,"` (empty payload) occurrences
