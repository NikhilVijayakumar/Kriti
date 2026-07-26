# pcems_2026 — Render-Paper Wiring + Reference-Material Grounding

## 0. Why This Document Exists

Asked directly: register `pcems_2026` as a standard, generate a paper from
real documentation (`E:\Python\Bodha\docs\paper`), would the result match
`reference/sample_paper` and `reference/template`'s quality, produced as
DOCX + PDF? Checked the actual pipeline rather than assuming. Two real gaps,
of different kinds:

1. **Render-paper is disconnected — mechanical bug, no design decision
   needed.** Fixed directly, no proposal required for this half.
2. **`reference/sample_paper`/`reference/template`'s extracted text is
   never consumed by any prompt.** This half needs a real decision (how
   much content, where, hand-picked vs. full-dump) — settled below.

---

## 1. Render-Paper — What's Actually Broken (direct fix, not a design question)

Checked `run_full_workflow.py` end to end:

- `render-paper`'s usecase has `steps: []` in `standard.yaml`, same as
  `cross-section-semantic-audit`/`document-semantic-audit`/`reviewer-
  simulation` before their triads get populated by `expand_triads()`. But
  **no equivalent population block exists for `render-paper`** — grepped
  the whole file, zero hits beyond the docstring's execution-order comment.
  `steps_of(steps, "render-paper")` returns empty; the generic single-step
  loop that calls it (`for usecase in ("render-charts", "render-audit-
  report", "render-paper")`) silently no-ops.
- `assemble-final-document.py`, `render-docx.py`, `render-pdf.py` are real,
  working scripts on disk (`pcems_2026/script/render/`) — **none of the
  three is registered in `standard.yaml`'s `scripts:` block.** Nothing to
  wire a step to yet, even before the missing population block.
- **`assemble-final-document.py` has a file-clobber bug independent of the
  wiring gap**: it writes the assembled HTML to `out_path` (`out_path
  .write_text(final_html, ...)`), then calls `write_envelope(out_path,
  ...)` — `write_envelope` does `out_path.write_text(json.dumps(envelope))`
  on that *same* path. The JSON status envelope overwrites the HTML the
  line before it. Every other script that produces a real artifact
  (`render_proposal.py`, `persist_reviewer_simulation.py`, etc.) writes its
  artifact to a path under `docs/paper/paper-{id}/...` and reserves
  `out_path` for the status envelope only — `assemble-final-document.py`
  is the one script in this pipeline that doesn't follow that split. This
  would break `render-paper` even if the wiring gap above were fixed.
- Even once wired: `render-docx.py` shells out to `pandoc`, which isn't on
  `PATH` in this environment (checked). `render-pdf.py` uses Playwright +
  Chromium, which **is** installed and would work today.

None of this is a design choice — it's "the last mile was never
connected." Fixed directly in this same pass:
- `assemble-final-document.py` writes HTML to `docs/paper/paper-{id}/
  assembled.html`, envelope carries that path in `html_path`.
- Register the 3 scripts in `pcems_2026/standard.yaml`.
- Add the missing `expand_triads()` population block (3 deterministic
  steps: assemble → docx → pdf), matching the 5e/5f/5g pattern.
- Chain the 3 steps' real outputs into each other (assemble's `html_path`
  feeds both render steps) — the existing generic single-step loop can't
  do this (it calls one step with a fixed empty input), so `render-paper`
  gets its own small chaining function, the same shape `_checkpoint()`
  already uses to thread `gather`'s output into `persist`'s input for
  `propose-{phase}`.
- Add `pypandoc-binary` to `requirements.txt` (bundles a real pandoc
  binary via pip — no system-level install needed) and give `render-
  docx.py` a fallback lookup through it when `pandoc` isn't on `PATH`.

---

## 2. Reference-Material Grounding — The Actual Decision

`reference/sample_paper/extracted/*.txt` (11 real accepted papers, full
text + `_summary.json` metadata) and `reference/template/extracted/
Template_PCEMS2026.txt` (the literal official template) exist, fully
extracted, and are referenced by **zero** files anywhere in `pcems_2026`.
Whatever compliance exists today is only what got hand-encoded into
`_master-schema.yaml`/`_style.css`/the prose guide files — never checked
against the actual reference artifacts.

**Checked the extracted text quality before deciding how to use it**: the
11 sample papers were PDF-extracted from two-column layouts, and the
extraction interleaves columns mid-sentence (confirmed by reading
`Credit_Card_Fraud_Detection...txt` — the abstract's prose is cut apart by
a sidebar list mid-paragraph). **Quoting this raw text into a prompt would
inject confusing, garbled calibration material** — not a hypothetical
risk, directly observed in the extracted file. The template extraction
(`Template_PCEMS2026.txt`), by contrast, is single-column and clean.

**Settled, not left open**:

1. **Template → `document-audit.md`'s "Template compliance" dimension**
   (restored earlier this session after being flagged as a regression).
   The extracted template text is small (28 lines, ~1KB) and clean —
   inline it directly under that dimension as the literal source of truth
   (title-block order, single-column requirement, image/table placement
   rule, APA reference style, Arial font/size spec per heading level),
   instead of the dimension relying only on prose guide references.
2. **Sample papers → `reviewer-simulation.md`'s "Writing, Organization,
   Figures" persona, as clean aggregate stats, not raw quoted text.**
   `_summary.json` gives exact, clean numbers across all 11 real accepted
   papers: 2,428–4,781 words (avg. 3,628), 4–6 pages (avg. ~5.5). Add this
   as an explicit calibration line — a generated paper wildly outside this
   range is a real organization/scope signal a reviewer would flag,
   grounded in actual accepted-paper data instead of an invented target.
   Not quoting the garbled prose itself — the numbers are the clean,
   useful part of this extraction; the sentences are not.
3. **Not done**: full-text injection of all 11 papers into any prompt
   (extraction quality rules this out) and a new deterministic "matches
   reference paper" rule (nothing here is mechanically comparable paper-
   to-paper — this is a judgment-call grounding addition to two existing
   LLM-scored dimensions, not a new Layer 1 check).

---

## 2a. Addendum — External Review Findings (post-implementation)

A review of this proposal's first implementation pass caught 2 real gaps
and raised 1 that turned out to be larger than stated. Checked each
against the actual code before acting:

- **Confirmed, fixed**: `extract-mermaid-images.py` existed but was never
  wired into `render-paper`'s chain (same class of gap as the original
  render-paper wiring), and had the *exact same* `out_path`-clobber bug
  `assemble-final-document.py` had — confirmed by reading its `main()`,
  fixed the same way (write the modified HTML back to `html_path`,
  reserve `out_path` for the envelope). Now the 4th step in the chain:
  assemble → rasterize-mermaid → docx → pdf.
- **Confirmed, fixed**: pandoc's default DOCX styles use Calibri; nothing
  passed `--reference-doc`. Built `generate_reference_docx.py` (one-shot,
  `python-docx`) producing `reference/template/
  Template_PCEMS2026_reference.docx` with the template's exact Arial
  12/12/12/11pt heading hierarchy (source: `Template_PCEMS2026.txt`,
  already used for the document-audit grounding above) — `render-docx.py`
  now defaults to it.
- **Refuted**: "`findings.html` doesn't exist, only `results.html`" —
  checked `templates/generation/html/`, `findings.html` exists and matches
  `_master-schema.yaml`'s `sections:` list exactly. No `results.html`
  anywhere in this tree.
- **Refuted**: "no word-count validation at assembly time" — `section-
  budget-fit-total` (fan-in usecase, `academic_schema.py`) already gates
  the whole-paper word count against `paper-budget.yaml` *before*
  `deterministic-audit` runs, earlier in the pipeline than assembly. Fail-
  fast at the right stage already exists; duplicating it at assembly adds
  nothing budget-fit didn't already catch.
- **Confirmed, larger than stated — flagging, not fixing here**: figure/
  table generation and "map raw docs into domains" aren't 2 separate gaps,
  they're one architectural fact. Traced the actual evidence-gathering
  chain (`discover_modules.py` → `gather_module_evidence.py` →
  `gather_domain_evidence.py`): `discover_modules.py` explicitly *excludes*
  `docs/` from module discovery and only recognizes directories containing
  `.py`/`.rs`/`.ts`/`.js` source as a "module"; `gather_module_evidence.py`
  parses Python ASTs (docstrings, classes, functions, imports) and previews
  raw source files — it has no branch for `.md` at all. This pipeline's
  novelty/gap/mathematics analysis is built to ground claims in a
  *codebase's source code*, not a folder of prose documentation. Bodha's
  `docs/paper` (pure documentation, not source) would be structurally
  invisible to this evidence chain regardless of how much good content it
  has — not a missing mapping step, a mismatch between what this system
  ingests and what Bodha's repo actually is. Same root cause covers the
  figures/tables gap: those are cross-cutting *narrative* domains (an LLM
  writing prose critique of "figure construction quality"), woven into
  `findings` as more paragraphs — there is no mechanism anywhere to embed
  an actual pre-existing image (Bodha's chart PNGs or anything else) as a
  literal `<img>` in the assembled document. This is the real blocker for
  the original question and needs its own proposal — it's a design
  decision (new evidence-gathering mode for docs-only repos? a manual
  content-seeding path? something else?), not a bounded fix like the rest
  of this document.

---

## 3. What This Does Not Change

- No new usecase, no new domain, no new database table — `render-paper`
  and `document-audit`/`reviewer-simulation` already exist; this closes
  gaps in them.
- `guide/Examples/*.md` (hand-authored per-domain writing examples) is a
  separate, already-wired mechanism — untouched here.
- Full grammar/style/APA checking remains the explicitly deferred item
  from the review-pipeline proposal — not in scope here either.
