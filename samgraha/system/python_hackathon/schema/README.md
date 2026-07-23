# knowledge.db — python_hackathon's own execution schema

Standard-owned tables that `python_hackathon` reads and writes for its own
scoring/reporting. Catalogued (not created) by samgraha's `custom_data_tables`
table, one row per table here, set at `register_standard` time from
`standard.yaml`'s `custom_tables:` list — see `../scripts/schema/standard.yaml`.

Unlike `/home/dell/PycharmProjects/samgraha/schema/knowledge/*.sql` (samgraha's
own tables, created and migrated by `crates/registry`'s Rust `const`
migrations), samgraha never creates or migrates a *standard's* own tables —
only catalogs that they exist (see that repo's
`schema/knowledge/08-custom_data_tables.sql`). So the files in this directory
are created by a plain idempotent Python script instead of a Rust migration:
`../scripts/schema/init_schema.py`, which runs
`common/hackathon_schema.py`'s `SCHEMA_SQL` (`CREATE TABLE IF NOT EXISTS`,
same discipline) and then seeds the lookup/catalog tables (domains,
templates, visualization types) from the real files on disk.

**No runtime dependency on this directory's `.sql` files** — same as the
samgraha repo's own convention: these are the canonical reference copy of
what `hackathon_schema.py`'s `SCHEMA_SQL` actually creates, kept here so the
shape is readable without opening the Python. If the two ever drift,
`hackathon_schema.py` is the source of truth — update these files to match.

## Design: deterministic and semantic scoring are genuinely different shapes

The two kinds of domain score aren't rows in one table with a `kind`
discriminator column any more — they're properly separate, related by
`team_id`/`domain_id` foreign keys into `hackathon_teams`/`hackathon_domains`:

- **`03-hackathon_deterministic_scores.sql`** — one score per (team, domain),
  written by `audit_*.py` via `common/det_audit.py`.
- **`04-hackathon_semantic_runs.sql`** — one row per (team, domain, **model**)
  — the `ensemble.required_models` list in `audit/semantic/document/*.yaml`
  means several models score the same domain independently. `model` answers
  "which model produced this analysis."
- **`05-hackathon_semantic_dimension_scores.sql`** — each semantic run's
  per-dimension score+evidence, normalized instead of nested JSON — the
  "separate table to save evidence" per model/domain.
- **`06-hackathon_semantic_findings.sql`** — each run's
  strengths/weaknesses/recommendations, one row each.
- **`12-views.sql`**'s `hackathon_semantic_domain_means` — the mean across
  models per (team, domain), as a live `AVG()` over `hackathon_semantic_runs`.
  This is "semantic mean per domain based on model": a SQL aggregate over
  already-stored rows, so it's always answerable without calling an LLM
  again.

## Design: narratives are normalized the same way

**`07-hackathon_narratives.sql`** (one row per narrative-generation run,
`team_id`/`domain_id` nullable for the competition-wide leaderboard
narrative, `model` records who wrote it) + **`08-hackathon_narrative_sections.sql`**
(each `{heading, text}` section as its own row) — replaces storing
`analysis/*.md`'s output as one JSON blob.

## Design: templates and visualizations are catalogued, not just files

**`09-hackathon_templates.sql`** — every file under `templates/reports/
{markdown,html}/`, seeded from the real filesystem. **`10-hackathon_visualization_types.sql`**
— every chart kind `common/render_charts.py` can produce and its scope
(per-team-domain / per-domain / per-team / global), seeded from the real
`chart_*()` functions. **`11-hackathon_visualizations.sql`** — every chart
*actually generated*, so a report step can check "do I already have this
one" (`hackathon_schema.get_visualization()`) before re-rendering.

## The point of all of this: backtrace without re-running semantic analysis

Every semantic result (audit score + dimensions + findings + narrative
sections) is stored in full, normalized, queryable form the first time it's
generated. Regenerating a report, a chart, or a leaderboard is a read from
these tables — it never needs to call a model again, and every number in a
generated report can be traced back to the exact run (and model) that
produced it.

## Read by / written by

**Read by:** `run_calculate.py` / `run_render.py` / `run_html.py` (via
`get_all_scores_as_dict`) to build the leaderboard, markdown/HTML reports,
and charts. **Written by:** `run_hackathon.py` / `run_det_audit.py`
(deterministic scores, team registration), `init_schema.py` (domains/
templates/visualization_types lookup rows), and
`../scripts/schema/persist_domain_semantic_score.py` /
`persist_narrative.py` (the semantic-step post-scripts).

See `../scripts/schema/standard.yaml` for the full usecase/step manifest
these tables serve.
