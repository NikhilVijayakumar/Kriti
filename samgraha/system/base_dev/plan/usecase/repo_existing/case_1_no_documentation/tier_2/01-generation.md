# Tier 2 — Generation (Path A)

**Use case:** Existing repo with code, no docs
**Path:** A (generate from scratch — no existing documentation)

## Domains

- `security`
- `feature`
- `architecture`
- `design`
- `engineering`
- `external-context`

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

- `vision` —derives→ `feature` (tier-gating: strict)
- `philosophy` —derives→ `feature` (tier-gating: strict)
- `vision` —derives→ `security` (tier-gating: strict)
- `philosophy` —derives→ `security` (tier-gating: strict)
- `philosophy` —guides→ `architecture` (tier-gating: strict)
- `philosophy` —guides→ `design` (tier-gating: strict)
- `philosophy` —guides→ `engineering` (tier-gating: strict)
- `security` —guides→ `architecture` (tier-gating: strict)
- `security` —guides→ `engineering` (tier-gating: strict)
- `architecture` —soft_aligns_with→ `engineering` (tier-gating: none)
- `external-context` —informs→ `engineering` (tier-gating: none)

## Within-Tier Ordering

- `external-context` must complete before `engineering` starts

## Tier Gate

All domains in tier 2 must reach `Acceptable` before tier 3 starts.

## Domain-Specific Notes

### security

- Scaffold reads `templates/generation/document/security.md` + `templates/generation/section/security/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/security.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### feature

- Scaffold reads `templates/generation/document/feature.md` + `templates/generation/section/feature/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/feature.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### architecture

- Scaffold reads `templates/generation/document/architecture.md` + `templates/generation/section/architecture/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/architecture.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### design

- Scaffold reads `templates/generation/document/design.md` + `templates/generation/section/design/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/design.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### engineering

- Scaffold reads `templates/generation/document/engineering.md` + `templates/generation/section/engineering/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/engineering.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends

### external-context

- Scaffold reads `templates/generation/document/external-context.md` + `templates/generation/section/external-context/*.md`
- Content-fill uses upstream context from completed tiers
- Validate runs against `audit/deterministic/document/external-context.yaml` + section rules
- Score persisted to `score_history.json` for cross-run trends
