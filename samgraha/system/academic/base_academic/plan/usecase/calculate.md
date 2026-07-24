# Use-case 6 — Calculate

**Depends on**: `semantic-audit` + `deterministic-audit` (all domains scored) +
`cross-section-semantic-audit` + `document-semantic-audit` (both run, for
whole-paper coherence scoring)

**Script**: `calculate.py` (deterministic, single step)

**Inputs**:
- `calculation/summary/final_score.yaml` — weights for semantic, deterministic, and document_coherence
- `calculation/summary/score_bands.yaml` — score → band lookup
- `calculation/summary/trend.yaml` — trend thresholds
- Latest `academic_semantic_runs` + `academic_semantic_dimension_scores` per (paper, domain)
- Latest `academic_deterministic_findings` per (paper, domain)
- Latest `academic_semantic_runs` with scope='cross-section' and 'document'

**Action**: Two-bucket scoring per domain (50/50 semantic + deterministic).
Whole-paper score uses 3-bucket: 40% domain mean + 30% cross-section + 30%
document coherence (falls back to 2-bucket if no cross/doc runs exist).
Writes one `academic_score_history` row per domain + one whole-paper row.
Append-only.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_score_history WHERE paper_id=? AND domain_id IS NULL` >= 1

**Verify script**: `script/verify/uc6_calculate.py --paper-id <id>`

**Rule**: Runs after both audits + cross-section + document audits.
Re-runnable.
