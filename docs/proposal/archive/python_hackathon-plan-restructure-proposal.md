# python_hackathon — Plan Restructure + Coverage Reporting Proposal

`plan/` describes a pipeline that doesn't exist and never ran, for a
use-case shape (`repo_new`/`repo_existing` × doc-generation cases ×
tiers) that doesn't apply to this standard at all. Every script this
conversation has built and verified working — `run_hackathon.py`,
`evaluate_rules.py`, 10 `audit_*.py` runners, `db.py`,
`statistics.py`/`leaderboard.py`, `render_charts.py`,
`render_reports.py`, `export_team_pdfs.py` — has zero relationship to
what `plan/` documents. This proposal replaces `plan/` with the actual
7-use-case pipeline that's been built, and adds the one piece that's
genuinely still missing: a coverage/status script, since with 7
use-cases and 10 domains × N teams × up to several models, it's
already easy to lose track of what's been run for whom.

---

## 0. Current state — grounded in what's on disk

| Piece | State | Evidence |
|---|---|---|
| `plan/usecase/**/*.md` (24 files) | **100% placeholder stub, not real content** | Every one of `repo_new/{case_1,case_2}/tier_{1-4}/{01-generation,02-audit,03-fix}.md` reads in full: `"Placeholder content for case_N scenario."` Confirmed by reading multiple files directly. |
| `plan/usecase/`'s whole shape | **Wrong use-case model entirely** | `repo_new` vs `repo_existing`, `case_1_no_documentation` vs `case_2_has_documentation`, `tier_1`–`tier_4`, `01-generation → 02-audit → 03-fix` — this is base_dev's documentation-generation taxonomy (does the repo have code/docs already, generate vs. audit-and-fix). python_hackathon has no generation step at all (confirmed audit-only earlier this conversation), a fixed team roster (not "new repo vs existing repo"), and a completely different real pipeline (§1 below). None of this use-case shape applies. |
| `plan/core/loop.yaml` | **Partially real, but stale** | Real stage names (`repository → det-audit → sem-audit → det-calculate → sem-calculate → aggregate → relative(z-score) → normalize → validate → report`) roughly match the *shape* of what got built, but names no analysis/narrative stage, no markdown/chart/HTML/PDF stages, and `aggregate`/`relative` describe the old file-tree (`score_aggregator.py`) approach that's since been replaced by `db.py`'s DB-driven adapter (§0 next row). |
| `plan/core/tiers.yaml` | **Real content, orphaned** | Genuine domain-relationship metadata (e.g. `infrastructure --guides--> engineering`, `engineering --requires--> testing`) — not placeholder garbage, but no script reads this file. `run_hackathon.py` iterates domains in whatever order `weights.yaml`'s dict gives it, ignoring any tier/dependency ordering. Decision needed (§7) on whether to keep this as informational-only or wire it into actual audit ordering. |
| `script/score_aggregator.py` | **Dead code** | Its own docstring still says `INPUT: aggregated_scores.json (output of score_aggregator.py)` — but grepped every other script, nothing imports it. `db.py`'s `get_all_scores_as_dict()` fully replaced its role (confirmed, per the report-analysis proposal's §6 resolution). Safe to archive/delete, not rewrite. |
| Coverage/status reporting | **Does not exist** | No script anywhere answers "what's been run so far, for which teams, which domains, which kind." The closest thing is a raw SQL query sketched in the report-analysis proposal's §5 (missing-model-combos query) — never built into a runnable script, never produces a report. |
| Partial-run support in `run_reporting.py` | **Does not exist** | Checked its `add_argument` calls directly — only `--standard`/`--db`/`--output-dir`. No `--deterministic-only`/`--semantic-only`/`--partial` flag; nothing gates z-score computation on domain completeness. |

## 1. The real pipeline — 8 use-cases, strict sequential gate, each with a completion definition and a verify script

Per your instruction: each use-case gets an exact, checkable
completion definition — not "roughly done" — and its own verification
script, so nothing can silently move to the next stage on incomplete
or wrong data. §1a gives the fixed order and the det/sem sequencing
rule; §1b defines each use-case precisely (inputs, action, exact
completion criteria, verify script); §2 (below, renumbered from the
old §"Deterministic audit" section) covers the one-command-all-teams
question; §3 covers verification-script design in full.

### 1a. Fixed order + the deterministic-before-semantic rule, stated explicitly

```
1 (Init)
  ↓  [gate: verify_usecase_1_init.py passes]
2a (Audit — Deterministic)         ← runs FIRST, always, per team
  ↓  [gate: verify_usecase_2a_audit_deterministic.py passes,
      at minimum for the team(s) being processed]
2b (Audit — Semantic)              ← starts only after 2a for that
  ↓   team/domain; accumulates independently afterward, no gate to
  ↓   "finish" before 3 can run (3's own gate handles this, see below)
3 (Calculate)
  ↓  [gate: verify_usecase_3_calculate.py passes]
4 (Analysis)
  ↓  [gate: verify_usecase_4_analysis.py passes]
5 (Markdown + Visualization)
  ↓  [gate: verify_usecase_5_markdown_charts.py passes]
6 (HTML Report)
  ↓  [gate: verify_usecase_6_html_report.py passes]
7 (PDF Generation)
     [gate: verify_usecase_7_pdf_generation.py passes]
```

**Why deterministic always precedes semantic, per team** — restating
your very first instruction in this whole conversation
("deterministic first for one repo... then semantic for same repo"),
now made an explicit, enforced rule rather than an implicit habit:
deterministic is fast, fully scripted, no agent/model cost — running
it first for a team gives a real baseline score immediately and
tells you which domains even *have* an audit script (§0 bug #3's
domains, already resolved, but the ordering logic doesn't assume that).
Semantic requires an agent session (slower, potentially spread across
days per model) — gating it behind "deterministic already ran for
this team" means you never waste a semantic session auditing a team
that isn't registered/isn't otherwise ready. `run_hackathon.py`'s
existing loop already does this per-team (2a before iterating 2b
concerns for the same team) — this section makes that ordering an
explicit, written rule instead of an implementation detail nobody
wrote down.

**2a/2b vs. 3 — the actual gate is at use-case 3, not between 2a and
2b**: 2b never "finishes" in the way 1/2a/3+ do — it accumulates
across independent sessions indefinitely (confirmed design, §5's
report-analysis proposal). So use-case 3 isn't gated on "2b complete
for all domains" (that could mean waiting forever) — it's gated on
"2a has run for the team(s) being calculated, and whatever 2b data
exists so far is used as-is" (§4 of this proposal's `--mode` flags
control this precisely: `--mode det` explicitly ignores 2b's state,
`--mode both` uses whatever's there). The verify script for 3 checks
that 2a's gate already passed for every team being calculated — it
does *not* require 2b completion, since 2b completion isn't a defined
end-state.

### 1b. Each use-case — inputs, action, exact completion criteria, verify script

**Use-case 1 — Init**
- **Input**: `.env`'s `PYTHON_HACKATHON_TEAMS_JSON` path, `teams.json`'s content.
- **Action**: `run_hackathon.py`'s startup path — `get_conn()` creates/opens the DB and schema; `_sync_teams()` registers any team from `teams.json` not already in `standard_participants`.
- **Completion criteria (exact, scriptable)**: DB file exists and is openable; `standard_participants`, `standard_domain_scores`, `standard_narratives` tables exist (schema check); every `team_name` in `teams.json` has exactly one matching row in `standard_participants` for this `standard` (a set-difference check, not just "some rows exist").
- **Verify script**: `verify_usecase_1_init.py --standard python_hackathon` — exits 0 and prints "PASS" only if the above all hold; exits 1 and lists exactly which `teams.json` entries are missing from the DB otherwise.

**Use-case 2a — Audit, Deterministic**
- **Input**: every team registered per use-case 1; `audit/deterministic/document/*.yaml` rules; `audit_*.py` runners.
- **Action**: `run_hackathon.py`'s deterministic pass — per team, per domain with a runner script, evaluate rules, upsert one `standard_domain_scores` row (`kind='deterministic'`).
- **Completion criteria**: for the team(s) in scope, every domain that *has* an `audit_*.py` script (all 10, per §0 bug #3's resolution — confirmed no domain is missing a runner anymore) has exactly one `kind='deterministic'` row in `standard_domain_scores`.
- **Verify script**: `verify_usecase_2a_audit_deterministic.py --standard python_hackathon [--team <name>]` — per team, reports `N/10` domains present; exits 0 only if `10/10` for every team in scope (or the named `--team`); otherwise exits 1 and lists exactly which (team, domain) pairs are missing.

**Use-case 2b — Audit, Semantic**
- **Input**: `audit/semantic/document/*.yaml` rubrics; whichever agent/model session runs them.
- **Action**: agent-driven — one `standard_domain_scores` row per (team, domain, model) that's been scored so far.
- **Completion criteria — two tiers, not one, since "complete" is genuinely ambiguous here (already flagged in an earlier proposal, resolved concretely now)**:
  - *Minimum bar (unblocks use-case 3)*: at least 1 semantic row per domain, per team — matches "a partial ensemble still produces a valid mean" (confirmed design).
  - *Full bar (informational only, never blocks anything)*: every configured model (from a list this script/`.env` defines) has scored every domain, every team.
- **Verify script**: `verify_usecase_2b_audit_semantic.py --standard python_hackathon [--team <name>]` — reports both tiers separately per team (`"7/10 domains have ≥1 model, 3/10 domains have all N configured models"`); exit code reflects the *minimum bar* only (0 = every domain has ≥1 model for every team in scope), since that's the only bar anything downstream actually depends on. The full-ensemble number is reported, never gates.

**Use-case 3 — Calculate**
- **Input**: use-case 2a's gate passed (required); use-case 2b's data as-of-now (whatever exists, no gate required); `calculation/aggregation/domain/*.yaml`.
- **Action**: `db.py`'s `get_all_scores_as_dict()` → `statistics.py`'s `run_z_adjustment()` → `leaderboard.py`'s `build_leaderboard()`.
- **Completion criteria**: `build_leaderboard()`'s output contains exactly one entry per team registered in use-case 1 (no team silently dropped); every entry has a non-null `final_score` and, for every domain that team has *any* audit data for (det and/or sem), a non-null `z_score`/`adjusted_score`.
- **Verify script**: `verify_usecase_3_calculate.py --standard python_hackathon` — re-runs (or loads a persisted copy of) the calculation, diffs the team list against `standard_participants`, checks no `None`/missing numeric field on any entry that should have one. Exits 1 and names the specific team/domain/field if anything's missing.

**Use-case 4 — Analysis**
- **Input**: use-case 3's output (aggregated scores + z-stats, not raw audit rows — confirmed design); `analysis/{domain}.md` × 10 + `analysis/00-leaderboard.md` rubrics.
- **Action**: agent-driven — writes `standard_narratives` rows (per team+domain, plus one competition-wide `participant_id=NULL, domain=NULL` row).
- **Completion criteria**: exactly one `standard_narratives` row for every (team, domain) pair that has *any* audit data (per use-case 2a/2b's state at the time analysis ran — a domain with zero audit data correctly has no narrative, confirmed existing design, not a gap); exactly one competition-wide row exists.
- **Verify script**: `verify_usecase_4_analysis.py --standard python_hackathon` — cross-references `standard_domain_scores` (which team+domain combos have data) against `standard_narratives` (which have a narrative); lists any combo with data but no narrative; separately checks the single competition-wide row exists and isn't duplicated.

**Use-case 5 — Markdown + Visualization Generation**
- **Input**: use-case 3's scores + use-case 4's narratives.
- **Action**: `render_charts.py` (7 chart types → PNG files) + `render_reports.py`'s markdown renderer (30 domain templates + 2 shared = 32 template *files on disk*, `chevron`-rendered).
- **Completion criteria**: every expected PNG file exists (per team × applicable chart types + shared domain/leaderboard-level ones) and is non-zero size; every expected markdown *output* file exists — **corrected count**: 30 per team (10 domains × {deterministic, semantic, summary}, for domains-with-data) + 1 team-final-summary = 31 per team, + 1 shared `global-leaderboard.md` — and contains no unrendered `{{...}}` Mustache tokens (a real, cheap correctness check — this exact class of bug, template/data mismatch producing literal `{{field}}` in output, was caught and fixed earlier this session; worth checking mechanically every time, not just when something looks visibly wrong).
- **Verify script**: `verify_usecase_5_markdown_charts.py --standard python_hackathon` — file-existence + non-zero-size sweep over the expected file list (derived from registered teams × domains-with-data, not a hardcoded count), plus a grep-style `{{`/`}}` leftover-token check on every markdown file.

**Use-case 6 — HTML Report Generation**
- **Input**: use-case 5's markdown-side DB reads (same data) + use-case 5's chart PNGs (must exist on disk already).
- **Action**: `render_reports.py`'s `render_html_all()` — **corrected count** (an earlier draft of this line said "32 per team," confirmed wrong against the actual verified test run earlier this session): 30 domain pages + 1 team-final-summary = **31 HTML files per team**, + 1 shared `global-leaderboard.html` (not per-team) — matching the `N*31 + 1` total already confirmed by a real pipeline run.
- **Completion criteria**: every expected HTML file exists, non-zero size, contains no unrendered `{{...}}` tokens (same check as use-case 5, applied to HTML output), and every `<img src="data:image/png;base64,...">` tag has a non-empty base64 payload (catches the "chart file didn't exist, base64 lookup silently returned empty string" failure mode already built into `_get_chart_b64()`'s fallback — that fallback exists specifically so a missing chart doesn't crash rendering, but it should never *silently* stay empty in a final, complete run).
- **Verify script**: `verify_usecase_6_html_report.py --standard python_hackathon` — file sweep + leftover-token check (shared helper with use-case 5's script, not reimplemented) + a regex check for `base64,"` (empty payload) occurrences.

**Use-case 7 — PDF Generation**
- **Input**: use-case 6's HTML output (all of it, per team).
- **Action**: `export_team_pdfs.py` — one PDF per team.
- **Completion criteria**: one PDF file per registered team, non-zero size, and — the concrete, valuable check given the exact "22 pages instead of 31" bug found and fixed earlier this session — **page count matches the expected count** (31 per team: 30 domain pages for domains-with-data + 1 team-summary; fewer if some domains have zero audit data, per use-case 5's "domains-with-data" scoping, not a hardcoded 31 always).
- **Verify script**: `verify_usecase_7_pdf_generation.py --standard python_hackathon` — file existence/size + `pypdf.PdfReader(path).pages` count check against the expected count computed the same way use-case 6's file sweep computed its expected HTML count (shared logic, not two independently-maintained "how many pages should this team have" calculations that could drift apart).

### 1c. Whole-pipeline verification — one more script, runs all 7 in order

Per your explicit ask ("we should have a script to verify all
usecase individually **and as a whole**, separate scripts") — the 7
scripts above answer "did stage N complete correctly," each in
isolation. A separate, 8th script answers "is the *entire* pipeline,
end to end, currently in a consistent, complete state" — genuinely
different from just calling the 7 individually, because it also
checks the *ordering* held (e.g. use-case 5's files aren't newer than
use-case 3/4's DB writes that produced their data — catches "someone
re-ran calculate after already generating markdown, and forgot to
regenerate markdown," which no individual stage-check can see since
each only looks at its own stage in isolation):

```
python verify_all_usecases.py --standard python_hackathon [--team <name>] [--stop-on-fail]
```

- Imports and calls each `verify_usecase_N_*.py`'s check function
  directly (not via `subprocess`, so failures carry structured
  data — which team, which domain, which file — not just exit codes)
  in strict order 1 → 2a → 2b → 3 → 4 → 5 → 6 → 7.
- **`--stop-on-fail`** (default `True`): halts at the first failing
  use-case, since a downstream use-case's own checks are meaningless
  if an upstream one already failed (e.g. checking use-case 6's HTML
  files for leftover `{{}}` tokens is pointless if use-case 4's
  narratives don't exist yet — the HTML would correctly show "no
  narrative" placeholders, which isn't a use-case-6 bug). Without the
  flag, runs all 7 regardless and reports every failure, for a full
  diagnostic sweep rather than "first thing to fix."
- **Freshness cross-check** (the part no individual script can do):
  compares each use-case's output timestamp against its input's — if
  `standard_domain_scores`'s newest row postdates the markdown/HTML
  files' modification time, flags "use-case 5/6 output is stale,
  re-run after the latest audit write" even though use-case 5/6's own
  *content* checks would otherwise report PASS (the files exist,
  aren't empty, have no leftover tokens — they're just describing
  old data). This directly serves your "each stage should ensure all
  data is created before moving to next" instruction at the
  whole-pipeline level, not just the per-stage level.
- **Output**: one consolidated report — pass/fail per use-case, plus
  the freshness cross-check's findings — using the same `chevron`
  template pattern as everything else (`templates/reports/pipeline-verification.md`),
  not a bespoke format.

## 2. Deterministic audit — one script, all teams, all domains

Per your "run all use-case for deterministic audit in one step if you
know which script to run" — this already exists, confirmed, not new
work: `run_hackathon.py`'s main loop (already iterates every
registered participant × every domain in `weights.yaml`, calling the
right `audit_{domain}.py` per `DOMAIN_AUDIT_MODULES`'s mapping). One
command (`python run_hackathon.py --standard python_hackathon`)
already does exactly "run deterministic audit for every team, every
domain" in one step — the `--deterministic-only` flag already exists
too (confirmed in an earlier read of `run_hackathon.py`'s
`add_argument` calls). This use-case is *documented as new work* by
`plan/`'s stale content, but is *actually already built* — the plan
restructure (§6) needs to say so, not describe it as pending.

## 3. Coverage/status script — genuinely new, your explicit ask

**Distinct purpose from §1b/1c's verify scripts, not overlapping
work**: the 8 verify scripts answer a strict yes/no — "did use-case N
complete correctly, is the pipeline as a whole in a consistent
state." `coverage_report.py` answers a softer, ongoing question —
"how far along is each team, right now, across everything" — useful
mid-competition while most teams are legitimately incomplete (not a
failure state, just not-done-yet), which is exactly when the strict
verify scripts would correctly report FAIL for most teams and stop
being a useful running-status tool. Both are needed; neither
replaces the other. `coverage_report.py` reuses the same underlying
queries §1b's `verify_usecase_2a`/`2b` scripts use (one shared query
module, not two independent implementations of "which domains does
this team have data for").

**The gap**: with 7 use-cases, 10 domains, N teams, and semantic audit
scoring accumulating across independent agent sessions over
potentially days, there's no single place to answer "what's actually
been done so far" — confirmed nothing like this exists (§0). New
script, `script/coverage_report.py`:

```
python coverage_report.py --standard python_hackathon [--team <name>]
```

**What it computes**, per team (or all teams if `--team` omitted):
- **Deterministic coverage**: for each of the 10 domains, does a
  `standard_domain_scores` row with `kind='deterministic'` exist?
  Pass/missing per domain.
- **Semantic coverage**: for each domain, which models have scored it
  so far (reuses the exact missing-combo query already sketched in
  the report-analysis proposal §5 — this script is what finally turns
  that raw SQL into something runnable and reportable, not new query
  logic).
- **Downstream-stage readiness**: has use-case 3 (calculate) been run
  since the last audit write landed (compare `standard_domain_scores.created_at`
  max against whether a fresh leaderboard/z-score run has happened —
  simplest correct signal: does at least one row exist per team, and
  is there evidence calculate/analysis/render have been re-run after
  the newest audit row — flagged as an implementation detail, not
  fully specified here, since "stale vs fresh" tracking needs one more
  decision, see §7).
- **Team-level summary line**: `"team-x: 7/10 deterministic, 3/10
  semantic (2+ models), NOT ready for final report"` or similar.

**Output — markdown via a template**, per your explicit instruction
("that script should provide report as markdown using a template
markdown"), not just console printout: new template
`templates/reports/coverage-status.md`, same `chevron` rendering
pattern as every other template in this system — one more consumer of
the shared `templates/` convention, not a special case.

```
templates/reports/coverage-status.md:

# Coverage Status — {{ standard }}

Generated: {{ generated_at }}

## Per-Team Summary

{{#teams}}
### {{ team_name }}
- Deterministic: {{ det_complete }}/10 domains
- Semantic: {{ sem_complete }}/10 domains ({{ sem_model_note }})
- Missing domains (deterministic): {{ det_missing_list }}
- Missing domains (semantic): {{ sem_missing_list }}
- Ready for final report: {{ ready_flag }}
{{/teams}}

## Competition-Wide

- Teams fully audited (deterministic): {{ fully_det_count }}/{{ total_teams }}
- Teams with at least one semantic model per domain: {{ fully_sem_count }}/{{ total_teams }}
```

## 4. `run_reporting.py` — partial-run flags, genuinely missing

Per your ask ("we should be able to re-run and generate all report
deterministic only semantic only or both or partial based on what is
completed") — confirmed missing (§0). New flags:

```
python run_reporting.py --standard python_hackathon [--mode {det,sem,both}]
```

- `--mode det` — run use-case 3 (calculate) using only deterministic
  scores, semantic contribution treated as 0 for every team equally
  (not "missing," genuinely not attempted yet — same shape as §5's
  missing-domain-is-zero rule, just applied to an entire audit *kind*
  rather than a domain).
- `--mode sem` — inverse, deterministic treated as 0.
  `--mode both` (default) — current behavior, uses whatever's in the
  DB for each kind.
- No new "partial" flag beyond this — **partial is already the
  default behavior**, not a mode to opt into: §5's missing-domain-
  is-zero rule (already built, confirmed in the report-analysis
  proposal's §7) means running use-case 3 with incomplete data already
  works today, silently. `--mode` is for deliberately excluding a
  whole *kind* of audit (e.g. "show me where things stand on rules
  alone, ignore semantic entirely for this run"), not for tolerating
  incompleteness — that tolerance already exists.

## 5. Z-score population — corrected: current behavior is split, and doesn't match what you asked for

**An earlier draft of this section claimed "team with a missing
domain contributes 0, already verified" as settled fact. Traced both
functions line-by-line — that's wrong, or at least incomplete.** The
real mechanism, split into two genuinely different cases that the
code treats differently:

- **A domain with *zero* rows of any kind for a team**
  (`db.py`'s `get_all_scores_as_dict()`, confirmed by reading it: the
  `domains` dict is built by iterating that team's actual DB rows —
  a domain never gets a dict key unless at least one row exists for
  it) — **this domain simply doesn't appear** in that team's entry at
  all. `statistics.py`'s `calculate_domain_stats()` then does
  `if domain in domains` before adding a team to the population — so
  a domain with zero data for a team means **that team is excluded**
  from the z-score population for that domain entirely. Not scored 0,
  not counted at all.
- **A domain with *partial* data** (e.g. deterministic scored,
  semantic not yet) — `domains[d]` *does* get created (a row exists,
  just not for both kinds), and `det = data["deterministic"] or 0.0`
  substitutes a real `0.0` for whichever kind is missing. This case
  *is* included in the z-score population, with that 0 baked into
  `raw_score`.

**This is the scenario you actually described** ("if any team has
some domain data missing add score zero") — a domain with no audit
data yet, the first case above. And for that exact case, **current
behavior is exclusion, not "score zero."** This isn't a documentation
gap to word more carefully — it's a real difference between what's
shipped and what you asked for. `get_all_scores_as_dict()` needs an
actual code change: for every domain in `weights.yaml`'s domain list
that a team has *zero* rows for, emit a `{"raw_score": 0.0, ...}`
entry anyway (matching the partial-data case's existing 0.0-injection
pattern, just applied one level up — per-domain-existence rather than
per-kind-existence within an already-existing domain entry).

**The consequence, restated correctly now that the mechanism is
precise**: once that fix lands, `calculate_domain_stats()` computes
`median`/`MAD`/`mean`/`stdev` across every team's raw score for a
domain, including teams scored 0 because they haven't been audited
yet. Early in a competition, if half the teams haven't been
semantically audited, their domains show a lower raw score than
completed teams — dragging the domain's mean down and inflating its
spread, which changes the z-score (and bonus/penalty) for teams that
*have* been audited, purely because other teams are incomplete.

Two options for how the *fixed* code should behave, not resolved here:
- **(a) Include everyone, 0 for a genuinely unaudited domain** —
  matches "add score zero" exactly as you described; requires the
  code change above. Z-scores are comparable-but-noisy mid-competition,
  self-correct once everyone's complete.
- **(b) Keep today's actual behavior** (exclude teams with zero data
  for a domain from that domain's population, still show them a raw 0
  in the leaderboard/UI) — cleaner statistics mid-competition, no code
  change needed, but doesn't match what you asked for, and means
  population size differs per domain (something `coverage_report.py`,
  §3, would need to surface so "who am I being compared against" is
  visible).

Recommend **(a)**, matching your literal description — which means
this section is now a genuine code-change item (§8's checklist,
updated), not just a documentation clarification.

## 6. Rewriting `plan/`

- **Delete** `plan/usecase/repo_new/` — the whole subdirectory, not
  just its files — since `repo_new/` is currently the *only* thing
  under `plan/usecase/`; nothing about that directory layer (or the
  `case_1_no_documentation`/`case_2_has_documentation`/`tier_N`
  nesting inside it) survives, not just the 24 placeholder `.md`
  files within it.
- **Replace** `plan/core/loop.yaml`'s stage list with §1a's 8-use-case
  chain (including the 2a-before-2b rule as an explicit, named
  constraint, not just an implementation detail), covering the
  analysis/markdown/HTML/PDF stages it currently omits.
- **New** `plan/usecase/` structure matching §1b's real shape —
  flat, no subdirectory nesting: the 8 use-case files
  (`1-init.md`, `2a-audit-deterministic.md`,
  `2b-audit-semantic.md`, `3-calculate.md`, `4-analysis.md`,
  `5-markdown-visualization.md`, `6-html-report.md`,
  `7-pdf-generation.md`) go directly under `plan/usecase/` itself,
  once `repo_new/`'s tree is gone — there's no "case" or "tier"
  concept left to nest under, this standard has one fixed pipeline,
  not a matrix of scenarios. Each file states: script name, inputs,
  action, **exact completion criteria**, and **its verify script's
  name** — not a generic generation/audit/fix template inherited from a
  different system class, and not just prose description without a
  checkable definition of "done."
- **New** `plan/core/verification.md` — documents all 9 verify
  scripts (7 per-use-case + `verify_all_usecases.py` +
  `coverage_report.py`) in one place: what each checks, its exit-code
  contract, and how `coverage_report.py` differs in purpose from the
  strict verify scripts (§3's clarification, restated here since this
  is exactly the kind of thing that gets re-litigated later if it's
  only ever said once in a proposal and never written into `plan/`
  itself).
- **`plan/core/tiers.yaml`** — decision needed (§7): keep as
  informational domain-relationship metadata (documented but unused),
  or wire it into `run_hackathon.py`'s domain iteration order. Not
  resolved here.
- **`script/score_aggregator.py`** — archive/delete, dead code (§0).

## 7. Open questions for confirmation

1. §3's "downstream-stage readiness" signal — what exactly counts as
   "stale" (calculate/analysis/render need re-running since the last
   audit write)? Needs one more decision (e.g. a `last_full_run_at`
   timestamp somewhere) before this part of the coverage script is
   fully specified — flagged, not designed here.
2. §5's z-score population question — (a) include-everyone-as-zero
   (recommended, matches your literal description) or (b) exclude
   incomplete teams from the population — needs your confirmation,
   this is a real statistics decision with consequences, not a detail.
3. `tiers.yaml`'s fate (§6) — keep as unused documentation, or wire
   into actual audit ordering in `run_hackathon.py`? If the latter,
   that's new scope beyond this proposal (changes execution order,
   not just plan docs).

## 8. Verification checklist

- [ ] §1a — `plan/core/loop.yaml` (or its replacement) states the
      2a-before-2b ordering rule explicitly, and states that 2b has
      no "complete" end-state (only 3's minimum-bar gate).
- [ ] §1b — all 8 use-cases (1, 2a, 2b, 3, 4, 5, 6, 7) have a written,
      exact completion criteria in the new `plan/usecase/` docs —
      not prose description alone, a checkable condition.
- [ ] §1b — 7 verify scripts exist: `verify_usecase_1_init.py`,
      `verify_usecase_2a_audit_deterministic.py`,
      `verify_usecase_2b_audit_semantic.py`,
      `verify_usecase_3_calculate.py`, `verify_usecase_4_analysis.py`,
      `verify_usecase_5_markdown_charts.py`,
      `verify_usecase_6_html_report.py`,
      `verify_usecase_7_pdf_generation.py` — each runnable standalone,
      each with a real exit-code contract (0 = pass, 1 = fail with
      specifics printed, not just "fail").
- [ ] §1b — `verify_usecase_5`/`6`'s "no leftover `{{}}` tokens" check
      and `verify_usecase_6`/`7`'s "expected page/file count" check
      share one computation of "which domains does this team have
      data for," not two independently-maintained counts that could
      silently drift apart.
- [ ] §1c — `verify_all_usecases.py` exists, runs all 7 stage-scripts
      in order via direct function calls (not `subprocess`), supports
      `--stop-on-fail`, and performs the freshness cross-check
      (output-newer-than-input) that no individual stage script can
      perform alone.
- [ ] §2 — plan docs state use-case 2a (deterministic, all teams, one
      command) is already built, not pending.
- [ ] §3 — `coverage_report.py` exists, produces per-team +
      competition-wide coverage via `templates/reports/coverage-status.md`,
      and shares its underlying queries with §1b's `verify_usecase_2a`/`2b`
      scripts rather than reimplementing "which domains does this team
      have data for" a third time.
- [ ] §4 — `run_reporting.py` accepts `--mode {det,sem,both}`; default
      behavior (no flag) is unchanged from today.
- [ ] §5 — **this is now a code-change item, not just documentation**:
      `get_all_scores_as_dict()` emits a `raw_score: 0.0` entry for
      every domain in `weights.yaml` a team has zero rows for, not
      just domains with partial (det-only or sem-only) data. Verify
      by registering a team with literally no audit data for one
      domain and confirming `calculate_domain_stats()` includes them
      at 0 for that domain, not silently excludes them. The z-score
      population decision itself (§7 Q2) is recorded explicitly in a
      plan doc either way.
- [ ] §6 — `plan/core/verification.md` exists, documents all 9 verify/
      coverage scripts, their exit-code contracts, and the coverage-
      vs-verify distinction in one place, not only in this proposal.
- [ ] §6 — `score_aggregator.py` is archived or deleted, not left
      as dead code with a misleading docstring.
- [ ] §7 — all three open questions have a recorded decision before
      `plan/`'s rewrite is considered final.
