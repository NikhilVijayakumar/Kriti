# pcems_2026 — Seeder Usecase-Wiring Gap Analysis & Fix Proposal

## 0. Context

Supersedes the closed `docs/proposal/archive/pcems_2026-samgraha-gap-fix-proposal.md`.
That proposal's two real blockers (11 usecases with zero steps; numbered
rubric filenames) are fixed and verified. Fixing them unmasked Layer A
audit check #6 (`audit_prompts_are_referenced`, `layer_a_audit.rs:143-163`):
13 prompts are declared in `standard.yaml` but wired to zero steps.

v1 of this document retracted a same-session patch (routing
`collate-references` into `generate-section-draft-references`) on the
theory that the generation tier runs before the citation tier. **That
theory was itself wrong** — a second verification pass (below) found the
patch's real problem is a hardcoded domain list that can never resolve for
this standard, independent of which usecase the script sits in. Two full
verification passes were needed before the root cause was right; both are
kept below so the trail is legible.

Method, unchanged from v1: for every orphaned prompt or usecase, trace its
output to a real downstream reader — a calculation file, another script,
or a registered completion predicate — before proposing a wire. Passing
Layer A only proves the graph is structurally connected; it doesn't prove
the pipeline runs, in order, without hard-failing on its own preconditions.

---

## 1. Taxonomy

| Cluster | Prompts / usecases | Root cause | Status |
|---|---|---|---|
| A | `module-analysis-architecture`, `cross-module-analysis-{architecture,dependencies,interactions}` | `diagram-architecture-analysis` usecase never declared in `standard.yaml`, despite 3 live downstream consumers and its own registered completion predicate already existing in `academic_schema.py:688-699`. | Confirmed |
| B | `semantic-audit-part`, `fit-to-budget`, `plagiarism-fingerprint-audit`, `targeted-rewrite` | Deterministic half of citations/enrichment/budget-fit/plagiarism usecases is wired; semantic half isn't. | Confirmed |
| C | `collate-references` placement, `generate-section` | See §2 — real root cause is Gap F, not tier ordering. | Corrected (see below) |
| D | `generate-novelty`, `generate-gaps`, `generate-mathematics` | `assemble-final-document.py` reads cross-cutting content from `academic_cross_module_analysis`, never from `academic_narratives`. No reader anywhere today. | **Owner decision: keep** — needs new domain rows + generate usecase + render-script update, see §5 |
| E | `literature-review-pass` | Overlaps `section-enrichment` but does a different, narrower job (citation grounding vs. general quality). | **Owner decision: sequential** — runs before `section-enrichment`, see §6 |
| F | `collate_references.py`'s domain gate | Hardcoded `academic_schema.GENERATED_DOMAINS` (11 base_academic domains) used as the gate list; 7 of those 11 don't exist in pcems_2026's `academic_domains` table at all. | **New — critical** |
| G | `validate-references` script | Named in `plan/usecase/4b-cite-references.md:5` as the script for `section-citations-references`; doesn't exist anywhere on disk (`grep` confirms only the plan doc mentions it). | **New** |
| H | Stage mismatch | `collate_references.py` writes `stage='cite'` (`academic_schema.py`'s `upsert_narrative` call inside it); wiring it into `generate-section-draft-references` means that usecase's own completion predicate (`_make_stage_predicate(domain, "generate")`, checks `stage='generate'`) can never see it. | **New** |
| I | `section-supplementary-content-{domain}` vs `section-enrichment-{domain}` | Naming mismatch — `academic_schema.py` registers the enrich-stage completion predicate as `section-supplementary-content-{domain}` (lines 775-780, and again in the `_PER_DOMAIN_PREDICATE_FACTORIES` fallback, line 993), but `standard.yaml`, `seeder.py`, every `4c-enrich-*.md` plan doc, and the verify-script generator (`generate_per_domain_usecases.py:83-86`) all use `section-enrichment-{domain}`. `academic_schema.py` is the one outlier. | **New** |
| J | Shared-vs-local domain list | `academic_schema.py:575-580`'s `STRUCTURAL_DOMAINS`/`GENERATED_DOMAINS` is base_academic's 12-domain list, imported and iterated at runtime by `collate_references.py` (Gap F). `generate_per_domain_usecases.py` already carries its own correct local 6-domain override (lines 23-27) and is not itself affected — it's a dev-time generator, not something the live pipeline runs. Today, `collate_references.py` is the only *runtime* script with this bug; the risk is any future script casually importing the shared list instead of querying live `academic_domains`. | **New — scoped narrower than first suspected** |

---

## 2. Cluster C / Gap F–I — `references`, Fully Traced

### 2.1 What v1 got wrong

v1 claimed the generation tier runs before the citation tier, so wiring
`collate-references` into `generate-section-draft-references` would hard-fail
against the script's own documented gate ("all 11 section-citations-{domain}
usecases completing first"). This is contradicted by `4a-generate-references.md:3`:
`Depends on: 4b-cite-introduction + ... (all citation stages)` — references'
generate stage is explicitly declared to run *after* every other domain's
citation stage. So ordering isn't the problem.

### 2.2 What's actually wrong (Gap F) — verified against the running code

`collate_references.py:75`:
```python
for domain in academic_schema.GENERATED_DOMAINS:
    complete, _detail = academic_schema.usecase_status(
        conn, paper_id, f"section-citations-{domain}")
    if not complete:
        outstanding.append(domain)
```
`academic_schema.py:575-580`:
```python
STRUCTURAL_DOMAINS = [
    "title-and-metadata", "abstract", "introduction", "related-work",
    "problem-definition", "methodology", "experimental-setup", "results",
    "discussion", "limitations", "conclusion", "references",
]
GENERATED_DOMAINS = [d for d in STRUCTURAL_DOMAINS if d != "references"]
```
11 domains. pcems_2026's `academic_domains`/`domain` tables only ever have 6
(`title-and-metadata, introduction, methodology, findings, conclusion,
references`) + `reviewer-simulation`. For the 7 domains in `GENERATED_DOMAINS`
that pcems_2026 never seeds (`abstract, related-work, problem-definition,
experimental-setup, results, discussion, limitations`),
`usecase_status` (`academic_schema.py:589-602`) hits its
`_PER_DOMAIN_PREDICATE_FACTORIES` fallback, finds `_domain_id(conn, domain)
is None`, and returns `(False, "unknown usecase 'section-citations-abstract'")`.
Those 7 domains are permanently `outstanding` — **the gate can never clear,
regardless of which usecase the script sits in or how many citation stages
actually complete.** This is independent of tier ordering; it would fail
identically whether wired into the generate stage or the cite stage.

### 2.3 Gap H — stage mismatch (compounds Gap F, doesn't cause it)

Even if Gap F were fixed, `collate_references.py`'s final write
(`academic_schema.upsert_narrative(conn, paper_id, "references", sections,
stage="cite", ...)`) writes `stage='cite'`. `generate-section-draft-references`'s
own completion predicate is `_make_stage_predicate("references", "generate")`
(`academic_schema.py:724-729`, since `references` is excluded from
`GENERATED_DOMAINS` — wait, checked again: the loop at line 724 iterates
`GENERATED_DOMAINS`, which excludes `references`, so `references` never gets a
`generate-section-draft-references` predicate registered via this loop at
all — it falls to the `_PER_DOMAIN_PREDICATE_FACTORIES` fallback instead,
which *does* register `generate-section-draft-` → checks `stage='generate'`).
Either way: a script that writes `stage='cite'` can never satisfy a predicate
checking `stage='generate'`. Wiring `collate-references` into
`generate-section-draft-references` means that usecase's own completion
check would never pass, on top of Gap F.

### 2.4 Gap G — `validate-references` doesn't exist

`academic_schema.py:753-772` already has a purpose-built, correctly-named
predicate for this: `_uc_section_citations_references`, checking `stage='cite'`
for the `references` domain, with a docstring stating exactly the intended
design: *"depends on every other domain's section-citations-* usecase
completing first (enforced by collate_references.py calling usecase_status()
per domain before it collates, not by this predicate...)"*. This predicate is
registered under the name `section-citations-references` — matching
`4b-cite-references.md`'s usecase, not its (nonexistent) `validate-references`
script. The plan doc's script name is simply wrong/stale; the predicate
infrastructure for the real design already exists and matches.

### 2.5 Independent corroboration `collate-references` belongs in the citations stage

`generate_per_domain_usecases.py:78-79` (the verify-script generator,
untouched by any of this session's changes) already generates:
```python
gen_verify("uc4b_collate_references.py", "section-citations-references")
```
— a verify wrapper for `section-citations-references`, explicitly named
`collate_references` in the filename. This is a third independent source
(alongside `collate_references.py`'s own docstring and
`academic_schema.py`'s predicate) agreeing on where this script belongs.

### 2.6 Corrected fix for `references`

1. **Fix Gap F first, in `collate_references.py` itself** — replace the
   `for domain in academic_schema.GENERATED_DOMAINS` loop with a query
   against the paper's *actual* seeded domains (`SELECT key FROM
   academic_domains WHERE key != 'references'`), not the shared
   base_academic constant. This is the blocking fix — everything else is
   moot until the gate can clear at all.
2. **Wire `collate-references` into `section-citations-references`**
   (replacing the generic `_CITATION_STEP_TEMPLATES` for that one domain
   only), matching all three independent sources above.
3. **Wire `generate-section-draft-references`** with the generic
   `generate-section` prompt (per `4a-generate-references.md`'s own spec:
   `generate-section (prompt, template=templates/generation/markdown/references.md)`),
   same shape as the other 5 domains but using the fallback prompt since
   no dedicated `prompt/generation/references.md` file exists.
4. **Do not create `validate-references`** — the plan doc's script name is
   stale; `section-citations-references`'s completion predicate already
   exists and is correctly named `section-citations-references` (matches
   the usecase, not a separate script name).

---

## 3. Cluster A — `diagram-architecture-analysis` (unchanged from v1, re-confirmed)

`academic_schema.py:688-699` already has a registered completion predicate,
`_uc_diagram_analysis`, checking `analysis_kind IN ('architecture',
'dependencies','interactions')` — this usecase was fully designed (schema,
predicate, downstream consumers in `gather_proposal_context.py` and the
docs-first ingestion mappers) and simply never added to `standard.yaml`'s
`usecases:` list or `seeder.py`'s `_WHOLE_DOCUMENT_STEP_MAP`.

**Fix**: declare `diagram-architecture-analysis` in `standard.yaml`, add a
7-ish-step template to `seeder.py` mirroring `_NOVELTY_ANALYSIS_STEPS` but
with 3 cross-module passes (architecture, dependencies, interactions)
instead of 1. `discover-modules`/`gather-module-evidence` are `INSERT OR
IGNORE`-idempotent — safe to re-run rather than adding a `depends_on`
ordering constraint on `novelty-analysis`; keeps each analysis usecase
independently runnable (recommendation unchanged from v1, now confirmed
safe rather than assumed).

---

## 4. Cluster B — Missing Semantic Half (unchanged from v1, one confirmation added)

**`semantic-audit-part`** — `persist_domain_semantic_score.py` already
accepts a `scope`/`part_kind` parameter (confirmed this pass) — the persist
side is ready; only the step wiring (gather part artifact →
`semantic-audit-part` → persist with `scope='section-part'`) into
`section-citations-{domain}`, `section-enrichment-{domain}`,
`section-budget-fit-{domain}` is missing. 18 existing calculation files
(`report/semantic/ensemble/{domain}-{part}.yaml`) already expect this
output.

**`fit-to-budget`** + **plagiarism escalation
(`plagiarism-fingerprint-audit`/`targeted-rewrite`)** — confirmed
`deterministic_fingerprint_check.py`'s own docstring: *"mechanical
plagiarism pre-screen"* — "pre-screen" language supports **always
escalate-then-confirm**, not conditional branching on FAIL. Recommend the
same always-run design for `fit-to-budget` (the prompt no-ops when already
in range) rather than building a conditional-step mechanism the seeder
doesn't otherwise have.

---

## 5. Cluster D — `generate-novelty`/`generate-gaps`/`generate-mathematics`: **owner decision: keep**

Owner decision: keep, not delete. This means more than leaving the
declarations in place — as-is, nothing reads their output, so "keep"
without further work still leaves them orphaned and still fails Layer A
check #6. Keeping them for real requires closing the gap
`assemble-final-document.py:120-124`'s own comment identifies: cross-cutting
content today comes from `academic_cross_module_analysis` (raw analysis
text), and a `generate-novelty` step would write to `academic_narratives`
(a polished draft) — nothing currently bridges the two.

**Traced implementation requirement, not just a wiring fix:**

1. `novelty`/`gaps`/`mathematics` are not seeded as `domain` rows anywhere —
   `seeder.py`'s `all_domain_keys` is only the 6 structural domains +
   `reviewer-simulation`. Confirmed via `academic_schema.py:238-240`'s
   `get_domain_id` — it does a plain `key=?` lookup with no fallback, and
   `upsert_narrative` (line 356) calls `get_domain_id(conn, domain) if domain
   else None` — a `persist-section-draft` step for `domain="novelty"` today
   would silently succeed with `domain_id=NULL`, an narrative row nothing
   can query back by domain. **Seed `novelty`/`gaps`/`mathematics` as
   `domain` rows first** (non-scored / cross-cutting, e.g. sort_order in the
   90s alongside `reviewer-simulation`'s 99) — otherwise every other part of
   this fix sits on a NULL foreign key.
2. Add a `generate-section-draft-{novelty,gaps,mathematics}` usecase (or a
   single parametrized step appended to the existing
   `novelty-analysis`/`gap-analysis`/`mathematics-analysis` usecases —
   pick one, don't do both) with steps: gather the already-persisted
   `academic_cross_module_analysis` row for that `analysis_kind` →
   `generate-{novelty,gaps,mathematics}` (prompt, turns the raw analysis
   into polished section prose) → `persist-section-draft` (now resolves a
   real `domain_id` per step 1).
3. Update `assemble-final-document.py`'s cross-cutting weave to read the
   new `academic_narratives` row (the polished draft) in preference to —
   or in addition to, if both should appear — the raw
   `academic_cross_module_analysis` blob it reads today. This is a real
   code change to the render script, not just seeder wiring; flag it as
   its own task in the fix order rather than folding it into "wire the
   prompt."

---

## 6. Cluster E — `literature-review-pass`: **owner decision: sequential**

Owner decision: sequential — `literature-review-pass` runs as its own
enrichment sub-step before `section-enrichment`, not a replacement for it.
Confirmed distinct operations support this: `literature-review-pass.md`
adds citation grounding and flags `[NEEDS CITATION]`; `section-enrichment.md`
does general quality strengthening — different concerns, sequencing them
doesn't duplicate work.

**Fix**: extend `_ENRICHMENT_STEP_TEMPLATES` (currently 2 steps —
`section-enrichment` prompt → `persist-section-draft`) to a 3-step
sequence: gather evidence → `literature-review-pass` (prompt, citation
grounding pass) → `section-enrichment` (prompt, general quality pass,
now operating on the citation-enriched draft) → `persist-section-draft`.
Each intermediate pass can either persist its own `academic_narratives`
row (more audit trail, more rows) or just hand its output forward in the
step chain to the final persist (simpler) — pick whichever the persist
script's existing envelope contract supports without a signature change;
check `persist_section_draft.py`'s expected payload shape before deciding
between the two.

---

## 7. Gap I — `section-enrichment` vs `section-supplementary-content`

`academic_schema.py` is the single outlier here — every other source
(`standard.yaml`, `seeder.py`'s `_USECASE_STEP_PATTERNS`, all 6
`4c-enrich-*.md` plan docs, and `generate_per_domain_usecases.py:83-86`,
which independently generates `uc4c_enrich_{domain}.py` verify wrappers
targeting the usecase name `section-enrichment-{domain}`) agree on
`section-enrichment-{domain}`. Only `academic_schema.py:775-780`'s
registration loop and its `_PER_DOMAIN_PREDICATE_FACTORIES` fallback entry
(line 993) use `section-supplementary-content-{domain}`.

Confirmed real consumers that would currently get `"unknown usecase"` for
every `section-enrichment-{domain}` lookup: `generate_audit_report.py:30`
(pipeline-progress-matrix column), `render_charts.py:166-188`,
`verify/_common.py:19` (the function every auto-generated `uc4c_enrich_*.py`
verify script calls), and `check_usecase_complete`'s runtime path via
`usecase_status`.

**Fix**: rename `academic_schema.py:777` and the factory prefix at line 993
from `section-supplementary-content-` to `section-enrichment-`. Single
smallest fix — one file is wrong, four others already agree.

---

## 8. Verification Discipline (why this took two passes)

v1's mistake: it found a plausible-sounding mechanism (tier ordering) that
matched the *symptom* (references' generate stage using
`collate-references` looked wrong) without running the actual gate logic
against pcems_2026's real domain list. The fix: for any claim about *why*
a script would fail, trace the exact runtime call — what list does it
iterate, what does that resolve to for *this* standard's actual seeded
data, not the shared base-class default. Static reading found the
*symptom* correctly both times; only checking the actual iterated
collection (`GENERATED_DOMAINS`, 11 items, vs. pcems_2026's real 6) found
the real cause.

Before any of these fixes are marked done: rerun the full independent
Layer A reproduction (all 8 checks, temp DB, fresh core schema — recreate
per the logic in this proposal's §2 verification steps if the previous
session's scratch script isn't available), **and** exercise
`collate_references.py` against a paper with pcems_2026's real 6-domain set
seeded, not just a structural Layer A pass — Gap F specifically would never
be caught by Layer A (it's a runtime script bug, not a missing-row
structural check).

---

## 9. Proposed Fix Order

| Phase | What | Depends on |
|---|---|---|
| 1 | Gap F — fix `collate_references.py`'s domain gate to query live `academic_domains`, not the shared `GENERATED_DOMAINS` constant | None |
| 2 | §2.6 — wire `collate-references` into `section-citations-references`; wire `generate-section-draft-references` with the generic `generate-section` prompt | Phase 1 |
| 3 | Gap I — rename `academic_schema.py`'s enrich-usecase registration to `section-enrichment-{domain}` | None |
| 4 | Cluster D — seed `novelty`/`gaps`/`mathematics` as `domain` rows; add their generate usecase + steps; update `assemble-final-document.py` to weave the resulting `academic_narratives` draft | None |
| 5 | Cluster E — extend `_ENRICHMENT_STEP_TEMPLATES` to a 3-step sequence (`literature-review-pass` → `section-enrichment` → persist) | None |
| 6 | Cluster A — declare `diagram-architecture-analysis` usecase + seeder step template | None |
| 7 | Cluster B — wire `semantic-audit-part` into citations/enrichment/budget-fit | None |
| 8 | Cluster B — wire `fit-to-budget` + plagiarism escalation (`plagiarism-fingerprint-audit`/`targeted-rewrite`), always-run design | None |
| 9 | Full Layer A re-verification + a live runtime exercise of `collate_references.py` (not just structural audit) + a live `register_standard_globally`/`register_standard` run (still-open from the prior proposal) | Phases 1-8 |

Both owner decisions are resolved (§5, §6). Phase 4 is the largest
remaining phase — it's a render-script change, not just seeder wiring.
Everything else is a traced, mechanical fix — but phase 9's runtime
exercise matters precisely because Gap F proves Layer A passing is not
sufficient evidence the pipeline actually runs.
