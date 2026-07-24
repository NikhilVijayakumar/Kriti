# Use-case 6a — Render Charts

**Depends on**: `calculate` (scores must exist before charts can be generated)

**Script**: `render-charts.py` (deterministic, single step)

**Inputs**:
- `academic_score_history` (latest per domain + whole-paper)
- `academic_deterministic_findings` (latest per domain)
- `academic_semantic_runs` (scope='cross-section' and 'document' for new charts)

**Action**: Generate chart images from score/audit data. Always generates
domain-score-bar; conditionally generates score-trend-line (if run_count > 1),
deterministic-findings-heatmap (on any FAIL), cross-section-score and
document-review-score (if those scope runs exist).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_visualizations WHERE paper_id=?` >= 1

**Verify script**: `script/verify/uc6a_render_charts.py --paper-id <id>`

**Rule**: Runs after calculate. Re-runnable — new charts overwrite old ones
via content hash.
