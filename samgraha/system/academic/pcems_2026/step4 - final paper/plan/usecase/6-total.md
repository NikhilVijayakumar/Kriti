# Use-case 6-total — Aggregate and Render Final Report

**Depends on**: All section-domain 5d-humanize-sem-{domain} usecases (6 total)

**Script**: `aggregate-scores` -> `render-paper` -> `validate-pipeline`

**Inputs**: All domain aggregation scores, all domain drafts, `calculation/report/summary/final_score.yaml`, `calculation/report/summary/score_bands.yaml`

**Action**: 
1. Aggregate all domain scores into a final paper score using weighted_merge
2. Apply score bands to determine paper rating
3. Render the final paper in markdown and HTML formats
4. Generate the audit report summarizing all domain findings

**Completion criteria**:
- `SELECT final_score FROM academic_final_scores WHERE paper_id=<id>` IS NOT NULL
- Final paper rendered at `output/papers/{paper_id}/paper.md`

**Verify script**: `script/verify/uc6_total.py --paper-id <id>`

**Rule**: Only runs after all domain pipelines complete. Terminal usecase — no downstream dependents.
