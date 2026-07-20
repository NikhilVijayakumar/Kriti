# Use-case 5 — Markdown + Visualization Generation

**Script**: `run_reporting.py` (calls `render_charts.py` + `render_reports.py` markdown renderer)

**Inputs**:
- Use-case 3's scores + use-case 4's narratives
- `analysis/` rubric files

**Action**:
- `render_charts.py`: 7 chart types -> PNG files
- `render_reports.py`: 32 markdown template files rendered via `chevron`

**Completion criteria**:
- Every expected PNG file exists, non-zero size
- Every expected markdown output file exists: 31 per team (10 domains x {deterministic, semantic, summary} for domains-with-data) + 1 team-final-summary) + 1 shared `global-leaderboard.md`
- No unrendered `{{...}}` Mustache tokens in any markdown file

**Verify script**: `verify_usecase_5_markdown_charts.py --standard python_hackathon`
- File-existence + non-zero-size sweep (derived from registered teams x domains-with-data)
- Grep-style `{{`/`}}` leftover-token check
