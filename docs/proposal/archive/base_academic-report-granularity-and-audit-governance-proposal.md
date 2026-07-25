# base_academic — Report Granularity + Domain Aggregation + Audit Run Governance Proposal

## 0. Why This Document Exists

`base_academic-template-visualization-depth-proposal.md` (implemented,
archived) added per-domain full/part semantic tables, a per-check
deterministic breakdown, and a pipeline-progress report — but it kept
the pre-existing shape of **one shared template per report kind, looped
internally over all domains** (`semantic.md`'s `{{#domains}}...{{/domains}}`
pattern). That shape is now confirmed to be the wrong target: it doesn't
scale to "one report per audit run," it has no per-domain aggregate
score, and the whole audit layer has no concept of "did anything actually
change since last run" — every invocation re-runs and re-renders
everything, deterministic or semantic, regardless of whether the source
changed.

Confirmed on disk today:

- **Report templates are reused across all 12 domains, not per-domain.**
  `templates/report/markdown/{deterministic,semantic,summary,pipeline-progress}.md`
  — 4 template kinds total, each a single file, each looping over every
  domain internally (`generate_audit_report.py:461-464`). Every domain's
  deterministic/semantic result renders through the *same* Mustache
  template, one row per domain in a shared table. Same for the `.html`
  twins. There is no per-domain, per-usecase template file anywhere.
- **`python_hackathon`'s report layer already does what this proposal
  is asking for**, and can be used as the concrete precedent instead of
  inventing a shape from scratch (located at `samgraha/system/
  python_hackathon/` — a sibling of `samgraha/system/academic/`, not of
  `base_academic` itself): `templates/reports/markdown/domain/
  {01-infrastructure,...,10-ai-explanations}/{deterministic,semantic,summary}.md`
  — 10 domains × 3 kinds = 30 files, plus the `.html` twins (60 total),
  plus 2 whole-run reports (`global-leaderboard`, `team-final-summary`).
  No template is shared across two domains or two report kinds. This is
  the pattern §2 below ports to `base_academic`.
- **No per-domain aggregate score or report exists.** `calculation/summary/
  final_score.yaml` defines two formulas: the per-domain one is a plain
  50/50 `deterministic`/`semantic` blend, but the whole-paper one is not
  a 50/50 of anything — it's `0.4 * domain_mean + 0.6 * doc_coherence`
  (`doc_coherence = mean(cross_section_score, document_score)`). Only the
  per-domain half is relevant here; nothing renders *that* half as its
  own artifact per domain — the number only shows up folded into the
  whole-paper `summary.md`. `python_hackathon` has both the calculation
  (`calculation/aggregation/domain/{domain}.yaml`, confirmed 10 files,
  each a `weighted_merge` of `calculation/deterministic/document/
  {domain}.yaml` + `calculation/semantic/ensemble/{domain}.yaml` at
  0.60/0.40) **and** a rendered artifact per domain
  (`templates/reports/markdown/domain/{domain}/summary.md`). `base_academic`
  has the formula but neither a `calculation/aggregation/domain/` dir
  nor a per-domain rendered summary — only the whole-paper one.
- **No git-commit gate anywhere.** Grepped `commit|git_hash|git rev-parse|
  git status|uncommitted|working tree` across all of `base_academic/
  {schema,script,plan,calculation}` — every "commit" hit is
  `sqlite3.Connection.commit()`, not git. No schema table has a
  `commit_sha`/`git_hash` column. No script shells out to `git` at all.
  `run_full_workflow.py` never checks whether the target repo's working
  tree is clean before running deterministic or semantic audits — it
  audits whatever's on disk, staged or not, tracked or not.
- **No skip-if-unchanged logic anywhere.** `run_full_workflow.py`'s
  Phase 6 (deterministic-audit, `run_full_workflow.py:778-796`) and
  Phase 7 (semantic-audit, `:797-820`) invoke every domain's audit step
  unconditionally on every run — no pre-check of "did this domain's
  input change since the last recorded run." `academic_deterministic_
  findings` and `academic_semantic_runs` are both append-only
  (`record_deterministic_findings()` / `upsert_semantic_score()`, both
  always `INSERT`, never look-before-write) — every re-run of
  `run_full_workflow.py` produces a brand new `run_number` for every
  domain, identical content or not.
- **`computed_against` (the one column that looks like a staleness
  mechanism) is dead code.** `academic_semantic_runs.computed_against`
  (schema/09) is documented in its own column comment as "a dict of
  {domain_key: iteration} snapshots... so staleness can be detected" —
  but `persist_domain_semantic_score.py` never passes it (defaults to
  `'{}'` on every row), and no code anywhere reads or compares it. It's
  a specified-but-unimplemented mechanism, not a working one — this
  proposal replaces the intent behind it with the commit-hash-based
  mechanism in §4/§5, since content-hash-per-domain and git-commit-hash
  cover the same "did the input change" question with an actual
  verifiable primitive instead of an uncollected dict. Since `commit_sha`
  takes over `computed_against`'s intended job, this proposal removes
  `computed_against` rather than shipping a third, competing dead-code
  path alongside it (§7).
- **`model` is a single free-text field, no multi-model support.**
  `academic_semantic_runs.model` (schema/09) and `academic_narratives.model`
  are both plain `TEXT`, populated from `payload.get("model", "")` in
  each persist script. The schema's `UNIQUE(paper_id, domain_id, scope,
  model, run_number, part_kind)` constraint *technically* allows several
  models' scores to coexist for the same domain+scope (model is part of
  the key) — but nothing in `run_full_workflow.py`, `plan/usecase/*.md`,
  or `calculation/semantic/*.yaml` drives more than one model per audit
  round, and there's no ensemble/mean calculation anywhere in
  `base_academic` to combine them if there were. `python_hackathon` has
  exactly this: `calculation/semantic/ensemble/01-infrastructure.yaml`
  — `calculation: reliability_aware_ensemble`, `mean_score = mean(scores)`,
  `stdev_score = stdev(scores)`, `agreement = High/Medium/Low` by stdev
  threshold, `final_score = mean_score`. `base_academic` has no
  `calculation/semantic/ensemble/` directory at all.

## 1. Scope

`base_academic/templates/report/**` (restructure to per-domain,
per-usecase files), a new `calculation/aggregation/domain/` directory, a
new `calculation/semantic/ensemble/` directory, `generate_audit_report.py`
(render-loop rewrite), `run_full_workflow.py` (add git-gate + skip-check
before Phase 6/7), `deterministic_audit.py` + `persist_domain_semantic_
score.py` (thread `commit_sha` through), and two schema columns. Doesn't
touch the generation templates (`templates/generation/**`, prior
proposal's territory), the usecase registration list (`plan/usecase/*.md`
/ `academic_schema.py`'s `_register_usecase*` calls — no new or removed
usecases, only new *reports* per existing usecase and new *gating* around
existing usecase invocation), or the chart/visualization layer (prior
proposal's §5, unaffected by report-file granularity).

## 2. Report Templates — One File Per (Domain × Report Kind), No Reuse

### 2a. New directory layout

Replace the 4 shared, domain-looping template files with a per-domain
tree, mirroring `python_hackathon`'s confirmed layout exactly:

```
templates/report/markdown/domain/{domain}/deterministic.md
templates/report/markdown/domain/{domain}/semantic-full.md
templates/report/markdown/domain/{domain}/semantic-part.md
templates/report/markdown/domain/{domain}/plagiarism.md
templates/report/markdown/domain/{domain}/humanize.md
templates/report/markdown/domain/{domain}/summary.md          -- §3
templates/report/html/domain/{domain}/... (same 6 files)
```

× 12 domains × 6 report kinds × 2 formats = **144 files**, replacing
today's 8 (`deterministic`/`semantic`/`summary`/`pipeline-progress` ×
`.md`/`.html`). `pipeline-progress.md`/`.html` and the whole-paper
`summary.md`/`.html` stay as the two remaining non-per-domain reports
(nothing to split — they're inherently cross-domain views):

```
templates/report/markdown/pipeline-progress.md   -- unchanged, §4c of prior proposal
templates/report/markdown/whole-paper-summary.md -- renamed from summary.md, §3c below
templates/report/html/pipeline-progress.html
templates/report/html/whole-paper-summary.html
```

### 2b. Why 6 report kinds per domain, not 3

This is the direct answer to "a category if it has 3 reports we get all
3, some categories have multiple deterministic/semantic usecases so they
get multiple reports": counting what actually produces persisted
findings per domain today —

| Report kind | Source usecase(s) | Why split from its neighbor |
|---|---|---|
| `deterministic.md` | `deterministic-audit-{d}` — one `academic_deterministic_findings` row, `scope='section'` | Single usecase, single report — no split needed |
| `semantic-full.md` | `semantic-audit-{d}` — `academic_semantic_runs` row, `scope='section-full'` | Whole-domain semantic judgment |
| `semantic-part.md` | the citations/enrichment/budget-fit part-level semantic audit (atomicity proposal §6, `scope='section-part'`, one row per `part_kind`) | **Different usecase, different scope, different rubric** (`semantic-audit-part.md`'s three-rubric prompt) from `semantic-full.md` — this is the concrete case of "one category, multiple usecases, multiple reports." Folding it into `semantic-full.md` (what the visualization-depth proposal did, as two tables in one shared file) is exactly the reuse this proposal is undoing. |
| `plagiarism.md` | `plagiarism-forensic-audit-{d}` — `academic_plagiarism_findings` row | Own usecase, own findings table, no current report at all (gap — the visualization-depth proposal's §0 already flagged `academic_section_citations` and `academic_humanize_passes` had no report; plagiarism has the same gap and was missed there) |
| `humanize.md` | `humanize-deterministic-{d}` + `humanize-semantic-{d}` — both write `academic_humanize_passes`, differ by `pass_kind` | Same table, two `pass_kind` values — one report, two sections inside it (`pass_kind` is a column on one table, not two usecases producing two different schemas the way full/part semantic does — no split needed here, this is the "3 reports, not more" side of the same rule) |
| `summary.md` | Aggregation of the above 5, §3 | New — the per-domain rollup |

The rule this proposal is codifying: **one template file per distinct
`(domain, source-table+scope combination)`**, not per domain and not per
audit-category-in-the-abstract. Two usecases that write to the same table
with the same scope share one report (humanize); two usecases that write
to the same table with different `scope` (semantic full vs. part) do not.

### 2c. `generate_audit_report.py` render loop rewrite

Today's single loop (`generate_audit_report.py:461-487`, iterating a
4-element list and rendering once per kind) becomes a nested loop —
outer over domains, inner over the 6 report kinds — each iteration
loading `templates/report/{markdown,html}/domain/{domain_key}/{kind}.{ext}`
and writing to a mirrored output tree:

```
docs/paper/paper-{id}/audit/domain/{domain_key}/{kind}.md
docs/paper/paper-{id}/audit/domain/{domain_key}/{kind}.html
docs/paper/paper-{id}/audit/pipeline-progress.md   -- unchanged location
docs/paper/paper-{id}/audit/whole-paper-summary.md -- renamed
```

`_get_domain_data()` and friends (already per-domain-looping internally)
don't change their query shape — they still fetch one domain's row at a
time — only the render/write step moves from "collect all domains into
one big context, render once" to "render once per domain, per kind, with
that domain's slice of context."

## 3. Domain Aggregate Report — `calculation/aggregation/domain/`

### 3a. New calculation files, one per domain

Direct port of `python_hackathon/calculation/aggregation/domain/*.yaml`'s
shape, pointed at `base_academic`'s existing deterministic/semantic
calculation files instead of `python_hackathon`'s:

```yaml
# calculation/aggregation/domain/methodology.yaml
id: aggregation_methodology
calculation: weighted_merge
scope: domain
inputs:
  deterministic: calculation/deterministic/methodology.yaml
  semantic: calculation/semantic/full-part-blend.yaml   # full + part blend, §3b
weights:
  deterministic: 0.50
  semantic: 0.50
formula: |
  final_score = (deterministic.score * weights.deterministic) + (semantic.score * weights.semantic)
```

× 12 domains (one per `STRUCTURAL_DOMAINS` entry). Weights match
`calculation/summary/final_score.yaml`'s existing 50/50 **per-domain**
split only — this file instantiates that one half of `final_score.yaml`
(the per-domain formula), not the whole file. `final_score.yaml`'s
whole-paper formula (`0.4 * domain_mean + 0.6 * doc_coherence`, §0) is
untouched and out of scope here — the per-domain aggregation files feed
into `domain_mean`, they don't replace or restate the whole-paper
formula. A concrete system (`pcems_2026`, `eswa_journal`) that wants
`methodology` weighted differently from `abstract` now has a file to
override instead of the per-domain half of the prose formula being
uniform-by-construction.

### 3b. Semantic score input to the aggregation — full + part blend

`inputs.semantic` above can't point directly at a single
`academic_semantic_runs` row — a domain has up to 4 semantic scores
(`section-full` + 3 `section-part` kinds, §2b). Needs one more
calculation file, `calculation/semantic/full-part-blend.yaml`, defining
how those 4 collapse into the one number `aggregation_domain`'s
`weighted_merge` consumes. **Name note**: `calculation/semantic/
section-parts.yaml` already exists today — it's the three mini-rubrics
(`citations`/`enrichment`/`budget-fit` dimensions + `pass_threshold`)
that `semantic-audit-part.md`'s prompt reads to score each part in the
first place. That file is a different concern (scoring rubric, consumed
at audit time) from this one (score-blending formula, consumed at
aggregation time) — reusing its name would silently overwrite it, so
this proposal's file is named `full-part-blend.yaml` instead, keeping
both:

```yaml
id: semantic_full_part_blend
calculation: weighted_merge
inputs:
  full: academic_semantic_runs WHERE scope='section-full'
  citations: academic_semantic_runs WHERE scope='section-part' AND part_kind='citations'
  enrichment: academic_semantic_runs WHERE scope='section-part' AND part_kind='enrichment'
  budget_fit: academic_semantic_runs WHERE scope='section-part' AND part_kind='budget-fit'
weights:
  full: 0.70
  citations: 0.10
  enrichment: 0.10
  budget_fit: 0.10
formula: |
  score = full.score * 0.70 + citations.score * 0.10 + enrichment.score * 0.10 + budget_fit.score * 0.10
note: >
  Part-level scores are missing until their usecases run (references
  domain has no part scores at all — collation only, no citations/
  enrichment/budget-fit stages of its own). Missing parts redistribute
  their weight to `full` rather than treating a missing part as 0 —
  same "don't penalize for not-yet-run" pattern as this proposal's
  document-level ensemble (§5c uses the identical rule for missing models).
```

### 3c. Per-domain `summary.md` + whole-paper `summary.md` → `whole-paper-summary.md`

`templates/report/markdown/domain/{domain}/summary.md` (§2a) renders
`aggregation_domain`'s `final_score`, `deterministic.score`,
`semantic.score` (the blended §3b number), and the score band
(`calculation/summary/score_bands.yaml`, unchanged, already domain-scope-
agnostic). The existing whole-paper `summary.md` is renamed
`whole-paper-summary.md` (§2a) so the two aren't confused by name — it
keeps its existing content (whole-paper `final_score` from
`calculation/summary/final_score.yaml`'s document-coherence formula,
unaffected by this proposal) and gains one addition: a table of all 12
domains' `aggregation_domain` scores, so a reader gets the roll-up
without opening 12 separate per-domain `summary.md` files.

## 4. Deterministic Audit Governance — Commit-Hash Gated

### 4a. Pre-flight clean-tree gate

New script, `script/schema/git_gate.py` — alongside `run_full_workflow.py`,
its only caller, not `script/common/` (that directory is the shared
DB/schema helper library — `academic_schema.py`, `_adapter.py` — imported
across every usecase script; `git_gate.py` shells out to `git`, touches
no SQLite, and has exactly one caller, so it doesn't belong in the
shared-library directory). Called once at the top of `run_full_workflow.py`'s
`main()` (before Phase 1, `run_full_workflow.py:631`), not per-domain:

```python
def require_clean_tree(repo_root):
    """Aborts the whole workflow run if repo_root has staged, unstaged,
    or untracked changes. No override — see §4a note."""
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain"],
        capture_output=True, text=True, check=True)
    if result.stdout.strip():
        raise SystemExit(
            "audit blocked: uncommitted or untracked changes in "
            f"{repo_root}:\n{result.stdout}\n"
            "Commit these changes, or add them to .gitignore if they're "
            "not meant to be tracked, before running the audit. The "
            "deterministic and semantic audits record the commit hash "
            "they ran against — an audit against a dirty tree can't be "
            "reproduced or trusted later.")

def current_commit(repo_root):
    return subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
```

**No `--force` bypass for the dirty-tree check itself** — unlike §4c's
skip-cache (which has a legitimate reason to force a re-run), there's no
legitimate reason to audit uncommitted state; the whole point of
recording `commit_sha` is that the audit result is reproducible against
that exact commit. If the *repo being audited* isn't a git repo at all
(no `.git` — some concrete systems might not be), `git status` itself
fails; that failure propagates as a clear error rather than silently
skipping the gate — this is a hard precondition, not a soft check.

### 4b. Schema — `commit_sha` on `academic_deterministic_findings`

```sql
-- schema/20-academic_deterministic_findings.sql
commit_sha TEXT NOT NULL,
-- the git commit (repo_root's HEAD) this audit ran against.
-- Populated from git_gate.current_commit() at invocation time, not
-- computed by this table's own logic.
```

`deterministic_audit.py` gains a `commit_sha` parameter (threaded from
`run_full_workflow.py`, which computes it once via `git_gate.current_
commit()` and passes it into every domain's step payload — one git call
per workflow run, not per domain). `record_deterministic_findings()`
gains the same parameter, stores it in the new column.

### 4c. Skip-if-unchanged

Before invoking `deterministic-audit-{d}` (`run_full_workflow.py:778-796`),
check the domain's latest `academic_deterministic_findings.commit_sha`
against the current commit:

```python
latest = academic_schema.get_latest_deterministic_findings(conn, paper_id, domain)
if latest and latest["commit_sha"] == current_commit and not force:
    print(f"skip {domain}: unchanged since {current_commit[:8]}")
    continue
```

`run_full_workflow.py` gains a `--force` flag (today has none, confirmed
§0) that bypasses this specific check — re-runs every domain's
deterministic audit regardless of commit match. Doesn't bypass §4a's
dirty-tree gate (that one has no override, per §4a).

## 5. Semantic Audit Governance — Model + Commit Gated

### 5a. Schema — `commit_sha` on `academic_semantic_runs`, same mechanism

```sql
-- schema/09-academic_semantic_runs.sql
commit_sha TEXT NOT NULL,
```

Same population path as §4b — `run_full_workflow.py` computes it once,
threads it through the semantic-audit triad's payload,
`persist_domain_semantic_score.py` passes it to `upsert_semantic_score()`.

### 5b. Skip rule — commit unchanged AND this model already scored it

Semantic's cache key is `(commit_sha, model)`, not `commit_sha` alone —
narrower than deterministic's, because a second model auditing the same
unchanged commit is new information (a new ensemble member, §6), not a
redundant re-run:

```python
existing = academic_schema.get_semantic_runs_for_commit(
    conn, paper_id, domain, scope, part_kind, commit_sha=current_commit)
if any(r["model"] == requested_model for r in existing) and not force:
    print(f"skip {domain}/{scope}: {requested_model} already scored {current_commit[:8]}")
    continue
```

If `commit_sha` differs from every existing row's commit, every model's
score for that domain/scope is stale — re-run for whichever models are
requested this round, same "content changed → semantic judgment must be
re-earned" reasoning as the deterministic audit's simpler rule.

### 5c. This rule must be declared, not just implemented

Two places, per the request that this be "available in prompt and
available in calculation and rules," not only encoded in
`run_full_workflow.py`'s Python:

- **`prompt/semantic-audit/*.md`** (currently no mention of rerun policy
  at all, confirmed §0) gains a short preamble: "This domain's semantic
  score is cached per `(commit, model)`. If you're re-running with the
  same model against the same commit, the cached score stands — you're
  here because either the code changed or a new model is being added to
  the ensemble." Informs the agent *why* it's being invoked, doesn't ask
  the agent to implement the check itself (that's `run_full_workflow.py`'s
  job, §5b) — the note prevents the agent from silently overwriting an
  unrelated existing score with a redundant run if it's ever invoked
  ad hoc, outside the orchestrator.
- **`calculation/semantic/rerun-policy.yaml`** (new, one file, not
  per-domain — the policy is uniform):
  ```yaml
  id: semantic_rerun_policy
  calculation: cache_key
  key_fields: [commit_sha, model]
  rule: >
    A semantic run is reusable (skip re-scoring) iff an existing row
    matches on both commit_sha and model for the same
    (paper, domain, scope, part_kind). Any mismatch requires a new run.
  ```
  This is the machine-readable form of §5b's rule — `run_full_workflow.py`'s
  skip-check should read `key_fields` from this file rather than hardcoding
  `(commit_sha, model)` inline, so a concrete system that wants a looser
  or stricter policy (e.g. commit-only, ignoring model) can override this
  one file instead of patching the orchestrator script. Same override
  mechanism every other `calculation/` file already uses.

## 6. Multi-Model Semantic Ensemble

### 6a. Requesting multiple models for one audit round

`run_full_workflow.py`'s semantic-audit invocation (`:797-820`) currently
threads a single `model` value per triad. Gains a `--models` flag
(comma-separated, e.g. `--models claude-sonnet-5,gpt-5`) — when set,
Phase 7 loops the semantic-audit triad once per model per domain instead
of once per domain, each becoming its own triad invocation with §5b's
skip-check applied per-model (so re-running with `--models claude-sonnet-5`
after an ensemble already has `claude-sonnet-5` + `gpt-5` scores just
confirms the cache hit for the one requested model, doesn't touch the
other).

**`--force` × `--models` — locked to per-model granularity.** `--force
--models claude-sonnet-5` re-runs only `claude-sonnet-5` against the
current commit; any other model already in the ensemble (`gpt-5`) is
left untouched. This is the only choice consistent with everything else
in §5/§6 being scoped per-`(commit_sha, model)` rather than per-domain —
`--force` bypasses §5b's skip-check for the specific `(domain, scope,
part_kind, model)` tuples the invocation actually touches, nothing wider.
Re-running the whole ensemble under `--force` means passing the full
`--models` list, not omitting it.

### 6b. Individual report per model

§2b's `semantic-full.md`/`semantic-part.md` render **every** model's
score for that domain/scope as a `{{#models}}...{{/models}}` block —
one row (or subsection, matching §4's per-domain-report style from the
visualization-depth proposal) per model that has scored this domain,
same shape as `python_hackathon`'s `model_results[]` pattern
(`fetch_semantic_data()`, confirmed in that system's
`render_reports.py:95`) — not a single collapsed number. The mean (§6c)
renders as an additional, clearly-labeled row below the per-model rows,
not in place of them.

### 6c. `calculation/semantic/ensemble/{domain}.yaml` — direct port

```yaml
# calculation/semantic/ensemble/methodology.yaml
id: semantic_ensemble_methodology
calculation: reliability_aware_ensemble
scope: section-full
inputs:
  from: academic_semantic_runs WHERE domain='methodology' AND scope='section-full'
  fields: [model, overall_score, reasoning]
formula: |
  mean_score = mean(scores)
  stdev_score = stdev(scores)
  agreement = "High" if stdev_score <= 5 else "Medium" if stdev_score <= 15 else "Low"
  final_score = mean_score
outputs:
  - score
  - agreement
  - stdev
note: >
  Single-model rounds (stdev undefined / n=1) report agreement="N/A" —
  same "not enough data" degrade-gracefully rule the visualization-depth
  proposal's chart specs already use (§0's model-score-spread chart
  skip-if-<3 rule is the same shape at a different threshold; here n=1
  is the floor since a mean of one score is still meaningful, just not
  an agreement signal).
```

`final_score` (the mean) is what §3b's `semantic/full-part-blend.yaml`
consumes as `full.score` — the ensemble mean, not any single model's
number, is what feeds the domain aggregate (§3a).

### 6d. Part-level ensemble files — resolved (§9)

Section-part scopes also get ensemble files, not just section-full.
Per-domain part-level ensemble lives at
`calculation/semantic/ensemble/{domain}-{part_kind}.yaml` (e.g.
`methodology-citations.yaml`, `methodology-enrichment.yaml`,
`methodology-budget-fit.yaml`). Same `reliability_aware_ensemble`
formula as §6c — the only difference is the `scope` field
(`section-part` instead of `section-full`) and the `WHERE` clause
adding `AND part_kind='{part_kind}'`.

Total ensemble files: 12 domains × 4 scopes (1 full + 3 parts) = 48.

## 7. Schema Changes — Consolidated

```sql
-- schema/20-academic_deterministic_findings.sql
commit_sha TEXT NOT NULL DEFAULT '',   -- §4b

-- schema/09-academic_semantic_runs.sql
commit_sha TEXT NOT NULL DEFAULT '',   -- §5a
-- computed_against column dropped (ALTER TABLE ... DROP COLUMN, SQLite
-- 3.35.0+) — dead code (§0), superseded by commit_sha as the actual
-- staleness mechanism. Its write in upsert_semantic_score()
-- (academic_schema.py:411-443, the computed_against=None param and the
-- INSERT's json.dumps(computed_against or {}) at line 442) is removed
-- in the same change, not left as an unused parameter.
```

`DEFAULT ''` (not a bare `NOT NULL`) so `ALTER TABLE ... ADD COLUMN`
succeeds against any table that already has rows (SQLite has supported
`ADD COLUMN ... DEFAULT` since 3.25.0) — no migration script needed.
Pre-existing rows backfill with `commit_sha=''`. §4c/§5b's skip-checks
both treat `''` as "unknown commit" — never a cache hit (`'' ==
current_commit` is never true for a real git SHA), so old rows simply
can't produce a false skip; the first post-upgrade audit run always
re-runs and overwrites them with a real hash. No changes to `UNIQUE`
constraints on either table — `commit_sha` is
metadata on the row, not part of either table's identity key (identity
stays `(paper_id, domain_id, scope, model, run_number, part_kind)` for
semantic runs, `(paper_id, domain_id, run_number)` for deterministic —
multiple runs at the same commit are still distinct rows, e.g. a
deliberate `--force` re-run, or a second model scoring an unchanged
commit).

## 8. New/Changed Files — Consolidated

**New report templates (144 files, §2a):**
`templates/report/{markdown,html}/domain/{domain}/{deterministic,semantic-full,semantic-part,plagiarism,humanize,summary}.{md,html}`
× 12 domains.

**Report templates today (8 files) — disposition of each:**
`deterministic.{md,html}` and `semantic.{md,html}` (4 files) are
**replaced** by the per-domain versions in §2a. `summary.{md,html}`
(2 files) is **kept and renamed** to `whole-paper-summary.{md,html}`
(§3c), content otherwise unchanged. `pipeline-progress.{md,html}`
(2 files) is **kept as-is**, untouched by this proposal. Of the 6
per-domain report kinds in §2a, `deterministic`/`semantic-full`/
`semantic-part`/`summary` map to (or split from) the 4 replaced files;
`plagiarism.{md,html}` and `humanize.{md,html}` are **entirely new**
report kinds — no template for either exists today (§2b).

**New calculation files:**
`calculation/aggregation/domain/{domain}.yaml` × 12 (§3a),
`calculation/semantic/full-part-blend.yaml` (§3b, one file, not
per-domain — formula is uniform, weights are the override surface; not
to be confused with the existing `calculation/semantic/section-parts.yaml`,
which stays untouched, §3b naming note),
`calculation/semantic/ensemble/{domain}.yaml` × 12 (§6c, section-full
  scope) + `calculation/semantic/ensemble/{domain}-{part_kind}.yaml` × 36
  (§6d, section-part scope: citations/enrichment/budget-fit per domain),
`calculation/semantic/rerun-policy.yaml` (§5c, one file).

**Changed scripts:**

| File | Change |
|---|---|
| `script/schema/git_gate.py` | New — `require_clean_tree()`, `current_commit()` (§4a) |
| `script/schema/run_full_workflow.py` | Calls `git_gate.require_clean_tree()` + `current_commit()` once at startup; Phase 6 gains skip-if-commit-unchanged (§4c); Phase 7 gains skip-if-(commit,model)-unchanged (§5b) + `--models` fan-out (§6a); new `--force` flag |
| `script/deterministic-audit/deterministic_audit.py` | Gains `commit_sha` param, threaded to `record_deterministic_findings()` (§4b) |
| `script/semantic-audit/persist_domain_semantic_score.py` | Gains `commit_sha` param (from payload, same pattern as §6 of the prior proposal's `--scope`/`--part-kind` fix), threaded to `upsert_semantic_score()` (§5a) |
| `script/common/academic_schema.py` | `record_deterministic_findings()` + `upsert_semantic_score()` gain `commit_sha` param; `upsert_semantic_score()` loses `computed_against` param + its INSERT column (§7 — dead code removed, not left dangling); new `get_semantic_runs_for_commit()` query helper (§5b) |
| `script/render-audit-report/generate_audit_report.py` | Render loop rewritten: outer loop over domains, inner loop over 6 per-domain report kinds (§2c); output path gains `domain/{domain_key}/` segment |
| `prompt/semantic-audit/*.md` | Rerun-policy preamble added (§5c) |
| `script/schema/generate_templates.py` | New — programmatic generator for 144 per-domain report templates (§9a) |

**Schema:** `commit_sha` column on both `academic_deterministic_findings`
and `academic_semantic_runs` (§7).

## 9. Open Questions — Resolved

- **§6c's ensemble scope** — resolved: ensemble files for **both**
  `section-full` and `section-part` (3 `part_kind` values). Per-domain
  ensemble files live at `calculation/semantic/ensemble/{domain}.yaml`
  (section-full scope) and `calculation/semantic/ensemble/
  {domain}-{part_kind}.yaml` (section-part scope, 3 files per domain =
  36 total). Part-level ensemble added because multi-model disagreement
  on citation quality or budget-fit can surface genuine rubric ambiguity,
  not just mechanical scoring differences. If a concrete system decides
  part-level ensemble adds noise, it overrides by deleting the part
  files — same "delete to disable" mechanism as any other
  `calculation/` override.

## 9a. Implementation Decisions (post-review)

- **Template generation** — 144 per-domain report templates generated
  programmatically from a Python script (`script/schema/generate_templates.py`)
  rather than hand-written. Script reads the domain list from
  `academic_schema.py`'s `STRUCTURAL_DOMAINS`, reads template shape specs
  from an inline dict, and writes all 144 files in one pass. Script is
  run once during implementation, committed alongside the output files,
  and can be re-run if template shapes change.
- **Commit granularity** — changes split across multiple commits by
  logical phase: schema+core, calculation YAMLs, report templates,
  render loop, governance scripts, prompt updates.
- **Part-level ensemble count** — 12 domains × 4 scopes (1 full +
  3 parts) = 48 ensemble YAML files total.

## 10. Explicitly Out of Scope

The 144 template files' actual markup beyond the shapes shown, the
`git_gate.py`/`run_full_workflow.py` skip-check code beyond the pseudocode
shown, `--models` fan-out's actual triad-spawning implementation, any
change to which usecases exist or what they check (this proposal only
changes reporting granularity and adds gating around existing usecase
invocation), and the visualization/chart layer (prior proposal's §5,
untouched — new charts for the per-domain summary report, if wanted, are
a follow-on, not covered here).
