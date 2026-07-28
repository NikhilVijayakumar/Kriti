# pcems_2026 — Proposal-Phase Understanding Check: Gaps vs. Stated Model

## 0. What was asked

Confirm this understanding of the `propose-*` system before building anything:
samgraha's `proposal` table (`schema/knowledge/15-proposal.sql`) should drive a
per-domain, phase-wise plan across audit/generation/fix, built by considering
each usecase's steps (deterministic or semantic), analyzing the repo, and
rendered through `templates/` in `pcems_2026`.

**Verdict: partially correct, with one blocking bug and two model
mismatches.** The propose-* system already exists, already runs 4 phases
(not 3), and is already domain-scoped — but it does not consult samgraha's
generic `usecase`/`step` registry at all, and every phase's render step is
currently a silent no-op because its template files don't exist on disk.

---

## 1. What already exists (traced against live code)

| Piece | Status | Where |
|---|---|---|
| 4 propose usecases, not 3 | Built | `standard.yaml:561-631` — `propose-generation`, `propose-audit`, `propose-report`, `propose-fix` |
| Each phase gathers domain-level context | Built | `gather_proposal_context.py` — `_gather_generation_context`, `_gather_audit_context`, `_gather_report_context`, `_gather_fix_context` |
| Persist + append-only history + redraft/rejection tracking | Built | `persist_proposal.py`, `academic_proposals` table (`is_latest`, `status`, `iteration`, `scope_domain_id`) |
| Approval gate | Built | `approve_proposal.py`, completion predicates `_make_proposal_predicate` (`academic_schema.py:1116-1132`) for generation/audit/report; `propose-fix` intentionally has no whole-paper predicate (domain-scoped, checked per-domain — `academic_schema.py:1109-1113`) |
| Render to markdown/html | **Broken** | `render_proposal.py:28-31,92` — see §2 |

This is a real, working, already-domain-scoped pipeline. It is not something
to build from scratch.

---

## 2. Gap 1 (blocking) — `templates/proposal/` doesn't exist

`render_proposal.py:28-31` reads templates from:
```
templates/proposal/markdown/{phase}.md
templates/proposal/html/{phase}.html
```
Neither directory exists anywhere under `pcems_2026/templates/` — confirmed
by listing (`templates/` only has `generation/` and `report/` subdirs).
`_load_template` (`render_proposal.py:34-39`) returns `None` when the file is
missing, and `main()` just skips that format — **no error, no exception**,
`write_envelope(status="ok", rendered=[])`. Every `propose-*` run today
completes "successfully" while writing zero files, for all 4 phases, every
time. `standard.metadata.json` only declares one `role: "proposal"` template
name (`"generation-proposal"`) with no physical file behind it either — the
metadata-level template catalog and the physical chevron files
`render_proposal.py` actually loads are two different things, and neither
exists for audit/fix/report.

The three prompts (`propose/audit-proposal.md`, `fix-proposal.md`,
`generation-proposal.md`) all explicitly instruct the model to match
`templates/proposal/markdown/{phase}.md`'s shape — so the prompts were
written assuming these files would exist, and they were never created.

**This is the actual, concrete, fixable gap** — not a design problem, a
missing-file problem. Fix: write 4 chevron templates (`generation.md`,
`audit.md`, `fix.md`, `report.md`, markdown + html) matching each prompt's
documented input shape (`domains[]`, `models[]`/`triggering_findings[]`/etc.
per phase, per each prompt's own "Output Format"/"Input" sections).

---

## 3. Gap 2 — proposals don't consult usecase/step at all

The stated model was "considering usecase and step, step can be
deterministic or semantic." Traced `gather_proposal_context.py` end to end:
none of its four `_gather_*_context` functions query samgraha's `usecase` or
`step` tables. Generation/audit context is built from:
- `academic_domains` (domain list + sort order)
- `calculation/generation/{domain}.yaml` (rule/check counts, word budgets)
- `audit/semantic/document/{domain}.md` (rubric criterion counts)
- `academic_narratives` (current stage per domain)

This is domain-and-rule-file granularity, not usecase-and-step granularity.
samgraha's own generic `proposal` table (`schema/knowledge/15-proposal.sql`,
linking `usecase_id`/`template_id`/`execution_id`) and its
`phases: [{domain, usecases[], steps[]}]` schema
(`step_execution.rs:142-155`, `metadata_validate.rs`) is **wired but
unused** by this standard — `persist_proposal.py`/`render_proposal.py` never
emit a top-level `"proposal"` key in their script envelope, so
`validate_proposal_envelope`/`check_has_proposal_template` never fire for
pcems_2026's actual propose-* runs. Two parallel proposal-tracking systems
exist (samgraha's generic one, pcems_2026's own `academic_proposals`); only
the latter is live.

If real usecase/step-level planning is wanted (e.g. "this phase will run
these N steps, M of them semantic, across these domains"), that's new
scope — not a wiring gap in what's there. It would mean either (a) having
`gather_proposal_context.py` additionally query `usecase`/`step` for the
domains in play and surface step kind/count per domain, or (b) switching
onto samgraha's generic phases-schema and actually emitting a `"proposal"`
envelope key so `validate_proposal_envelope` cross-checks it. Recommend
clarifying which before scoping further — they're different amounts of work
and change what the templates in §2 need to render.

---

## 4. Gap 3 — "analyse the repo" already happens, but earlier, not at propose time

Generation-phase context reads already-persisted
`academic_cross_module_analysis` rows (novelty/gaps/mathematics/
architecture — `_gather_generation_context`, `gather_proposal_context.py:96-102`).
Repo analysis itself runs earlier, in the `*-analysis` usecases
(`novelty-analysis`, `gap-analysis`, `mathematics-analysis`,
`diagram-architecture-analysis`), well before `propose-generation` runs.
Audit/fix/report phases don't reference repo analysis at all — audit reads
rule/rubric file counts, fix reads failing deterministic findings, report
reads score history. If "analyse the repo" was meant literally (fresh
analysis triggered from inside the propose step), that duplicates work the
`*-analysis` usecases already do and isn't how any current phase behaves.

---

## 5. Recommendation

1. **Do §2 first** — it's the only actual bug, it's small (4 templates,
   pattern already established by `templates/generation/markdown/*.md` and
   `templates/report/markdown/*.md`), and every propose-* run is silently
   broken until it's done.
2. Don't build usecase/step-level proposal planning (§3) or repo
   re-analysis at propose time (§4) without confirming that's genuinely
   wanted — as described, both are new capabilities layered onto a system
   that currently works at domain+rule-file granularity, not a fix to
   something broken.

No implementation proposal is written for §3/§4 here since the request's
premise needs confirming first — see open questions below.
