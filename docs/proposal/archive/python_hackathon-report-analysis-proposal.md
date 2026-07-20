# python_hackathon — Execution Pipeline + Report-Time Analysis Proposal

**Proposal 2 of 3, in dependency order** —
`python_hackathon-visualization-and-detail-templates-proposal.md`
(proposal 1) defines the visualization catalog and per-section
template depth this proposal's §9/§10 design against;
`python_hackathon-pipeline-verification-proposal.md` (proposal 3)
checks whether scripts exist to actually execute what all three
propose. Written before proposal 1 existed (flagged honestly in
proposal 1's own opening) — proposal 1 §3 covers what that means for
this proposal's chart scope.

Two things, not one, because the current state has two different-sized
gaps: (1) the layer that turns raw audit checks into stored,
per-participant, per-domain scores **doesn't exist at all** — nothing
runs the deterministic/semantic audits, nothing persists results,
nothing registers who's competing; (2) the base_dev-style narrative +
visualization + HTML layer this proposal was asked to add **also
doesn't exist**. Both are covered here, built on the base_dev
proposal's corrected lessons (§1) rather than repeating its mistakes.

Not a from-scratch design — python_hackathon already has real,
working parts: 10 domains' worth of deterministic rules and semantic
prompts (`audit/{deterministic,semantic}/document/*`), working
formulas (`calculation/`), and a fully-implemented z-score + weighted
leaderboard (`script/statistics.py`, `script/leaderboard.py`). This
proposal wires those together and adds what's missing — it does not
rewrite what already works.

---

## 0. Current state — grounded in what's actually on disk

**Implementation status note**: Items marked **Built** or **Fixed**
in the table below and in bugs #1–#5 have been verified implemented
in code and confirmed working. Items marked **Missing** or **Designed
(not built)** exist only in this proposal — they need implementation.
The same confident phrasing ("Fixed in §6") applies to both states;
look for the explicit "(implemented, verified)" tag to distinguish.

| Piece | State | Evidence |
|---|---|---|
| Deterministic rules (10 domains) | **Built** | `audit/deterministic/document/*.yaml` — weight/mandatory/condition per rule, same shape as base_dev's rules |
| Deterministic scoring formula | **Built** | `calculation/deterministic/document.yaml` — `weighted_pass_rate` |
| Semantic prompts (10 domains) | **Built** | `audit/semantic/document/*.yaml` — one prompt + `evidence_requirements` schema per domain, `.yaml` not base_dev's `.md` |
| Semantic ensemble formula | **Built** | `calculation/semantic/ensemble/*.yaml` — mean/stdev/agreement across `required_models: [claude-3-5-sonnet, gemini-1.5-pro, gpt-4o]` |
| Deterministic **audit runner** | **Missing** | `audit_infrastructure.py` etc. (7 scripts) print raw booleans (`uv_lock_present: true`) to stdout — nothing evaluates them against the `.yaml` rules' `condition`/`weight`/`mandatory` fields, nothing produces a 0–100 score |
| Semantic **audit runner** | **Missing** | Nothing calls the 3 models the ensemble formula expects inputs from |
| Score aggregation | **Built, unfed** | `score_aggregator.py`/`statistics.py`/`leaderboard.py` are complete, correct z-score (MAD-based, tanh-bounded) and weighted-leaderboard math — but they read a `results/{team}/{domain}/{model}.json` file tree that **nothing populates** |
| Team/repo registration | **Missing entirely** | No `.samgraha` involvement for this standard at all — `results/{team}/` directory names are the only place a team identity exists today, informally |
| DB persistence | **Missing** | Everything is files; no participant table, no results table |
| Markdown report **templates** | **Built** — corrects the previous draft, which assumed these were missing | `templates/reports/domain/{domain}-{deterministic,semantic,summary}.md` (30 files, all 10 domains × 3 kinds) + `templates/reports/global-leaderboard.md` + `templates/reports/team-final-summary.md`. Mustache syntax (`{{#each}}`/`{{this.x}}`), not base_dev's `{{path}}`-only style — §9 below. |
| Markdown **renderer** | **Missing** | Nothing reads these templates and substitutes data — same "config exists, runner doesn't" pattern as the rest of §0. |
| Narrative / visualization / HTML | **Missing** | Pipeline stops at `leaderboard.md`. `team-final-summary.md`'s `{{ executive_summary }}` is already the intended slot for §8's agent-written narrative — one field, already there, waiting for content. |
| Stage ordering | **Documented** | `plan/core/loop.yaml` — repository → det-audit → sem-audit → det-calculate → sem-calculate → aggregate → relative(z-score) → normalize → validate → report. Treated as the source of truth for ordering below. |

**Four bugs found in the existing code, verified by reading, not
assumed** — reclassified from an earlier "flag, don't fix" pass after
review pushback: these block §4/§6 outright, not cosmetic:

1. **`leaderboard.py`'s `DOMAIN_KEY_MAP` silently zeroes 3 domains'
   weights (CRITICAL).** *(implemented, verified)* — `leaderboard.py`'s
   `_load_weights()` normalizes keys to underscores at load time.
2. **Stdout contamination in 2 of 7 audit scripts (HIGH).**
   *(implemented, verified)* — `audit_testing.py` and
   `audit_model_artifact.py` info prints go to stderr.
3. **3 of 10 domains have no deterministic audit script at all
   (HIGH).** *(implemented, verified)* — `audit_documentation.py`,
   `audit_data_quality.py`, `audit_ai_explanations.py` exist; orchestrator
   checks for script existence before attempting deterministic pass.
4. **The 60/40 det/sem split is duplicated, not undocumented**
   *(implemented, verified)* — reads from
   `calculation/aggregation/domain/{domain}.yaml` at runtime.
5. **`{domain}-semantic.md`'s "Median Score" label doesn't match what
   gets computed (MEDIUM).** *(implemented, verified)* — label reads
   "Mean Score," templates use `{{ mean_score }}`.

**Three more pre-existing inconsistencies — no longer deferred, each
gets a resolution below** (an earlier draft of this proposal called
these "not this proposal's job to fix"; correcting that — §4 can't be
built without picking an answer for #1):
1. Final-score scale disagreement: `weights.yaml` says `final_scale: 150`,
   `loop.yaml` says `cap: 20`, `validate_scores.py` checks
   `final_score in [0,20]`. Three different numbers for the same thing
   — resolved in §11 (needs your call on the actual number, but the
   *code* gets made internally consistent regardless of which number).
2. `calculation/semantic/document.yaml` points `inputs.from` at
   `audit/semantic/document/{domain}.md` — the real files are `.yaml`.
   One-line fix, done as part of §4's semantic runner (it has to read
   the right path to work at all).
3. Semantic agreement is defined twice, differently: the ensemble
   formula (`calculation/semantic/ensemble/*.yaml`) uses banded
   thresholds (stdev ≤5/15 → High/Medium/Low), `leaderboard.py`'s
   `_semantic_agreement_bonus` uses a continuous `1 - stdev/25` curve.
   Resolved in §5 — the mean-of-models design changes what "agreement"
   even needs to mean here.

## 1. Design principles carried from base_dev — the "clean now" lessons

Applied below, not restated as abstract advice:

- **Reuse before inventing** (the `score_history.json` lesson) —
  `statistics.py`/`leaderboard.py`'s math is reused byte-for-byte;
  §6 only changes where their input comes from, never the formulas.
- **Generic schema, never entity-named tables** (the `vision_reports`
  mistake) — the new registration table is `standard_participants`,
  not `hackathon_teams`. "python_hackathon" and the team name are data
  in it, not part of a table/column name — same test applied in §2/§3.
- **Semantic judgment that requires actual understanding is
  agent-driven, not scripted** — applies cleanly to the *new* narrative
  layer (§8, mirrors base_dev's `analysis/{domain}.md` exactly). Does
  **not** cleanly apply to the *existing* semantic-audit-scoring step
  (§5) — that's closer to "call 3 rating APIs and store the numbers"
  than "an agent forms a judgment," so it's addressed as its own
  decision, not assumed to be agent-driven by default.
- **File vs. DB decided by the generic-schema test, not by default** —
  if a table can stay standard/participant-name-as-data, DB is fine
  (§2/§3 pass this test — do it). If it can't, keep it a file (nothing
  here fails the test, unlike base_dev's would-be `vision_history`
  table).
- **Always-present summary, explicit "not implemented" for gaps** —
  same shape as base_dev's tier "Not available," applied per-domain
  per-participant here (§7).
- **A verification checklist ships with the proposal** (§12), so
  implementation is checkable against this doc directly, not against
  memory of a conversation.

## 2. New DB schema — participant registration

```sql
CREATE TABLE standard_participants (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    standard            TEXT    NOT NULL,   -- e.g. "python_hackathon" — data, not a table name
    participant_name    TEXT    NOT NULL,   -- slug identifier (e.g. "goal-gpt")
    repo_path           TEXT    NOT NULL,   -- local clone path
    team_name           TEXT,               -- display name (e.g. "Goal GPT")
    team_leader         TEXT,               -- team lead name
    members_json        TEXT,               -- JSON: [{"name":"...", "role":"lead|member"}]
    repo_https          TEXT,               -- HTTPS clone URL
    repo_ssh            TEXT,               -- SSH clone URL
    presentation_order  INTEGER,            -- display order in reports
    time_slot           TEXT,               -- presentation slot (e.g. "11:00 - 11:30 am")
    metadata_json       TEXT,               -- nullable: extensibility catch-all
    registered_at       TEXT    NOT NULL,
    UNIQUE(standard, participant_name)
);
```

**Why explicit columns instead of just `metadata_json`** — the HTML
report templates (§10) need to render team leader, members, and repo
URLs directly in Mustache templates. Mustache can't do
`{{ metadata_json.team_leader }}` (it's a flat string, not a nested
object). Extracting these into real columns means `chevron.render()`
gets `{"team_leader": "Vishnu R Menon"}` as a top-level field, not a
JSON blob that needs a second parse step. Core team identity fields
(team name, leader, members, repo URLs, presentation slot) get
columns; everything else stays in `metadata_json` for extensibility.

**Why not a separate `standard_teams` table** — team and participant
are the same entity here (one repo submission per team). A separate
table would require a JOIN for every report query with no normalization
benefit — there's no "one team, many participants" relationship.

**Why not `register_repository`** (samgraha's existing MCP tool) —
checked `crates/registry/src/migration.rs`'s `REG_V1` comment: that
table (`repository_cache`) stores *dependency-manifest* metadata for
one project's own dependency graph — a completely different concept
from "which teams are competing." Repurposing it would be a semantic
misuse of an existing table, not reuse.

**Why a new table and not just a column on `standard_audit_runs`** —
registration (who's competing) and results (many audit runs per
competitor) have different lifecycles: register once, audit
repeatedly. Two tables for two lifecycles is normal relational
practice, not premature structure — see §3 for where the audit-run
granularity problem actually shows up.

## 3. New DB schema — audit results storage

`standard_audit_runs` (existing, V33) is one row per `(standard,
pipeline)` run, with a single `score` and `model` — built for "did
this standard's audit pass," not "10 domains × up to 3 models × N
participants," and z-score computation (§6) needs the per-model,
per-domain breakdown, not a single rolled-up number. Stuffing that
into `standard_audit_runs.report`'s JSON blob would work but pushes
the leaderboard's aggregation logic from SQL into application code —
defeats the point of moving off files. New table, same column-naming
conventions as `standard_audit_runs` for consistency:

```sql
CREATE TABLE standard_domain_scores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id  INTEGER NOT NULL REFERENCES standard_participants(id),
    domain          TEXT    NOT NULL,   -- "infrastructure", etc. — data, not schema
    kind            TEXT    NOT NULL,   -- "deterministic" | "semantic"
    model           TEXT    NOT NULL DEFAULT '',  -- '' for deterministic (single pass);
                                         -- model id for semantic (one row per model that's
                                         -- run this participant+domain so far — §5)
    score            REAL   NOT NULL,
    raw_evidence_json TEXT,             -- rule/criterion pass-fail detail, JSON
    created_at      TEXT    NOT NULL,
    UNIQUE(participant_id, domain, kind, model)
);
CREATE INDEX idx_sds_participant_domain ON standard_domain_scores(participant_id, domain);
```

One row per (participant, domain, kind, model) — a domain's
deterministic score is one row (`model=''`, re-running it upserts —
`kind="deterministic"` is defined to run exactly once per
participant+domain, per your description, so a re-run is a
correction, not a second data point); its semantic score is one row
per model that has evaluated it so far, growing as more
model-backed sessions run §5's rubric (`UNIQUE` constraint makes this
an upsert per model, not an ever-growing duplicate set if the same
model runs twice). Missing domain (§7) = simply no row, not a row
with a zero — the query layer distinguishes "scored zero" from
"never run."

**`standard_narratives`** — the agent-driven narrative output from §8,
DB-native for the same reason §3's scores are: the data's already
relational, no reason to round-trip through a file first.

```sql
CREATE TABLE standard_narratives (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id  INTEGER REFERENCES standard_participants(id),  -- NULL for the
                                         -- competition-wide narrative (§8)
    domain          TEXT,               -- NULL for the competition-wide narrative
    sections_json   TEXT    NOT NULL,   -- [{"heading":..., "text":...}, ...] — same
                                         -- shape as base_dev's {domain}-narrative.json
    created_at      TEXT    NOT NULL
);
```

No `UNIQUE` constraint here on purpose — SQLite treats `NULL`s as
distinct from each other, so `UNIQUE(participant_id, domain)` would
silently fail to dedupe the competition-wide row (`participant_id IS
NULL` every time), letting duplicates through. Upsert handled in
application code instead (`SELECT` existing row for this
participant+domain, `UPDATE` if found, `INSERT` if not) rather than
leaning on a constraint that doesn't actually cover the NULL case.

## 4. Orchestrator — the missing execution layer

No `init.py`-equivalent exists for this standard. New script,
`run_hackathon.py`, following `loop.yaml`'s stage order, one
participant fully processed before the next starts — matches your
literal ask ("deterministic first for one repo... then semantic for
same repo... then do for other repo"):

```
for participant in list registered standard_participants:
    for domain in weights.yaml's domains (reuse verify_standard.py's
                  load_weights() — it already does exactly this lookup):

        # Deterministic (scripted, existing runners + new middle layer)
        raw = run audit_{domain}.py-equivalent against participant.repo_path
        rule_results = evaluate raw against audit/deterministic/document/{domain}.yaml
                       (new: condition/weight/mandatory → pass/fail per rule —
                       same shape as base_dev's evaluate_rules.py, doesn't exist yet here)
        score = apply calculation/deterministic/document.yaml's weighted_pass_rate
        INSERT INTO standard_domain_scores (kind="deterministic", model=NULL, ...)

        # Semantic (scripted or agent-driven — see §5's decision)
        for model in configured models for this domain:
            score = evaluate audit/semantic/document/{domain}.yaml's prompt against repo
            INSERT INTO standard_domain_scores (kind="semantic", model=<model>, ...)

    # domain loop for this participant is now fully done, deterministic
    # and semantic both, before moving to the next participant
```

The "evaluate raw facts against the rule's `condition`/`weight`" step
doesn't exist anywhere in this standard today — it's the direct
analog of base_dev's `evaluate_rules.py`, adapted to this standard's
7 existing `audit_*.py` scripts' output shape instead of rewriting
them (they already gather the right raw facts, e.g.
`audit_infrastructure.py`'s `uv_lock_present` maps directly to rule
`inf-001`'s `evidence.target: uv.lock` — the runners are fine, only
the rule-evaluation step on top of them is missing).

**Fixing §0's bug #2 (stdout contamination)**: the orchestrator
captures each `audit_*.py`'s stdout and `json.loads()`s it — that
breaks today for `audit_testing.py`/`audit_model_artifact.py`. Fix at
the source, not with a fragile "find the JSON line" parser in the
orchestrator: change their info `print()`s (lines 155-160 and
256-261 respectively) to `print(..., file=sys.stderr)`. Two-line
change per file, keeps stdout JSON-only for every script uniformly —
the orchestrator's stdout capture doesn't need script-specific
exceptions.

**Fixing §0's bug #3 (3 missing audit scripts)**: `documentation`,
`data-quality`, `ai-explanations` have no `audit_*.py`. Don't write
stub scripts that fake an empty result — that's indistinguishable
from a real script that legitimately found nothing. Instead, the
orchestrator's domain loop checks whether an `audit_{domain}.py`
exists before attempting the deterministic pass; if it doesn't, skip
straight to §7's missing-domain handling (no row written) for that
domain's deterministic score specifically — the domain can still get
a semantic score via §5 if its `audit/semantic/document/{domain}.yaml`
prompt exists (it does, for all 10). A domain missing *only* its
deterministic runner isn't fully "not implemented" the way §7
describes a domain with nothing at all — it's partially scored,
deterministic contributes 0 via the same weighted-merge formula (§0
bug #4) that already handles a 0 input gracefully, no special case
needed beyond "no deterministic row exists."

**Fixing §0's bug #4 (60/40 split hardcoded, not read)**: the
orchestrator's aggregation step reads `weights.deterministic`/
`weights.semantic` from `calculation/aggregation/domain/{domain}.yaml`
per domain (already there, already 0.60/0.40 for all 10, checked) —
the same `load_yaml()`-then-index pattern `verify_standard.py`
already uses elsewhere in this standard — instead of `score_aggregator.py`'s
hardcoded `DET_WEIGHT`/`SEM_WEIGHT` constants. If a future domain
needs a different split (e.g. a domain with no meaningful
deterministic checks), the yaml already supports it per-domain; the
hardcoded constants today don't.

### 4a. Deterministic audit gap log — all 10 domains, exhaustively checked

Widened per your last message from the 5 scripts already read to all
10 domains in `audit/deterministic/document/` — every domain's rules
read against whether a script exists and, where one does, whether it
actually fulfills what its own rules ask for. No domain skipped.

| # | Domain | Script | Coverage | Gap |
|---|---|---|---|---|
| 01 | infrastructure | `audit_infrastructure.py` | Matches its own rules exactly (uv.lock/Dockerfile/compose file presence) | Rules themselves are file-presence-only — not deepened here since not in your named categories (static analysis/git/testing/model/artifact); noted for completeness, not proposed as work. |
| 02 | engineering | `audit_python.py` | Config-presence only (radon.cfg/.bandit/pyproject.toml sections) | **Shallow — real gap.** Never runs radon/mypy. Expansion below. |
| 03 | testing | `audit_testing.py` | Actually runs pytest, parses JSON report, coverage | **Already deep.** No work proposed. |
| 04 | documentation | **none** | — | **Missing entirely** (§0 bug #3). Rules need: file presence (trivial), markdown section detection ("Installation"/"Setup" heading — needs real parsing, not just grep), link resolution (`doc-003` — relative links checkable locally; external links need a network call, which would break `audit_model_artifact.py`'s established offline-only precedent for this standard — flagging the tension, not resolving it silently). Low complexity apart from that one question. |
| 05 | security | `audit_security.py` | Actually runs bandit + real secret regex scan | **Already deep.** No work proposed. |
| 06 | mlops | `audit_mlops.py` | Directory-presence only (.dvc/dvc.yaml/mlruns/data) | **Shallow — real gap.** Never inspects DVC pipeline structure or MLflow run history. Expansion below. |
| 07 | runtime | `audit_model_artifact.py` | Deep for `run-002`–`run-005` (format/VRAM/timing/API-contract, all via real sandboxed execution) | **`run-001` (entrypoint exists) is never actually evaluated by anything.** The script takes `--entrypoint` as an explicit CLI arg, default `None` — it doesn't discover `main.py`/`app.py`/`run.py` itself (checked: no such glob/existence logic anywhere in the file). Something has to do that discovery and hand the result in; today nothing does. Small, specific gap inside an otherwise-thorough script — the orchestrator (§4) should do this discovery before invoking it. |
| 08 | team-workflow | `audit_git.py` | Real git history analysis — commits, authors, conventional-commit rate, GitFlow branches, PR evidence | **Already deep.** No work proposed. |
| 09 | data-quality | **none** | — | **Missing entirely** (§0 bug #3). Rules need: local file/directory presence (`.csv`/`.parquet`/`.jsonl`, `data`/`dataset` dirs) and a regex scan of README for known data-hub URLs (kaggle/huggingface/drive) — both trivial, no subprocess, no network, simpler than #02/#06's expansion below. |
| 10 | ai-explanations | **none** | — | **Missing entirely** (§0 bug #3). Rules need: dependency-list scan (`requirements.txt`/`pyproject.toml` for openai/anthropic/etc.) and a filename-pattern glob (`*prompt*`, `system_instructions*`) — both trivial, same complexity class as #09. |

**Net**: 4 real gaps, not 2 — the previous pass caught engineering and
mlops (deepening), missed runtime's `run-001` sub-gap and understated
documentation/data-quality/ai-explanations as just "no script" without
noting they're actually the *easiest* of the gaps to close (no
subprocess, no external tool, no new evidence type — plain file/regex
checks the existing `file_presence`/`regex_match`/`dependency_presence`
evidence types in §0 bug #3's domains already describe). Build order,
cheapest first: 09, 10 (trivial) → 04 (trivial except the link-check
network question) → 07's entrypoint-discovery fix (small, inside §4's
orchestrator) → 02, 06 (real new subprocess-running logic, below).

**Two deepening gaps, matched by their rules being equally shallow today**
— checked `audit/deterministic/document/02-engineering.yaml` (5 rules,
all `file_presence`/`config_analysis` evidence types — "radon
configuration present," not "radon reports acceptable complexity")
and `06-mlops.yaml` (2 rules, both `file_presence`) — the scripts
aren't underperforming their own rules, the rules themselves only ever
asked for config presence. Deepening means changing both together,
same evidence-type pattern `audit_security.py`/its rules already use
(`bandit_executed`, `bandit_high_severity_issues` — actual tool
output, not just "bandit is configured").

**`audit_python.py` — proposed expansion**, mirroring
`audit_security.py`'s existing shape (config check, then actually run
the tool, capture structured output, degrade gracefully if the tool
isn't installed — same pattern `audit_testing.py` already uses for
optional pytest plugins):

- Run `radon cc <repo> -j` (cyclomatic complexity, JSON output) →
  count of functions above a complexity threshold, not just "radon.cfg
  exists."
- Run `mypy <repo> --ignore-missing-imports` (or respect an existing
  `mypy.ini`/`pyproject.toml` config if present) → error count, not
  just "mypy is configured."
- Bandit stays owned by `audit_security.py` — not duplicated here,
  engineering's rules would reference security's existing bandit
  results rather than re-running it (`domain_relationships`-style
  cross-domain reference, matching how `tiers.yaml`/relationships
  already model domains informing each other elsewhere in this
  standard's design).

**`audit_mlops.py` — proposed expansion**:

- If `dvc.yaml` exists: parse it, count declared pipeline `stages` —
  a real DVC pipeline vs. an empty/placeholder file look identical
  under today's file-presence check; stage count distinguishes them.
- If `mlruns/` exists: count actual run directories under it (MLflow's
  own on-disk layout, one dir per run) — evidence of *use*, not just
  that the tool was initialized once and never run again.
- Both stay fully offline/local-filesystem — no network calls, no
  executing untrusted training code, consistent with `audit_model_artifact.py`'s
  existing "ALL tests run OFFLINE" discipline (its own docstring, §0).

**Rule-file changes this implies** (not just script changes) —
`eng-001`/`eng-002` and `mlp-001`/`mlp-002`'s `evidence.type` moves from
`file_presence`/`config_analysis` to something like `tool_execution`
with a `metric`/`threshold` pair, matching the richer shape
`audit/deterministic/document/03-security.yaml`'s bandit-backed rules
likely already use (worth confirming when this gets built — not
re-verified here, flagged as the pattern to match rather than assumed
identical). This is real scope, not a one-line change — two scripts
gain real subprocess-running logic, two rule files gain a new evidence
type, and `calculation/deterministic/document.yaml`'s
`weighted_pass_rate` formula needs those richer evidence values to
still resolve to a clean pass/fail per rule.

### 4b. Team registration — `teams.json` config file

Heimdall-style team configuration at `python_hackathon/teams.json`:

```json
[
  {
    "team_name": "Goal GPT",
    "participant_name": "goal-gpt",
    "team_leader": "Vishnu R Menon",
    "members": [
      {"name": "Vishnu R Menon", "role": "lead"},
      {"name": "Alice Smith", "role": "member"}
    ],
    "repo_https": "https://github.com/ckr-11/goalGPT",
    "repo_ssh": "git@github.com:ckr-11/goalGPT.git",
    "repo_path": ".hackathon/goal-gpt",
    "presentation_order": 1,
    "time_slot": "11:00 - 11:30 am"
  }
]
```

`run_hackathon.py` auto-loads `teams.json` if present — no CLI change
needed. Each entry maps directly to §2's `standard_participants`
columns: `team_name` → `team_name`, `team_leader` → `team_leader`,
`members` → `members_json` (JSON-serialized), `repo_https` →
`repo_https`, `repo_ssh` → `repo_ssh`, `presentation_order` →
`presentation_order`, `time_slot` → `time_slot`. The existing
`--register` CLI flag still works for one-off registrations without a
config file.

**`register_participant()` signature change** — the current function
only accepts `(conn, standard, name, repo_path, metadata=None)`,
which means calling it as-is leaves all 7 new columns NULL and dumps
everything into `metadata_json` — directly contradicting §2's reason
for adding the columns. Updated signature:

```python
def register_participant(conn, standard, name, repo_path,
                         team_name=None, team_leader=None, members=None,
                         repo_https=None, repo_ssh=None,
                         presentation_order=None, time_slot=None,
                         metadata=None):
```

`members` (a list of dicts) gets JSON-serialized to `members_json`.
All new fields are nullable — a participant registered via the old
`--register` CLI (which only passes name + repo_path + metadata_json)
still works, those columns just stay NULL. `teams.json` entries
provide the full set.

**Why a file and not CLI args** — 5-10 teams with 3-4 members each
is too much data for `--register NAME REPO_PATH METADATA_JSON` on one
command line. The JSON file is the authoritative source of who's
competing; the DB is the runtime copy. Backward compatible: if
`teams.json` doesn't exist, `run_hackathon.py` falls back to reading
participants from DB only (current behavior).

## 5. Semantic audit — agent-driven via MCP, multiple agent sessions, no API (resolved)

**Decided, not a decision point anymore** — corrects the previous
draft's framing, which assumed API calls to 3 named providers were
the only way to fill the ensemble. They're not: the same rubric
(`audit/semantic/document/{domain}.yaml`'s existing prompt) gets run
by whichever agent/CLI session the user is driving at the time —
Claude Code (Sonnet or Opus), Gemini via its own CLI, OpenCode,
Claude via a different agent context (e.g. Antigravity) — each is a
**separate agent-driven pass over the same rubric**, no API
credentials needed for any of them, matching base_dev's "agent
already speaks MCP" pattern exactly, just applied to the scoring step
here instead of only the narrative step.

**Mechanism**:

```
for a given (participant, domain):
    whichever agent runs the audit reads audit/semantic/document/{domain}.yaml's
    prompt, evaluates the repo, produces {score, reasoning, evidence}
    (the file's own evidence_requirements schema — already correctly shaped
    for this, no change needed)

    → INSERT/UPSERT standard_domain_scores(kind="semantic", model=<this
      agent's model id, self-reported>, score=..., raw_evidence_json=...)
```

Repeated across sessions, potentially days apart, potentially by a
different person running a different tool — that's *why* `model` is
tracked per row (§3's schema already has this): it's the join key
that lets "team X, domain Y, scored by Sonnet" and "team X, domain Y,
scored by Gemini" coexist as two rows instead of overwriting each
other, without needing all agents in the room at once.

**Final semantic score for a (participant, domain) = mean of every
model's row so far** — computed at aggregation time (§6), not stored
as its own row (recomputes correctly as more models' rows arrive
over time, no stale cached mean to invalidate).

**Coverage tracking** — the practical problem multi-session,
multi-tool auditing creates: knowing what's left to run. One query
answers it directly from `standard_domain_scores`:

```sql
-- Which (participant, domain, model) combos are missing, given a target model list?
SELECT p.participant_name, d.domain, m.model
FROM standard_participants p
CROSS JOIN (SELECT DISTINCT domain FROM standard_domain_scores) d
CROSS JOIN (SELECT 'claude-sonnet' AS model UNION SELECT 'claude-opus'
            UNION SELECT 'gemini' UNION SELECT 'antigravity-claude') m
LEFT JOIN standard_domain_scores s
  ON s.participant_id = p.id AND s.domain = d.domain
  AND s.model = m.model AND s.kind = 'semantic'
WHERE s.id IS NULL;
```

Run before a session starts to know exactly which (team, domain)
pairs that session's model hasn't covered yet — avoids redundant
re-runs and makes partial-ensemble progress visible instead of
implicit.

**Resolves §0's inconsistency #3** (duplicate agreement-formula
definitions) — revised after finding `01-infrastructure-semantic.md`'s
template (§9) expects an `agreement_level` field reading "High" /
"Medium" / "Low," not a raw number: **both formulas survive, as two
different consumers of the same `stdev`, not two competing
implementations.**

- `leaderboard.py`'s continuous `1 - stdev/25` curve computes the
  actual bonus/penalty applied to the score (already handles `<2`
  models correctly, `return 0.0` — checked) — used for the leaderboard
  math (§6), never shown to a human directly.
- `calculation/semantic/ensemble/*.yaml`'s banded thresholds
  (stdev ≤5 → "High", ≤15 → "Medium", else "Low") compute a
  **display-only label**, fed into the `{domain}-semantic.md`
  template's `agreement_level` field (§9) — a human reads "High
  agreement," not "+4.2 bonus factor."

Same `stdev`, computed once, rendered two ways — the "inconsistency"
was really two legitimate uses of one number that happened to look
like competing formulas until the template's actual consumer showed up.

**Deterministic vs. semantic cadence, restated per your description**:
deterministic is one scripted pass per participant, run once (§4).
Semantic is N agent-driven passes per participant, accumulating over
time as different model sessions run it — not required to happen in
the same sitting as the deterministic pass, and not required to be
"done" before the participant is considered scored (a partial
ensemble — even one model — still produces a valid mean, just a less
agreed-upon one, exactly what the agreement bonus already measures).

## 6. Z-score / leaderboard — reused, not rewritten

**Confirmed end-to-end flow**, per your last message — stated
explicitly here since it's the spine everything else in this proposal
hangs off, and it already matches the 32 existing templates' field
names exactly (good independent confirmation neither of us designed
this from scratch, it was already encoded in `{domain}-summary.md`):

```
per (team, domain):
  raw_domain_score  = weighted_merge(det_score, sem_score)   -- §0 bug #4's yaml, 0-100
                       where sem_score = mean(every model's row so far, §5)
  → scores.raw_merge (template field, {domain}-summary.md)

across all teams, per domain:
  z_score, bonus     = statistics.py's calculate_domain_stats()       -- MAD-based, tanh-bounded
  final_domain_score = raw_domain_score + bonus, capped [0,100]
  → team_stats.z_score / team_stats.relative_bonus / scores.final_domain_score

per team, across all domains:
  weighted_total = Σ (final_domain_score / 100) * domain_weight      -- weights.yaml, sums to 100
  → this is "final score" in your message, pre-scale

  final_score = round((weighted_total / 100) * 20, 2)                -- §12 Q1's resolution
  → team.final_score (global-leaderboard.md, team-final-summary.md), "/20"
```

**One real discrepancy this surfaces**: `leaderboard.py` today has a
*second* bonus stage between the last two steps —
`_semantic_agreement_bonus()` (Phase 4, `leaderboard.py:117-128`)
adds up to ±15 more points at the **team** level, based on inter-model
stdev, on top of `weighted_total`, before scaling
(`max_possible = total_weight + max_sem_bonus`). Your description of
the flow stops at "aggregate all domain scores, that's the final
score, scale to 20" — no second bonus stage. Recommend **dropping
Phase 4** rather than keeping it silently: it would double-count
agreement that's already folded into each domain's `sem_score` (mean
of N models) and its `final_domain_score` (z-score against other
teams' domain scores already reflects how consistent/extreme a team's
result was). Flagging as a real code-behavior change, not assuming —
`leaderboard.py`'s `build_leaderboard()` loses its Phase 4 block and
`final_normalized`'s formula simplifies to exactly the 3-line version
above (`max_possible` becomes `total_weight` only, no `+ max_sem_bonus`).

`statistics.py`'s `calculate_domain_stats()`/`run_z_adjustment()` and
`leaderboard.py`'s `build_leaderboard()` already take in-memory dicts
shaped like `{team: {domain: {...}}}` — they don't care where that
dict came from. New adapter function, replacing
`score_aggregator.py`'s file-tree walk, not touching the math:

```python
def load_aggregated_scores_from_db(conn, standard: str) -> dict:
    """Same output shape score_aggregator.py's aggregate_all_teams() produces,
    sourced from standard_domain_scores instead of results/{team}/{domain}/*.json.
    Semantic score per domain = mean of all standard_domain_scores rows with
    kind="semantic" for that (participant, domain) — §5's "accumulates over
    multiple agent sessions" design, computed fresh each time, not cached.
    Deterministic/semantic weighting reads calculation/aggregation/domain/
    {domain}.yaml's weights.deterministic/weights.semantic per domain (§4's
    fix for §0 bug #4) instead of score_aggregator.py's hardcoded 0.60/0.40."""
    ...
```

Everything downstream (`run_z_adjustment()`, `build_leaderboard()`,
`render_leaderboard_md()`) runs unmodified against this dict — the
z-score formula, the sigmoid bonus, the weighted sum, all stay exactly
as implemented today.

**Fixing §0's bug #1 — corrected direction, per §0's revised
analysis.** `DOMAIN_KEY_MAP`'s underscored values
(`team_workflow`/`data_quality`/`ai_explanations`) are *not* the bug —
they're what `templates/reports/global-leaderboard.md` and
`team-final-summary.md` already use as Mustache variable paths across
3 files, and Mustache identifiers can't contain hyphens. `DOMAIN_KEY_MAP`
stays exactly as it is today. The fix is one line, at the one place
`weights.yaml` gets loaded — normalize its domain keys to underscores
immediately after parsing, so every downstream consumer (the leaderboard
weight lookup *and* the template data dicts, §9) sees one consistent
key convention instead of two:

```python
def _load_weights(weights_file):
    with open(weights_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["domains"] = {k.replace("-", "_"): v for k, v in cfg["domains"].items()}
    return cfg
```

One change, in `leaderboard.py`'s existing `_load_weights()` — not a
new function, not a change to `DOMAIN_KEY_MAP`, not a change to
`weights.yaml` itself (which stays human-readable with hyphens, since
nothing about *authoring* the weights needs Mustache-safe identifiers,
only *consuming* them downstream does).

## 7. Missing-domain handling

Already half-implemented: `score_aggregator.py`'s `aggregate_team()`
returns `{"error": "domain directory missing", "raw_score": 0.0}` for
a domain with no results directory. Same rule, DB-native: a domain
with **no rows** in `standard_domain_scores` for a participant means
score 0 for that domain in the leaderboard weighting (§6 unaffected —
0 just flows through the existing weighted sum), and:

- No deterministic/semantic breakdown rendered for it (§8/§9's HTML
  shows "Not implemented" instead of a chart or narrative).
- **No semantic-narrative generation attempted for it** — the
  agent-driven step (§8) is only invoked for domains that have at
  least a deterministic row; there's nothing to narrate about a domain
  nobody attempted.

## 8. New analysis layer — agent-driven narrative (mirrors base_dev)

Same mechanism as base_dev's corrected §5/§10: a rubric file per
domain under a top-level `analysis/` directory (sibling to `audit/`,
not nested in it — same reasoning as base_dev: this step doesn't
score anything, `audit/`'s job), triggered by the user, performed by
whichever agent has MCP access, reading `standard_domain_scores` for
one participant + domain directly (via DB query, not a file — the
data's already relational here, no reason to export it to JSON first)
and writing a narrative.

Two levels, same as base_dev's per-domain + final-summary split:

- **Per participant, per domain** — `analysis/{domain}.md` rubric
  (10 files, one per hackathon domain) — "here's how team X did on
  infrastructure, and why." Skipped entirely for domains with no rows
  (§7 — including the 3 domains missing their `audit_*.py` runner,
  §0 bug #3/§4: they may still have a semantic row via §5 even with
  no deterministic one, in which case the narrative covers the
  semantic side and states plainly that deterministic wasn't run for
  this domain, rather than skipping the narrative entirely).
- **Competition-wide** — `analysis/00-leaderboard.md` rubric — "across
  all N teams, what separated the top and bottom, what's the common
  failure mode this run." Always generated once the leaderboard exists,
  same "always present" rule as base_dev's Final Summary.

### Dual narrative sources — agent-written + rule-based, both shown if present

Every domain page has **two independent narrative sources**, both
rendered if they exist, either skipped if absent:

1. **Agent-written narrative** — from `standard_narratives` (§3's table,
   `participant_id` + `domain` → `sections_json`). Written by whichever
   agent runs the `analysis/{domain}.md` rubric via MCP. Rich analysis:
   strengths, weaknesses, recommendations, context-aware.

2. **Rule-based narrative** — built at render time from deterministic
   rule results in `standard_domain_scores.raw_evidence_json`. Not
   agent-written, not stored in `standard_narratives`. Covers: pass
   rate (X/Y rules, Z%), list of failed rules with descriptions, subset
   of mandatory failures. Always available after deterministic scoring
   runs — no agent call needed.

Both are `{"heading": "...", "text": "..."}` section lists, same shape
as `standard_narratives.sections_json`. The renderer passes both to
chevron as `agent_narrative` and `rule_narrative` — if either is
`None`/empty, its `{{#...}}` block simply doesn't render. No empty
sections, no fallback logic, no conditional in the template beyond
chevron's built-in falsy-section behavior.

**Why both exist**: the rule-based narrative is always available
immediately after deterministic scoring (no agent dependency), while
the agent-written narrative arrives later (after semantic scoring +
analysis pass). During partial evaluation, the rule-based narrative
fills the page. After full evaluation, both appear — the rule-based
summary gives a quick pass/fail overview, the agent narrative gives
the deeper analysis. No competition between them, complementary.

**`_build_rule_narrative(det_data)`** — new helper in `render_reports.py`:
```python
def _build_rule_narrative(det_data):
    """Build narrative blocks from deterministic rule results."""
    rules = det_data.get("deterministic_rules", [])
    passed = [r for r in rules if r["passed"]]
    failed = [r for r in rules if not r["passed"]]
    mandatory_failed = [r for r in failed if r.get("mandatory")]

    blocks = []
    # "Pass Rate" — X/Y rules passed (Z%)
    # "Failed Rules" — each: id, description, detail
    # "Mandatory Failures" — subset where mandatory=True (if any)
    return blocks
```

## 9. Markdown report templates — script + template, not agent-driven

**Scope correction from your last message**: only the semantic *audit*
(§5) and the semantic *analysis*/narrative (§8) are agent-driven via
MCP. Everything downstream of both — score calculation, z-score/bonus,
markdown rendering, HTML rendering — is scripted. This section is the
markdown side of that; §10 is the HTML side.

**All 32 markdown templates already exist** (§0) —
`templates/reports/domain/{domain}-{deterministic,semantic,summary}.md`
× 10 domains, plus `global-leaderboard.md` and `team-final-summary.md`.
This section wires a renderer to them, it doesn't design new ones —
your "each audit needs a separate template" requirement is already
satisfied by the existing 3-per-domain split (deterministic /
semantic / summary), not something to add.

**Technical requirement the existing templates impose**: they use real
Mustache syntax — `{{#each deterministic_rules}}...{{/each}}`,
`{{ this.id }}` — not base_dev's `report.py`, whose `substitute_template()`
only does flat `{{path}}` lookups with no loop construct at all (checked
— it has no `{{#each}}` handling, couldn't render these templates as
they're written). Two options: hand-roll `{{#each}}` support into a
new engine, or use an existing small Mustache renderer (`chevron` —
pure-Python, no transitive dependencies, does exactly this syntax).
**Recommend `chevron`** — Mustache's section/loop semantics (falsy
values, nested sections, `{{.}}` current-item refs) are easy to get
subtly wrong reimplementing from scratch; a small, correct, existing
implementation beats a hand-rolled partial one for something this
central to every report this proposal produces.

**One renderer, five template kinds, one data-fetch function each**
(your "script to fetch data and feed to template" requirement, one
per template kind, matching each template's distinct data shape):

| Template | Fetches from | Notable fields |
|---|---|---|
| `{domain}-deterministic.md` | `standard_domain_scores` where `kind='deterministic'` + `raw_evidence_json` | `deterministic_rules[]` (id/description/passed/weight/mandatory — direct unpack of `raw_evidence_json`), `deterministic_findings` (built by the same rule-evaluation step in §4, not agent-written) |
| `{domain}-semantic.md` | `standard_domain_scores` where `kind='semantic'`, all rows for that (participant, domain) | `model_results[]` (one row per model — id/score/reasoning), `mean_score` (§0 bug #5 — was mislabeled "Median"), `agreement_level` (banded, §5), `stdev_score` (continuous, §5) |
| `{domain}-summary.md` | Both of the above + §6's z-score adapter output | `scores.{deterministic,semantic,raw_merge,final_domain_score}`, `global_stats.{mean,stdev}`, `team_stats.{z_score,relative_bonus}` |
| `team-final-summary.md` | §6's `build_leaderboard()` output, filtered to one participant + `standard_narratives` | `executive_summary` ← **this is where §8's agent-written narrative plugs in directly**, no new slot needed, it was already there |
| `global-leaderboard.md` | §6's `build_leaderboard()` output, all participants + `standard_narratives`' competition-wide row | `teams[]` (ranked), `global_stats.{domain}.{mean,stdev}` |

Each fetch function returns a plain dict shaped exactly like the
template's variable paths (post-§6-fix, underscored domain keys
throughout) — `chevron.render(template_str, data_dict)`, no templating
logic beyond that in the renderer itself.

### HTML data-fetch extensions (§10's three additional functions)

The HTML renderer calls the *same* five data-fetch functions above for
the markdown layer, then extends each result with additional fields
§10's HTML templates need. These are separate `fetch_*_html_data()`
functions, not replacements — markdown rendering is unchanged.

| HTML Fetch | Extends | Additional fields |
|---|---|---|
| `fetch_summary_html_data()` | `fetch_summary_data()` | `agent_narrative` (from `standard_narratives`), `rule_narrative` (built from `raw_evidence_json`), `chart_base64`, `domain_badge` (`_score_badge()`) |
| `fetch_team_summary_html_data()` | `fetch_team_summary_data()` | `team_profile` (from `get_team_profile()`: team_name, leader, members, repo URLs, time_slot), `narrative_blocks` (competition-wide from `standard_narratives`), `radar_chart_base64` |
| `fetch_leaderboard_html_data()` | `fetch_leaderboard_data()` | `narrative_blocks` (competition-wide from `standard_narratives`), `rank_chart_base64` |

Domain deterministic and semantic HTML pages don't need separate
`fetch_*_html_data()` — they use the same data as their markdown
versions (rule results, model scores) plus `chart_base64` and
`domain_badge` injected by `render_html_all()`.

## 10. HTML report templates — design system locked, full template set

Same data as §9, richer presentation — not a redesign of what §9
renders, a second rendering of the same fetched data plus charts,
team profiles, and the full narrative already sitting in
`standard_narratives` (both agent-written and rule-based, per §8's
dual-source design).

**Design system session complete** (superseding the "invoke
`huashu-design` first" instruction this section used to carry — that
step is done, not still pending). Ran the skill's mandatory
three-direction gate: 🎲 roulette forced **Swiss Monochrome**, 🏆
reference direction was the **Chatbot Arena leaderboard** (real,
well-regarded, structurally analogous multi-judge scoring UI), 🧠
best-designer pick was **GitHub Primer** (status-badge language,
closest real-world analog to a CI-checks report). All three built as
full representative pages (`{domain}-summary` + `global-leaderboard`),
screenshotted, shown side by side. **Chosen: GitHub Primer, for every
page** — recorded in `html-design/direction-approved.md` along with
the screenshots and your exact words ("stick with C for both").

Locked design-system rules, binding on every template below:
- Color carries semantic meaning only — score-band status
  (Success/Attention/Danger), never decoration. Primer's actual
  values: success `#1a7f37`/`#dafbe1`, attention `#9a6700`/`#fff8c5`,
  danger `#cf222e`/`#ffebe9`.
- Every literal score/count/identifier in monospace with
  `font-variant-numeric: tabular-nums` — columns of numbers align like
  a ledger.
- Light background throughout — these become PDFs (below), dark
  backgrounds waste toner and read poorly printed.
- Status badges are the primary at-a-glance signal, applied
  *identically* across every page so the color key is learned once,
  not re-taught per page type.

### Design tokens — one shared source, not inline per page

Per your ask: color/typography/spacing get formalized into one shared
token system, referenced by every template, not a `<style>` block
re-declared 32+ times. The two approved demo pages already prove this
is stable, not still speculative — both were built independently by
different subagents and **converged on identical `:root{...}` custom
properties**, checked directly rather than assumed:

```css
--canvas: #ffffff;            --border-default: #d0d7de;
--canvas-subtle: #f6f8fa;     --border-muted: #d8dee4;
--canvas-inset: #eaeef2;      --fg-default: #1f2328;
--fg-muted: #656d76;          --fg-subtle: #6e7781;
--accent-fg: #0969da;         --accent-subtle: #ddf4ff;
--success-fg: #1a7f37;        --success-subtle: #dafbe1;   --success-emphasis: #2da44e;
--danger-fg: #cf222e;         --danger-subtle: #ffebe9;    --danger-emphasis: #cf222e;
--attention-fg: #9a6700;      --attention-subtle: #fff8c5; --attention-emphasis: #bf8700;
--neutral-subtle: #eaeef2;    --shadow-sm: 0 1px 0 rgba(31,35,40,0.04);
```

That's real signal — two independent implementations landing on the
exact same values means the direction is coherent enough to formalize,
not an accident to paper over.

**Three token categories, current state graded honestly, not all
equally ready to lock:**

| Category | State in the approved demo | What's needed |
|---|---|---|
| **Color** | Fully formalized — the `:root` block above, used consistently in both pages | Ready to extract as-is into a shared file. Nothing to redesign. |
| **Typography** | Font stacks confirmed and consistent (`-apple-system, BlinkMacSystemFont, "Segoe UI"...` for body/UI, `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas...` for every score/count/identifier) — but font **sizes** are ad hoc, not a scale: 11/12/13/13.5/14/16/24/28px all appear, chosen per-element rather than from a named set. | Needs a real type scale (e.g. `--text-xs` through `--text-2xl`) — this is exactly the "系统 not filler" step `huashu-design`'s own workflow calls for (核心哲学 §3: "先答五问，再规划系统" — vocalize the system, don't let each component invent its own numbers). Not something to invent unilaterally in this proposal. |
| **Spacing** | Not tokenized at all — raw values scattered (`padding:32px 24px 64px`, `padding:20px 24px`, `padding:12px 20px`, `padding:2px 8px`...) with no evident scale relationship. | Needs an explicit spacing scale (e.g. 4/8/12/16/24/32/48/64px named `--space-1` through `--space-8`) derived from the values already in use, not new numbers invented from nothing. Same "system, not filler" step as typography. |

**Mechanism — how "not inline" actually gets enforced**: one shared
partial, e.g. `_design-tokens.html` (a `<style>` block containing only
`:root{...}` custom properties + the type/spacing scale once
formalized), included via Mustache's partial mechanism — this is the
*only* thing in this proposal still using Mustache partials, since
charts are PNG files, not partials (below): `{{> design_tokens}}`,
referenced once by every one of the 32 page templates. Change a color
or a spacing value in one file, every page picks it up — the actual
technical meaning of "avoid inline theme," not just a style preference.

**Charts are a different case, revised** — the pipeline-verification
proposal resolved chart output as matplotlib-generated PNG files, not
inline SVG (reversing an earlier assumption in this section).
Matplotlib renders at generation time, outside the browser, so it
can't reference CSS `var()` at all — `{{> design_tokens}}`'s
mechanism only applies to the 32 page templates, not the chart layer.
Single source of truth still holds, just via a different path:
`render_charts.py` reads the *same* token file's resolved hex values
(parsed once, e.g. from the shared `:root{...}` block or a sibling
JSON export of it) and passes them as matplotlib color parameters —
one token source, two consumption mechanisms (`var()` for pages at
render time, direct hex read for charts at generation time), not two
independently-maintained color lists that could drift apart.

**This formalization is itself a `huashu-design` step, not something
this proposal invents standalone**: the skill's own core philosophy
(§3, "先答五问，再规划系统") and Phase 6 ("用户选定后 → 回到核心哲学
+工作流程的 Junior Designer pass，把那一版做扎实") describe exactly
this — after a direction is picked, formalize it into a real,
systematic design system before building out the full template set.
Color is done (grounded above); typography and spacing need that pass
run before the 32-template build starts, not decided ad hoc per
template as they're written — otherwise the "one shared token file"
mechanism has nothing coherent to hold.

**Page granularity — confirmed, not still a design call**: standalone
page per template, 1:1 with §9's 32 markdown files (an earlier draft
of this section floated "assembled sections in fewer pages" as a
recommendation — you chose the literal 1:1 mapping instead, already
recorded in §12's decisions). So the HTML template set is:

| # | Template | Count | Mirrors (§9) | Extra beyond markdown |
|---|---|---|---|---|
| 1 | `{domain}-deterministic.html` | ×10 | `{domain}-deterministic.md` | Status badge per rule row (pass=green/fail=red), not just a checkmark |
| 2 | `{domain}-semantic.html` | ×10 | `{domain}-semantic.md` | **This is the "mean template"** — its headline number is already `mean_score` (§9, §0 bug #5's fix), banded `agreement_level` shown as a status badge, per-model rows below it |
| 3 | `{domain}-summary.html` | ×10 | `{domain}-summary.md` | Embeds the field-distribution chart (component #1, below) + full multi-section narrative (markdown only gets one paragraph) |
| 4 | `team-final-summary.html` | ×1/team | `team-final-summary.md` | Full narrative from `standard_narratives`, not just `executive_summary`'s one field |
| 5 | `global-leaderboard.html` | ×1, shared | `global-leaderboard.md` | Embeds the rank-distribution chart (component #2, below) + full competition-wide narrative |

31 pages generated per team (30 domain pages + their team-summary) +
1 shared leaderboard page, matching the audience/distribution model
from the huashu-design session (§0 of `design-spec.md`): each team's
31 pages become **one PDF per team**; the leaderboard stays a single
shared artifact, not duplicated into every team's PDF.

### Detail visualization — its own generation layer, not inline-duplicated

Per your ask: the charts are **separate from the pages that embed
them**, not hand-copied SVG pasted into each page template. **Revised
from an earlier draft of this section**, which scoped only 2 charts
as Mustache HTML partials — two things changed since:
`python_hackathon-visualization-and-detail-templates-proposal.md`
(written after this section, sequencing note in that proposal's
opening) widened the catalog to 7 chart types, and
`python_hackathon-pipeline-verification-proposal.md` resolved chart
output as matplotlib-generated PNG files, not inline SVG/Mustache
partials — reversing this section's original "`{{> chart_field_distribution}}`"
mechanism, which is now moot (PNGs are files embedded via `<img>`/
base64, not template markup rendered via `chevron`).

Current state, all 7: 2 originally scoped here
(`field-distribution`, `rank-distribution`), 5 added by the
visualization-catalog proposal (`det-vs-sem contribution`,
`rule-pass-rate breakdown`, `model-score spread`,
`team domain-profile radar`, `domain-weight breakdown`) — full
descriptions and per-chart data requirements live in that proposal's
§1, not repeated here to avoid two documents drifting out of sync.

Mechanism, corrected: `render_charts.py` (proposed in the
pipeline-verification proposal §1) generates one PNG file per chart,
colored from the same design-token source as the pages (previous
subsection, "Charts are a different case, revised"). **Markdown never
embeds charts — confirmed, not a lingering assumption**: markdown
templates (§9) stay content-only (scores, tables, narrative text),
exactly as originally scoped; visualization is HTML-only, one more
thing HTML adds on top of the same data (alongside the fuller
narrative §9 already called out). HTML pages embed the PNG via
base64 (self-contained, matches `_img_to_base64()`). HTML → PDF (§10's
per-team export) is where a judge/team actually sees the charts —
markdown stays the plain-text/diffable artifact it always was.

Why this separation matters beyond "your ask": §6's data-fetch
functions already compute the raw numbers these charts need
(`global_stats.mean/stdev`, `team_stats.z_score`); `render_charts.py`'s
7 functions receive that same data and only own the *rendering* of it
as a PNG. If the visualization mechanism changes again later, only
those 7 functions change — not the 32 page templates that embed their
output, since a page template only ever sees "here's a base64 image
string," never how it was produced.

### PDF assembly per team

Confirmed requirement (huashu-design session, audience question): each
team receives one PDF, not 31 separate HTML files to click through.
`huashu-design`'s own toolkit already has the exact mechanism for
"many standalone HTML pages → one merged PDF" (`scripts/export_deck_pdf.mjs`
— per-page `playwright` `page.pdf()` + `pdf-lib` merge, vector text
preserved, searchable). Applying it here: one PDF per team, built from
that team's 31 rendered pages in a fixed order (10 domains ×
{deterministic, semantic, summary}, then `team-final-summary` last).
The shared `global-leaderboard.html` is not part of any team's PDF —
distributed as its own artifact (HTML and/or its own single-page PDF),
per the "all can see leaderboard, one shared report" audience model.

**`dataviz`** skill for the chart palette specifically, applied within
Primer's locked color meaning (score-band status) rather than a free
palette choice — the two aren't in tension: `dataviz` governs mark
specs/legibility, Primer governs what the colors *mean*.

**Data-fetch reuse, revised from the earlier draft of this section**:
the HTML renderer extends §9's *same* five data-fetch functions with
three additional `fetch_*_html_data()` wrappers (§9's "HTML data-fetch
extensions" table) — one data layer, feeding four consumers: the
markdown renderer (§9), the HTML renderer (this section),
`render_charts.py`'s 7 chart functions, and `_build_rule_narrative()`
(§8's rule-based narrative builder). No separate "HTML data fetcher"
or "chart data fetcher" gets written; markdown itself only ever
consumes text/table fields from that data, never a chart.

### `render_html_all()` — the HTML rendering pipeline

New function in `render_reports.py`, called after chart generation in
`run_reporting.py`:

```python
def render_html_all(conn, standard, output_dir, results, domain_stats,
                    adjusted_scores, weights_cfg, charts_dir):
```

Steps:
1. Create `html/` subdirectory inside `output_dir`.
2. Load shared `_styles.html` partial (inlined in every page, not a
   `<link>` — each file must be standalone for PDF merge).
3. **Global leaderboard** (once): `fetch_leaderboard_html_data()` →
   chevron render → write `html/global-leaderboard.html`.
4. **Per-participant loop**: for each participant, for each domain:
   - Deterministic: same data as markdown, add `chart_base64` +
     `domain_badge` → write `html/domain/{name}/deterministic.html`.
   - Semantic: same data as markdown → write `html/domain/{name}/semantic.html`.
   - Summary: `fetch_summary_html_data()` (extends summary data with
     `agent_narrative`, `rule_narrative`, `chart_base64`, `domain_badge`)
     → write `html/domain/{name}/summary.html`.
5. **Team final summary**: `fetch_team_summary_html_data()` (extends
   team summary data with `team_profile`, `narrative_blocks`,
   `radar_chart_base64`) → write `html/{participant}-summary.html`.

### Team profile in `team-final-summary.html`

The team-final-summary page shows team identity, not just scores.
Data from §2's extended `standard_participants` via
`get_team_profile(conn, participant_id)`:

```
Header:
  eyebrow: "Team Final Report"
  h1: team_profile.team_name (or participant_name if team_name is null)
  meta-row:
    - Team Leader: team_profile.team_leader
    - Members: team_profile.members (formatted list)
    - Repository: team_profile.repo_https (linked)
    - Time Slot: team_profile.time_slot

Scorecards:
  - Final Score: final_score / 20 (with badge)
  - Rank: team_rank of total_teams

Radar chart:
  <img src="data:image/png;base64,{radar_chart_base64}">

Domain table:
  10 rows: domain | score | badge (success/attention/danger)

Model aggregate:
  {{#model_aggregate_scores}} model | mean {{/...}}

Narrative:
  {{#narrative_blocks}} (competition-wide, from standard_narratives NULL/NULL)
  heading + text rendered as <h3> + <p>
```

### Dual narrative rendering in domain summary pages

`{domain}-summary.html` renders both narrative sources independently:

```mustache
{{#agent_narrative}}
<section class="narrative">
  <div class="section-header"><h2>Agent Analysis</h2></div>
  <div class="section-body">
    {{#sections}}
    <div class="block">
      <h3>{{ heading }}</h3>
      <p>{{ text }}</p>
    </div>
    {{/sections}}
  </div>
</section>
{{/agent_narrative}}

{{#rule_narrative}}
<section class="narrative rule-based">
  <div class="section-header"><h2>Rule Execution Summary</h2></div>
  <div class="section-body">
    {{#sections}}
    <div class="block">
      <h3>{{ heading }}</h3>
      <p>{{ text }}</p>
    </div>
    {{/sections}}
  </div>
</section>
{{/rule_narrative}}
```

If `agent_narrative` is `None` (no agent has written this domain's
narrative yet), its `{{#agent_narrative}}` block is skipped entirely.
Same for `rule_narrative` (should never be empty after deterministic
scoring, but guarded regardless). No empty sections render.

### Chart base64 embedding

`render_charts.py` generates PNGs to `charts_dir/`. A new helper:

```python
def chart_to_base64(chart_path):
    """Read a PNG file and return its base64-encoded string."""
    import base64
    with open(chart_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")
```

HTML templates embed charts as self-contained data URIs:

```html
<img src="data:image/png;base64,{{ chart_base64 }}" alt="Chart">
```

No external file references — each HTML file is standalone, works
when opened directly, works when merged into PDF. Chart file paths
are never exposed in the rendered output.

### `_score_badge()` helper

```python
def _score_badge(score):
    """Map a 0-100 score to a Primer status badge."""
    if score >= 75:
        return {"label": "Strong", "css_class": "success"}
    if score >= 50:
        return {"label": "Attention", "css_class": "attention"}
    return {"label": "Needs Work", "css_class": "danger"}
```

Used by `fetch_summary_html_data()` (per-domain badge) and
`fetch_team_summary_html_data()` (final-score badge). The badge
appears in scorecard sections and domain tables — same status-color
language across every page, per §10's locked Primer rules.

## 11. Out of scope

- Building actual multi-provider *API* client code (as opposed to the
  agent-driven sessions §5 actually uses) — not needed per §5's
  resolution, noted here only because an earlier draft assumed it
  would be.
- Rewriting `statistics.py`/`leaderboard.py` — reused as-is (§6),
  aside from the `_load_weights()` normalization fix (§0 bug #1) and
  reading the det/sem split from yaml instead of hardcoding it
  (§0 bug #4).
- Redesigning the 32 existing markdown templates' content/structure —
  §9 renders them as authored, only fixes the one mislabeled field
  (§0 bug #5).
- A fix-loop/gate mechanism — this standard is audit-only, per your
  statement; nothing here adds one.

## 12. Open questions for confirmation

1. ~~§10's page-vs-section granularity call~~ — **resolved**: 1:1
   standalone pages per template, matching §9's markdown set.
2. `analysis/00-leaderboard.md`'s narrative — heuristic or agent
   judgment? Given it's comparing N teams' actual results, recommend
   agent-driven (matches §8's other rubric, and there's real
   comparative judgment to make, not just arithmetic) — flagging since
   base_dev's equivalent question defaulted to heuristic-first, and
   this one has a real argument for the opposite default.
3. ~~Should `run_hackathon.py` support targeted re-run~~ — **resolved**:
   `--participant` filter exists (line 204 of `run_hackathon.py`);
   `UNIQUE` constraint makes re-run an upsert — same behavior as
   full re-run, just scoped. No additional work needed.
4. §4a's `doc-003` ("no broken links in README") needs real network
   access to validate external URLs — every other script in this
   standard is deliberately offline-only
   (`audit_model_artifact.py`'s own docstring: "ALL tests run
   OFFLINE"). Recommend checking relative/local links only (no network
   call, consistent with the rest of the standard) and treating
   external links as unverifiable rather than failing them — but this
   changes what `doc-003` actually certifies, worth confirming rather
   than silently narrowing the rule's scope.
~~§5 — single model now vs. 3-provider API integration~~ — resolved,
no longer open (§5).
~~§0's DOMAIN_KEY_MAP/stdout/missing-scripts/60-40 bugs~~ — resolved,
no longer open (§0/§4/§6).
~~Markdown/HTML template design~~ — resolved, templates already exist
(§9/§10), not a from-scratch design question.
~~§0's final-score scale (150 vs. 20)~~ — **resolved, confirmed by
you**: 20. `weights.yaml`'s `final_scale: 150` gets fixed to `20`
(§6's formula already reflects this).
~~§6's Phase 4 (team-level semantic-agreement bonus)~~ — **resolved,
confirmed by you**: dropped. `leaderboard.py`'s Phase 4 block
(`_semantic_agreement_bonus()`, `sem_bonus_total`, lines 117-128) is
removed; `final_normalized`'s formula becomes exactly §6's 3-line
version (`max_possible = total_weight`, no `+ max_sem_bonus`).

## 13. Verification checklist

- [ ] §0 bug #1 — `leaderboard.py`'s `_load_weights()` normalizes
      `weights.yaml`'s domain keys to underscores at load time;
      `DOMAIN_KEY_MAP` is unchanged from today; all 10 domains'
      weights are non-zero in a real leaderboard run.
- [ ] §0 bug #2 — `audit_testing.py`/`audit_model_artifact.py`'s info
      `print()`s go to stderr; their stdout is JSON-only.
- [ ] §0 bug #3 — the orchestrator checks for `audit_{domain}.py`'s
      existence before attempting a deterministic pass for
      `documentation`/`data-quality`/`ai-explanations`; no stub
      scripts were written.
- [ ] §0 bug #4 — the det/sem split is read from
      `calculation/aggregation/domain/{domain}.yaml` at runtime, not
      hardcoded as a Python constant anywhere.
- [ ] §0 bug #5 — `{domain}-semantic.md`'s label reads "Mean Score,"
      not "Median Score"; no code anywhere computes an actual median.
- [ ] §2 — `standard_participants` exists; `standard`/`participant_name`
      are columns holding data, no table named after a specific team.
- [ ] §3 — `standard_domain_scores` exists with the `UNIQUE(participant_id,
      domain, kind, model)` constraint; a missing domain is an absent
      row, not a zero-value row. `standard_narratives` exists, upsert
      handled in application code (not a DB constraint, per the NULL
      caveat documented in §3).
- [ ] §4 — `run_hackathon.py` processes one participant's full
      deterministic-then-semantic cycle before starting the next.
      A rule-evaluation step exists turning `audit_*.py` raw output
      into weighted scores per `audit/deterministic/document/*.yaml`.
- [ ] §4a — all 10 domains have a script (`audit_documentation.py`,
      `audit_data_quality.py`, `audit_ai_explanations.py` newly exist,
      closing §0 bug #3). `audit_python.py` actually runs radon and
      mypy (not just config-presence checks); `audit_mlops.py`
      actually inspects `dvc.yaml` stage count and `mlruns/` run count
      (not just directory presence). The orchestrator (§4) discovers
      `main.py`/`app.py`/`run.py` and passes it as
      `audit_model_artifact.py --entrypoint`, closing `run-001`'s gap.
      `audit_git.py`/`audit_testing.py`/`audit_model_artifact.py`'s
      existing checks/`audit_security.py` are untouched (already
      sufficient depth, confirmed, not re-built).
- [ ] §5 — no API-client code for external LLM providers exists
      anywhere in this standard; semantic scoring happens exclusively
      through agent-driven sessions writing to `standard_domain_scores`;
      the coverage-tracking query returns correct missing (participant,
      domain, model) combos against a real partial run.
- [ ] §6 — the confirmed flow (raw domain score → per-domain z-score
      bonus → weighted aggregate → ÷100×20 scale) matches exactly;
      `weights.yaml`'s `final_scale` is `20`; Phase 4's team-level
      semantic-agreement bonus is either fully removed from
      `leaderboard.py` or explicitly confirmed kept — not left
      ambiguous either way. `statistics.py`'s z-score/bonus math
      itself is otherwise unchanged.
- [ ] §7 — a participant with a domain missing shows "Not
      implemented" in HTML, scores 0 in the leaderboard weighting, and
      has no narrative generated for that domain.
- [ ] §8 — `analysis/{domain}.md` × 10 + `00-leaderboard.md` exist,
      mirroring base_dev's rubric structure; no scripted
      "narrative generator" script exists anywhere.
- [ ] §9 — all 32 existing markdown templates render correctly via
      `chevron` (not a hand-rolled `{{#each}}` implementation); each
      of the 5 template kinds has its own data-fetch function; no
      existing template file's content/structure was altered beyond
      the §0 bug #5 label fix.
- [ ] §10 — all 32 HTML templates exist (10 domains × 3 kinds +
      team-final-summary + global-leaderboard), 1:1 with §9's markdown
      set; every one uses Primer's status-color language identically
      (no page reinvents its own color meaning); all 7 charts (2
      originally scoped here + 5 from the visualization-catalog
      proposal) are generated as PNG files by `render_charts.py`, not
      hand-copied inline SVG duplicated across pages — checked against
      the pipeline-verification proposal, not this section alone;
      every field §9's table lists is represented (nothing markdown
      shows is silently dropped); missing domains show a "Not
      implemented" section, not a broken chart; per-team PDF export
      produces one PDF per team from that team's 31 pages in the fixed
      domain order, with the shared leaderboard excluded from every
      team's PDF.
- [ ] §10 design tokens — `_design-tokens.html` (or equivalent shared
      partial) exists with the color `:root` block verified above, a
      named typography scale, and a named spacing scale; every one of
      the 32 page templates includes it via `{{> design_tokens}}`
      rather than declaring its own `<style>` block; zero raw hex
      color values or ad hoc pixel sizes appear outside that one
      shared file within the 32 templates. `render_charts.py` (PNG
      generation, not a Mustache partial) reads its colors from the
      same token source at generation time rather than duplicating a
      second hardcoded palette — checked separately, since matplotlib
      can't use `var()` at all (previous subsection covers this); the
      type/spacing scale was produced via a `huashu-design` pass, not
      invented ad hoc while writing template #1 and copied forward.
- [ ] §2 extended schema — `standard_participants` has `team_name`,
      `team_leader`, `members_json`, `repo_https`, `repo_ssh`,
      `presentation_order`, `time_slot` columns; `metadata_json` is
      still populated for extensibility; `get_team_profile()` helper
      returns a dict with all team fields.
- [ ] §4b teams.json — `python_hackathon/teams.json` exists with at
      least one sample team entry; `run_hackathon.py` auto-loads it
      when present; `--register` CLI flag still works independently.
- [ ] §8 dual narrative — `_build_rule_narrative()` produces sections
      from deterministic rule results; `agent_narrative` and
      `rule_narrative` render independently in HTML templates; absent
      source skips its block (no empty sections).
- [ ] §9 HTML data-fetch extensions — `fetch_summary_html_data()`,
      `fetch_team_summary_html_data()`, `fetch_leaderboard_html_data()`
      exist; each extends its markdown counterpart with narrative
      blocks, chart base64, team profile, and/or badge.
- [ ] §10 `render_html_all()` — 32 HTML files generated; team
      profiles render in `team-final-summary.html` (team name, leader,
      members, repo URLs); dual narratives render in domain summary
      pages; charts embedded as base64 data URIs; `_score_badge()`
      produces consistent Primer status badges across all pages.
- [ ] §10 `chart_to_base64()` — helper exists in `render_charts.py`;
      all chart PNGs are embeddable as self-contained data URIs; no
      external file references in rendered HTML.
