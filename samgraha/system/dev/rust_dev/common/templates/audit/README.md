# Audit Report Templates

Generic, domain-parameterized report templates for the four-report model
(§5 of proposal.md).

## Structure

Report templates live per-tier, next to the audit rules they render. Each
domain's tier is resolved via `common/plan/core/tiers.yaml` (`common/tier{t}` below — see
proposal §5.1):

```
common/tier{t}/templates/audit/
├── deterministic/
│   ├── document/{domain}-report.md    # Whole-document deterministic findings
│   └── section/{domain}-report.md     # Per-section deterministic findings
├── semantic/
│   ├── document/{domain}-report.md    # Whole-document LLM judgment findings
│   └── section/{domain}-report.md     # Per-section LLM judgment findings
└── summary/{domain}-report.md         # Aggregates all four with scoring formula
```

This README sits at `common/templates/audit/` as the single
documentation point for the pattern; the templates themselves live in each
`common/tier{t}/`.

## Template variables

All templates use Jinja2 syntax. Domain-specific values are injected at render
time — the templates themselves are domain-agnostic. Key variables:

| Variable | Used in | Purpose |
|----------|---------|---------|
| `{{ domain }}` | all | Domain name (vision, architecture, etc.) |
| `{{ document_path }}` | all | Path to the audited document |
| `{{ score }}` | detail templates | Report-level score (0–100) |
| `{{ final_score }}` | summary | Aggregated score |
| `{{ rules }}` | deterministic | List of rule evaluation results |
| `{{ findings }}` | semantic | List of LLM judgment findings |

## Scoring formula (summary template)

```
final_score = (deterministic_whole/100 × 25)
            + (deterministic_section/100 × 25)
            + (semantic_whole/100 × 25)
            + (semantic_section/100 × 25)
```

Each report contributes equal weight (25 points). Severity is handled inside
each report's own scoring criteria, not at aggregation.
