# base_academic — Template Directory Restructure Proposal

## 0. Why This Document Exists

Scoped to `base_academic/templates/` only — narrower than
`archive/base_academic-data-pipeline-proposal.md` §6, which this document
supersedes on template layout specifically, leaving §1–§5 and §7–§12 of that
document untouched.

Confirmed gaps on disk today (`base_academic/templates/`):

- **Only 3 template files exist, total:**
  `templates/audit/report/_audit-report-schema.md`,
  `templates/generation/document/_master-schema.yaml`,
  `templates/generation/document/html/_audit-report-schema.html`.
- **The one HTML file that exists is misplaced.** It is the audit report's
  HTML (`<title>Audit Report — ...`, score-summary table, chart grid) but it
  sits under `templates/generation/document/html/`, not
  `templates/audit/report/`. Meanwhile `plan/usecase/6b-render-paper.md`
  lists `templates/generation/document/html/_master-schema.html` as a
  required input for the paper-render track — no such file exists; the file
  occupying that slot is actually the audit report's HTML.
- **`generate_audit_report.py` never reads the template it ships with.**
  `_load_template()` (`script/render-audit-report/generate_audit_report.py:20-25`)
  is defined but never called — `main()` builds the markdown report by hand
  with an f-string (lines 122-136), ignoring
  `templates/audit/report/_audit-report-schema.md` entirely. The script also
  never renders HTML at all, despite `6a-render-audit-report.md`'s Action
  line ("Assemble markdown + charts → HTML → PDF") — `_audit-report-schema.html`
  has no caller anywhere in the codebase.
- **No per-section generation markdown templates exist.**
  `_master-schema.yaml`'s `sections:` list names 12 structural domains plus 3
  `cross_cutting` ones, but `templates/generation/document/` has no
  `title-and-metadata.md`, `abstract.md`, etc. backing it — despite the
  archived proposal's §6.2 describing "`{domain}.md` — existing pattern, one
  per structural domain" as if it already existed on disk.
- **`academic_report_history.report_kind` is too coarse for a split audit
  report.** `schema/18-academic_report_history.sql:10` —
  `CHECK (report_kind IN ('paper','audit'))`. `record_report()`
  (`script/common/academic_schema.py:663-679`) flips the prior row's
  `is_latest` to 0 for the same `(paper_id, report_kind, format)` before
  inserting — three audit sub-reports sharing `report_kind='audit'` would
  each invalidate the other's `is_latest` flag on every run, which is wrong
  once deterministic/semantic/summary become independently-rendered files
  (§3).
- **Mustache syntax (`{{ }}`, `{{#domains}}`) is already written into both
  existing templates, but nothing in the codebase renders it.** No
  `chevron.render()` call exists anywhere under `base_academic/`. `chevron`
  is already a dependency elsewhere in this repo
  (`python_hackathon/script/common/render_reports.py` imports it) — this
  proposal reuses it rather than adding a second templating library, per the
  archived proposal's own §6.3 reasoning.

## 1. Two Top-Level Categories: `generation/` and `report/`

| Old path | New path |
|---|---|
| `templates/generation/document/_master-schema.yaml` | `templates/generation/markdown/_master-schema.yaml` |
| *(missing)* | `templates/generation/markdown/{section}.md` — 15 new files, §4 |
| *(missing, wrong file sits here today)* | `templates/generation/html/_master-schema.html` |
| `templates/audit/report/_audit-report-schema.md` | `templates/report/markdown/summary.md` (rewritten, §3) |
| `templates/generation/document/html/_audit-report-schema.html` | `templates/report/html/summary.html` (moved, §3) |
| *(missing)* | `templates/report/markdown/deterministic.md`, `semantic.md` |
| *(missing)* | `templates/report/html/deterministic.html`, `semantic.html` |

`templates/audit/` and `templates/generation/document/` are removed —
everything now hangs off `templates/generation/` and `templates/report/`
directly, each with a flat `markdown/` and `html/` child. No third
top-level category for "audit steps": that phrase resolves to `report/`
being split per audit step (§3), not a separate directory.

## 2. What `markdown/` vs `html/` Each Own

Same split for both categories:

- **`markdown/`** — data substitution only. Populated straight from SQLite
  query results (scores, verdicts, findings, section drafts). No chart
  images; mermaid blocks, where present in generated section prose, stay as
  literal ` ```mermaid ` fences (GitHub/most viewers render them natively —
  unchanged from the archived proposal's §6.4 rule).
- **`html/`** — same data, plus `{{#charts}}...{{/charts}}` image blocks
  (`<img src="{{ chart_path }}">`) and rasterized mermaid diagrams. This is
  the only layer that touches `academic_visualizations` /
  `render_charts.py` output. `_audit-report-schema.html`'s existing
  `<style>` block (score-bar coloring, `.pass`/`.fail`/`.warn` classes,
  `.charts` flex grid) is the pattern every other `html/` template reuses,
  not a one-off.

## 3. `report/` — One Template Pair Per Audit Step

Replaces the single combined `_audit-report-schema.md/html` with three
narrower templates, matching the request's named report types:

```
templates/report/
├── markdown/
│   ├── deterministic.md
│   ├── semantic.md
│   └── summary.md
└── html/
    ├── deterministic.html
    ├── semantic.html
    └── summary.html
```

| Template | Data source | Content |
|---|---|---|
| `deterministic` | `academic_deterministic_findings` (latest `run_number` per domain) | Per-domain pass/fail table, failed-check details |
| `semantic` | `academic_semantic_runs` + dimension scores/findings | Per-domain score, mean, domains-below-threshold |
| `summary` | `academic_score_history`, `academic_report_history`, plus a one-line rollup of the other two | Whole-paper final score, band, trend, links/embeds to the deterministic and semantic reports, chart grid |

**Plagiarism is not a fourth template.** The request names three report
types (deterministic, semantic, summary); plagiarism verdicts
(`academic_plagiarism_findings`) fold into `summary` as one section, same
shape as the existing combined file's "Plagiarism Summary" block. Splitting
it out into its own `plagiarism.md`/`.html` pair is a one-file addition
later if that section grows — no system needs it today, so it doesn't get a
template of its own now (same override-later rule the archived proposal
already applies to `paper:`/`journal:` section splits).

**Schema change required.** `report_kind CHECK` becomes
`CHECK (report_kind IN ('paper','audit-deterministic','audit-semantic','audit-summary'))`
in `schema/18-academic_report_history.sql:10`. Existing `report_kind='audit'`
rows can't be split retroactively (the old combined file didn't distinguish
which sub-report a row represented) — backfill relabels them
`'audit-summary'`, the closest existing equivalent since the old file was
summary-shaped.

**`generate_audit_report.py` changes:**
1. `TEMPLATES_DIR` splits into two: `templates/report/markdown/` and
   `templates/report/html/`.
2. One render function per template (`_render_deterministic`,
   `_render_semantic`, `_render_summary`), each calling
   `chevron.render(_load_template(name), context)` instead of building
   markdown by hand — this is what actually uses `_load_template()`, dead
   since it was written.
3. Each function calls `record_report(conn, paper_id, format, path,
   report_kind="audit-deterministic"|"audit-semantic"|"audit-summary")` —
   6 calls total per run (3 templates × markdown/html), each independently
   tracked as `is_latest`.
4. HTML rendering actually happens now (previously absent despite
   `6a-render-audit-report.md` describing it) — `render_charts.py`'s output
   paths feed the `{{#charts}}` context for each `html/` template.

## 4. `generation/` — Per-Section Markdown + One HTML Shell

**15 new markdown skeletons**, one per entry in `_master-schema.yaml`'s
`sections:` (12) and `cross_cutting:` (3) lists — heading/subheading
scaffold only, the same "structure is a template's job, filling it is a
script/prompt's job" split the codebase already draws elsewhere:

```
templates/generation/markdown/
├── _master-schema.yaml   (moved, content unchanged — see below)
├── title-and-metadata.md
├── abstract.md
├── introduction.md
├── related-work.md
├── problem-definition.md
├── methodology.md
├── experimental-setup.md
├── results.md
├── discussion.md
├── limitations.md
├── conclusion.md
├── references.md
├── novelty.md
├── gaps.md
└── mathematics.md
```

**Not a duplicate of `prompt/assemble-paper-structure/generate-section.md`.**
That file is the agent-facing instruction prompt (how to write the section).
`templates/generation/markdown/{section}.md` is the deterministic scaffold
the agent's output gets slotted into (what headings/order the section must
have) — same script-vs-template boundary the archived proposal draws
throughout, just applied to a layer that was speced but never built.

**One HTML shell, not 15.** `templates/generation/html/_master-schema.html`
is the whole-assembled-document shell `assemble-final-document.py` renders
through (per `6b-render-paper.md`) — it consumes every section's already-
concatenated markdown plus rasterized mermaid images, so it doesn't need a
per-section split the way `markdown/` does. This is the file
`6b-render-paper.md` already lists as a required input; today that path is
occupied by the audit report's HTML by mistake (§0) — this proposal is what
actually creates the real one.

`_master-schema.yaml` moves unchanged except its header comment, which
currently points at `docs/proposal/base_academic-data-pipeline-proposal.md
§6.2` (now `archive/`) — update the comment to point at this document
instead.

## 5. Final Proposed Tree

```
base_academic/templates/
├── generation/
│   ├── markdown/
│   │   ├── _master-schema.yaml
│   │   ├── title-and-metadata.md
│   │   ├── abstract.md
│   │   ├── introduction.md
│   │   ├── related-work.md
│   │   ├── problem-definition.md
│   │   ├── methodology.md
│   │   ├── experimental-setup.md
│   │   ├── results.md
│   │   ├── discussion.md
│   │   ├── limitations.md
│   │   ├── conclusion.md
│   │   ├── references.md
│   │   ├── novelty.md
│   │   ├── gaps.md
│   │   └── mathematics.md
│   └── html/
│       └── _master-schema.html
└── report/
    ├── markdown/
    │   ├── deterministic.md
    │   ├── semantic.md
    │   └── summary.md
    └── html/
        ├── deterministic.html
        ├── semantic.html
        └── summary.html
```

## 6. Migration Steps

1. `git mv templates/generation/document/_master-schema.yaml templates/generation/markdown/_master-schema.yaml`
2. `git mv templates/generation/document/html/_audit-report-schema.html templates/report/html/summary.html`
3. `git mv templates/audit/report/_audit-report-schema.md templates/report/markdown/summary.md` (then split its domain-table rows into `deterministic.md`/`semantic.md` per §3, leaving `summary.md` as rollup-only)
4. Remove now-empty `templates/audit/` and `templates/generation/document/`.
5. Author `templates/report/markdown/deterministic.md`, `semantic.md` and `templates/report/html/deterministic.html`, `semantic.html` (new files — content not written by this proposal, §8).
6. Author the 15 `templates/generation/markdown/{section}.md` skeletons and `templates/generation/html/_master-schema.html` (new files — content not written by this proposal, §8).
7. `schema/18-academic_report_history.sql:10` — update `CHECK` constraint; backfill existing `report_kind='audit'` rows to `'audit-summary'`.
8. `script/render-audit-report/generate_audit_report.py` — split `TEMPLATES_DIR`, add `chevron.render()` calls, add HTML rendering, 6 `record_report()` calls (§3).
9. `plan/usecase/6a-render-audit-report.md` — update template path references to `templates/report/{markdown,html}/*`.
10. `plan/usecase/6b-render-paper.md` — update `templates/generation/document/html/_master-schema.html` reference to `templates/generation/html/_master-schema.html`.

## 7. Open Questions

- **Plagiarism's own template** (§3) — revisit if its `summary.md` section
  outgrows a single subsection; no template split until then.
- **`chevron` as a new runtime import for `base_academic`** — already a
  repo dependency (`python_hackathon`), but confirm it's declared wherever
  `base_academic`'s own script dependencies are tracked, not just installed
  incidentally via `python_hackathon`'s requirements.

## 8. Explicitly Out of Scope

Actual prose/markup content of the 15 `generation/markdown/*.md` skeletons,
`generation/html/_master-schema.html`, and the 4 new `report/*` templates
(`deterministic.md/.html`, `semantic.md/.html`) — this proposal specifies
each file's location, data source, and structural boundary, not its
finished text. `render-docx.py`, `extract-mermaid-images.py`, and the
mermaid/pandoc dependency questions are unchanged from the archived
proposal's §6.3/6.4/§11 and are not revisited here.
