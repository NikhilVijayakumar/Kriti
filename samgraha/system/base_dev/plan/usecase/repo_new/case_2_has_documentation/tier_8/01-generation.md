# Tier 8 — Generation (Path A)

**Use case:** New repo, some pre-existing docs
**Path:** A (generate from scratch — no existing documentation)

## Domains

- `readme`
- `product-guide`

## Pipeline per Domain

Each domain in this tier follows the Path A pipeline:

1. **Scaffold** (`scripts/scaffold.py`) — read template, emit heading skeleton to `{domain}.md`
2. **Content-fill** (semantic) — LLM writes prose per section, filling TODO placeholders
3. **Post-hook: compile** — ingest into knowledge.db (when built)
4. **Evaluate rules** (`scripts/evaluate_rules.py`) — evaluate deterministic rules against document
5. **Evaluate semantic** (`scripts/evaluate_semantic.py`) — heuristic semantic criteria evaluation
   - Pre-script: `scripts/gather_semantic_context.py` — gather check metrics as grounding evidence
6. **Calculate** (`scripts/calculate.py`) — compute 4-bucket score from evaluated results
7. **Report** (`scripts/report.py`) — render markdown report from templates
8. **Analyze** (`scripts/analyze.py`) — generate structured fix plan, save to `{domain}-fix-plan.json`
9. **Visualize** (`scripts/visualize.py`) — generate 8 PNG charts
10. **Report HTML** (`scripts/report_html.py`) — render self-contained HTML report with embedded charts
11. **Fix** (semantic, conditional) — only if score < threshold; re-fill content, re-audit

## Tier Gate

All domains in tier 8 must reach `Acceptable` before tier 9 starts.

## Domain-Specific Notes

### readme

- Scaffold reads `templates/generation/document/readme.md` + `templates/generation/section/readme/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/readme.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### product-guide

- Scaffold reads `templates/generation/document/product-guide.md` + `templates/generation/section/product-guide/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/product-guide.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends
