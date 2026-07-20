# python_hackathon — Report Pipeline Verification Proposal

**Proposal 3 of 3, in dependency order** — after
`python_hackathon-visualization-and-detail-templates-proposal.md`
(proposal 1, defines what's needed) and
`python_hackathon-report-analysis-proposal.md` (proposal 2, defines
the design system and template set), this proposal checks whether
scripts actually exist to build any of it, and proposes the ones that
don't. Verification only — no code written here, per instruction.

---

## 0. What was checked, and how

Direct inspection, not assumption: read `render_reports.py` in full,
grepped it for `.html`/`chart`/`svg`/`pdf` (zero matches for all
four), and searched the whole `python_hackathon/` tree for any
chart-generation, HTML-render, or PDF-export script by name. Findings
below are grounded in that, not inferred from the proposals' own
descriptions of what "should" exist.

## 1. Visualization-generation script

**Status: does not exist.** The 7 chart types (proposal 1 §1) have no
generation function anywhere. The 2 chart types prototyped during
proposal 2's `huashu-design` session are hand-authored static SVG,
hardcoded sample numbers baked directly into the demo HTML files
(`primer-summary.html`, `primer-leaderboard.html`) — there is no
`chart_field_distribution(data) -> svg_string`-shaped function, no
counterpart to base_dev's `visualize.py` at all in this system.

**Proposed**: a new `script/render_charts.py`, one function per chart
type in proposal 1's catalog (7 functions), each taking the same data
shape `render_reports.py`'s existing fetch functions already produce
(§2 below explains why this is fetch-function reuse, not new
computation). **Output format resolved as matplotlib-generated PNG
files, not inline SVG** — reversing the inline-SVG lean an earlier
draft of this section took; see §6 for the reasoning. Mirrors
base_dev's `visualize.py` shape exactly now, not just in structure
(`CHART_CATALOG` dict of name → function) but in output medium too —
one PNG-generation pattern across both systems in this project family,
not two different chart philosophies.

## 2. Markdown-template data-mapping

**Status: exists, correctly, for what it currently covers; does not
yet cover proposal 1's additions.**

`render_reports.py`'s 5 fetch functions
(`fetch_deterministic_data`/`fetch_semantic_data`/`fetch_summary_data`/
`fetch_leaderboard_data`/`fetch_team_summary_data`) are real, read
from `standard_domain_scores` correctly, and `render_all()` calls
`chevron.render()` against the 32 existing markdown templates — this
was verified working in an earlier round of this conversation (all 16
task items confirmed against the codebase directly). **Resolved,
correcting this section's earlier hedge**: `detail`/`reasoning` are
confirmed already present in both fetch functions' output (proposal 1
§0 verified this directly against the actual code) — this was never
a data-layer gap. What proposal 1 does need (§3 of that proposal):
`evaluate_domain()` extended to also surface `severity` per rule
(currently dropped despite existing in every rule's YAML source), and
`fetch_team_summary_data()` extended to emit list-shaped domain scores
alongside its existing flat fields, for the radar chart.

**Proposed**: no new script — two small, additive extensions to
functions that already exist and already work for everything else
they cover, not a new mapping layer.

## 3. HTML-generation script

**Status: does not exist.** `render_reports.py` is markdown-only (zero
`.html` references, confirmed by direct grep). The 2 HTML pages that
exist (`primer-summary.html`, `primer-leaderboard.html`) are one-off
design-demo artifacts — hand-written by design subagents during
proposal 2's `huashu-design` session, hardcoded sample data, not
template files, not driven by any render script. Nothing takes real
`standard_domain_scores`/`standard_narratives` data and produces any
of the 32 HTML pages proposal 2 §10 specifies.

**Proposed**: a new `script/render_html_reports.py`, structurally
parallel to `render_reports.py` — same 5 fetch functions reused
(§2, no duplicate data layer, per proposal 2 §10's explicit "no
separate HTML data fetcher" instruction), but rendering against 32 new
`.html.mustache`-style templates (or `.html` files with embedded
Mustache tags, matching the existing `.md` templates' convention)
instead of the 32 `.md` files, using `chevron.render()` the same way,
plus `{{> design_tokens}}` and the relevant `{{> chart_*}}` partials
per proposal 2/1. The two approved demo pages become the reference
implementation to extract these 32 templates from — not a fresh
design pass, the visual language is already locked.

## 4. HTML → PDF script

**Status: does not exist**, anywhere in `python_hackathon/`. Proposal
2 §10 names the intended mechanism — `huashu-design`'s own
`scripts/export_deck_pdf.mjs` (per-page `playwright` `page.pdf()` +
`pdf-lib` merge) — but that script lives in the skill's own asset
directory (`C:\Users\nikhi\.claude\skills\huashu-design\scripts\`),
not copied or adapted into this project, and it's built for a generic
"deck" (ordered list of HTML files → one PDF), not specifically for
"31 pages × N teams, one PDF per team, batched by team boundary."

**Proposed**: a new `script/export_team_pdfs.py` (or a thin wrapper
invoking the existing `.mjs` script once per team) that: for each
registered participant, collects their 31 rendered HTML pages (10
domains × 3 kinds + team-final-summary) in the fixed domain order
proposal 2 §10 specifies, and merges them into one PDF named for that
team, excluding the shared `global-leaderboard.html` from every team's
PDF (also per proposal 2 §10's explicit rule). Whether this wraps the
existing `.mjs` via `subprocess` or reimplements the same
`playwright`+`pdf-lib` pattern directly in Python (matching this
project's otherwise-all-Python script convention, vs. pulling in a
Node dependency for one script) is a real choice, not decided here —
flagged in §6.

## 5. Summary table

| Script | Status | Action |
|---|---|---|
| `render_charts.py` | Missing | Create — 7 chart functions per proposal 1 §1, matplotlib → PNG files |
| `render_reports.py` (markdown) | Exists, works | **No change** — markdown stays content-only, never embeds charts (§6) |
| `render_html_reports.py` | Missing | Create — 32 HTML templates, reuses existing fetch functions, embeds chart PNGs via base64 (§6) |
| `export_team_pdfs.py` | Missing | Create — per-team merge, excludes shared leaderboard |

Four pipeline stages named across the three proposals; one exists and
works, three don't exist at all. Nothing here contradicts proposal 2's
design decisions — this is purely "does the plumbing exist to execute
them," and for 3 of 4 stages, it doesn't yet.

## 6. Open questions for confirmation

1. `export_team_pdfs.py` — wrap `huashu-design`'s existing `.mjs` via
   `subprocess` (reuses tested code, adds a Node dependency to an
   otherwise-Python project) or reimplement the same
   `playwright`+`pdf-lib` pattern in Python (stays dependency-consistent,
   duplicates ~50 lines of already-working logic)? Recommend wrapping
   via `subprocess` first — reuse over reinvention, matching this
   whole conversation's repeated lesson — revisit only if the Node
   dependency proves genuinely disruptive to this project's setup.
2. `render_charts.py`'s output format — **resolved: matplotlib →
   PNG files, not inline SVG.** Reverses this proposal's earlier
   recommendation (inline SVG, "matches the 2 approved demo pages").
   **Corrected reasoning** — an intermediate draft of this decision
   justified it partly by "serves markdown and HTML from one file";
   that's wrong and now retracted: **markdown never embeds charts at
   all** — confirmed, markdown stays content-only (scores, tables,
   narrative text), visualization is exclusively an HTML/PDF concern.
   The real reasons PNG still wins, independent of that dropped
   argument: matplotlib handles the harder new chart types
   (10-spoke radar, distribution bell-curves with confidence bands)
   correctly out of the box, where hand-rolled SVG geometry risks
   getting the math subtly wrong. **Real cost, not hidden**: PNG makes
   chart labels non-text — not searchable/copyable in the exported
   PDF, unlike inline SVG. Mitigated by every number a chart shows
   already existing as real text elsewhere on the same page (the
   tables/narrative near it) — the chart is a visual aid on top of
   already-searchable data, not the only place a number lives. The two
   approved demo pages' inline SVG stays as the reference for visual
   language (colors, layout, what each chart communicates) —
   matplotlib output should match that appearance, the generation
   mechanism changing shouldn't change how the chart looks.
3. Should `render_html_reports.py` and `render_reports.py` (markdown)
   be unified into one script with a `--format {md,html}` flag, or
   stay two separate files? Both call the same 5 fetch functions —
   recommend keeping them separate files (matches `render_reports.py`'s
   already-shipped, working shape; merging it now risks regressing
   something already verified working for a consolidation that saves
   little).

## 7. Verification checklist

- [ ] §1 — `render_charts.py` exists with 7 matplotlib-based functions,
      one per proposal 1 §1's catalog, each consuming existing
      fetch-function output (no new data computation) and writing PNG
      files (not returning inline SVG); colors match the design-token
      hex values (proposal 2 §10), read from the token source at
      generation time rather than resolved via CSS `var()`.
- [ ] §2 — `evaluate_domain()` surfaces `severity` per rule;
      `fetch_team_summary_data()` emits list-shaped domain scores — the
      two real extensions proposal 1 §3 identifies (not the stale
      `detail`/`reasoning` hedge this checklist used to carry; both
      already confirmed present, no work needed there).
- [ ] §3 — `render_html_reports.py` exists, produces all 32 HTML pages
      from real DB data, reuses `render_reports.py`'s 5 fetch
      functions rather than duplicating them, embeds chart PNGs via
      base64 (not `<img src>` file paths — keeps each page self-contained).
- [ ] §3 — markdown templates (`render_reports.py`) contain **no**
      chart references, `![]()` or otherwise — confirmed unchanged
      from its existing content-only scope; visualization stays
      exclusively in the HTML/PDF layer.
- [ ] §4 — a working per-team PDF export exists, producing one PDF
      per registered participant from their 31 pages in fixed domain
      order, with `global-leaderboard.html` excluded from every one.
- [ ] §6 — all three open questions have a recorded decision, not left
      ambiguous once implementation starts.
