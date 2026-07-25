# Documentation Plan

Orchestration layer for tier-by-tier documentation generation, audit, and fix. Ties together the existing layers without adding new judging or producing logic.

## How it works

1. **Two entry paths** — generate from scratch (Path A) or audit existing docs and fix (Path B)
2. **Tier gate** — domains in a tier run in parallel; no tier advances until every domain in it clears the score threshold (the Acceptable band minimum, resolved at runtime from `score_bands`)
3. **Fix loop** — failing sections get regenerated via the `## Audit Fix` slot in generation templates, re-audited, repeated up to 5 times before flagging for human review

## Files

| File | Purpose |
|------|---------|
| `tiers.yaml` | Domain→tier assignments, relationships, relationship type enum. Transcribed from `00-domain-relationships.md`. |
| `loop.yaml` | Per-domain procedure: path selection, scoring, fix loop, tier gate, special cases. |

## Source of truth

`tiers.yaml` is a transcription of `00-domain-relationships.md` (prose for humans, YAML for the engine). If that file changes, this file changes with it — not independently maintained.

## Scoring

Uses the same `calculation/summary/` formulas and bands as every other layer. Tier gate threshold: **the Acceptable band minimum** (resolved at runtime from `score_bands`). No per-bucket sub-gate.

## Iterations

Max 5 per domain. After 5: flag for human review, gate stays hard (domain doesn't clear until human resolves).

## Within-tier ordering

All domains in a tier run in parallel, except: **External Context completes before Engineering** in Tier 2 (External Context informs Engineering — Engineering's generation needs it as input context).

## Canonical entry point

`script/init.py` is the single-command orchestrator covering the full pipeline:

```
python init.py \
  --system-root <system-dir> \
  --repo-root <repo-dir> \
  --use-case <case> \
  --out-dir <output-dir> \
  [--dry-run]
```

Use cases: `repo_new/case_1_no_documentation`, `repo_new/case_2_has_documentation`,
`repo_existing/case_1_no_documentation`, `repo_existing/case_2_has_documentation`.

`init.py` reads `tiers.yaml` + `loop.yaml`, determines Path A (generate) vs Path B
(audit existing) per domain, and runs the tier-by-tier pipeline automatically.
The individual scripts below are the fallback/debug path — use `init.py` for the
common case.

## Script chain

The pipeline executes these scripts in order per domain. `init.py` calls them
as Python imports (not subprocess); each can also be run standalone via CLI.

| # | Script | CLI | Input | Output |
|---|--------|-----|-------|--------|
| 1 | `scaffold.py` | `--system-root --domain --out` | `templates/generation/document/{d}.md` + `section/{d}/*.md` | `{domain}.md` heading skeleton with TODO markers |
| 2 | `generate_structural_sections.py` | `--system-root [--domain] [--doc] [--out] [--out-dir]` | Template structural section definitions | Constraints, dependencies, etc. injected into doc |
| 3 | *(LLM content-fill)* | — | Scaffolded doc + upstream tier context | Filled doc (TODO markers replaced with prose) |
| 4 | `validate.py` | `--system-root --repo-root --out [--docs-root] [--domain]` | `script/mapping.yaml` check-name scripts | `{domain}-validation.json` |
| 5 | `evaluate_rules.py` | `--system-root --domain --doc --out` | `audit/deterministic/{document,section}/{d}.yaml` | `{domain}-det-eval.json` |
| 6 | `evaluate_semantic.py` | `--system-root --domain --doc --out` | `audit/semantic/{document,section}/{d}.md` | `{domain}-sem-eval.json` |
| 7 | `calculate.py` | `--system-root --domain --out [--out-dir] [--previous-report]` | `calculation/summary/*.yaml` + eval outputs | `{domain}-scores.json` (7 formulas: final_score, score_bands, trend_comparison, etc.) |
| 8 | `analyze.py` | `--system-root --domain --out-dir --out` | `{domain}-scores.json` + `{domain}-validation.json` + eval outputs | `{domain}-fix-plan.json` |
| 9 | `report.py` | `--system-root --domain --scores --out [--type] [--scope]` | `{domain}-scores.json` + `templates/audit/*/` | `{domain}-report.md` |
| 10 | `visualize.py` | `--system-root --results-dir --out-dir [--scores-json]` | Check-result JSONs + scores | 8 PNG charts |
| 11 | `report_html.py` | `--system-root --results-dir --charts-dir --out [--scores-json]` | visualize.py PNGs + all result tables | `{domain}-report.html` |

Optional pre-scripts (run before step 6 when available):
- `gather_semantic_context.py` — `--system-root --domain --out-dir --out` — gathers check metrics as grounding evidence for semantic evaluation.
- `generate_traceability.py` — `--system-root [--domain] [--doc] [--out] [--out-dir]` — generates traceability sections.

## Data flow

```
scaffold.py
  └→ generate_structural_sections.py
       └→ [LLM content-fill]
            ├→ validate.py            → {domain}-validation.json
            ├→ evaluate_rules.py      → {domain}-det-eval.json
            └→ evaluate_semantic.py   → {domain}-sem-eval.json
                 └→ calculate.py      → {domain}-scores.json
                      ├→ analyze.py   → {domain}-fix-plan.json
                      ├→ report.py    → {domain}-report.md
                      ├→ visualize.py → 8 PNGs
                      └→ report_html.py → {domain}-report.html
```

If `final_score < threshold` (from `score_bands`), the fix loop triggers:
`analyze.py`'s fix-plan identifies failing sections, content is re-filled,
and the pipeline re-runs from step 4 (validate) — up to 5 iterations before
flagging for human review.
