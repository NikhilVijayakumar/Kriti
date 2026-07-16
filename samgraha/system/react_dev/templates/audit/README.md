# Audit Report Templates

Generic, domain-parameterized report templates for the four-report model
(§5 of proposal.md).

## Structure

```
templates/audit/
├── deterministic/
│   ├── document/         # Whole-document deterministic findings
│   │   └── report-template.md
│   └── section/          # Per-section deterministic findings
│       └── report-template.md
├── semantic/
│   ├── document/         # Whole-document LLM judgment findings
│   │   └── report-template.md
│   └── section/          # Per-section LLM judgment findings
│       └── report-template.md
├── summary/              # Aggregates all four with scoring formula
│   └── report-template.md
└── archive/              # Superseded flat report templates (reference only)
```

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

## Archive

`archive/` contains the old flat report templates (pre-five-model). Kept for
reference on tone, formatting, and section structure. Do not use for new audits.
