# python_hackathon — Visualization Catalog + In-Depth Per-Section Templates Proposal

**Proposal 1 of 3, in dependency order** — this defines *what* needs
visualizing and *what depth* the markdown templates need, before
`python_hackathon-report-analysis-proposal.md` (proposal 2, HTML/PDF
design system) picks a visual language for it, before
`python_hackathon-pipeline-verification-proposal.md` (proposal 3)
checks whether scripts exist to actually produce any of it.

**Honest note on sequencing**: this proposal is being written *after*
proposal 2 already exists and after two chart types
(`_chart-field-distribution`, `_chart-rank-distribution`) were already
scoped and prototyped in that proposal's design-demo round. That's out
of the intended dependency order — flagging it rather than pretending
otherwise. What this means practically: proposal 2's already-approved
work isn't invalidated, but §3 below covers what needs revisiting in
it once this proposal's catalog is wider than the 2 chart types it
started with.

---

## 0. Current state

| Piece | State |
|---|---|
| Chart types scoped | 2 — field-distribution (domain-summary), rank-distribution (leaderboard). Both from proposal 2, not from a systematic catalog. |
| Chart-generation script | **None exists.** Both charts today are hand-authored static SVG inside two demo HTML files with hardcoded sample numbers — no function takes real data in and produces a chart out. |
| Markdown template depth | Flat — one row per rule (`{{#each deterministic_rules}}`) or per model (`{{#each model_results}}`), showing `id`/`description`/`passed`/`weight`/`mandatory` or `model_name`/`score`. |
| Evidence computed, passed through, only the template drops it | **Corrected after direct verification** — `evaluate_rules.py`'s `evaluate_domain()` computes `detail` per rule, and `render_reports.py:73`'s `fetch_deterministic_data()` **already** passes it through unchanged (`"deterministic_rules": result["rules"]`, and `result["rules"]` entries already carry `.detail`). The gap is exclusively that no template field reads `{{ this.detail }}` — confirmed by reading `01-infrastructure-deterministic.md` directly, it stops at `mandatory`. Zero data-layer work needed, template-only. |
| Semantic reasoning: same pattern | **Corrected after direct verification** — `render_reports.py:95`'s `fetch_semantic_data()` already reads `evidence.get("reasoning", "")` into every `model_results[]` entry. The gap is the template squeezing it into a Markdown table cell (`01-infrastructure-semantic.md:12`), not a missing field. Template-only here too. |
| `severity` exists in source, dropped one layer up | All 10 `audit/deterministic/document/*.yaml` files carry a `severity: error/warning/info` field per rule (verified: 10/10 files match). `evaluate_rules.py`'s `evaluate_domain()` does **not** extract it — its `rule_results` entries carry `id`/`description`/`passed`/`weight`/`mandatory`/`detail`, never `severity` (verified: zero matches for `"severity"` in that file). Relevant to §1's rule-pass-rate chart below — the richer grouping is available at the source, just not surfaced yet. |

## 1. Visualization catalog — every domain × audit-kind, not just 2 chart types

Systematic pass, same discipline as base_dev's `CHART_CATALOG` (8
named chart types, explicit purpose per type) — not two charts
invented for two specific templates and stopped there.

| Chart | Applies to | Data needed | Purpose |
|---|---|---|---|
| **field-distribution** (existing) | `{domain}-summary` ×10 | `global_stats.{mean,stdev}`, `scores.raw_merge`, `scores.final_domain_score` | This team's score against the field, for one domain |
| **rank-distribution** (existing) | `global-leaderboard` | Per-domain scores, all teams | Where every team sits, per domain, all at once |
| **det-vs-sem contribution** (new) | `{domain}-summary` ×10 | `scores.deterministic`, `scores.semantic`, the 0.60/0.40 weights from `calculation/aggregation/domain/{domain}.yaml` | Visually shows *why* the raw merge landed where it did — a team strong on rules but weak on semantic judgment (or vice versa) looks identical as a single raw-merge number; this chart makes the split visible. Simple split/stacked bar, two segments sized by weighted contribution. |
| **rule-pass-rate breakdown** (new) | `{domain}-deterministic` ×10 | `deterministic_rules[]` **plus a new `severity` field** (see below — not currently in the data) | Not every failing rule costs the same — grouping passed/failed shows at a glance whether failures are cosmetic or structural. A flat table buries this; base_dev's `rule_weights_heatmap` is the direct precedent. **Grouping, corrected**: `severity` (error/warning/info) already exists in every rule's YAML source but is dropped by `evaluate_rules.py`'s extraction — proposing a one-line addition (`"severity": rule.get("severity", "warning")`) to `evaluate_domain()`'s `rule_results.append(...)` rather than falling back to a degraded `mandatory × pass/fail` (4-bucket) grouping that ignores real, already-authored data. Once added, group by `severity × passed` (up to 6 buckets). |
| **model-score spread** (new) | `{domain}-semantic` ×10 | `model_results[]` (already fetched — one row per model) | A dot-plot or small bar-per-model chart of the N semantic scores for *this* domain/team, with the `mean_score` and `agreement_level` band overlaid — makes "3 models mostly agreed, 1 was an outlier" visible instead of requiring the reader to eyeball a 2-4 row table. **Minimum-data guard**: skip the chart (show only the existing `model_results[]` table) when fewer than 3 models have run for this (participant, domain) — a dot-plot of 1-2 points is noise, not signal, and this matches §5's "accumulates over multiple agent sessions" reality where partial ensembles are the normal early state, not an edge case. |
| **team domain-profile radar** (new) | `team-final-summary` ×1/team | All 10 domains' `final_domain_score` for one team — **as a list, not 10 scalars** (see below) | Base_dev precedent: `chart_scoring_radar`. A 10-spoke radar shows a team's shape — "strong on runtime/testing, weak on documentation/data-quality" — legible in one glance, where the existing flat 10-row score table requires reading every row to form the same impression. **Data-shape note**: `render_reports.py`'s `fetch_team_summary_data()` currently builds `scores` as a dict of 10 named scalar fields (`scores.infrastructure`, `scores.engineering`, ...) for the flat table — the radar chart *function* (matplotlib, `render_charts.py` — not a template partial) needs an iterable `[{domain, score}, ...]` list to loop over. Small additive change: emit both shapes from the same fetch function, not a breaking change to the existing flat fields. |
| **domain-weight breakdown** (new) | `global-leaderboard` — **placement reconsidered, see note** | `weights.yaml`'s 10 domain weights | Shows *why* the leaderboard is shaped the way it is — runtime (weight 15) moving a team's rank matters more than documentation (weight 5) doing the same. **Placement note**: `weights.yaml` is static config — identical for every team, every run, not per-run competition data. Two real options, not obviously resolved either way: (a) `global-leaderboard` — the *one* shared page, so a static chart appears exactly once total, cheapest; (b) `team-final-summary` — gives each team direct context for their own rank, but duplicates the identical static chart once per team's PDF (N copies of the same data). Leaning (a) for the duplication-cost reason, clearly labeled as "scoring methodology" rather than "this run's results" so it doesn't read as competition data — flagged as an open question (§4) rather than decided unilaterally, since "avoid duplicating static data N times" and "give each team direct context" are both real, competing considerations. |

7 chart types total (2 existing + 5 new), not 2. Each maps to exactly
one template kind — no chart is shared across template kinds, unlike
proposal 2's original 2-chart scope where both charts were already
template-specific.

## 2. In-depth per-section markdown templates

**The gap, concretely**: `evaluate_rules.py` (already built, per
proposal 2's report-analysis proposal §4) computes a `detail` string
for *every* rule on *every* run — human-readable evidence like
`"uv.lock: present"` or `"radon_high_complexity_count: 3 (threshold: 5)"`.
None of the 32 markdown templates render it. A judge reading
`{domain}-deterministic.md` today sees a rule passed or failed and its
weight — not *why*, even though the *why* is already sitting in the
data, computed, and simply not passed through.

**Proposed fix — one new per-rule detail block, reused across all 10
`{domain}-deterministic.md` templates** (Mustache section, not a
redesign of the table — additive):

```
{{#each deterministic_rules}}
### {{ this.id }} — {{ this.description }}
**Status:** {{ this.passed }} · **Weight:** {{ this.weight }} · **Mandatory:** {{ this.mandatory }}

{{ this.detail }}
{{/each}}
```

Same fix, same shape, for `{domain}-semantic.md`'s `model_results[]`
— currently shows `model_name`/`score`/`reasoning` as a flat table
row; `reasoning` is confirmed to already be the model's real
explanation text (verified in §0, not truncated or dropped). The fix
is specifically: keep the existing summary table for `model_name`/
`score` (still useful as a scan-first row), then add a `{{#each
model_results}}` block below it — same pattern as the deterministic
fix above, not a table-cell workaround (Markdown tables don't render
multi-line prose well; `<pre>`/blockquote-in-a-cell was considered and
rejected for that reason):

```
{{#each model_results}}
#### {{ this.model_name }} — {{ this.score }}/100
{{ this.reasoning }}
{{/each}}
```

**Why this is "per section per domain" and not a blanket template
rewrite**: the fix is identical in *shape* across all 10 domains (loop
over rules/models, show detail/reasoning) but the *content* is
naturally per-domain, since each domain's rules and evidence strings
are different — no domain-specific template logic needed, just making
sure the data that's already domain-specific (the `detail` strings)
actually reaches the page.

## 3. Impact on already-built pieces (corrected — data layer needs
   zero changes, this is template-only)

An earlier draft of this section hedged ("needs confirming/extending")
on whether `fetch_deterministic_data()`/`fetch_semantic_data()` pass
`detail`/`reasoning` through. Directly verified now (§0): **both
already do, unchanged, no extension needed.** Correcting rather than
leaving the hedge in place:

- `render_reports.py`'s `fetch_deterministic_data()` — **zero changes
  needed.** `deterministic_rules[]` already carries `.detail` per rule.
- `render_reports.py`'s `fetch_semantic_data()` — **zero changes
  needed.** `model_results[]` already carries `.reasoning` per model.
- `evaluate_rules.py`'s `evaluate_domain()` — **one real change**:
  add `severity` to each `rule_results` entry (§1's rule-pass-rate
  chart needs it; nothing today extracts it despite it being present
  in every rule's YAML source).
- `render_reports.py`'s `fetch_team_summary_data()` — **one small
  additive change**: emit the list-shaped domain scores §1's radar
  chart needs, alongside the existing flat scalar fields (not a
  replacement, both shapes coexist).
- The 32 markdown templates — 10 `{domain}-deterministic.md` files
  gain the detail-block section above; `{domain}-semantic.md` files
  get `reasoning` given room; the other 3 template kinds
  (`{domain}-summary`, `team-final-summary`, `global-leaderboard`)
  are unaffected by this proposal, only by §1's new charts.
- Proposal 2's chart scope (2 types) — extends to 7 (§1). Its already-
  written §10 sections for the 2 existing charts don't need conceptual
  rework, just the addition of 5 more chart rows to its table — and,
  per the pipeline-verification proposal's later §6 resolution, all 7
  (not just the 5 new ones) are matplotlib-generated PNG files, not
  HTML/Mustache partials as an earlier draft of both documents assumed.

## 4. Open questions for confirmation

1. §1's domain-weight breakdown chart placement — `global-leaderboard`
   (shown once total, cheapest, recommended) or `team-final-summary`
   (duplicated once per team's PDF, but gives each team direct
   context for their own rank)? Real tradeoff, not decided here.

## 5. Verification checklist

- [ ] §1 — all 7 chart types have a named function in `render_charts.py`
      planned (2 existing + 5 new: `chart_det_sem_contribution`,
      `chart_rule_pass_rate`, `chart_model_spread`, `chart_team_radar`,
      `chart_domain_weights`), each producing a PNG file (matplotlib,
      per the pipeline-verification proposal's §6 resolution — **not**
      an HTML template/partial, corrected here from an earlier draft
      of this checklist that still named `.html` chart-partial files),
      each mapped to exactly one template kind, each with its edge-case
      behavior specified (model-spread's <3-model skip; empty-data /
      single-team cases don't crash the renderer, they degrade to
      "not enough data" same as §7 of the report-analysis proposal's
      missing-domain handling).
- [ ] §1 — `evaluate_domain()` surfaces `severity` per rule (new,
      one-line change); rule-pass-rate groups by `severity × passed`,
      not the degraded `mandatory × passed` fallback.
- [ ] §1 — `fetch_team_summary_data()` emits list-shaped domain scores
      alongside the existing flat fields, for the radar chart.
- [ ] §2 — confirmed (not just asserted) that `detail`/`reasoning` are
      already present in `fetch_deterministic_data()`/
      `fetch_semantic_data()`'s output — §3 states this is
      template-only work, zero data-layer changes.
- [ ] §2 — all 10 `{domain}-deterministic.md` templates render the
      per-rule detail block; all 10 `{domain}-semantic.md` templates
      give `reasoning` a `{{#each}}` block below the summary table,
      not a table cell.
- [ ] §3 — proposal 2 (`python_hackathon-report-analysis-proposal.md`)
      §9/§10's template tables are updated to reference this
      proposal's 7-chart catalog, not the original 2.
- [ ] Mechanism check — **corrected, this item is now moot.** An
      earlier draft of this checklist asked whether `chevron`'s
      Mustache-partials support (`{{> chart_name}}`) was confirmed
      working, on the assumption charts would be Mustache partials.
      That assumption was dropped once matplotlib/PNG was decided
      (report-analysis-proposal.md §10, pipeline-verification-proposal.md
      §6) — charts are generated files, not template markup, so there's
      no partials mechanism to verify. `chevron` only still matters for
      `{{> design_tokens}}` (colors/type/spacing), which is unaffected.
- [ ] File count after this proposal: 32 markdown templates (unchanged,
      **never gain charts** — markdown stays text-only, per the
      confirmed pipeline design) + `render_charts.py`'s 7 chart
      functions (new, produce PNG files, not template files) — not
      "39 template files," that count no longer applies.
