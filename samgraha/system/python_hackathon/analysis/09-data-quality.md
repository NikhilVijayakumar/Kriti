# Data Quality Analysis Prompt

Guides the per-team analysis for the Data Quality domain — read by
whichever agent runs it via MCP, after scoring has completed. Explains
how trustworthy a team's data sources are. Not parsed by a script —
this is a prompt.

## Version
1.0.0

## Analysis Intent
Data Quality scores (weight: 10) measure whether a team's datasets
are identifiable, well-sourced, and clearly documented. In ML hackathons,
the model is only as trustworthy as its data. This step interprets
data presence and sourcing evidence.

## Inputs
- `standard_domain_scores` DB table — all teams' data-quality domain
  scores (queried via MCP)
- Per-team deterministic findings: `data/` directory presence, data
  file types and sizes, data-hub URL references (HuggingFace, Kaggle)
- Semantic findings: data collection methodology documentation,
  preprocessing steps, cleaning procedures described in README

## Narrative Guidance
The Data Quality narrative must cover:
1. **Score Overview** — team's data quality score out of 10, with
   competition average comparison.
2. **Data Presence** — is there an identifiable `data/` directory or
   local dataset files? Projects with no visible data are scored
   poorly — where did the model train?
3. **Data Sourcing** — are data sources referenced? HuggingFace hub
   URLs, Kaggle dataset links, or other verified external sources are
   positive signals. Name the sources found.
4. **Methodology Documentation** — does the README or dedicated docs
   explain data collection, preprocessing, and cleaning? Vague or
   missing methodology is a common weakness.
5. **Data File Health** — what formats are the data files in? CSV,
   parquet, JSON? Are file sizes reasonable? Corrupted or placeholder
   files are a critical finding.
6. **Strengths** — clear data directory, verified external sources,
   thorough methodology documentation, clean data files.
7. **Weaknesses** — no data directory, no source attribution, no
   methodology description, data files missing or corrupted, committed
   large binary files without DVC.
8. **Recommendations** — "add a `data/README.md` documenting source
   and preprocessing", "reference the HuggingFace dataset URL in your
   README", "move large data files to DVC tracking".

## Visualization Guidance
- `domain_scores` — always include.
- `data_sources` — include: bar chart of source types (HuggingFace,
  Kaggle, local, unknown) across teams.
- `methodology_coverage` — include: heatmap of methodology documentation
  completeness per team.

## Output Schema
```json
{
  "domain": "09-data-quality",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Data Presence", "text": "..."},
    {"heading": "Data Sourcing", "text": "..."},
    {"heading": "Methodology Documentation", "text": "..."},
    {"heading": "Data File Health", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
