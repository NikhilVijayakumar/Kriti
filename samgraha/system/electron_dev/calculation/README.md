# Calculation Layer

Authoritative source for audit scoring formulas. The engine reads these files to compute scores; templates reference them by ID for documentation only.

## Stable IDs

Each file carries a stable `id` field — the coupling mechanism between templates and calculation specs. Templates reference the ID, not the file path, so neither side breaks if storage moves (e.g. into `help.db`).

| File | ID |
|---|---|
| `deterministic/document.yaml` | `deterministic_document_v1` |
| `deterministic/section.yaml` | `deterministic_section_v1` |
| `semantic/document.yaml` | `semantic_document_v1` |
| `semantic/section.yaml` | `semantic_section_v1` |
| `summary/final_score.yaml` | `final_score_v1` |
| `summary/score_bands.yaml` | `score_bands_v1` |
| `summary/trend.yaml` | `trend_v1` |

Templates point at these IDs in two ways:
- **Inside a code block**: `# calculation: deterministic_section_v1` (after the formula line)
- **Italic caption** (where no code block exists): `*Ratings computed per \`calculation: score_bands_v1\`.*`

## Structure

```
calculation/
├── deterministic/
│   ├── document.yaml    # Whole-document deterministic score
│   └── section.yaml     # Per-section deterministic score + rollup
├── semantic/
│   ├── document.yaml    # Whole-document semantic score
│   └── section.yaml     # Per-section semantic score + rollup
└── summary/
    ├── final_score.yaml # Weighted sum of 4 bucket scores
    ├── score_bands.yaml # Rating thresholds (Excellent → Needs Improvement)
    └── trend.yaml       # Trend detection with float-noise tolerance
```

## Scoring Flow

```
audit/deterministic/document/{domain}.yaml  →  deterministic/document.yaml  ─┐
audit/deterministic/section/{domain}/*.yaml →  deterministic/section.yaml   ─┤
audit/semantic/document/{domain}.md         →  semantic/document.yaml        ─┤→ final_score.yaml → score_bands.yaml
audit/semantic/section/{domain}/*.md        →  semantic/section.yaml         ─┘                  ↓
                                                                                             trend.yaml
```

## Key Design Decisions

- **Generic, not per-domain**: One formula per bucket type; domain-specific inputs come from `audit/` YAML/MD files, not from calculation files.
- **Mandatory = severity, not scoring mode**: A mandatory rule that fails scores 0 for that rule, same as any failed rule. No extra penalty.
- **Unweighted section rollup**: Each section's weighted_pass_rate / sum_capped_at_100 already reflects its own rule weights. The rollup averages across sections present, excluding absent optional sections.
- **Trend tolerance = 0.1 per score**: Prevents float-noise flip-flopping. Applied independently to each of the 5 scored entities (4 buckets + final score).
- **Score bands apply to final_score only**: Individual bucket scores use the same band logic in trend displays but the rating label appears only in the summary report.

## Files

- `deterministic/document.yaml` — id: `deterministic_document_v1`, `weighted_pass_rate` formula for whole-document deterministic scoring
- `deterministic/section.yaml` — id: `deterministic_section_v1`, `weighted_pass_rate` per section + unweighted average rollup
- `semantic/document.yaml` — id: `semantic_document_v1`, `sum_capped_at_100` formula for whole-document semantic scoring
- `semantic/section.yaml` — id: `semantic_section_v1`, `sum_capped_at_100` per section + unweighted average rollup
- `summary/final_score.yaml` — id: `final_score_v1`, `weighted_sum` with 25/25/25/25 equal weights across 4 buckets
- `summary/score_bands.yaml` — id: `score_bands_v1`, `threshold_lookup` mapping scores to rating labels
- `summary/trend.yaml` — id: `trend_v1`, `trend_comparison` with null=baseline, tolerance=0.1
