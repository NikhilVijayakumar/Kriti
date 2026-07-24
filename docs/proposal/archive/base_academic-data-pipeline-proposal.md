# base_academic — Data Model, Templates & Pipeline Correction Proposal

## 0. Why This Document Exists

Supersedes the usecase shape in `base_academic-usecase-proposal.md` on several
points below — that document got the usecase *taxonomy* right but stopped
short of the data layer, template layer, and document-assembly pipeline this
one specifies. §8 originally folded in a registration-breaking bug found by
direct verification of the shipped implementation; that bug was
independently fixed in the codebase before this revision, so §8 now covers
the narrower orphan-cleanup gap that remains in the fix that landed.

Confirmed gaps in what's on disk today (`academic/base_academic/`):

- **No `schema/*.sql` files.** `script/common/academic_schema.py` defines
  all 14 tables as inline `CREATE TABLE` strings in Python. Compare
  `python_hackathon/schema/*.sql` — one file per table, each with a comment
  explaining *why* it's shaped that way, cataloged into `custom_data_tables`
  via `standard.yaml`'s `custom_tables:` block. base_academic has the
  `custom_tables:` catalog entries but not the source-of-truth `.sql` files
  they're supposed to describe.
- **Score history is destroyed on re-audit.** `academic_schema.py:496-503`
  — `upsert_semantic_score` does `UPDATE ... WHERE id=?` and
  `DELETE FROM academic_semantic_dimension_scores/findings` on every re-run.
  There is no way to see "how did this domain's score change over the last 5
  audit passes" — the old row is gone.
- **No visualization tables.** `python_hackathon` has
  `hackathon_visualization_types`/`hackathon_visualizations` for matplotlib
  chart tracking (idempotent — a report step checks before re-rendering).
  base_academic has nothing equivalent.
- **No `domains/*.md` golden-standard files.** `python_hackathon/domains/`
  has 10 files, one per domain, defining the audit standard in prose before
  any script/prompt reads it. base_academic has zero — `calculation/semantic/
  document.yaml` references rubric content that was never written down as a
  human-readable standard.
- **No `plan/usecase/*.md` files.** `python_hackathon/plan/usecase/` has 7
  files in a fixed shape (Script / Inputs / Action / Completion criteria /
  Verify script / Rule). base_academic has none — the previous proposal
  described usecases in prose inside a design doc, not as this per-usecase,
  independently-verifiable artifact.
- **Templates are single-shot, not master+section.** `templates/generation/
  document/generate-section.md` is one generic prompt for any domain. No
  document-level schema template exists to say what order sections go in,
  and no HTML template/docx path exists at all.
- **Plagiarism/humanize is 2 steps where the working manual precedent uses
  3.** `Bodha/docs/paper/Bodha/drafts/ai-evaluation-prompt.md` (Pass 1
  forensic audit + Pass 2 targeted rewrite of only flagged sentences) and
  `ai-humanifier.md` (Pass 3 — full-section rewrite using Pass 1/2 as
  context) are two different files doing two different things. The current
  `plagiarism-fingerprint-check` → `humanize` usecase pair collapses this
  into one audit + one full rewrite, skipping the cheaper targeted-rewrite
  pass that only touches flagged sentences.
- **`register_standard` parsing is fixed; step-expansion has a narrower
  remaining gap.** The `steps: null` bug from earlier this session is
  resolved — the 6 previously-empty usecases now have `steps: []`, and
  `run_full_workflow.py` has grown an `expand_triads()` function that
  inserts domain/module-expanded steps into `step`/`step_script`/
  `step_prompt` directly after `register_standard` + `classify-repo` run
  (`_insert_step()` dedupes by `(usecase_id, step_order)`, so re-running
  with the *same* domain/module set is safe). What's still unaddressed:
  `_insert_step` never deletes — if a repo's domain or module list *shrinks*
  between runs (a module gets removed, a concrete system's domain list
  changes), the old higher-`step_order` rows from the larger set are never
  cleaned up and stay orphaned in `step`/`step_script`/`step_prompt`. See
  §8 for the fix, revised to match this actual runtime-expansion design
  rather than the static pre-generation approach an earlier draft of this
  proposal assumed was needed.

## 1. Schema-as-Files Convention

Every `academic_*` table gets its own file under `base_academic/schema/`,
mirroring `python_hackathon/schema/` exactly — numbered, one `CREATE TABLE`
per file, a comment block explaining the shape's reasoning (not just what
columns exist). `script/common/academic_schema.py`'s `ensure_schema()` reads
and executes these files instead of embedding the DDL as Python string
literals — same separation `hackathon_schema.py` doesn't quite have either,
but that's this proposal's convention for base_academic, not a fix owed to
python_hackathon.

```
base_academic/schema/
├── 01-academic_papers.sql
├── 02-academic_repos.sql
├── 03-academic_domains.sql
├── 04-academic_modules.sql
├── 05-academic_module_analysis.sql
├── 06-academic_cross_module_analysis.sql
├── 07-academic_narratives.sql
├── 08-academic_narrative_sections.sql
├── 09-academic_semantic_runs.sql
├── 10-academic_semantic_dimension_scores.sql
├── 11-academic_semantic_findings.sql
├── 12-academic_plagiarism_findings.sql
├── 13-academic_humanize_passes.sql
├── 14-academic_templates.sql
├── 15-academic_score_history.sql        # NEW — §5
├── 16-academic_visualization_types.sql  # NEW — §7
├── 17-academic_visualizations.sql       # NEW — §7
├── 18-academic_report_history.sql       # NEW — §6
└── 19-views.sql                          # NEW — mirrors hackathon's 12-views.sql
```

Each existing table (1-14) gets its `.sql` file extracted verbatim from
`academic_schema.py`'s current inline strings — no shape changes for those,
just moving the source of truth to disk where `custom_data_tables` already
claims it lives.

## 2. Data-Management Scripts (What Exists, What's Missing)

`script/common/academic_schema.py` already has the right shape for a CRUD
layer — `register_paper`, `upsert_module`, `upsert_narrative`,
`upsert_semantic_score`, `upsert_plagiarism_finding`,
`upsert_humanize_pass`, `seed_templates` — this is the same pattern
`hackathon_schema.py` uses (`get_conn`/`ensure_schema`/`seed_*`/`upsert_*`/
`get_*`). It does not need a rewrite. It needs:

1. `ensure_schema()` to execute `schema/*.sql` files instead of inline DDL
   (§1).
2. `upsert_semantic_score` to **stop destroying history** — see §5.
3. New functions for the 4 new tables: `record_score_snapshot`,
   `record_visualization`/`get_visualization` (same signature shape as
   `hackathon_schema.py`'s), `record_report`/`get_latest_report`/
   `list_report_history`.

This is the "script to manage this data" the request asks for — it already
exists, it's just incomplete and partially wrong, not absent.

Separately: samgraha's own `01-usecase.sql` through `07-execution.sql`
(`E:\Python\samgraha\schema\knowledge\`) are **not** written to by
base_academic scripts directly — they're samgraha-owned, populated by
`register_standard` reading `standard.yaml`, and by `run_script_step`/
`prepare_semantic_step`/`complete_semantic_step` writing `execution` rows.
No standard's own scripts insert into `usecase`/`script`/`prompt`/`step`/
`step_script`/`step_prompt` directly — that would bypass the one boundary
samgraha actually enforces (see `schema/knowledge/README.md`,
`crates/registry`'s migrations own those tables exclusively). What
base_academic's scripts own is `custom_data_tables` cataloging (already
correct, via `standard.yaml`'s `custom_tables:` block) plus its own 18
`academic_*` tables.

## 3. Documentation Precondition — Simplified Entry Gate

Correction to the previous proposal's 3-way entry classification: the
system now requires documentation to exist before anything else runs —
either pre-existing analysis docs, or freshly generated ones, or (for a
docs-only repo with no implementation at all) the author's own notes. A
repo with **neither** documentation **nor** an implementation to analyze is
out of scope — there is nothing to generate from, matching the original
"new repo, we can't do anything" framing.

`classify-repo` (script) now resolves to one of 4 states, not 3:

| State | Docs? | Impl? | Action |
|---|---|---|---|
| `NO_DOCS_NO_IMPL` | no | no | **Refuse.** Report and stop — nothing to draft from. |
| `DOCS_ONLY` | yes | no | `draft-from-docs-only` — unvalidated, per original design |
| `IMPL_NO_ANALYSIS` | no | yes | `generate-analysis-docs` (mandatory) → falls through to `IMPL_WITH_ANALYSIS` |
| `IMPL_WITH_ANALYSIS` | yes | yes | `generate-paper-draft` directly |

`generate-analysis-docs` is not optional once an implementation exists — it
is the only path that produces documentation for an `IMPL_NO_ANALYSIS` repo.
There is no shortcut that generates a paper from an implementation without
first producing analysis docs — that was implicit before; this makes it the
literal gate a script enforces (`classify-repo` refuses to hand
`IMPL_NO_ANALYSIS` straight to `generate-paper-draft`).

**Migration cost, not just a design change.** `classify_repo.py:58-63`
currently implements exactly the 3 old states, and
`academic_schema.py:46`'s `CHECK (classification IN ('NEW_NO_IMPL',
'EXISTING_NO_ANALYSIS', 'EXISTING_WITH_ANALYSIS'))` enforces them at the DB
level — this is not just a docstring change. Concretely:

1. `academic_schema.py:46` — `CHECK` constraint gains `DOCS_ONLY` and
   `IMPL_NO_ANALYSIS`/`IMPL_WITH_ANALYSIS` replace
   `EXISTING_NO_ANALYSIS`/`EXISTING_WITH_ANALYSIS` (rename, not just
   addition — keep the CHECK exhaustive, don't leave the old 3 values
   valid alongside the new 4).
2. `classify_repo.py:58-63` — currently returns `NEW_NO_IMPL` for *any*
   no-implementation repo without checking for docs at all. Needs a
   `has_docs` check added to that branch to split it into `NO_DOCS_NO_IMPL`
   vs `DOCS_ONLY`.
3. `run_full_workflow.py` — every `if classification == "NEW_NO_IMPL"` (or
   equivalent) branch needs updating to the new 4-value set, including the
   entry-usecase dispatch logic that currently picks
   `draft-from-docs-only` vs `generate-paper-draft` off the classification
   string.
4. Any already-written `academic_repos` rows under the old 3-value scheme
   need a backfill (`NEW_NO_IMPL` rows need inspecting for `has_docs` to
   split correctly — this can't be a blind rename since the split adds
   information the old value didn't carry).

## 4. `plan/usecase/*.md` — Structured Usecase Documents

New directory, one file per usecase, in `python_hackathon`'s exact shape
(Script / Inputs / Action / Completion criteria / Verify script / Rule) —
this is what actually makes a usecase independently checkable instead of
just described in a design doc nobody re-reads once implementation starts.

```
base_academic/plan/usecase/
├── 0-classify-repo.md
├── 1-generate-analysis-docs.md
├── 2a-draft-from-docs-only.md
├── 2b-generate-paper-draft.md
├── 3-deepen-sections.md
├── 4-semantic-audit.md
├── 5a-plagiarism-forensic-audit.md      # Pass 1+2 — was one usecase, now split (§9)
├── 5b-humanize.md                        # Pass 3
├── 6-calculate.md
└── 7-render.md                           # markdown -> html -> pdf/docx (§6)
```

Example shape (`4-semantic-audit.md`):

```markdown
# Use-case 4 — Semantic Audit

**Script**: Agent-driven, pre/post scripts gather-domain-evidence / persist-domain-semantic-score

**Inputs**:
- `domains/{domain}.md` golden-standard rules (§5)
- `calculation/semantic/document.yaml` rubric
- Current draft for {domain}

**Action**: Score {domain} against its golden-standard rules + rubric. One
`academic_semantic_runs` row per (paper, domain, model) — never overwritten,
see academic_score_history for the trend view (§5).

**Completion criteria**:
- Minimum bar: >= 1 semantic run per domain per paper
- Full bar (informational): every configured model has scored every domain

**Verify script**: `verify_usecase_4_semantic_audit.py --standard base_academic --paper-id <id>`

**Rule**: Starts after deterministic audit for that domain. Accumulates —
no "complete" end-state, same as python_hackathon's 2b.
```

Every usecase file gets its own `verify_usecase_N_*.py`, same convention as
`python_hackathon/script/verify/` — a completion check independent of
whether the orchestrator claims success. This is the concrete answer to
last session's finding: a workflow report saying "ran: 9, failed: 0" is not
evidence anything actually happened; a verify script that queries the DB
directly is.

## 5. Score History (Fixes the Destroyed-History Bug)

`upsert_semantic_score`'s current `UPDATE`+`DELETE` behavior is the actual
bug behind "we also save historic report score also not just latest one."
Two changes:

1. **`academic_semantic_runs` stops being upserted by (paper, domain,
   model).** Add `run_number INTEGER NOT NULL DEFAULT 1` to the `UNIQUE`
   constraint: `UNIQUE(paper_id, domain_id, model, run_number)`. Each audit
   pass inserts a new row with `run_number` incremented, same pattern
   `academic_narratives.iteration` and `academic_humanize_passes.iteration`
   already use elsewhere in this same table set — this table was the
   inconsistent one, not the model to replicate.
2. **New table `academic_score_history`** — one row per `calculate.py` run,
   independent of any single domain, tracking the whole-paper trend:

```sql
CREATE TABLE IF NOT EXISTS academic_score_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,  -- NULL = whole-paper final_score
    final_score   REAL    NOT NULL,
    score_band    TEXT    NOT NULL,
    trend_delta   REAL,    -- vs previous snapshot for this (paper, domain)
    calculated_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_score_history_lookup
    ON academic_score_history(paper_id, domain_id, calculated_at);
```

`calculate.py` writes one row here every run (never updates), same
"backtrace, never regenerate silently" principle as
`hackathon_visualizations`. This is what the improvement-over-time
visualization (§7) actually queries — not a live re-scoring, a real stored
trend line.

**`upsert_semantic_score` function change, concretely** (currently
`academic_schema.py:484-514`):

```python
def upsert_semantic_score(conn, paper_id, domain, model, score, result=None):
    domain_id = get_domain_id(conn, domain)
    ...
    max_run = conn.execute(
        "SELECT COALESCE(MAX(run_number), 0) FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=? AND model=?",
        (paper_id, domain_id, model or ""),
    ).fetchone()[0]
    cur = conn.execute(
        "INSERT INTO academic_semantic_runs "
        "(standard, paper_id, domain_id, model, run_number, overall_score, reasoning, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (_STANDARD, paper_id, domain_id, model or "", max_run + 1, score, reasoning, ts),
    )
    run_id = cur.lastrowid
    # no DELETE — run_id is new and unique, dimension_scores/findings just
    # get freshly inserted rows against it, nothing to clear
```

The existing `DELETE FROM academic_semantic_dimension_scores/findings WHERE
run_id=?` calls (lines 502-503) are removed entirely, not just moved —
every `run_id` is now unique per insert, so there is never a pre-existing
row at that `run_id` to clear. Callers that want "the latest score" (report
rendering, `academic_score_history`) query
`MAX(run_number)`/`ORDER BY run_number DESC LIMIT 1`, not assume there's
only one row.

## 6. Templates: Master Schema + Per-Section + HTML + DOCX

### 6.1 Generic section list — base_academic's own, not eswa's

`Bodha/docs/paper/Bodha/drafts/` splits into 8 files (`0. Abstract.md`
through `8. Reference.md`) — that's eswa-specific and stays eswa-specific.
Per the explicit instruction this session, base_academic defines its own
generic section list instead of adopting that split verbatim. Derived from
`Bodha/docs/paper/Bodha/drafts/world-class journal paper.md` (the one
reference document in this material that is genuinely venue-agnostic —
9 sections, no ESWA-specific formatting rules mixed in) plus the 3
cross-cutting domains this session adds:

**Structural domains** (map to actual paper sections, in order):
`title-and-metadata`, `abstract`, `introduction`, `related-work`,
`problem-definition`, `methodology`, `experimental-setup`, `results`,
`discussion`, `limitations`, `conclusion`, `references`

**Cross-cutting domains** (audited across the whole document, not confined
to one section — same 3 kinds already built for module/cross-module
analysis in the prior proposal, now promoted to real audited paper
domains): `novelty`, `gaps`, `mathematics`

This is base_academic's **default baseline**, not a replacement for the
earlier, carefully-verified finding that `pcems_2026` (6 domains) and
`eswa_journal` (11 domains) have genuinely divergent domain lists and
content depth (`base_academic-proposal.md` §2, archived). A concrete system
can still narrow, rename, or deepen any of these — this just means neither
system has to author its domain list from zero anymore; it starts from this
generic 15 and overrides what genuinely differs, the same override rule
`system.yaml` already documents for everything else.

### 6.2 Master schema template + per-section templates

Two template layers, matching the explicit "file/scaffolding = script,
structure = template" split:

```
base_academic/templates/generation/document/
├── _master-schema.md          # NEW — defines section order + doc-level frontmatter, per {paper, journal}
├── {domain}.md                 # existing pattern, one per structural domain — heading/subheading skeleton only
└── html/
    └── _master-schema.html     # NEW — HTML mirror of the master schema, for §6.3
```

`_master-schema.md` is not a prompt — it is a manifest a **script** reads
(scaffolding is the script's job, per this session's explicit split), e.g.:

```yaml
# templates/generation/document/_master-schema.yaml
sections: [title-and-metadata, abstract, introduction, related-work,
           problem-definition, methodology, experimental-setup, results,
           discussion, limitations, conclusion, references]
```

Single list, not a `paper:`/`journal:` split. An earlier draft of this
proposal had both keyed separately with identical values and a comment
saying they "might" need to diverge — that's a hypothetical, not a
requirement either concrete system has today. A concrete system that
genuinely needs a different paper-vs-journal section set overrides this
whole file (same override rule as everything else in `system.yaml`); no
system needs that today, so the base file doesn't carry the unused
structure. Add the split back when a third system actually needs it, not
before.

`persist-section-draft`'s post-script reads this manifest to know which
file to write into `docs/paper/{system}/drafts/document/{domain}.md` and in
what order to concatenate them for `assemble-final-document` (§6.4) — the
manifest is the single source of truth for section order, not a hardcoded
list duplicated in every script.

### 6.3 HTML template + DOCX generation

New template + new script, neither exists today:

- `templates/generation/document/html/_master-schema.html` — Jinja/mustache
  HTML shell (base_academic already has a working templating precedent to
  reuse: `python_hackathon`'s `render_reports.py` uses `chevron`, the same
  library should drive this rather than introducing a second templating
  dependency).
- New script `render-docx.py` (deterministic) — **shells out to `pandoc`**
  (`pandoc report.html -o report.docx`) rather than writing a custom
  HTML→DOCX converter. Pandoc is an already-solved problem here; reuse it.

### 6.4 Mermaid → image extraction

New script `extract-mermaid-images.py` (deterministic), runs before HTML
rendering:

1. Scan a section's markdown for ` ```mermaid ` fenced blocks.
2. For each block, check `academic_visualizations` (§7) for an existing
   rendered image with a matching content hash — reuse it if present ("if
   image are present already we will use same," per this session).
3. Otherwise render via `mmdc` (mermaid-cli, the standard tool — same
   reuse-over-reimplementation reasoning as pandoc above) to PNG/SVG, record
   the new file in `academic_visualizations` with `chart_type='mermaid-diagram'`.
   `mmdc` needs a headless Chrome/Chromium install underneath it — this is
   not a small dependency the way `pandoc` is; it's a full browser binary.
   Check for it explicitly (`shutil.which("mmdc")` plus a one-time smoke
   render, not just the binary's presence) and **hard-fail the step** if
   missing, don't skip it — a section with an unrendered mermaid block
   would otherwise ship raw ` ```mermaid ` fence text into the HTML/PDF/DOCX
   output looking like a rendering bug, not a missing-dependency message.
4. Replace the fenced block with a standard `![...](path)` image reference
   in the HTML-bound copy of the markdown (the `.md` source keeps the
   mermaid block — GitHub/most viewers render it natively; only the
   HTML/PDF/DOCX pipeline needs a rasterized image).

### 6.5 Assembly script

`assemble-final-document.py` (deterministic) — reads `_master-schema.yaml`
for section order, concatenates each domain's latest draft from
`academic_narratives` (stage=`humanize` if it exists, else `deepen`, else
`generate` — always the most-processed version), runs
`extract-mermaid-images.py`, renders through `_master-schema.html`, then
`render-docx.py` for the DOCX variant and the existing `playwright`-based
approach (`python_hackathon/script/usecase-7-pdf/export_team_pdfs.py`
already proves this works, same library, no new dependency) for PDF.
Writes to `docs/paper/{system}/final/{system}-{paper|journal}.{md,html,pdf,docx}`
and records the run in `academic_report_history` (§6.6) — this is
`usecase 7 — render` from the previous proposal, now concrete instead of
"still unbuilt."

### 6.6 Report archive/latest (mirrors `prana`'s convention)

`E:\Python\prana\docs\raw\report\{report-type}\{archive,latest}\
{report-type}-audit-{YYYY-MM-DD}-{NNNN}.md` is the filesystem-level
precedent — timestamped filename, `latest/` holds the current one,
`archive/` holds every prior one. base_academic's version is DB-first
(per this session — "all data is in db so that report can be easily
regenerated at any time") with the filesystem output being a rendered
projection, not the source of truth:

```sql
CREATE TABLE IF NOT EXISTS academic_report_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html','pdf','docx')),
    final_score   REAL,
    score_band    TEXT,
    file_path     TEXT    NOT NULL,
    is_latest     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_report_history_lookup
    ON academic_report_history(paper_id, format, is_latest);
```

Every new run sets the prior `is_latest=1` row (same paper+format) to `0`
before inserting the new one — same "archive vs latest" split as `prana`,
enforced by the `record_report()` function in `academic_schema.py`, not by
filesystem convention alone. Because everything (drafts, scores, findings,
reports) lives in the DB, regenerating any past report is just re-running
`assemble-final-document.py` against the same `paper_id` — no re-audit, no
re-generation, matching "report can be easily regenerated at any time as
long as data is in db."

## 7. Visualization (matplotlib, score-over-time)

New tables, direct mirror of `hackathon_visualization_types`/
`hackathon_visualizations`:

```sql
CREATE TABLE IF NOT EXISTS academic_visualization_types (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key     TEXT    NOT NULL UNIQUE,
    scope         TEXT    NOT NULL CHECK (scope IN ('per_domain','per_paper','global')),
    description   TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS academic_visualizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_type_id INTEGER NOT NULL REFERENCES academic_visualization_types(id) ON DELETE CASCADE,
    paper_id      INTEGER REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    content_hash  TEXT,     -- for mermaid-diagram entries, dedupes re-rendering (§6.4)
    file_path     TEXT    NOT NULL,
    created_at    TEXT    NOT NULL
);
```

Seeded chart kinds (script: `render_charts.py`, same structure as
`python_hackathon`'s):

| `chart_key` | scope | Source |
|---|---|---|
| `score-trend-line` | `per_domain` | `academic_score_history`, one line per domain over time |
| `overall-score-trend` | `per_paper` | `academic_score_history` where `domain_id IS NULL` |
| `model-agreement-radar` | `per_domain` | `academic_semantic_runs` — spread across models per domain |
| `domain-score-bar` | `per_paper` | Latest `academic_score_history` row per domain, side by side |
| `mermaid-diagram` | (not a generated chart type — cataloged the same way for reuse-check purposes, §6.4) | |

Same matplotlib + `Agg` backend + `plt.savefig(..., dpi=300)` pattern
`Bodha/docs/paper/Bodha/drafts/visualizations/generate_plots.py` already
uses by hand — this just makes it a registered, re-runnable script instead
of a one-off.

## 8. `standard.yaml` Step-Expansion — Fix the Orphan Gap in the Existing Runtime Approach

An earlier draft of this proposal, written against an older snapshot of the
implementation, proposed a static `build_standard_manifest.py`
pre-generation step because at the time `standard.yaml` had `steps: null`
for 6 usecases and no expansion mechanism existed at all. Since then the
implementation moved on independently: `steps: null` is now `steps: []`
(registration parses cleanly), and `run_full_workflow.py` grew
`expand_triads()` — called after `register_standard` + `schema-init` +
`classify-repo`, it looks up each usecase's registered `script`/`prompt`
ids and calls `_insert_step()` per (domain) or (domain × enrichment_kind)
combination, directly inserting into `step`/`step_script`/`step_prompt`.
`_insert_step()` checks `WHERE usecase_id=? AND step_order=?` before
inserting, so calling `expand_triads()` twice with the *same* domain/module
set is a no-op the second time, not a duplicate.

**This is the right approach — this proposal now adopts it rather than
re-proposing a static alternative that would just be redundant with
working code.** One real gap remains, not addressed by the current
`_insert_step` dedup logic: it only prevents duplicates when the input set
is unchanged. If a repo's domain list narrows (a concrete system's
`academic_domains` changes) or its module count drops (`discover-modules`
finds fewer modules on a later run — code got deleted, a module merged),
the steps inserted for the *larger* previous set at higher `step_order`
values are never removed. They stay in `step`/`step_script`/`step_prompt`,
referencing domains/modules that may no longer exist in
`academic_domains`/`academic_modules`, and `run_triads_for_usecase`'s
index-based `domains[i]` pairing (matching the `i`-th triad to the `i`-th
domain in the *current* list) would silently mispair a stale step with the
wrong current domain if the counts don't line up cleanly.

**Fix**: `expand_triads()` deletes every step for a usecase whose
`step_order` exceeds `3 * len(domains)` (or the relevant multiplier for
that usecase's triad width) before inserting — i.e., truncate to the
current set's size first, then dedup-insert as it already does. This keeps
the existing runtime-insertion design, just makes it correct when the
input set shrinks between runs, which `_insert_step`'s dedup alone doesn't
cover.

## 9. Plagiarism/Humanize — 3 Passes, Not 2

Corrects the previous proposal's `plagiarism-fingerprint-check` →
`humanize` pair. The actual working precedent
(`ai-evaluation-prompt.md` + `ai-humanifier.md`) is 3 passes:

1. **Pass 1 — Forensic audit** (`5a`, semantic): linguistic fingerprint
   scan, burstiness score, hollow-sentence detection. Produces a risk
   report + per-sentence flags, **not** a rewrite.
2. **Pass 2 — Targeted rewrite** (`5a`, same usecase, second semantic
   step): rewrites **only** the High/Critical-flagged sentences from Pass
   1. Cheap — most of the section is untouched.
3. **Pass 3 — Full humanize** (`5b`, separate usecase): whole-section
   3-layer rewrite (structural rhythm, technical-DNA injection, voice
   restoration), using Pass 1+2's findings as context. This is the existing
   `templates/generation/humanifier.md`, unchanged in substance.

`5a` persists to `academic_plagiarism_findings` (already exists — add a
`pass` column: `forensic` or `targeted-rewrite`). `5b` persists to
`academic_humanize_passes` (unchanged). The fix_loop only escalates to `5b`
if Pass 2's targeted rewrites don't bring the section under the risk
threshold — saving a full-section rewrite for when the cheap pass isn't
enough, matching the original 3-pass design's actual cost structure instead
of jumping straight to the expensive option every time.

**New template required — not covered by an existing file.** Pass 2's
targeted-rewrite prompt does not exist anywhere today.
`templates/generation/humanifier.md` covers Pass 3 (full-section rewrite);
nothing covers "rewrite only these specific flagged sentences, leave the
rest of the section untouched." This proposal specifies that
`templates/generation/document/targeted-rewrite.md` needs to be authored,
using `ai-evaluation-prompt.md`'s Pass 2 rules (specificity injection,
rhythm-break, transition relocation, active-voice-where-natural — see the
"Rewrite Rules" section of that file) as the source content, same sourcing
relationship §10 has to `world-class journal paper.md`. Its *shape and
dependency* (a new prompt, registered under `5a`'s second semantic step, is
required for §9 to work at all) is in scope here; its finished prose is
not — same split §12 draws for the domain files, now applied consistently
instead of silently assuming this template already exists.

## 10. Golden-Standard Domain Files (`domains/*.md`)

New `base_academic/domains/*.md`, one per domain from §6.1's list (15
files), same shape as `python_hackathon/domains/04-documentation-standards.md`
(Standard Definition + Expected Evidence, split into what a deterministic
script can check vs. what needs semantic judgment). Content synthesized
from `world-class journal paper.md`'s checklist (§4 material already
extracted this session — algorithmic clarity, mathematical grounding,
baseline-comparison counts, statistical-significance-test requirements,
reference distribution percentages, etc.), generalized the same way §6.1's
domain list is generalized — venue-specific numbers (ESWA's 35-45 reference
count, its exact Scopus tier language) stay in the concrete system's
override, not in the base file.

Each `domains/{name}.md` feeds both `calculation/deterministic/*` (new —
base_academic currently has no deterministic layer at all, contradicting
nothing in its own design, since the earlier finding was "no
section-scoped audits," not "no deterministic checks whatsoever"; simple
mechanical checks — reference count, presence of a complexity-analysis
subsection, baseline count — belong here) and the existing
`calculation/semantic/document.yaml` rubric shape.

**Sequencing dependency, stated explicitly.** §4's `4-semantic-audit.md`
usecase lists `domains/{domain}.md` as an input — that file has to exist
before `semantic-audit` can run meaningfully. This proposal specifies where
those 15 files live, what shape they follow, and what source material
(`world-class journal paper.md`, generalized per §6.1) they're synthesized
from; it does not write their prose. That means `semantic-audit` is
blocked on a follow-up authoring pass, not blocked on anything architectural
in this document — worth tracking as a literal prerequisite task, not just
an "out of scope" footnote, since without it §4's usecase has no rubric to
score against regardless of how correctly everything else in this proposal
gets built.

## 11. Open Questions / Risks

- **Pandoc/mermaid-cli as hard runtime dependencies** — neither is in the
  current samgraha or base_academic dependency surface, and `mmdc`
  specifically pulls in a headless-Chrome install, not a small binary (§6.4).
  Needs an actual availability check (`shutil.which` plus a smoke-render for
  `mmdc`) with a hard failure and clear message, not a silent skip, if
  either is missing at render time.
- **`expand_triads()`'s orphan-cleanup fix** (§8) — the truncate-before-insert
  approach is straightforward, but hasn't been checked against what happens
  to `execution` rows (§knowledge-schema `07-execution.sql`) that reference
  a `step_id` about to be deleted. `step_script`/`step_prompt` cascade via
  `ON DELETE CASCADE`; whether `execution` does too, or whether deleting a
  step with prior execution history should be blocked instead of silently
  losing that history, needs checking against the actual FK definition
  before implementing.
- **`academic_semantic_runs`'s new `run_number` column** (§5) changes an
  existing table's `UNIQUE` constraint — needs a migration path for
  whatever rows already exist under the old `UNIQUE(paper_id, domain_id,
  model)` shape (backfill `run_number=1` for all of them, then apply the
  new constraint), not just a new-file definition.
- **§3's classification backfill** — existing `NEW_NO_IMPL` rows in
  `academic_repos` need inspecting (not blind-renaming) to split correctly
  into `NO_DOCS_NO_IMPL` vs `DOCS_ONLY`, since the old value didn't record
  which case it was.

## 12. Explicitly Out of Scope

Actual script/template file contents: the 15 `domains/*.md` files' full
prose (§10), `targeted-rewrite.md`'s full prompt text (§9),
`_master-schema.yaml`'s real section list values if it turns out to need
more than §6.2's single generic list — this proposal specifies each of
these files' shape, location, and source material, not their finished
text. Note this is narrower than an earlier draft's version of this
section: §9 and §10 both now state explicitly that a new template/file is
*required* for those sections' usecases to function at all — "out of
scope" here means the prose isn't written in this document, not that the
requirement is deferred or optional.

Fixing `register_standard.rs` itself (adding `#[serde(default)]` would
silently accept a still-`null` manifest rather than surface the real
problem, which is that every usecase needs its steps populated one way or
another — §8 keeps the existing runtime-expansion design and only adds the
missing cleanup step, it doesn't touch the Rust struct). Migrating
`pcems_2026`/`eswa_journal` to the new `domains/*.md` +
`_master-schema.yaml` baseline — follow-up, not this document.
