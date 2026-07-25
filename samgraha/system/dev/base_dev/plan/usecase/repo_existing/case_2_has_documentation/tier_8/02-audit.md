# Tier 8 — Audit (Path B)

**Use case:** Existing repo, existing docs
**Path:** B (audit existing documentation — docs already present)

## Domains

- `readme`
- `product-guide`

## Pipeline per Domain

Each domain in this tier follows the Path B pipeline (no scaffold/content phase):

1. **Pre-hook: staleness check** — skip if doc unchanged since last audit
2. **Evaluate rules** (`scripts/evaluate_rules.py`) — evaluate deterministic rules against existing docs
3. **Evaluate semantic** (`scripts/evaluate_semantic.py`) — heuristic semantic criteria evaluation
   - Pre-script: `scripts/gather_semantic_context.py` — gather check metrics as grounding evidence
4. **Validate** (`scripts/validate.py`) — run 18 deterministic check scripts
5. **Calculate** (`scripts/calculate.py`) — compute 4-bucket score from evaluated results
6. **Report** (`scripts/report.py`) — render markdown report
7. **Analyze** (`scripts/analyze.py`) — generate structured fix plan
8. **Visualize** (`scripts/visualize.py`) — generate 8 PNG charts
9. **Report HTML** (`scripts/report_html.py`) — render self-contained HTML report
10. **Fix** (semantic, conditional) — only if score < threshold; modify existing sections

## Tier Gate

All domains in tier 8 must reach `Acceptable` before tier 9 starts.

## Domain-Specific Notes

### readme

- Existing doc detected at `docs/readme.md` or `readme.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### product-guide

- Existing doc detected at `docs/product-guide.md` or `product-guide.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)
