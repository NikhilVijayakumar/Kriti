# Tier 3 — Generation (Path A)

**Use case:** New repo, some pre-existing docs
**Path:** A (generate from scratch — no existing documentation)

## Domains

- `feature-design`
- `feature-technical`

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

## Upstream Dependencies

- `external-context` —informs→ `feature-design` (tier-gating: none)
- `external-context` —informs→ `feature-technical` (tier-gating: none)
- `feature` —derives→ `feature-design` (tier-gating: strict)
- `design` —derives→ `feature-design` (tier-gating: strict)
- `feature` —derives→ `feature-technical` (tier-gating: strict)
- `engineering` —derives→ `feature-technical` (tier-gating: strict)
- `architecture` —derives→ `feature-technical` (tier-gating: strict)
- `prototype` —validates→ `feature-design` (tier-gating: strict)
- `prototype` —validates→ `feature-technical` (tier-gating: strict)

## Tier Gate

All domains in tier 3 must reach `Acceptable` before tier 4 starts.

## Domain-Specific Notes

### feature-design

- Scaffold reads `templates/generation/document/feature-design.md` + `templates/generation/section/feature-design/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/feature-design.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### feature-technical

- Scaffold reads `templates/generation/document/feature-technical.md` + `templates/generation/section/feature-technical/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/feature-technical.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends
