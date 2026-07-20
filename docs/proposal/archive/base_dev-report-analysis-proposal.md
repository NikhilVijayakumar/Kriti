# base_dev — Report-Time Semantic Analysis + Visualization Plan Proposal

Adds one new *scripted* stage and one new *agent-driven* stage between
`calculate.py` and `report.py`: a **deterministic analysis** step
(`analyze_trend.py`, multi-window trend, reusing the existing
`score_history.json`) and a **semantic analysis** step — not a Python
script. The semantic step is triggered by the user, performed by
whichever agent has MCP access, guided by a rubric file per domain
under `analysis/` — a top-level directory, sibling to `audit/`/`plan/`/
`script/`, not nested inside `audit/` (kept out of `audit/` deliberately:
this step doesn't score anything, `audit/`'s job) — mirroring the
*structure* of the existing `audit/semantic/document/` rubrics, not
their location. The agent reads the deterministic
JSON, writes narrative + viz-plan files directly, and calls
`audit_fix_plan` directly for findings worth a DB fix plan — no client
library needed, the agent already speaks MCP. `visualize.py` and
`report_html.py` run after, both post-script. The rendered report/HTML
never includes fix-plan content — that's DB-only, retrieved separately.

No samgraha MCP-side changes needed — `audit_fix_plan` already exists,
already writes to DB, and already generates the plan content itself
server-side (see §5).

Revised after three rounds: a pass against `crates/registry/src/migration.rs`
(samgraha's schema) found the fix-plan design already matched what's
built; a pass against `init.py`/`report.py`/`visualize.py` found the
archive design duplicated an existing mechanism; a third pass replaced
the originally-proposed `analyze_semantic.py` script (and its
speculative stdio JSON-RPC client) with an agent-driven, rubric-guided
step — since the actor invoking this step is, by construction, already
an MCP client. All three corrections are folded in below.

---

## 1. Problem

`visualize.py` always emits the same fixed 8 charts regardless of what
the audit found. `report_html.py` embeds those charts plus raw tables —
no written analysis, no historical trend beyond one-step, no "here's
what matters and why." Nothing looks at the data and decides what's
relevant.

Existing `analyze.py` (phase 8, pre-report) is a **different**,
unchanged concern: it produces the fix-plan that drives the *fix loop*
gate (tier can't advance until it clears). This proposal's fix-plan
trigger is separate — semantic, for human review, generated after the
report data exists — not a gate mechanism.

## 2. Hard constraint

**The semantic analyzer never looks at images.** It reads only text/JSON
(scores, findings, trend data). Charts are generated *after* the
analyzer runs and are for the human reading the HTML report — not an
input to any automated judgment. Keeps the analyzer deterministic-input
and keeps chart generation a pure rendering step with no judgment logic
of its own.

## 3. Pipeline change

Two new steps inserted between `calculate.py` (phase 6) and
`report.py` (phase 7) in `init.py`'s per-domain loop:

| Phase | Script | Input | Output |
|---|--------|-------|--------|
| 6 | `calculate.py` (unchanged) | eval outputs | `{domain}-scores.json`; `init.py` already appends it to `score_history.json` (`append_score_history()`, `init.py:110-143`) before this |
| **6.5 (new)** | `analyze_trend.py` | `{domain}-scores.json` + **existing** `score_history.json` (via `load_score_history()`, already imported by `init.py`) | `{domain}-trend.json` — extends the single-step trend `calculate.py` already computes, adds two more windows |
| **6.6 (new, agent not script)** | user triggers; agent reads `analysis/{domain}.md` rubric | scores + trend + validation/det-eval/sem-eval findings | agent writes `{domain}-narrative.json` + `{domain}-viz-plan.json` directly; calls `audit_fix_plan` per selected finding directly (not a file, not a script) |
| 7 | `report.py` (modified) | scores + trend + narrative | `{domain}-report.md` — appends trend/analysis after existing template/fallback content; **no fix-plan content** |
| 10 | `visualize.py` (modified) | check results + scores + **`--viz-plan`** | PNG charts, filtered to the plan's selection (§6) |
| 11 | `report_html.py` (modified) | report.md/PNGs/narrative | `{domain}-report.html`; **no fix-plan content** |

(Phase numbers match `init.py`'s existing comments — Phase 8 `analyze`/
fix-loop and Phase 9 sit between 7 and 10 unchanged, per §1.)

## 4. `analyze_trend.py` (6.5) — deterministic analysis

**No new archive file.** `init.py` already has one:
`append_score_history()` / `load_score_history()` (`init.py:110-153`),
writing a single shared `score_history.json` (JSON array, all domains
together), called right after `phase_calculate()`
(`init.py:568-575`). An earlier draft of this proposal invented a
separate `{domain}-history.jsonl` per domain — that would have been a
second, competing archive. Dropped. `analyze_trend.py` reads the
existing file, doesn't write it.

`calculate.py`'s `trend_comparison(current, previous, tolerance)`
(`calculate.py:184-210`) already gets called once, against the single
most recent history entry, inside `phase_calculate()`
(`init.py:254-264`) — that's today's `vs_last_run`, already shipped.
`analyze_trend.py` adds the two windows that don't exist yet, calling
the *same* function against different `previous` values pulled from the
*same* history list — pure reuse, no signature change needed:

```
python analyze_trend.py --system-root <path> --domain <domain> \
  --scores <{domain}-scores.json> --history <score_history.json> \
  --out <{domain}-trend.json>
```

```json
{
  "formula": "trend_v2",
  "vs_last_run":    {"delta": 3.5,  "direction": "improving"},
  "vs_last_3_runs": {"delta": 9.0,  "direction": "improving", "runs_compared": 3},
  "vs_baseline":    {"delta": 21.5, "direction": "improving", "baseline_timestamp": "2026-06-01T09:00:00Z"}
}
```

- `vs_last_run` — recomputed here too (cheap, keeps `{domain}-trend.json`
  self-contained) but identical to what `scores["trend"]` already holds.
- `vs_last_3_runs` — compares against the entry 3 runs back in this
  domain's filtered history (`domain_history[-3]`), not an average.
  Simpler, still reuses `trend_comparison()` unmodified.
  `runs_compared` < 3 when fewer than 3 prior entries exist for this
  domain — stated explicitly, not assumed.
- `vs_baseline` — compares against `domain_history[0]`.
- Empty/short history → falls back to `"baseline"` direction, matching
  `trend_comparison()`'s existing no-previous behavior.

**One small addition needed**: `append_score_history()`'s entry shape
(`init.py:122-132`) has no `model` field. Add one line — see §7.

**Why a file, not a samgraha DB table.** Same reasoning as before,
now pointed at the *existing* file: a DB table for this would have to
be either domain-named/domain-shaped (repeats the coupling mistake
`vision_reports`/`architecture_reports`/etc. already made — base_dev
renames a domain, samgraha's schema has to follow) or genuinely
generic, matching `standard_audit_runs`/`summary_reports`'s
`target_type`/`target_name`-as-data pattern. Per the knowledge-hub
README's own rule: *"Nothing names a domain... everything specific is
a row, never a table or column."* `score_history.json` already
satisfies "generic" by construction — samgraha's schema stays
completely unaware base_dev's domains exist. Stays a file.

## 5. Semantic analysis (6.6) — agent-driven, not a script

**Not `analyze_semantic.py`.** Earlier drafts of this proposal made
this a Python script and then had to invent a way for that script to
reach `audit_fix_plan` (a stdio JSON-RPC client shelling out to the
samgraha MCP binary). Wrong layer: the thing that should perform
semantic judgment and call MCP tools is whatever agent the user is
already driving this pipeline through — it's already an MCP client by
definition. No script, no new client code, no binary-path question
(closes old open-question #3 for free).

**Mechanism**: one rubric file per domain,
`analysis/{domain}.md`, mirroring the structure of the
existing `audit/semantic/document/{domain}.md` audit rubrics — same
document shape (Version / Intent / Objectives-equivalent / Guidance /
Output Schema), so the pattern is familiar to anyone who's read the
audit rubrics, but read by an agent as a prompt, not parsed by a
script as rules. Example built as part of this proposal:
`analysis/01-vision.md`. Rolling out the other 15
(§14) is implementation work, not a design question — the template is
settled once one is reviewed.

**Trigger**: the user asks for it, per domain or per tier, once
`analyze_trend.py` (6.5) has produced `{domain}-trend.json` for that
domain. Not part of `init.py`'s automated per-domain loop (§12) — it's
a deliberate, on-demand step, same way `mcp__samgraha__audit`'s own
doc-audit path already works: the tool bundles `semantic_review.tasks`
and the *calling agent* judges them and reports back via
`store_section_report`, rather than the tool judging itself. This
step follows that same shape: bundle inputs (already at known paths,
§4's rubric documents exactly which), agent judges, agent writes the
outputs.

**What the agent reads** — same three sources every domain's rubric
names: `{domain}-scores.json`, `{domain}-trend.json`, and this run's
findings (`{domain}-validation.json`/`-det-eval.json`/`-sem-eval.json`
— same sources `analyze.py`'s `analyze_findings()` already reads, kept
consistent rather than reimplemented).

**What the agent writes** — directly, via its own file-write
capability, no intermediate script:

`{domain}-narrative.json` — structured, not raw markdown (avoids a
markdown-to-HTML converter or new dependency for one section —
`report_html.py` already renders JSON→HTML directly for every other
section):

```json
{
  "domain": "01-vision",
  "sections": [
    {"heading": "Summary", "text": "Score 71.5 (Good), improving — up 3.5 vs last run, 9.0 over last 3 runs, 21.5 since baseline."},
    {"heading": "Key Risks", "text": "3 mandatory semantic criteria failing in 'problem' and 'solution' sections."}
  ]
}
```

`{domain}-viz-plan.json` — which charts from the catalog (§6) are
relevant this run:

```json
{
  "domain": "01-vision",
  "charts": ["domain_scores", "section_heatmap"],
  "focus_sections": ["problem", "solution"],
  "reason": "rule_weights_heatmap skipped — no rule-weight variance this run"
}
```

**Fix-plan trigger — called directly, not written to a file.**
`mcp__samgraha__audit_fix_plan`'s own schema takes only
`finding`/`domain`/`report_id`/`report_type`/`target_path` — no
`steps`/`title`/`summary` fields. That means samgraha generates the
plan *content* itself, server-side, from the finding — this step's
actual judgment call is narrower than "author a phase-by-phase plan":
**which findings are worth a DB fix plan** (skip trivial ones,
prioritize high-impact ones, don't re-trigger one already open — the
per-domain rubric's "Fix-Plan Trigger Criteria" section states the
domain-specific bar). The phase-by-phase detail (`fix_plan_steps`:
action, target, rationale, detail, verification, rollback —
`migration.rs:816-829`) is produced by samgraha, not authored here.
The agent calls `audit_fix_plan` once per selected finding, directly,
the same way it would call any other MCP tool mid-task:

```
audit_fix_plan(
  finding=<finding object>,
  domain="01-vision",
  report_id=<01-vision-trend.json's run timestamp — bookkeeping-only
             per the tool's own description, ISO-8601 is already
             unique and traceable, no hash needed>,
  report_type="documentation-tier-analysis",
  target_path=<vision doc path>,
)
```

Retrieval (`audit_fix_plan_get` / `audit_fix_plan_render`) is a
separate, later, on-demand action — not part of this step's output,
and not embedded in the HTML report.

## 6. `visualize.py` change — chart catalog + `chart_tier_progression` fix

Today: 8 charts, always all of them, called per-domain via
`phase_visualize()` (`init.py:363-377`), which only has that domain's
`out_dir` — it never sees other domains' data.

```
python visualize.py --system-root <path> --results-dir <path> --out-dir <path> \
  --scores-json <path> --viz-plan <{domain}-viz-plan.json>
```

`generate_all_charts()` filters its existing chart-function list down
to `plan["charts"]` when given; runs all of them (current behavior)
when it isn't.

**Chart name mapping** — the 8 functions (`visualize.py:151-552`:
`chart_check_results_by_domain`, `chart_category_breakdown`,
`chart_rule_weights_heatmap`, `chart_scoring_radar`,
`chart_score_bands`, `chart_domain_scores_bar`,
`chart_section_pass_rate_heatmap`, `chart_tier_progression`) don't
1:1 match the viz-plan's shorthand names (`domain_scores`,
`section_heatmap`, etc., used in §5/`01-vision.md`). Needs one small
`CHART_CATALOG = {"domain_scores": chart_domain_scores_bar, ...}` dict
in `visualize.py` that `--viz-plan` filtering looks up against —
translation only, no chart logic changes.

**`trend_history` is new work, not a filter.** §5/`01-vision.md`
reference a `trend_history` chart ("include once `runs_compared >= 3`")
that doesn't exist yet — no `chart_trend_history()` function is in
`visualize.py` today. It's the one genuinely new chart in this
proposal (reads `score_history.json`, same data `analyze_trend.py`
already reads) — everything else is selecting among charts that
already exist.

**Correction**: `chart_tier_progression` (`visualize.py:503-552`) reads
`all_domain_scores` — cross-domain data. Called from per-domain
`phase_visualize()`, it silently only sees one domain and produces a
near-empty chart. Moves out of the default per-domain catalog, only
generated from the system-scope step (§10) — which by then has
`results.json` (`init.py:858`, written once after all tiers complete,
already contains every domain's scores) to pass as `--scores-json`.
No new data-loading path needed, just pointing at a file that already
exists by that point in the run.

## 7. Model attribution

Add a `model` field to `append_score_history()`'s entry shape
(`init.py:122-132`) — one line, populated from `evaluate_semantic.py`'s
own `model` stamp (currently a fixed string like today's
`formula: "trend_v1"` convention, since only heuristic evaluation
exists; becomes a real model id once LLM-based semantic evaluation
replaces the heuristic, already flagged as future work in that file's
docstring). Flows: `evaluate_semantic.py` → `calculate.py`'s output →
`append_score_history()`'s entry — one hop further than it goes today,
into a field that already exists as a call site (`init.py:575`), not a
new file.

Separate from and doesn't conflict with samgraha's own `audit` tool
`model` param (tags samgraha's *own* audit runs) — this tracks which
model ran *this* system's `evaluate_semantic.py`/`analyze_semantic.py`
steps.

**Grouped-by-model view**, computed from `score_history.json`, added to
the narrative (§5) rather than a new score bucket:

```json
{
  "by_model": {
    "heuristic-v1": {"runs": 12, "score_range": [45, 71], "latest": 71},
    "claude-sonnet-5": {"runs": 2, "score_range": [88, 91], "latest": 91}
  },
  "overall_trend": {"delta": 21.5, "direction": "improving"}
}
```

`vs_baseline`/`overall_trend` (§4) always span the full history
regardless of model — one number that answers "are we actually
improving" even after an evaluator swap.

## 8. `report.py` change — where trend/narrative actually go

The gap the first draft left open: `render_report()` either fills a
template (`substitute_template()` — simple `{{path}}` lookups, no
loops) or falls through to `_generate_fallback_report()`
(`report.py:108-196`, procedural markdown). Neither has a slot for a
list of narrative sections.

Resolution: **append, don't extend the template engine.** A new
`render_trend_and_narrative(trend, narrative) -> str` function builds a
markdown block:

```markdown
## Trend

| Window | Delta | Direction |
|---|---|---|
| vs last run | +3.5 | improving |
| vs last 3 runs | +9.0 | improving |
| vs baseline | +21.5 | improving |

## Analysis

### Summary
Score 71.5 (Good), improving — up 3.5 vs last run...

### Key Risks
3 mandatory semantic criteria failing...
```

`phase_report()` (`init.py:279-312`) appends this after each of the 4
existing report variants (det-doc/det-sec/sem-doc/sem-sec), when
`{domain}-trend.json`/`{domain}-narrative.json` exist. No change to
`substitute_template()` or the fallback generator — both keep working
exactly as today when the new files don't exist (e.g. an old run, or a
domain where 6.5/6.6 were skipped).

## 9. Tier-by-tier report structure

`report_html.py` currently builds one flat page per domain — no tier
grouping. Restructure around `plan/core/tiers.yaml` (move
`visualize.py`'s existing `_load_tiers()` to `_common.py` so both
scripts share it):

```
For each tier in tiers.yaml (in order):
    Render "Tier N — {domain, domain, ...}" heading
    For each domain in that tier:
        If {domain}-report.md / -scores.json / -narrative.json exist:
            render narrative → charts → tables, in that order
            (narrative first: "what this means" before "the raw data")
        Else:
            render "Not available" — this tier/domain hasn't run yet
```

TOC: Tier 1 … Tier 8, then Final Summary (§10). A partial pipeline run
still renders a complete page; later tiers say "Not available" instead
of the report failing to build.

## 10. Final summary (always present)

Same agent-driven mechanism as §5, one more level up: after the last
tier completes, the user triggers a **system-scope** pass, guided by a
system-level rubric (`analysis/00-summary.md` —
implementation work, §14, not yet written), reading every domain's
`score_history.json` entries (already all in the one shared file)
instead of one domain's. Same output shapes as §5, wider input, plus:

- Tier/system-level trend/model rollups (§4/§7) — same aggregation
  shape, wider `domain` filter on the same `score_history.json`, not a
  new data source.
- `chart_tier_progression` (§6) generated here — this is the first
  point with real cross-domain data.
- Tier/system-level fix-plan triggers via `audit_fix_plan`, called
  directly by the agent (§5) — same call, wider scope, not a new
  mechanism.

If some tiers are missing (partial run), the summary says so explicitly
("Tiers 4–8 not yet run; summary covers Tiers 1–3 only") instead of
silently scoring on partial data. Always renders — even a zero-tier run
gets "nothing audited yet."

## 11. Report page aesthetics — design skills

Two separate concerns, two skills, at implementation time (not part of
this proposal's data/pipeline design):

- **`huashu-design`** — overall HTML page layout/theme (tier sections,
  summary, navigation). Its own workflow drafts 3 directions before
  picking one — follow that when the template gets built.
- **`dataviz`** — palette/mark-spec rules for the matplotlib charts
  (`visualize.py`'s `COLORS`/`DOMAIN_COLORS`), so charts and page theme
  read as one system.

Neither changes the data model in §3–10 — only how the same JSON/PNGs
get styled once rendered.

## 12. `init.py` wiring

Concrete touch points, all additive:

- `phase_calculate()` — no change (already writes `score_history.json`,
  §4). `append_score_history()` gains the `model` field (§7).
- New `phase_analyze_trend()` only, called between the existing
  `phase_calculate()` call (`init.py:569`) and `phase_report()` call
  (`init.py:579`). **No `phase_analyze_semantic()`** — §5/§10 aren't
  scripts, so there's nothing for `init.py` to call there; the
  automated loop simply produces `{domain}-trend.json` and stops
  short of narrative/viz-plan, same as it already stops short of
  anything requiring a human decision.
- `phase_report()` (`init.py:279-312`) — pass trend path through,
  append the Trend table (§8) unconditionally. The Analysis section
  only appends once `{domain}-narrative.json` exists — i.e. reports
  generated before the agent-driven step runs just won't have it yet,
  same "if exists" pattern as everything else in this proposal.
- `phase_visualize()` (`init.py:363-377`) — pass `--viz-plan` when
  `{domain}-viz-plan.json` exists; unchanged (all 8 charts) otherwise.
  Drop `chart_tier_progression` from its default set (§6).
- `phase_report_html()` — pass narrative path (same if-exists
  handling); no reorder needed, it already runs after
  `phase_visualize()` (`init.py:631-637`).
- No system-scope call added to `init.py` — §10's final summary is
  triggered by the user the same way §5 is, after the loop finishes,
  not wired into the automated pipeline.

**Confirming intentionally**: the automated `init.py` loop produces
`{domain}-trend.json` and stops — narrative/viz-plan don't exist until
the user separately triggers §5 for that domain. A report generated
right after an automated run (`phase_report()` fires immediately after
`phase_analyze_trend()`, before any human/agent has looked at it) will
have the Trend table but no Analysis section, and its HTML will have
charts but no narrative — by design, not a bug to fix later. The
"if exists" handling in §8/§9 is what makes that a normal, expected
state rather than a broken one.

## 13. Test strategy

No test framework exists anywhere in `system/base_dev/script/` today —
every script's "test" is its `main()` printing a summary
(`evaluate_semantic.py`, `analyze.py`, etc. already do this). Match
that convention: `analyze_trend.py` prints a summary after writing
output, same as every sibling script. It's the only new script (§5's
step has no script to test — its "test" is whether the rubric produces
a narrative a human agrees with, a review concern for §14, not a unit
test concern). `analyze_trend.py`'s window-comparison logic should have
one `assert`-based sanity block behind `if __name__ == "__main__"`,
matching the bar every non-trivial function in this codebase should
already clear, framework or not.

## 14. Implementation priority

1. `analyze_trend.py` — self-contained, reuses `score_history.json` +
   `trend_comparison()` as-is, no dependency on §5.
2. `analysis/01-vision.md` (already written as part of
   this proposal) — review it as the template, then author the
   remaining 15 domain rubrics (§5) mirroring
   `audit/semantic/document/`'s file list, plus one system-level
   rubric (`00-summary.md`, §10). **Largest single piece of work
   here** — ~100 lines/domain like `01-vision.md` × 15 + the
   system-level rubric, ~1500 lines of domain-specific prose. Template
   is settled once `01-vision.md` is reviewed; the rest is authoring,
   not design.
3. `visualize.py` — `--viz-plan` flag + catalog filter + drop
   `chart_tier_progression` from the default set.
4. `report.py` — append trend/narrative block (§8).
5. `report_html.py` — tier restructuring + narrative placement (§9).
6. `init.py` — wire `analyze_trend.py` + the if-exists narrative/viz-plan
   handling together (§12), last, once every piece it calls is stable.

## 15. Out of scope

- Does not touch `analyze.py` / the tier-gate fix loop / its fix-plan
  format — that stays exactly as-is (§1).
- Does not add an LLM call inside `visualize.py` or `report_html.py` —
  those stay pure renderers; the LLM/agent involvement is entirely in
  the on-demand §5/§10 step, never inside the automated `init.py` loop.
- No samgraha MCP-side changes — `audit_fix_plan` and friends called
  directly by the agent, as designed, no new client code (§5).
- Does not change the 32 usecase `.md` docs; can note the new optional
  phase 6.5 and the on-demand §5/§10 step there in a later pass once
  they exist.

## 16. Decisions (locked)

Former open questions, resolved — no longer optional, implementation
should match these exactly:

1. **`vs_last_3_runs`** = compare against the entry 3 runs back
   (`domain_history[-3]`), not an average. Reuses `trend_comparison()`
   unmodified; a concrete data point, not a smoothed abstraction.
2. **Archive retention** = none. `score_history.json` grows unbounded,
   same as it already does today independent of this proposal. No
   rotation/cleanup logic to build.
3. **`analyze_trend.py`'s output stays file-only** — no push to
   samgraha's DB (`store_document_report` or otherwise). The agent
   reads `{domain}-trend.json` directly off disk (§5). Revisit only if
   a concrete consumer needs to query trend data through samgraha's
   own tools instead of base_dev's file layout — no such consumer
   exists today, so no write path is built for one.
4. **Trigger UX for §5/§10** = ad hoc for now (user asks the agent
   directly, e.g. "analyze tier 1 for vision"). No skill/slash-command
   built as part of this proposal — revisit once the rubric pattern is
   proven on `01-vision.md` in real use.

## 17. Verification checklist

One line per section, each independently checkable against the
implementation:

- [x] §4 — `analyze_trend.py` exists, reads `score_history.json` +
      `{domain}-scores.json` only, writes `{domain}-trend.json` with
      `vs_last_run`/`vs_last_3_runs`/`vs_baseline`, calls
      `trend_comparison()` unmodified. No new archive file anywhere.
- [ ] §5 — `analysis/{domain}.md` exists for all 16
      domains + `00-summary.md`, same section shape as
      `01-vision.md`. No `analyze_semantic.py` file exists anywhere in
      the repo. (Only `01-vision.md` exists so far; remaining 15 +
      `00-summary.md` pending.)
- [x] §6 — `visualize.py` accepts `--viz-plan`; a `CHART_CATALOG` dict
      maps shorthand names to the 8 existing `chart_*` functions;
      `chart_tier_progression` is absent from the default (no-plan)
      catalog; `chart_trend_history` is a new function reading
      `score_history.json`.
- [x] §7 — `append_score_history()`'s entry dict has a `model` key.
      `evaluate_semantic.py` stamps `"model": "heuristic-v1"` in its
      return; `calculate.py` reads it from `{domain}-sem-eval.json` and
      carries it through to scores. Full 3-hop flow complete.
- [x] §8 — `report.py` has `render_trend_and_narrative()`; existing
      `substitute_template()`/`_generate_fallback_report()` are
      byte-for-byte unchanged; a report generated with no
      trend/narrative files present looks identical to today's output.
- [x] §9 — `report_html.py` groups sections by `plan/core/tiers.yaml`
      tier order; a domain with no report data renders "Not
      available"; where present, narrative renders before charts.
- [x] §10 — a system-scope narrative/viz-plan pass exists, driven by
      `00-summary.md`, producing the always-present Final Summary
      section; `chart_tier_progression` is generated only here, from
      `results.json`.
- [x] §12 — `init.py`'s automated loop calls `phase_analyze_trend()`
      but nothing narrative/viz-plan-producing; a domain run purely
      through `init.py` has `{domain}-trend.json` but no
      `{domain}-narrative.json` until the agent step runs separately.
- [ ] §16.1–4 — each decision matches implementation exactly (3-back
      comparison, no retention logic, no DB push, no skill/command
      built).
